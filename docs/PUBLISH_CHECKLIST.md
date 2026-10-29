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
- [x] Author states this is independently authored, non-sponsored code and has chosen MIT for original software. Review any contrary institutional/IP agreements if applicable.
- [x] Dataset attribution and citation metadata are recorded; v0.3.0 Zenodo archive is published.
- [x] Archived software has a version DOI and a pinned source commit: [Zenodo v0.3.0](https://doi.org/10.5281/zenodo.23752944), [source snapshot](https://github.com/Farshidbagheri/Observation-aware-ehr-data/tree/b9bcdc523d6416dec471699edfb8ede590a3378a).
- [ ] Optional: create a GitHub v0.3.0 tag/release pointing to the archived snapshot (no tag is implied by the DOI).

**Publication status:** GitHub source is public and the v0.3.0 Zenodo software deposit is published under MIT. Remaining independent scientific review and dependency/environment locking are quality-improvement tasks, not claims of clinical validation. Do not publish restricted clinical data.
