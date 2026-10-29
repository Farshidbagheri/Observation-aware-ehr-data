# Engineering roadmap with evidence-gated milestones

## Implemented locally, v0.2

- Strict source-preserving canonical ledger for ED vitals/Pyxis and conservative hospital labevents/eMAR joins
- Availability provenance (`unknown`, `storetime_proxy`, explicit `charttime_proxy` or artificial delay)
- Independent as-of reference, SQLite query parity, optional real MongoDB query engine
- Configurable CLI, Docker Compose and CI integration definition
- Aggregate-only offline report, 12 descriptive graph types, dataset checksum verification

## Required before scientific publication or DOI claims

- Run live MongoDB integration and publish exact execution provenance, repeat across hardware and database versions
- Add append-only bitemporal history with observed correction metadata and test revision visibility
- Introduce normalized relational schema comparable to a document-oriented representation; current SQLite JSON table is not a full relational-DB comparison
- Pre-register cohort/time-zero and outcome definitions, sample-size/positivity checks, sensitivity analyses
- Add ethical review, artifact checksums, source provenance, CITATION.cff, software licensing approval and archive release

## Explicit exclusions

No invented EHR encounters, timestamps, antibiotic administration, sepsis outcomes, effect sizes, model accuracy or claim of improved patient care.
