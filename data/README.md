# Source data are NOT shipped in the repository

Run `python scripts/fetch_demo.py --dataset both` to obtain official PhysioNet v2.2 **public demos** and verify the `SHA256SUMS.txt` manifests, or place the two open v2.2 demos provided for the project under `data/raw/{ed,hosp}/`.

- ED DOI: https://doi.org/10.13026/jzz5-vs76
- Clinical DOI: https://doi.org/10.13026/dp1f-ex47
- License: ODbL-1.0, separate from the research software license.
- Do not commit raw files, patient-level derived tables, local SQLite DBs, credentials, or restricted MetroHealth/MIMIC data.
