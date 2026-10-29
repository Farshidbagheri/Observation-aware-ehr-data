"""Data-contract and leakage-safe event normalization for a research prototype.

Note: MIMIC clock times are deidentified/shifted and timestamps in CSV are typically
naive; this code compares dataset-local timestamps and does not assign a timezone.
"""
from __future__ import annotations

import csv
import gzip
import hashlib
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Iterable


def parse_time(value: str | None) -> datetime | None:
    if not value or value.lower() in {"nan", "none", "null"}:
        return None
    return datetime.fromisoformat(value.strip().replace(" ", "T"))


def fmt_time(value: datetime | None) -> str | None:
    return value.isoformat(timespec="seconds") if value else None


def read_table(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing dataset file: {path} (download with scripts/fetch_demo.py)")
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def resolve_csv(root: Path, table: str) -> Path:
    candidates = [root / f"{table}.csv.gz", root / f"{table}.csv"]
    for path in candidates:
        if path.exists():
            return path
    raise FileNotFoundError(f"Cannot find {table}.csv[.gz] in {root}")


def validate_source(source: str) -> None:
    allowed = {"unknown", "charttime_proxy", "storetime_proxy", "synthetic_delay"}
    if source not in allowed:
        raise ValueError(f"Invalid availability source {source!r}")


def build_event(kind: str, row: dict[str, str], ordinal: int, *, stay_id: str,
                event_time: str | None, available_at: str | None,
                availability_source: str, dataset: str) -> dict[str, Any]:
    validate_source(availability_source)
    if availability_source == "unknown" and available_at is not None:
        raise ValueError("unknown availability cannot have available_at")
    parsed_event, parsed_available = parse_time(event_time), parse_time(available_at)
    if parsed_event and parsed_available and parsed_available < parsed_event:
        # Events that predate the timestamp may occur in messy real data; fail rather
        # than silently alter or normalize the semantics.
        raise ValueError(f"Availability precedes event time for {kind} row {ordinal}")
    return {
        "event_id": f"{dataset}:{kind}:{stay_id}:{ordinal}",
        "stay_id": str(stay_id),
        "subject_id": str(row.get("subject_id", "")),
        "kind": kind,
        "event_time": fmt_time(parsed_event),
        "available_at": fmt_time(parsed_available),
        "availability_source": availability_source,
        "dataset": dataset,
        "payload": {k: v for k, v in row.items() if v not in ("", None)},
    }


def synthetic_delay(event: dict[str, Any], seed: int = 2026,
                    allowed_minutes: tuple[int, ...] = (0, 15, 45, 90)) -> dict[str, Any]:
    """Explicit *artificial* release delay; never represent it as actual clinician availability."""
    if not event["event_time"]:
        return dict(event)
    key = f"{seed}/{event['event_id']}".encode()
    index = int.from_bytes(hashlib.sha256(key).digest()[:4], "big") % len(allowed_minutes)
    value = dict(event)
    value["available_at"] = fmt_time(parse_time(event["event_time"]) + timedelta(minutes=allowed_minutes[index]))
    value["availability_source"] = "synthetic_delay"
    value["synthetic_delay_minutes"] = allowed_minutes[index]
    return value


def load_ed(ed_dir: Path, *, mode: str = "strict", seed: int = 2026,
            dataset_id: str = "mimic-iv-ed-demo-v2.2") -> tuple[list[dict], dict]:
    """Load ED demo, preserve documented time semantics, and separate time assumptions.

    strict: exclude unknown-availability events from as-of queries.
    proxy: treat ED vitalsign/pyxis charttime as a *proxy*, not true availability.
    synthetic: add deterministic artificial release delays to ED vitalsign/pyxis.
    Triage, medrecon, diagnosis lack a valid decision-time event clock in this demo;
    these are not inserted into the time-indexed event stream.
    """
    if mode not in {"strict", "proxy", "synthetic"}:
        raise ValueError("mode must be strict, proxy or synthetic")
    stays = read_table(resolve_csv(ed_dir, "edstays"))
    valid = {str(s["stay_id"]): s for s in stays}
    out: list[dict] = []
    counts = {}
    for table in ("vitalsign", "pyxis"):
        rows = read_table(resolve_csv(ed_dir, table))
        counts[table] = len(rows)
        for i, row in enumerate(rows):
            stay = str(row["stay_id"])
            if stay not in valid:
                raise ValueError(f"Orphan {table} stay_id {stay}")
            t = row.get("charttime")
            event = build_event(table, row, i, stay_id=stay,
                                event_time=t, available_at=t if mode == "proxy" else None,
                                availability_source="charttime_proxy" if mode == "proxy" else "unknown",
                                dataset=dataset_id)
            if mode == "synthetic":
                event = synthetic_delay(event, seed=seed)
            out.append(event)
    metadata = {"ed_stays": len(stays), "ed_rows": counts, "mode": mode, "dataset_id": dataset_id,
                "no_availability_truth_claim": True,
                "excluded_from_timed_stream": ["triage", "medrecon", "diagnosis"],
                "pyxis_is_dispensing_not_administration": True}
    return out, metadata


def assign_hospital_event_to_ed_stay(row: dict[str, str], stays: list[dict], *, max_hours_after: int = 0) -> str | None:
    """Conservative temporal match: same subject/hadm, charttime during ED stay.

    Does not imply that every hospital-recorded event was available during ED care.
    """
    t = parse_time(row.get("charttime"))
    if t is None:
        return None
    for stay in stays:
        if row.get("subject_id") != stay.get("subject_id") or not row.get("hadm_id") or row.get("hadm_id") != stay.get("hadm_id"):
            continue
        a, b = parse_time(stay.get("intime")), parse_time(stay.get("outtime"))
        if a and b and a <= t <= b + timedelta(hours=max_hours_after):
            return str(stay["stay_id"])
    return None


def add_hospital_events(events: list[dict], ed_dir: Path, hosp_dir: Path, *,
                        dataset_id: str = "mimic-iv-clinical-demo-v2.2") -> tuple[list[dict], dict]:
    """Optional hospital demo join; storetime is a proxy for system recording, not clinician viewing."""
    stays = read_table(resolve_csv(ed_dir, "edstays"))
    result = list(events)
    metadata: dict[str, Any] = {"hospital_rows": {}, "matched_ed_window": {}, "unmatched": {}}
    for table in ("labevents", "emar"):
        file = hosp_dir / f"{table}.csv.gz"
        if not file.exists():
            file = hosp_dir / f"{table}.csv"
        if not file.exists():
            metadata["hospital_rows"][table] = "missing"
            continue
        rows = read_table(file)
        matched = 0
        for i, row in enumerate(rows):
            stay_id = assign_hospital_event_to_ed_stay(row, stays)
            if stay_id is None:
                continue
            t, store = parse_time(row.get("charttime")), parse_time(row.get("storetime"))
            # Missing or contradictory storetimes are not coerced to charttime.
            if not t:
                continue
            available = fmt_time(store) if store and store >= t else None
            ev = build_event(table, row, i, stay_id=stay_id, event_time=fmt_time(t),
                             available_at=available, availability_source="storetime_proxy" if available else "unknown",
                             dataset=dataset_id)
            result.append(ev)
            matched += 1
        metadata["hospital_rows"][table] = len(rows)
        metadata["matched_ed_window"][table] = matched
        metadata["unmatched"][table] = len(rows)-matched
    metadata["hospital_storetime_not_proof_of_clinician_viewing"] = True
    return result, metadata


def asof_reference(events: Iterable[dict], stay_id: str, landmark: str) -> list[dict]:
    """Leakage-safe *with respect to the declared availability timestamp*, not clinical truth."""
    cutoff = parse_time(landmark)
    if cutoff is None:
        raise ValueError("landmark is required")
    result = [e for e in events if e["stay_id"] == str(stay_id)
              and e.get("available_at") and parse_time(e["available_at"]) <= cutoff]
    return sorted(result, key=lambda x: (x["available_at"], x["event_id"]))


def write_jsonl(path: Path, rows: Iterable[dict]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    count=0
    with path.open("w",encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row,sort_keys=True,ensure_ascii=False)+"\n")
            count+=1
    return count


def read_jsonl(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]
