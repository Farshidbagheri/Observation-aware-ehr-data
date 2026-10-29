# Descriptive research atlas QA

- Origin: official public MIMIC-IV-ED Demo 2.2 and MIMIC-IV Clinical Demo 2.2; SHA256 verified during acquisition.
- Unit: ED encounter for temporal panels; vitalsign row for field completeness; laboratory record for recording delays.
- Time zero: ED arrival; no retrospectively inferred Sepsis-3 onset.
- Denominator: ED stays still eligible at each time-bin start, not all source rows.
- Small cells: suppressed if fewer than ten stays with a recorded observation.
- Wilson 95% intervals: descriptive row-level coverage; repeated rows within stay are correlated, so these are not patient-level inferential confidence intervals.
- Pyxis is medication dispensing, not verified administration.
- STORETIME is recording proxy and does not prove observation by a clinician.
- No trained predictive model, adjudicated sepsis outcome, valid counterfactual policy evaluation, or external validation.
- Primary source citations: https://doi.org/10.13026/jzz5-vs76 and https://doi.org/10.13026/dp1f-ex47.
- SVG and PNG are produced from the same real aggregate input; JSON is machine-readable and excludes patient identifiers.
