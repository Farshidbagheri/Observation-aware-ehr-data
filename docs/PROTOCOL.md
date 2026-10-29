# Research protocol

## Primary engineering question

Can a longitudinal EHR event history support as-of queries that return only records whose **declared release timestamp** is at or before a specified landmark, while preserving missing or uncertain observation-time semantics? Compare SQLite and MongoDB query correctness against an independent Python reference.

**Falsifiable condition:** A query violates the stated contract if it includes an event released after its landmark, includes an event with unknown availability under strict mode, or returns a different ordered event-ID set than the reference.

## Data and cohort

- Sources: public MIMIC-IV-ED Demo 2.2 and MIMIC-IV Clinical Demo 2.2.
- Clinical sample: 222 ED stays among 64 distinct ED patients in the selected public demo.
- Time origin for descriptive figures: recorded ED arrival. It is **not** a clinically adjudicated sepsis onset.
- Hospital records: matched by subject/admission plus ED interval. Records without the required identifiers/timestamps remain unmatched.
- Treatment: Pyxis indicates dispensing; eMAR records require event-specific validation. Neither is treated as the first verified IV antibiotic administration timestamp.

## Information-availability modes

- `strict`: unknown-availability ED records are excluded from decision-time retrieval; valid hospital storage times may be used as declared proxies.
- `proxy`: sensitivity-only assumption that ED chart time approximates release time; never confused with verified clinician access.
- `synthetic`: deterministic artificial release delays for software correctness tests only. Generated timings and fixtures are not clinical observations.

## Validation

1. Verify downloaded data against official source SHA-256 manifests.
2. Check encounter keys, joins, timestamp ordering, unknown and contradictory release times.
3. Compare as-of query event IDs, ordering, future-release exclusion, and unknown-release exclusion against the Python reference.
4. Repeat the same landmarks for SQLite and MongoDB 7; document service/driver overhead and workstations when reporting latency.
5. Generate descriptive plots with explicit units, denominators, low-count handling, and source citations.
6. Validate local Markdown navigation and file existence; reject broken research image references in CI.

## Interpretation

Storage and documentation timestamps are **not** validated clinician observation timestamps. The database benchmark cannot determine true patient risk-from-waiting. The open demonstration population is too small and selected to support an externally valid sepsis-treatment policy or clinical prediction metric.

## Future study prerequisites

For a causal timing analysis, prespecify suspected-sepsis eligibility, decision time zero, administered IV antibiotic timestamp, outcome horizon, time-varying confounders, competing risks, intervention regimes, positivity, censoring rules, sensitivity analyses, subgroup diagnostics and external validation. The clinical dataset must remain within approved institutional governance and IRB permissions.

See [architecture](ARCHITECTURE.md), [figures](FIGURES.md), [metrics](EVALUATION_APPLICABILITY.md), and [limitations](RESEARCH_LIMITATIONS.md).
