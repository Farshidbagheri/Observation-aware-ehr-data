#!/usr/bin/env python3
"""Download *open* official PhysioNet demo files. Never download credentialed datasets.

Official source pages:
 ED: https://physionet.org/content/mimic-iv-ed-demo/2.2/
 Hospital: https://physionet.org/content/mimic-iv-demo/2.2/
License: Open Data Commons Open Database License v1.0 (consult original LICENSE.txt).
"""
from __future__ import annotations
import argparse
import hashlib
import json
import urllib.request
from pathlib import Path

DATASETS={
    "ed":{
        "base":"https://physionet.org/files/mimic-iv-ed-demo/2.2/",
        "files":["ed/edstays.csv.gz","ed/vitalsign.csv.gz","ed/pyxis.csv.gz",
                 "ed/triage.csv.gz","ed/medrecon.csv.gz","ed/diagnosis.csv.gz",
                 "LICENSE.txt","SHA256SUMS.txt"],
        "citation":"10.13026/jzz5-vs76"},
    "hosp":{
        "base":"https://physionet.org/files/mimic-iv-demo/2.2/",
        "files":['hosp/admissions.csv.gz', 'hosp/d_hcpcs.csv.gz', 'hosp/d_icd_diagnoses.csv.gz', 'hosp/d_icd_procedures.csv.gz', 'hosp/d_labitems.csv.gz', 'hosp/diagnoses_icd.csv.gz', 'hosp/drgcodes.csv.gz', 'hosp/emar.csv.gz', 'hosp/emar_detail.csv.gz', 'hosp/hcpcsevents.csv.gz', 'hosp/labevents.csv.gz', 'hosp/microbiologyevents.csv.gz', 'hosp/omr.csv.gz', 'hosp/patients.csv.gz', 'hosp/pharmacy.csv.gz', 'hosp/poe.csv.gz', 'hosp/poe_detail.csv.gz', 'hosp/prescriptions.csv.gz', 'hosp/procedures_icd.csv.gz', 'hosp/provider.csv.gz', 'hosp/services.csv.gz', 'hosp/transfers.csv.gz', 'icu/caregiver.csv.gz', 'icu/chartevents.csv.gz', 'icu/d_items.csv.gz', 'icu/datetimeevents.csv.gz', 'icu/icustays.csv.gz', 'icu/ingredientevents.csv.gz', 'icu/inputevents.csv.gz', 'icu/outputevents.csv.gz', 'icu/procedureevents.csv.gz', 'LICENSE.txt', 'README.txt', 'SHA256SUMS.txt'],
        "citation":"10.13026/dp1f-ex47"}
}

def fetch(which:str,root:Path) -> dict:
    base=DATASETS[which]["base"]
    target_dir=root/which
    target_dir.mkdir(parents=True,exist_ok=True)
    status=[]
    for item in DATASETS[which]["files"]:
        # Flatten hosp/ed source subfolder to simplify --ed-dir and --hosp-dir.
        dest=target_dir/Path(item).name
        url=base+item
        if not dest.exists():
            req=urllib.request.Request(url,headers={"User-Agent":"ObservationAwareEHR/0.1 (+public-data-only)"})
            with urllib.request.urlopen(req,timeout=90) as r,dest.open("wb") as f:
                while True:
                    chunk=r.read(131072)
                    if not chunk:break
                    f.write(chunk)
        h=hashlib.sha256(dest.read_bytes()).hexdigest()
        status.append({"file":str(dest),"url":url,"sha256":h,"bytes":dest.stat().st_size})
    # Check downloaded content against the official source's SHA256SUMS.txt.
    # The source archive preserves ed/ and hosp/ prefixes; local paths are flattened.
    expected = {}
    hashes = (target_dir / "SHA256SUMS.txt").read_text(encoding="utf-8")
    for line in hashes.splitlines():
        fields = line.strip().split(maxsplit=1)
        if len(fields) == 2 and len(fields[0]) == 64:
            expected[Path(fields[1].lstrip("*/")).name] = fields[0].lower()
    for entry in status:
        filename = Path(entry["file"]).name
        if filename == "SHA256SUMS.txt":
            continue
        if filename not in expected:
            raise ValueError(f"Official SHA256 manifest does not list {filename}")
        if entry["sha256"].lower() != expected[filename]:
            raise ValueError(f"SHA256 MISMATCH for {filename}: source may be corrupted or different version")
        entry["sha256_verified"] = True
    # Manifest is derived, not a claim about data privacy beyond official demo policy.
    report={"dataset":which,"doi":DATASETS[which]["citation"],"files":status,
            "license":"ODbL-1.0 for source data; preserve original LICENSE.txt and attribution"}
    (target_dir/"download_manifest.json").write_text(json.dumps(report,indent=2))
    return report

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--dataset",choices=["ed","hosp","both"],default="ed")
    p.add_argument("--root",type=Path,default=Path("data/raw"))
    a=p.parse_args()
    for ds in (["ed","hosp"] if a.dataset=="both" else [a.dataset]):
        report=fetch(ds,a.root)
        print(f"{ds}: downloaded/verified local hashes for {len(report['files'])} files. See {a.root/ds/'download_manifest.json'}")
