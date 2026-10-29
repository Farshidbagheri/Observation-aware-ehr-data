# Publish this independent repository safely

The authorship package is intentionally **not pushed to GitHub yet**. Create a new empty repository in your GitHub account named `observation-aware-ehr-data` (Private until institutional/IP review is complete). Do **not** initialize it with a README because this package includes one already.

After extracting the ZIP in its repository root:

```bash
git init -b main
git add .
git status --short      # Check: data/raw/, outputs/ MUST NOT be staged
git commit -m "Initial observation-aware ED data research demonstrator"
git remote add origin https://github.com/Farshidbagheri/observation-aware-ehr-data.git
git push -u origin main
```

Alternative: create the empty repository first and request ChatGPT to publish the code using the existing GitHub connector, after confirming the repository exists. **Do not modify the earlier NVIDIA/Zenodo release.**

## After publication

- Observe GitHub Actions for both Python core and MongoDB service integration checks.
- Confirm data/raw/, outputs/, any credentials, and PHI are absent from tracked files.
- Run `python scripts/fetch_demo.py --dataset both` on the local machine with Internet access.
- `docker compose up -d` then `python -m obs_ehr benchmark --backend both` for actual local MongoDB measurements.
- Review reproducibility and add exact machine specs before mentioning performance in the fellowship application.
- Do not create a DOI for a draft without a meaningful completed and openly releasable version.
