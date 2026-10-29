# One local SQLite run, real MIMIC public-demo v2.2 inputs

Execution: 2026-10-28, Python 3.13 in an ephemeral container; `backend=sqlite`, `repeats=10`, `max_stays=60`, `mode=strict`, source events 4,548, queries 120, timed calls 1,200.

| Metric | Observed |
|---|---:|
| Insert+index operation time in this process | 38.226 ms |
| Median query execution | 0.0065 ms |
| 95th percentile query execution | 0.0971 ms |
| Oracle mismatches | 0 |
| Retrieved records from declared future | 0 |
| Returned records of unknown declared availability | 0 |

**Not a comparison and not a clinical finding.** Single-process Python timings are highly environment-dependent and do not support universal claims. SQLite stores JSON text in a simple events table: this is not a claim to have compared a production-grade normalized relational schema with MongoDB. The MongoDB server was not available locally; the live integration job is defined for external execution.
