# Descriptive research atlas QA

- Origin: official public MIMIC-IV-ED Demo 2.2 and MIMIC-IV Clinical Demo 2.2; SHA256 verified during acquisition.
- Unit: ED encounter for temporal panels; vitalsign row for field completeness; laboratory record for recording delays.
- Time zero: ED arrival; no retrospectively inferred Sepsis-3 onset.
- Denominator: ED stays still eligible at each time-bin start, not all source rows.
- Small cells: suppressed if fewer than ten stays with a recorded observation.
- Patient-cluster 95% percentile intervals: 2,000 bootstrap replicates sampling patients (subject_id) with replacement, seed 2026; completeness is row-weighted within the selected demo. Not externally representative.
- Pyxis is medication dispensing, not verified administration.
- STORETIME is recording proxy and does not prove observation by a clinician.
- No trained predictive model, adjudicated sepsis outcome, valid counterfactual policy evaluation, or external validation.
- Primary source citations: https://doi.org/10.13026/jzz5-vs76 and https://doi.org/10.13026/dp1f-ex47.
- SVG and PNG are produced from the same real aggregate input; JSON is machine-readable and excludes patient identifiers.
