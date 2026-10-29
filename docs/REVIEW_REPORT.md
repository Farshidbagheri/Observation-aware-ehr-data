# Technical and scientific audit

Reviewed areas: scientific claims, data provenance, source licensing, repository navigation, reproducibility, visualization semantics, and continuous integration. This is an **internal audit checklist**, not an external peer-review endorsement.

| Review area | Finding | Remediation / evidence |
|---|---|---|
| README presentation | Broken private-repository CI badge, duplicated explanations, mobile two-column images | Removed unreliable badges; consolidated overview, single-column scientific images, verified navigation |
| Dashboard access | GitHub shows `index.html` source, not a rendered site | Explain offline viewing and provide all figures directly in Markdown |
| CI coverage | Historic import-path failure and cancelled superseded runs | Corrected import path; [complete real-data verification](https://github.com/Farshidbagheri/Observation-aware-ehr-data/actions/runs/40804105789) and [atlas build](https://github.com/Farshidbagheri/Observation-aware-ehr-data/actions/runs/40804105595) succeeded |
| Documentation drift | Multiple old statements incorrectly said MongoDB had not been executed and referred to retired figure locations | Replace stale claims with independently linked run evidence and explicit limitations |
| Statistical uncertainty | Original Wilson row intervals ignored within-patient correlation | Replaced with reproducible 2,000-resample patient-cluster percentile intervals; no population inference claimed |
| Link integrity | Some historical HTML/image references and script names were stale | Replace links and add an offline relative-link gate |
| Benchmark interpretation | SQLite and MongoDB have different service/serialization overhead | Retain measured results while refusing general superiority claims |
| Medical validity | No adjudicated sepsis outcomes, validated treatment clocks, or causal identification | Exclude clinical treatment-effect claims, inappropriate model metrics and patient-level recommendations |
| Provenance | Source demonstration data are open but not representative | Cite PhysioNet versions and license; check upstream manifests; keep row-level source data out of Git |
| Software distribution | CITATION exists but the repository has no confirmed approved open-source license | Avoid claiming unrestricted reuse; request institutional/IP review before publishing a license |
| Feature maturity | No true bitemporal version correction or prospective deployment | Keep these on the roadmap; do not describe them as implemented |

## Acceptance criteria for a research release

1. The README renders on GitHub mobile without dependence on inaccessible badge images or executable HTML.
2. Every local Markdown link resolves to a tracked file; any omitted third-party link is clearly labeled.
3. All source-dependent tests run on the verified public demos; non-data unit tests run without downloads.
4. The atlas publishes only aggregate results and does not include protected patient-level records.
5. The two cited source-revision workflows finished green; any newer source revision must be reverified independently.
6. Claims about causal effects, model accuracy, deployment, and general database speedups are absent until directly supported.

## Remaining release gates and investigations

- Independently assess patient-cluster bootstrap coverage and sensitivity to patient weighting, sparse cells, and selection from the small demo.
- Add duplicate-event, contradictory timestamp, timestamp-ordering, join-coverage and selection-bias audit panels.
- Implement documented time/version corrections and bitemporal as-of semantics with independent temporal-oracle checks.
- Benchmark across dataset sizes and index configurations with controlled environments, query plans, cold/warm run separation, and confidence intervals across independent machines.
- Before sepsis-causal modeling: obtain an approved outcome-linked ED cohort, define time zero and actual administration time, emulate target trials, and report positivity and censoring diagnostics.

**Release blockers:** institutional/IP permission, software license selection, final independent visual/data review, and dependency-environment archive. Technical CI success does not resolve these governance gates.

An internally audited research prototype is not equivalent to a published, externally peer-reviewed or clinically validated system.
