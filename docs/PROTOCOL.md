# Research protocol — Observation-Aware EHR v0.2

## Objective and falsifiable engineering claim

**Objective:** construct longitudinal event histories where queries at decision time `t` can access only records whose *declared* release proxy is at or before `t`. Confirm this contract against an independent Python reference and matched SQLite/MongoDB implementations. Compare measured latency without predicting the winner.

**Not claimed:** verified clinician-view timestamps, true correction histories, sepsis labels, biological treatment effects, optimal antibiotic timing, external validity, or clinical deployment.

## Data and time semantics

- **Public sources:** MIMIC-IV ED demo 2.2 and clinical demo 2.2, retaining official ODbL attribution and manifests.
- **Observation time:** original chart time (`charttime`). Do not modify or fill it.
- **Availability:** hospital `storetime` only when nonempty and `storetime >= charttime`; labeled `storetime_proxy` (not proof of viewing).
- **Unknown:** missing, invalid or contradictory availability remains unavailable; not coerced to charttime.
- **ED mode (`strict`, default):** no ED measurement is considered available without release evidence.
- **ED mode (`proxy`, sensitivity only):** ED charttime treated as hypothetical availability, explicitly labeled.
- **Artificial availability delays:** optional controlled data-integrity tests, NEVER presented as MIMIC timings or study findings.
- **ED stay:** subject, hadm (when present), and charttime within ED intime/outtime. No cross-hospital timeline alignment claim.
- **Clinical medications:** Pyxis is a dispense event, eMAR requires additional validation; neither used to estimate first antibiotic administration.

## Prespecified evaluations

1. Schema integrity: unique event IDs, valid ED stay keys, parsed nonnegative hospital release lag, duplicates, missing time fields.
2. Observation leakage: reference as-of oracle at multiple decision landmarks, matched in SQLite and MongoDB.
3. Provenance: preserve dataset name, event kind and source of availability assumption; audit all imputation/proxy decisions.
4. Performance: ingest ms and query p50/p95 at identical query workload and identical record set, multiple repetitions; **environment-specific** only.
5. Sensitivity: strict vs explicit charttime proxy; unknown observations excluded. Do not silently mix results from different assumptions.
6. Descriptive figures: produce 12 plots from actual aggregate public-demo records. Figures do not imply causal effects.
7. Future bitemporal corrections: implement append-only correction/version ledger and rollback before claiming robust revision queries; not included yet.
8. Future causal study: pre-register target trial (eligibility, time-zero, treatment regimes, outcomes, censoring) and positivity diagnostics on approved full EHR; not feasible on current demos.

## Release gates

- [x] Real public demo files verified against official SHA256SUMS (37 gz files; 6 ED + 31 clinical).
- [x] Offline end-to-end strict-mode normalization on supplied demos.
- [x] SQLite as-of query matched independent reference at all executed landmarks.
- [ ] MongoDB live parity on an authenticated MongoDB server.
- [ ] Independent-machine reproducibility, service configuration, confidence intervals for performance.
- [ ] Full bitemporal correction lineage.
- [ ] Clinical temporal causal estimator or medically interpretable personalized treatment recommendation.

## Ethical use

Raw public MIMIC demos remain in ignored `data/raw/`. Patient-level JSONL and local machine logs stay ignored. The evidence JSON contains only aggregated descriptive counts. Full MIMIC/MetroHealth datasets require their own explicit permissions and must remain on authorized infrastructure. Researchers must seek appropriate IRB, data governance and clinician review before extending to clinical policy evaluation.
