# Research limitations and nonclaims

The project is an observation-process and data-engineering study, not a sepsis detection system or a clinically validated antibiotic timing model.

## Study scope

- The datasets are **selected public de-identified demonstration extracts**, not representative full-population cohorts. The ED subset has 222 stays among 64 people; counts from the hospital tables cannot be read as independent patients.
- The research question of individualized antibiotic initiation in suspected sepsis remains future work. This repository has no adjudicated exposure strategy, verified antibiotic administration time, complete evolving confounders, target trial, or treatment-response effect.
- Dataset chart time, storage time, and any inferred release proxy are distinct from actual clinician viewing or action time. A correct database as-of query is only correct **relative to the declared release model**.
- Source joins use subject, admission and overlapping ED time window. A record excluded by the join is not necessarily wrong or clinically irrelevant; coverage is not complete.
- Missingness and measurement density reflect clinical and documentation processes; biological absence and no recorded measurement are not interchangeable.

## Statistics and visualization

- The figure showing Wilson intervals assumes independent source rows, although patients contribute repeat vitalsign rows. These intervals must be read as **descriptive binomial reference intervals only**, not patient-cluster-corrected confidence limits. Cluster-resampling is a priority improvement.
- Plots are exploratory and do not provide preregistered hypotheses, uncertainty from an external cohort or causal identification.
- Sparse-cell suppression provides a simple precaution but is not a full disclosure-risk assessment for every possible derived output.
- The dashboard requires local browser rendering, as GitHub's repository code view does not execute HTML.

## Data systems

- SQLite stores document payloads as JSON text; comparing it with MongoDB is not a comparison of a conventional normalized relational production schema against a document model.
- The published benchmark records one GitHub runner environment, one bounded query workload and specific indexes. It does not establish scaling behavior, throughput under concurrency, resource utilization, cold-cache performance, or any database's broad superiority.
- The system does not implement an authenticated clinical application, audited clinician access, revision-history bitemporal retrieval, or operational hospital deployment.
- Artificial delays and local fixtures exist **only for deterministic software tests**, not as clinical data or synthetic clinical findings.

## Governance

Raw records and derived patient-level event streams remain outside tracked files. Full restricted MIMIC or MetroHealth sources require separate permissions, institutional governance and appropriate IRB approval. No prospective clinical deployment is claimed.

For evidence and next actions see [verification](../evidence/VERIFICATION.md), [architecture](ARCHITECTURE.md) and [review report](REVIEW_REPORT.md).
