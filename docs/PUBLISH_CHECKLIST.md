# Research release checklist

- [x] Source code and publication atlas are stored in this repository.
- [x] The original MIMIC-IV public demo datasets and SHA-256 acquisition requirements are documented.
- [x] The atlas has been generated in a successful independent GitHub Actions run.
- [x] Real MongoDB and SQLite queries were compared in the recorded limited benchmark.
- [x] Raw patient-level data and locally normalized event streams are excluded from tracked artifacts.
- [x] Both code-validation and atlas workflows completed successfully for the validated source revision ([research](https://github.com/Farshidbagheri/Observation-aware-ehr-data/actions/runs/40804105789), [atlas](https://github.com/Farshidbagheri/Observation-aware-ehr-data/actions/runs/40804105595)). Check any newer commit separately.
- [ ] An independent reviewer signs off on figures, numerical denominators, and interpretations against the source tables.
- [ ] A lockfile, environment image, and repeatability record have been archived.
- [x] Original software MIT license text and third-party ODbL attribution are documented.
- [ ] Author confirms authority to grant MIT rights under any institutional, employment, sponsor, or collaboration agreements.
- [x] Data-source attribution and citation metadata are recorded; final archive release notes remain pending.
- [ ] An immutable repository release is tagged and linked to an archive/DOI (if appropriate).

**Publication decision:** remain private pending authorization to release research code, choice of software license, and manual content review. The source data used are separately public under ODbL 1.0. The repository description and topics also need to be set in GitHub's About panel.  A citation file does not grant reuse rights. Do not publish MetroHealth or other restricted clinical data.
