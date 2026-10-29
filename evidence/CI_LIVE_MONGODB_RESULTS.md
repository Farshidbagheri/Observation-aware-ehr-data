# First real-data MongoDB ↔ SQLite benchmark (verified GitHub Actions)

Source: [successful Research verification run #40795487976](https://github.com/Farshidbagheri/Observation-aware-ehr-data/actions/runs/40795487976), real deidentified **public MIMIC-IV-ED Demo 2.2 + Clinical Demo 2.2** downloaded and SHA256-verified against PhysioNet manifests.

**Workload:** 4,548 canonical events; strict availability assumptions; 120 decision landmarks; 10 repeats = 1,200 timed queries per backend. The same Python reference oracle checked both engines.

| Metric | SQLite (in-process) | MongoDB 7 (PyMongo, local service) |
|---|---:|---:|
| Ingest (ms) | 54.885 | 73.758 |
| Query p50 (ms) | 0.0065 | 0.5517 |
| Query p95 (ms) | 0.0719 | 0.6565 |
| Query count | 1,200 | 1,200 |
| Reference mismatches | 0 | 0 |
| Future-available leaks | 0 | 0 |
| Unknown-availability records shown | 0 | 0 |

**Interpretation:** Both implementations satisfied the declared retrieval contract on the tested real-demo records. In **this one narrow benchmark**, SQLite was faster. It would be scientifically misleading to conclude that either technology is universally superior: SQLite runs in-process, MongoDB carries driver/service overhead, and our SQLite baseline stores JSON rather than a fully normalized production schema. No multi-host repeats, CI confidence intervals, query plan comparisons or cold-cache studies were performed. We have **not** established clinical availability truth or counterfactual antibiotic effects.

Full machine-readable results: [`real_demo_benchmark_ci_2026-10-29.json`](real_demo_benchmark_ci_2026-10-29.json). The associated workflow artifact holds aggregate-only reports and 12 PNG/SVG visualizations (14-day artifact retention).
