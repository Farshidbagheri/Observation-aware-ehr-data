# Study design and validity limitations

1. **Clinical question:** individualized, uncertainty-qualified timing of first antibiotic *administration* in suspected ED sepsis. This pilot does not estimate it.
2. **Information availability:** ED `vitalsign.charttime` = chart event time; actual physician availability may differ. `labevents.storetime` and `emar.storetime` can be used as *record-storage* proxies, not guaranteed read times. Selection of `unknown` vs `proxy` vs `synthetic` is explicit.
3. **Clinical outcomes:** The 100-patient demos are insufficient to derive a trustworthy sepsis cohort, positivity, confounder adjustment, or clinical timing curves. Pyxis time is not first antibiotic administration.
4. **Synthetic causal benchmark:** Independent separate known-truth simulator; no physiologic or clinical calibration and not a proof of treatment benefit.
5. **Database experiment:** Compare MongoDB documents with a simple SQLite normalized-ish table carrying JSON; it is *not* a comprehensive MongoDB vs relational database system benchmark. The benchmark measures matched as-of queries and basic ingest. Warm-up, execution plans and repeated independent runs are needed for general performance conclusions.
6. **Data joins:** `subject_id` and `hadm_id` matching, plus ED time windows, can miss relevant events and should never be considered complete. Some ED encounters lack a linked admission ID. Hospital `emar` may contain documented medication events but its timestamps are distinct from directly observed administration, and medication specifics require clinical audit.
7. **No MongoDB or Synthea superiority assumed:** This MVP uses open MIMIC samples and synthetic delay for timestamp sensitivity, not ORiGAMi training or proof of representation learning.
8. **Any next-stage full MIMIC or HiRID dataset stays on permitted infrastructure** and is never committed to public GitHub or used without the dataset's DUA, institutional policies, and collaborator permissions.

## Proposed next phase

1. Confirm source table provenance, missingness, and compatibility of deidentified relative times.
2. Introduce schema evolution events, retroactive correction records, and time-travel (bitemporal) query semantics with independent acceptance tests.
3. Create a meaningful representation-learning task and preregister baselines and leakage audits before moving to optional ORiGAMi study.
4. Only then attempt authorized ED sepsis cohort, independent clinical plausibility review and causal identification diagnostics.
