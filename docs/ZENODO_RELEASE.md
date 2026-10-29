# Zenodo source archive: first software deposit

**Project:** Observation-Aware EHR Data  
**Resource type:** Software  
**Creator:** Farshid Bagheri Saravi  
**Affiliation:** Case Western Reserve University  
**Version:** 0.3.0  
**DOI reserved in existing draft:** `10.5281/zenodo.23752944`  
**Zenodo status:** Draft; **not published, not a citable DOI yet**.

## What to upload

Use a **new GitHub source ZIP downloaded after the licensing/README commit**.
Do not use the older v0.3 source ZIP already in the Zenodo draft: it predates
the MIT license and attribution/DOI documentation. Use the GitHub
**Code → Download ZIP** control, or download the immutable commit-specific source
ZIP after confirming the exact commit SHA.

Upload **only this EHR repository**. Exclude CVs, fellowship proposals, GPU
repository sources, original medical CSV/GZ tables, local JSONL event streams,
credentials, local database files, and any test result with subject identifiers.

Before replacing the ZIP, check it contains `LICENSE`,
`RIGHTS_AND_LICENSES.md`, `CITATION.cff`, `README.md`,
`src/`, `tests/`, `scripts/`, `docs/` and the seven figure pairs.
The GitHub code archive contains only tracked files from that commit,
not ignored `data/raw/` data.

## Zenodo form settings

- Resource type: **Software**
- Title: **Observation-Aware EHR Data: Temporal Provenance and Decision-Time Retrieval**
- Creator: **Farshid Bagheri Saravi**; affiliation: Case Western Reserve University
- Description: summarize tested observation-time storage/retrieval and its limits;
  state that the experiments use public MIMIC-IV demo data and include no
  validated antibiotic-treatment effect or clinical decision system.
- Version: **0.3.0**
- License: **MIT** (remove Zenodo default CC BY 4.0)
- Files access: Public **only after rights and contents have been approved**
- Repository URL: https://github.com/Farshidbagheri/Observation-aware-ehr-data
- Programming language: Python
- Publisher: Zenodo
- Keyword suggestions: electronic health records; clinical informatics;
  observation process; temporal data provenance; MongoDB; SQLite; MIMIC-IV;
  reproducible research; decision-time queries.
- Community, Journal, Thesis, Funding, Dates and Conference: leave empty unless
  accurate and directly supported.
- Related works (optional): link the original MIMIC-IV-ED demo DOI
  `10.13026/jzz5-vs76` and clinical demo DOI `10.13026/dp1f-ex47`.
  These are **source datasets**, not previous versions of this software.

## Essential sequence

1. Save the current Zenodo draft; **do not delete it** or lose its DOI.
2. Confirm author has authority to release this software under MIT.
3. Verify the new GitHub commit passed the relevant automated checks.
4. Download a fresh ZIP from that exact repository commit.
5. In Zenodo draft, **remove the previous ZIP and upload the new one**.
6. Select **MIT** as the software record license, check title, author,
   description, version and attached ZIP.
7. Preview, then click **Publish** only when all content and rights are approved.
8. After Zenodo issues a public record, confirm that the DOI resolves and that
   it is the version-specific DOI. Then update the code repository citation
   and the MongoDB fellowship Research Summary/CV.

An archive with only an unversioned `main` link is less reproducible than the
version/commit-specific package. The reserved DOI is **not** a scientific
peer-review certificate. Future versions of the repository should be deposited
as new versions, not silently substituted into this immutable citation.
