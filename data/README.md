# Source data are NOT shipped in the repository

Run `python scripts/fetch_demo.py --dataset both` to obtain official PhysioNet v2.2 **public demos** and verify the `SHA256SUMS.txt` manifests, or place the two open v2.2 demos provided for the project under `data/raw/{ed,hosp}/`.

- ED DOI: https://doi.org/10.13026/jzz5-vs76
- Clinical DOI: https://doi.org/10.13026/dp1f-ex47
- License: ODbL-1.0, separate from the research software license.
- Do not commit raw files, patient-level derived tables, local SQLite DBs, credentials, or restricted MetroHealth/MIMIC data.

### Required dataset citations

Johnson, A., Bulgarelli, L., Pollard, T., Celi, L. A., Horng, S., & Mark, R. (2023). *MIMIC-IV-ED Demo (version 2.2).* PhysioNet. https://doi.org/10.13026/jzz5-vs76

Johnson, A., Bulgarelli, L., Pollard, T., Horng, S., Celi, L. A., & Mark, R. (2023). *MIMIC-IV Clinical Database Demo (version 2.2).* PhysioNet. https://doi.org/10.13026/dp1f-ex47

These two **public demonstration datasets** are licensed under the [Open Data Commons ODbL 1.0](https://opendatacommons.org/licenses/odbl/1-0/). The full MIMIC-IV datasets require separate credentialed access. Figures and derived data must be reviewed against applicable attribution and license obligations before wider release.
