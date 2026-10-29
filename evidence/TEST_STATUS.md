# Verification status — 2026-10-28, v0.2 local execution

## Confirmed on uploaded public MIMIC-IV Demo v2.2 files

- Original published SHA256 manifest matched: 6/6 ED CSV.GZ files and 31/31 clinical CSV.GZ files.
- 222 ED stays (64 distinct ED subjects), 1,038 ED vitals, 1,082 ED Pyxis rows, 1,833 hospital labevents and 595 hospital eMAR event rows joined within ED time windows.
- Strict event ledger: 4,548 events; 2,332 with storetime proxy, 2,216 with unknown availability.
- 13 Python tests **passed**, 1 live MongoDB integration test **skipped** (MongoDB service / PyMongo not present).
- 12 PNG + SVG descriptive plots from aggregate real-demo measures generated locally; HTML dashboard saved at `evidence/verified_demo_dashboard.html`.
- The SQLite as-of benchmark executed and matched the Python reference (120 landmark queries x 10 repeats). See `evidence/LOCAL_SQLITE_RUN.md` for exact measured values and limitations.

## Important exclusions

- **No live MongoDB benchmark executed**, so no MongoDB performance numbers or comparison claims.
- Neither the demo nor chart/storetime proxies establish who saw which data at decision time.
- No patient-specific treatment recommendation, sepsis effect, bitemporal correction truth, clinician calibration or causal identification was estimated.
- Original deidentified patient-level raw data and normalized JSONL are excluded from GitHub and the release bundle.
