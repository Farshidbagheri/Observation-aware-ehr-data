#!/usr/bin/env python3
"""Audit all 37 real public MIMIC demo CSV schemas; aggregate-only outputs."""
import csv,gzip,json,argparse
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scripts.fetch_demo import DATASETS

KEYS=("subject_id","hadm_id","stay_id","charttime","storetime")
def inventory(root):
    results=[]
    for group in ("ed","hosp"):
        for rel in DATASETS[group]["files"]:
            if not rel.endswith(".csv.gz"):continue
            path=root/group/Path(rel).name
            if not path.exists():raise FileNotFoundError(path)
            with gzip.open(path,"rt",encoding="utf-8",newline="") as f:
                reader=csv.DictReader(f)
                cols=list(reader.fieldnames or [])
                nonmissing={x:0 for x in KEYS if x in cols}
                n=0
                for row in reader:
                    n+=1
                    for x in nonmissing:
                        if row.get(x,"").strip():nonmissing[x]+=1
            results.append({"table":group+"/"+Path(rel).name.replace(".csv.gz",""),
                "n_records":n,"n_columns":len(cols),"columns":cols,
                "key_nonmissing_fraction":{x:round(nonmissing[x]/n,5) if n else None for x in nonmissing}})
    return results

def plot(results,target):
    matrix=np.array([[float("nan") if k not in row["columns"] else row["key_nonmissing_fraction"].get(k) or 0
                     for k in KEYS] for row in results])
    fig,ax=plt.subplots(figsize=(9,15),layout="constrained")
    cmap=plt.colormaps["YlGnBu"].copy();cmap.set_bad("#e3e7ea")
    im=ax.imshow(matrix,aspect="auto",vmin=0,vmax=1,cmap=cmap)
    ax.set_yticks(range(len(results)),[f'{r["table"]}  (n={r["n_records"]:,})' for r in results],fontsize=8)
    ax.set_xticks(range(len(KEYS)),KEYS,rotation=0)
    ax.set_title("07 / CROSS-DATASET SCHEMA FINGERPRINT\nAll 37 verified public-demo CSV sources",loc="left",pad=18,fontsize=13,fontweight="bold")
    fig.colorbar(im,ax=ax,shrink=.35,label="Non-empty fraction among rows (grey = column absent)")
    fig.text(.02,.005,"Source fields only, not clinician-observable decision-time data. Grey is not a missing clinical measurement.",fontsize=8)
    target.parent.mkdir(parents=True,exist_ok=True)
    for ext in ("png","svg"):fig.savefig(target.with_suffix("."+ext),dpi=300,bbox_inches="tight")
    plt.close(fig)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--root",type=Path,default=Path("data/raw"))
    p.add_argument("--out",type=Path,default=Path("evidence/publication_atlas"))
    a=p.parse_args()
    a.out.mkdir(parents=True,exist_ok=True)
    rows=inventory(a.root)
    assert len(rows)==37,f"Expected 37 public-demo CSV source tables; got {len(rows)}"
    (a.out/"all_source_schema_inventory.json").write_text(json.dumps({
        "task":"descriptive_public_demo_schema_audit",
        "source_versions":{"ed":"MIMIC-IV-ED-Demo 2.2","clinical":"MIMIC-IV-Clinical-Demo 2.2"},
        "n_csv_tables":len(rows),"tables":rows},indent=2)+"\n",encoding="utf-8")
    plot(rows,a.out/"figures/07_schema_fingerprint")
    print(f"Audited {len(rows)} real CSV sources; no rows or identifiers exported")

if __name__=="__main__":main()
