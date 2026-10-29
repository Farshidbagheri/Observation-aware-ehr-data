from __future__ import annotations
import csv
import gzip
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
import pytest
from obs_ehr.core import (load_ed,asof_reference,build_event,synthetic_delay,
    add_hospital_events,write_jsonl,read_jsonl)
from obs_ehr.storage import SQLiteStore
from obs_ehr.benchmark import run_benchmark
from obs_ehr.toy import generate_toy


def csv_gz(path:Path,rows:list[dict]):
    path.parent.mkdir(parents=True,exist_ok=True)
    with gzip.open(path,"wt",encoding="utf-8",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]))
        writer.writeheader();writer.writerows(rows)


@pytest.fixture
def demo(tmp_path):
    ed=tmp_path/"ed";hosp=tmp_path/"hosp"
    csv_gz(ed/"edstays.csv.gz",[
        {"subject_id":"100", "hadm_id":"900", "stay_id":"1", "intime":"2026-01-01 10:00:00", "outtime":"2026-01-01 14:00:00"},
        {"subject_id":"101", "hadm_id":"901", "stay_id":"2", "intime":"2026-02-01 10:00:00", "outtime":"2026-02-01 14:00:00"}])
    csv_gz(ed/"vitalsign.csv.gz",[
        {"subject_id":"100","stay_id":"1","charttime":"2026-01-01 10:05:00","heartrate":"102"},
        {"subject_id":"100","stay_id":"1","charttime":"2026-01-01 11:10:00","heartrate":"110"},
        {"subject_id":"101","stay_id":"2","charttime":"2026-02-01 11:05:00","heartrate":"99"}])
    csv_gz(ed/"pyxis.csv.gz",[
        {"subject_id":"100","stay_id":"1","charttime":"2026-01-01 10:15:00","name":"TEST DISPENSE (not administration)"}])
    csv_gz(hosp/"labevents.csv.gz",[
        {"subject_id":"100","hadm_id":"900","charttime":"2026-01-01 10:10:00","storetime":"2026-01-01 11:05:00","valuenum":"2.4"},
        {"subject_id":"101","hadm_id":"901","charttime":"2026-02-01 10:10:00","storetime":"","valuenum":"1.4"}])
    csv_gz(hosp/"emar.csv.gz",[
        {"subject_id":"100","hadm_id":"900","charttime":"2026-01-01 10:20:00","storetime":"2026-01-01 10:30:00","medication":"synthetic_med"}])
    return ed,hosp


def test_strict_unknowns_excluded(demo):
    data,_=load_ed(demo[0],mode="strict")
    assert len(data)==4
    assert not asof_reference(data,"1","2026-01-01T12:00:00")
    assert all(x["availability_source"]=="unknown" for x in data)


def test_proxy_explicit_not_clinician_truth(demo):
    data,meta=load_ed(demo[0],mode="proxy")
    q=asof_reference(data,"1","2026-01-01T10:20:00")
    assert len(q)==2
    assert all(x["availability_source"]=="charttime_proxy" for x in q)
    assert meta["pyxis_is_dispensing_not_administration"]


def test_synthetic_shift_deterministic(demo):
    first,_=load_ed(demo[0],mode="synthetic",seed=19)
    second,_=load_ed(demo[0],mode="synthetic",seed=19)
    assert first==second
    assert all(e["availability_source"]=="synthetic_delay" for e in first)
    assert all(e["available_at"]>=e["event_time"] for e in first)


def test_storetime_is_only_proxy(demo):
    records,_=load_ed(demo[0],mode="strict")
    all_records,meta=add_hospital_events(records,*demo)
    labs=[x for x in all_records if x["kind"]=="labevents"]
    assert len(labs)==2
    assert len(asof_reference(all_records,"1","2026-01-01T10:45:00"))==1 # eMAR storetime, not lab yet
    assert len(asof_reference(all_records,"1","2026-01-01T11:15:00"))==2
    assert labs[0]["availability_source"]=="storetime_proxy"
    assert labs[1]["availability_source"]=="unknown"
    assert meta["hospital_storetime_not_proof_of_clinician_viewing"]


def test_no_early_availability():
    with pytest.raises(ValueError):
        build_event("lab",{"subject_id":"1"},1,stay_id="1",event_time="2026-01-01T11:00:00",
                    available_at="2026-01-01T10:00:00",availability_source="storetime_proxy",dataset="dummy")


def test_sqlite_matches_reference(demo):
    data,_=load_ed(demo[0],mode="synthetic")
    db=SQLiteStore()
    db.replace(data)
    for cutoff in ["2026-01-01T10:00:00","2026-01-01T10:20:00","2026-01-01T12:00:00"]:
        assert db.asof("1",cutoff)==asof_reference(data,"1",cutoff)
    db.close()


def test_benchmark_no_leak(demo):
    data,_=load_ed(demo[0],mode="synthetic")
    report=run_benchmark(data,backend="sqlite",repeats=2)
    assert report["correctness"]["sqlite"]["future_available_leaks"]==0
    assert report["correctness"]["sqlite"]["mismatched_queries"]==0
    assert report["latency_ms"]["sqlite"]["n_measurements"]>0


def test_jsonl_roundtrip(demo,tmp_path):
    data,_=load_ed(demo[0])
    p=tmp_path/"events.jsonl"
    assert write_jsonl(p,data)==len(data)
    assert read_jsonl(p)==data


def test_toy_known_truth():
    rows=generate_toy(100,seed=23)
    assert rows==generate_toy(100,seed=23)
    assert all(row["synthetic_ground_truth"] and row["true_delay_effect"]>0 for row in rows)
    assert 0 < sum(r["observed_delay"] for r in rows) < 100


def test_not_confuse_no_charttime_with_availability(demo):
    data,_=load_ed(demo[0],mode="strict")
    assert all(e["event_time"] and e["available_at"] is None for e in data)
