# Engineering architecture

## Goal

Construct reproducible event histories for retrospective decision-time queries while preserving the distinction between clinical event time and declared information availability. This repository evaluates *storage/query semantics* using public demonstration datasets; it does not derive a clinical treatment policy.

## Data flow

```text
PhysioNet ED and Clinical demo CSVs
  |-- versioned SHA-256 acquisition check (scripts/fetch_demo.py)
  |-- source inventory / coverage audit (scripts/source_inventory.py)
  |
  +--> cohort-window matching [subject_id, hadm_id, charttime within ED visit]
          |
          v
      canonical event ledger (src/obs_ehr/core.py)
        event_id, stay_id, kind, dataset
        event_time, available_at, availability_source
        original payload (LOCAL ONLY)
          |
          +--> Python as-of reference
          +--> indexed SQLite JSON-backed table
          +--> indexed MongoDB document collection
                    |
                    v
          query parity, future-release leakage check,
          p50/p95 latency in documented workload
  |
  +--> aggregate observation atlas (scripts/publication_atlas.py)
          |
          +--> seven figures / SVG / PNG
          +--> source-only JSON summaries
          +--> offline HTML dashboard
```

## Time and data semantics

| Field | Meaning | Limitation |
|---|---|---|
| `event_time` | Source-reported chart time | Not necessarily a measurement start, order time, or clinician-view time |
| `available_at` | Declared release time used in the query contract | May be unknown or a documented proxy |
| `availability_source` | `unknown`, `charttime_proxy`, `storetime_proxy`, `synthetic_delay` | Only proxy modes are hypotheses; artificial delays are for tests |
| `stay_id` | ED encounter identifier | Does not equate to admission or patient identity |
| `payload` | Source fields, held in local outputs | Never publish patient-level material to GitHub |

The **strict** mode leaves ED events without verified release evidence unavailable to as-of queries. The hospital storage timestamp is used only when nonmissing and noncontradictory. No inference of clinician observation is made.

## Storage backends

The SQLite adapter stores serialized event documents with an index on `(stay_id, available_at)`. The MongoDB adapter stores corresponding documents with matching query predicates and an index on the same fields. Both responses are compared with a Python reference at identical landmarks.

These are *two implementations of one as-of retrieval contract*, not equivalent full-featured production SQL and document database schemas. The benchmark includes different driver/service overheads; the observed speed difference is not a comparative product claim. Correctness is evaluated against the **declared availability proxy**, not true information available to a clinician.

## Scientific output contract

- All published plots derive from public demonstration source files rather than generated patient records.
- Source archives are downloaded from PhysioNet and checked against its manifests in CI.
- Aggregates document denominator, unit of analysis, missingness, low-count handling, and interpretations.
- Test fixtures and artificial delays are kept distinct from real-data findings.
- No unsupervised clusters, prediction metrics, model attributions, or causal effects are published without a study that supports them.

## Remaining engineering work

Before representing the system as production-grade or bitemporal, implement correction lineage and version-history queries; define a comparable normalized SQL baseline; add model-free temporal stress tests, memory and scaling profiles, repeated environment-controlled performance evaluation, and independent-machine reproducibility. Clinical deployment would require a separately authorized cohort and protocol.
