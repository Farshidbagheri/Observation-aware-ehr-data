# Verification and evidence ledger

The two current source-validation workflows completed successfully on source commit `65769670b3` (October 29, 2026); GitHub Actions subsequently committed the generated aggregate figures as `a978035ffb`, without a source-code change. Those successful checks should not be interpreted as clinical model validation or general database-performance superiority.

| Workflow | Scope | Verified outcome |
|---|---|---|
| [Research verification](https://github.com/Farshidbagheri/Observation-aware-ehr-data/actions/runs/40804105789) | Unit tests, official public-demo download/integrity, real-data SQLite/MongoDB evaluation, artifact QA | 21 unit tests passed (4 source-dependent skipped in the unit-only environment), 14 public-demo tests passed, 1 live MongoDB fixture test passed; all three jobs successful |
| [Reproduce observation atlas](https://github.com/Farshidbagheri/Observation-aware-ehr-data/actions/runs/40804105595) | Official demo manifests, seven figures, 37-table schema audit and artifact publication | 11 public-demo tests passed; complete workflow successful |
| [Historic measured database benchmark](CI_LIVE_MONGODB_RESULTS.md) | Indexed event-time-proxy as-of retrieval over the bounded public demo | Reference parity and measured machine-specific p50/p95; not a production database comparison |

Earlier failed or cancelled GitHub runs are **historical and retained for transparency**. Repeated commits triggered superseded workflows that were cancelled by concurrency controls. A previous full verification failure was due to a Python import path; the current green workflow uses the corrected invocation.

### What these tests prove

- The publication workflow acquired the official public demo files with checksum verification.
- Canonical event histories and the Python reference are consistent with the tested SQLite/MongoDB as-of retrieval contracts.
- All seven PNG/SVG figure pairs and an offline HTML dashboard are generated and committed; the source inventory covers 37 CSV files.
- Published research artifacts are aggregate-only. Raw and patient-level derived records stay outside the tracked repository.

### What these tests do not prove

- Patient-level clinical risk prediction, sepsis causal treatment effects, true clinician access time, comprehensive bitemporal revision history, or clinical deployment.
- Representative clinical population estimates, unbiased selection or general superiority of one database.
- Locked dependency environments, independent hardware benchmarking, or approval to release institutional intellectual property.

The **current** status of any subsequent commit is always available in [GitHub Actions](https://github.com/Farshidbagheri/Observation-aware-ehr-data/actions). This ledger documents the cited runs, not a permanent green-build guarantee.
