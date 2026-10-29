# Rights, licenses and research-data attribution

The repository contains **original research software and documentation** plus
**aggregate figures derived from public clinical demonstration data**.
The software license and the data-source license are different.

## Original research software: MIT

Copyright © 2026 Farshid Bagheri Saravi.

The author's original Python modules, test code, analysis scripts and original
software documentation are made available under the [MIT License](LICENSE),
provided the author has the legal right to grant that license. The MIT grant
applies only to original materials owned or appropriately licensed by the author.
It does **not** transfer ownership of any source datasets, institutional work,
or other parties' intellectual property.

If any source was developed under an agreement assigning rights to an institution,
sponsor or collaborator, obtain the required written permission **before public
release**. The license file cannot override such rights or employment terms.

## Public source data: ODbL 1.0, not MIT

This repository does **not** include any raw MIMIC CSV or compressed clinical
source tables. Its acquisition script downloads two openly available public
demonstration sources directly from PhysioNet:

- Johnson, A., Bulgarelli, L., Pollard, T., Celi, L. A., Horng, S. & Mark, R.
  (2023). *MIMIC-IV-ED Demo, version 2.2*. PhysioNet.
  https://doi.org/10.13026/jzz5-vs76
- Johnson, A., Bulgarelli, L., Pollard, T., Horng, S., Celi, L. A. & Mark, R.
  (2023). *MIMIC-IV Clinical Database Demo, version 2.2*. PhysioNet.
  https://doi.org/10.13026/dp1f-ex47

Both original databases are distributed under **Open Data Commons Open
Database License 1.0 (ODbL 1.0)**, rather than MIT. Consult and preserve
the original PhysioNet license and attribution when using or redistributing
any data or adapted database. All real-data illustrations and aggregate
statistics here are derived from those openly available demonstration sources,
with provenance and denominators documented in
[docs/FIGURES.md](docs/FIGURES.md).

The *full*, credential-restricted MIMIC-IV / MIMIC-IV-ED databases and
institutional healthcare data are **not included**, and no permission to share
those records is conferred by the public demos.

## Research results, third-party packages and clinical limitations

- Figures are descriptive outputs from the public demo; neither data nor
  aggregate plots establish actual clinician information access.
- This repository does not reproduce or license other research groups' source code.
  Third-party software dependencies retain their own licenses.
- No patient-level original MIMIC records, normalized local event streams,
  restricted clinical databases, secrets or credential files belong in a release.
- This is research software, **not** a medical device, patient-specific treatment
  recommendation, clinical sepsis-effect estimate or externally validated model.

## Published Zenodo software archive and citations

**Published research software:** Farshid Bagheri Saravi (2026).
*Observation-Aware EHR Data: Temporal Provenance and Decision-Time Retrieval*
(Version 0.3.0) [Computer software]. Zenodo.
https://doi.org/10.5281/zenodo.23752944

- **Version-specific DOI:** https://doi.org/10.5281/zenodo.23752944
- **All-versions concept DOI:** https://doi.org/10.5281/zenodo.23752943
- **Software license in the deposited record:** MIT
- **Source snapshot associated with the software deposit:**
  https://github.com/Farshidbagheri/Observation-aware-ehr-data/tree/b9bcdc523d6416dec471699edfb8ede590a3378a
- **Archive documentation:** [docs/ZENODO_RELEASE.md](docs/ZENODO_RELEASE.md)

Zenodo's record-level MIT license applies to the author's original licensed
software. The original public MIMIC source databases are separately offered
under ODbL 1.0 and are not distributed inside this source ZIP.
No DOI certifies peer review, clinical validation or external performance.

The software author's MIT copyright statement is not a legal determination
of institutional or coauthor rights. Public release is conditioned on the
author verifying those rights.
