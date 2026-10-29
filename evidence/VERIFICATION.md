# Verification and evidence ledger

The repository contains **two distinct test paths**. A successful observation-atlas build demonstrates source integrity, aggregate generation and figure publishing; it does not automatically mean every database and clinical analysis test passed.

| Evidence | Method / scope | Trace |
|---|---|---|
| Atlas reproduction | Official demo acquisition, public-data tests, all 37 source schemas, seven PNG/SVG figure pairs | [successful GitHub Actions run](https://github.com/Farshidbagheri/Observation-aware-ehr-data/actions/runs/40801312279) |
| Database parity | Real MIMIC demo event ledger compared against independent Python oracle in SQLite and live MongoDB 7 | [Measured results and caveats](CI_LIVE_MONGODB_RESULTS.md) |
| Historical complete verification | The 2026-10-29 comprehensive run passed unit tests and live MongoDB fixture checks, but its real-demo test-collection command failed due to an import path | [Failing run](https://github.com/Farshidbagheri/Observation-aware-ehr-data/actions/runs/40801700654) |
| Current status | A commit only establishes a source change, not a successful build. | [See current GitHub Actions](https://github.com/Farshidbagheri/Observation-aware-ehr-data/actions) |

The comprehensive workflow should report **all three successful jobs**: unit tests, live MongoDB integration, and verified public-demo audit. Any failure remains a release blocker until the current run is green.

For data provenance, the acquisition script verifies all 37 official CSV GZIP inputs against the source manifests. The open demo is not a representative population sample and the aggregate counts are not efficacy or causal treatment estimates.

All reproducible published results remain in `evidence/publication_atlas/`; the dated benchmark record is preserved as a historically measured run, with exact scope and hardware caveats.
