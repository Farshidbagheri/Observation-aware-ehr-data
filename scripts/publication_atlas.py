#!/usr/bin/env python3
"""Real MIMIC-IV v2.2 DEMO descriptive observation-process atlas.

No simulated patients, clinical outcome estimates, sepsis labels, or counterfactuals.
Charttime is recording time; storetime is only a recording proxy; Pyxis != administration.
This module exports only aggregate evidence and figure assets.
"""
from __future__ import annotations
import argparse, json, math
from pathlib import Path
from collections import defaultdict
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from obs_ehr.core import read_table, resolve_csv, parse_time

BINS=(0,30,60,120,240,480,10**7)
LABELS=("0–30m","30–60m","1–2h","2–4h","4–8h","8+h")
FIELDS=("heartrate","resprate","o2sat","sbp","dbp","temperature")
NAMES=("Heart rate","Respiratory rate","SpO2","Systolic BP","Diastolic BP","Temperature")
PALETTE=("#0d9488","#4361a8","#d6a15d","#ba718a")
MIN_CELL=10

def patient_cluster_interval(rows, field, *, replicates=2000, seed=2026):
    """Percentile bootstrap of field completeness, resampling patients as clusters.

    The target is source-row completeness in this *selected demo*, not a
    confidence limit for an external patient population.
    """
    by_patient=defaultdict(lambda: [0, 0])
    for row in rows:
        patient=row["subject_id"]
        by_patient[patient][0]+=1
        by_patient[patient][1]+=int(bool(row.get(field,"").strip()))
    clusters=np.asarray(list(by_patient.values()),dtype=np.int64)
    if not len(clusters): raise ValueError("No patient clusters")
    if replicates<100:raise ValueError("Too few bootstrap replicates")
    rng=np.random.default_rng(seed)
    samples=rng.integers(0,len(clusters),size=(replicates,len(clusters)))
    totals=clusters[samples].sum(axis=1)
    assert np.all(totals[:,0]>0)
    rates=totals[:,1]/totals[:,0]
    lo,hi=np.quantile(rates,[.025,.975])
    return [round(float(lo),5),round(float(hi),5)],len(clusters)


def ecdf(values):
    x=np.sort(np.asarray(values,dtype=float))
    return x,np.arange(1,len(x)+1)/len(x)

def metric_status():
    why="No trained prediction model, adjudicated ED clinical outcome, disjoint test predictions, or identifiable causal estimand in this descriptive demo."
    metrics=[{"id":f"M{i:02d}","status":"not_applicable","value":None,"reason":why} for i in range(1,11)]
    metrics += [{"id":f"S{i:02d}","status":"not_applicable","value":None,
        "reason":"No validated signal reference, event annotations, imaging mask, or survival/competing-risk reference."} for i in range(1,7)]
    return metrics

def build(ed,hosp):
    stays=read_table(resolve_csv(ed,"edstays"))
    vit=read_table(resolve_csv(ed,"vitalsign"))
    pyxis=read_table(resolve_csv(ed,"pyxis"))
    labs=read_table(resolve_csv(hosp,"labevents"))
    emar=read_table(resolve_csv(hosp,"emar"))
    sid={str(s["stay_id"]):s for s in stays}
    dur={k:(parse_time(s["outtime"])-parse_time(s["intime"])).total_seconds()/60 for k,s in sid.items()}
    if any(v<0 for v in dur.values()):raise ValueError("Negative ED duration")
    at_risk=[sum(d>=lo for d in dur.values()) for lo in BINS[:-1]]
    marks={f:[set() for _ in LABELS] for f in (*FIELDS,"pyxis","labevents","emar")}
    def record(kind,k,t):
        if not t or k not in sid:return
        minute=(t-parse_time(sid[k]["intime"])).total_seconds()/60
        if not 0<=minute<=dur[k]:return
        for j,(lo,hi) in enumerate(zip(BINS,BINS[1:])):
            if lo<=minute<hi:
                marks[kind][j].add(k)
                break
    for v in vit:
        t=parse_time(v.get("charttime"));k=str(v["stay_id"])
        for f in FIELDS:
            if v.get(f,"").strip():record(f,k,t)
    for p in pyxis:record("pyxis",str(p["stay_id"]),parse_time(p.get("charttime")))
    index=defaultdict(list)
    for s in stays:
        if s.get("hadm_id"):index[(s["subject_id"],s["hadm_id"])].append(s)
    joined={"labevents":0,"emar":0}
    for name,rows in (("labevents",labs),("emar",emar)):
        for row in rows:
            t=parse_time(row.get("charttime"))
            if not t:continue
            for s in index.get((row.get("subject_id"),row.get("hadm_id")),[]):
                if parse_time(s["intime"])<=t<=parse_time(s["outtime"]):
                    joined[name]+=1;record(name,str(s["stay_id"]),t);break
    coverage=[]
    for f in FIELDS:
        n=sum(bool(v.get(f,"").strip()) for v in vit)
        interval,clusters=patient_cluster_interval(vit,f)
        coverage.append({"field":f,"recorded":n,"denominator":len(vit),
            "fraction":round(n/len(vit),5),"patient_cluster_bootstrap95":interval,
            "patients_with_vital_rows":clusters})
    matrix=[]
    for f in FIELDS:
        matrix.append([round(len(marks[f][j])/at_risk[j],5)
           if at_risk[j]>=MIN_CELL and len(marks[f][j])>=MIN_CELL else None for j in range(6)])
    series={}
    for name in ("pyxis","labevents","emar"):
        series[name]=[{"n_stays":len(marks[name][j]),"eligible_stays":at_risk[j],
            "fraction":round(len(marks[name][j])/at_risk[j],5)
              if at_risk[j]>=MIN_CELL and len(marks[name][j])>=MIN_CELL else None}
            for j in range(6)]
    lag=[];missing=0;reverse=0
    for l in labs:
        t=parse_time(l.get("charttime"));s=parse_time(l.get("storetime"))
        if not s:missing+=1
        elif t and s<t:reverse+=1
        elif t:lag.append((s-t).total_seconds()/60)
    return {"study":"MIMIC-IV ED Demo 2.2 + Clinical Demo 2.2",
       "task_profile":"no_predictive_model","n_ed_stays":len(stays),
       "n_ed_subjects":len(set(s["subject_id"] for s in stays)),
       "n_vitalsign_rows":len(vit),"n_pyxis_rows":len(pyxis),
       "n_hospital_labs":len(labs),"n_hospital_emar":len(emar),
       "matched_ed_window":joined,"time_bin_labels":LABELS,
       "at_risk_stays":at_risk,"vital_any_record_by_bin_rate":matrix,
       "vital_field_coverage":coverage,"nonvital_record_by_bin":series,
       "uncertainty_method":{"name":"patient_cluster_percentile_bootstrap","resamples":2000,"seed":2026,
           "unit":"subject_id","target":"field presence among source vital rows in selected demo"},
       "lab_record_lag_n":len(lag),"lab_store_missing_n":missing,
       "lab_store_before_chart_n":reverse,
       "_duration_minutes":list(dur.values()),"_lag_minutes":lag}

def figures(r,root):
    root.mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({"font.size":10,"axes.spines.top":False,"axes.spines.right":False,
        "savefig.dpi":300,"font.family":"DejaVu Sans"})
    def save(fig,name):
        fig.text(.02,-.035,"PUBLIC MIMIC v2.2 demos | descriptive only | no clinical treatment-effect inference",
            fontsize=8,color="#53677b")
        for ext in ("png","svg"):fig.savefig(root/(name+"."+ext),bbox_inches="tight",facecolor="white")
        plt.close(fig)
    mat=np.array([[np.nan if v is None else v for v in row] for row in r["vital_any_record_by_bin_rate"]])
    fig,(a,b)=plt.subplots(2,1,figsize=(10,7),layout="constrained",gridspec_kw={"height_ratios":[5,1]})
    cm=plt.colormaps["YlGnBu"].copy();cm.set_bad("#e9edf0")
    im=a.imshow(mat,aspect="auto",vmin=0,vmax=1,cmap=cm)
    a.set_yticks(range(6),NAMES);a.set_xticks(range(6),LABELS)
    a.set_title("01 / ED OBSERVATION MATRIX · recorded features by time",loc="left",pad=16)
    for i in range(6):
        for j in range(6):
            a.text(j,i,"—" if np.isnan(mat[i,j]) else f"{mat[i,j]*100:.0f}%",
             ha="center",va="center",color="white" if not np.isnan(mat[i,j]) and mat[i,j]>.55 else "#213548")
    fig.colorbar(im,ax=a,label="Stays with a recorded feature / eligible stays",shrink=.78)
    b.step(range(6),r["at_risk_stays"],where="mid",color=PALETTE[1],lw=3)
    b.set_xticks(range(6),LABELS);b.set_ylabel("Eligible stays");b.set_ylim(bottom=0)
    b.set_title("Eligibility denominators · suppressed if recorded stays <10",loc="left",fontsize=9)
    save(fig,"01_observation_atlas")
    fig,ax=plt.subplots(figsize=(10,5.5),layout="constrained")
    for y,(label,q) in enumerate(zip(NAMES[::-1],r["vital_field_coverage"][::-1])):
        lo,hi=q["patient_cluster_bootstrap95"]
        ax.plot([100*lo,100*hi],[y,y],color=PALETTE[1],lw=3)
        ax.scatter(100*q["fraction"],y,color=PALETTE[0],s=75,zorder=3)
        ax.text(100*hi+2,y,f"{q['recorded']}/{q['denominator']}",va="center")
    ax.set_yticks(range(6),NAMES[::-1]);ax.set_xlim(0,125)
    ax.set_xlabel("Completeness of source vitalsign rows (%)")
    ax.set_title("02 / PATIENT-CLUSTER BOOTSTRAP · vital-field completeness",loc="left",pad=14)
    ax.grid(axis="x",alpha=.2);save(fig,"02_completeness_intervals")
    fig,ax=plt.subplots(figsize=(10,5.8),layout="constrained")
    for name,color in zip(("pyxis","labevents","emar"),PALETTE):
        rates=[np.nan if v["fraction"] is None else 100*v["fraction"]
           for v in r["nonvital_record_by_bin"][name]]
        ax.plot(range(6),rates,marker="o",lw=2.5,label=name,color=color)
    ax.set_xticks(range(6),LABELS);ax.set_ylim(0,105)
    ax.set_ylabel("Eligible stays with ≥1 recorded event (%)")
    ax.set_xlabel("Minutes after ED arrival (not treatment time)")
    ax.set_title("03 / MULTISOURCE OBSERVATION INTENSITY",loc="left",pad=14)
    ax.legend(ncol=3,frameon=False);ax.grid(alpha=.2)
    save(fig,"03_temporal_recording")
    fig,(a,b)=plt.subplots(1,2,figsize=(11,5),layout="constrained")
    d=np.array(r["_duration_minutes"])/60
    x,y=ecdf(d);a.step(x,y,lw=3,color=PALETTE[0])
    a.set(xlabel="ED stay duration (hours)",ylabel="Empirical cumulative fraction")
    a.set_title("ECDF · n="+str(r["n_ed_stays"]),loc="left");a.grid(alpha=.2)
    b.boxplot(d,vert=False,patch_artist=True,boxprops={"facecolor":"#a8d7d3"})
    b.set_yticks([]);b.set_xlabel("ED stay duration (hours)")
    b.set_title("Median, IQR and outliers",loc="left")
    fig.suptitle("04 / ED ENCOUNTER DURATION DISTRIBUTIONS",fontweight="bold")
    save(fig,"04_encounter_duration")
    fig,(a,b)=plt.subplots(1,2,figsize=(11,5),layout="constrained")
    lag=np.asarray(r["_lag_minutes"],dtype=float);x,y=ecdf(lag)
    a.step(x,y,lw=3,color=PALETTE[1]);a.set_xlim(0,min(1440,max(1,np.quantile(lag,.99))))
    a.set(xlabel="Store − chart lag, minutes (axis clipped to p99)",ylabel="Cumulative fraction")
    a.set_title("ECDF · valid laboratory lags",loc="left")
    b.hist(lag[lag<=240],bins=np.linspace(0,240,49),color=PALETTE[0],edgecolor="white")
    b.set(xlabel="Recording lag, minutes (0–240)",ylabel="Hospital lab records")
    b.set_title("High-resolution histogram",loc="left")
    fig.suptitle("05 / LAB RECORDING LATENCY · NOT CLINICIAN VIEWING TIME",fontweight="bold")
    save(fig,"05_lab_recording_lag")
    # The source is partitioned into matched vs unmatched rows.
    # Draw two outgoing branches; unmatched rows are NOT downstream of matched ones.
    fig,ax=plt.subplots(figsize=(11,6),layout="constrained")
    ax.set(xlim=(0,10),ylim=(0,4.6));ax.axis("off")
    for j,(name,total,match) in enumerate([
        ("labevents",r["n_hospital_labs"],r["matched_ed_window"]["labevents"]),
        ("eMAR",r["n_hospital_emar"],r["matched_ed_window"]["emar"])
    ]):
        y=3.45-2.05*j
        ax.text(2.0,y,f"{name} source\n{total:,} rows",ha="center",va="center",
                color="white",fontweight="bold",
                bbox={"boxstyle":"round,pad=.7","fc":"#213d57","ec":"none"})
        ax.text(7.15,y+.44,f"Matched to ED interval\n{match:,} rows",
                ha="center",va="center",color="white",fontweight="bold",
                bbox={"boxstyle":"round,pad=.65","fc":"#106e73","ec":"none"})
        ax.text(7.15,y-.44,f"Not matched to ED interval\n{total-match:,} rows",
                ha="center",va="center",color="white",fontweight="bold",
                bbox={"boxstyle":"round,pad=.65","fc":"#8d585e","ec":"none"})
        for dy in (+.44,-.44):
            ax.annotate("",xy=(5.12,y+dy),xytext=(3.25,y),
                        arrowprops={"arrowstyle":"-|>","lw":2,"color":"#7893a4"})
    ax.set_title("06 / CROSS-SYSTEM RECORD LINKAGE · two exclusive outcomes",
                 loc="left",pad=16)
    save(fig,"06_cross_source_linkage")
    return sorted(p.name for p in root.glob("*.svg"))

def dashboard(r,names,path):
    from html import escape
    cards="".join('<article><img loading="lazy" src="figures/'+escape(n)+'" alt="'+escape(n)+'"><h2>'+
       escape(n[:-4].replace("_"," ").title())+'</h2></article>' for n in names)
    items=[("ED stays",r["n_ed_stays"]),("ED patients",r["n_ed_subjects"]),
           ("Vital rows",r["n_vitalsign_rows"]),("ED-linked lab rows",r["matched_ed_window"]["labevents"])]
    boxes="".join(f"<div class='k'><small>{escape(k)}</small><strong>{v:,}</strong></div>" for k,v in items)
    html='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Observation Atlas · MIMIC v2.2 demo</title><style>:root{font:16px system-ui;color:#152c41;background:#edf3f7}body{margin:0}header{padding:3em 5vw;background:linear-gradient(110deg,#142940,#087c7d);color:white}header h1{font-size:clamp(2em,5vw,4em);margin:.25em 0}header p{max-width:800px;color:#d5f2f1;line-height:1.6}main{max-width:1250px;margin:auto;padding:2em}.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:1em}.k,article,aside{background:white;border-radius:14px;padding:1.1em;box-shadow:0 8px 32px #0a304011}.k small{display:block;color:#60758a}.k strong{font-size:2em}.gallery{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,530px),1fr));gap:1.4em;margin-top:1.5em}article img{width:100%}article h2{font-size:1em}aside{margin-top:1.4em;border-left:5px solid #087c7d}footer{text-align:center;padding:2em;color:#64748b}</style><header><div>REPRODUCIBLE CLINICAL DATA ENGINEERING · PUBLIC MIMIC DEMOS</div><h1>Observation Atlas</h1><p>What was recorded, when, and how EHR events link across systems. Every figure is generated from real deidentified public-demo records with explicitly described denominators. Not a diagnosis system or causal treatment model.</p></header><main><div class="kpis">__BOXES__</div><aside><strong>Scientific validity boundary:</strong> charttime ≠ clinician availability; storetime ≠ verified clinician access; Pyxis dispensing ≠ drug administration. Suppressed small cells are not biological negatives. No model accuracy, causal effect or clinical benefit is claimed.</aside><div class="tools"><label for="figure-search">Explore research figures</label> <input id="figure-search" aria-label="Filter figure titles" type="search" placeholder="Search: temporal, observation, linkage…" autocomplete="off"></div><div class="gallery">__CARDS__</div><dialog id="lightbox" aria-label="Expanded scientific figure"><button id="close" type="button">Close enlarged figure ×</button><img alt="" style="display:block;max-width:95vw;max-height:85vh;width:auto" id="expanded"></dialog></main><script>const box=document.getElementById("lightbox"),expanded=document.getElementById("expanded");document.querySelectorAll(".gallery article img").forEach(el=>{el.tabIndex=0;el.style.cursor="zoom-in";const show=()=>{expanded.src=el.src;expanded.alt=el.alt;box.showModal()};el.addEventListener("click",show);el.addEventListener("keydown",e=>{if(e.key==="Enter")show()})});document.getElementById("close").addEventListener("click",()=>box.close());document.getElementById("figure-search").addEventListener("input",e=>document.querySelectorAll(".gallery article").forEach(card=>{card.hidden=!card.textContent.toLowerCase().includes(e.target.value.toLowerCase())}));</script><footer>MIMIC-IV-ED Demo 2.2 and MIMIC-IV Demo 2.2 · ODbL 1.0 · Research use only</footer></html>'''
    path.write_text(html.replace("__BOXES__",boxes).replace("__CARDS__",cards),encoding="utf-8")

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--ed-dir",type=Path,default=Path("data/raw/ed"))
    p.add_argument("--hosp-dir",type=Path,default=Path("data/raw/hosp"))
    p.add_argument("--output",type=Path,default=Path("evidence/publication_atlas"))
    a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
    r=build(a.ed_dir,a.hosp_dir)
    clean={k:v for k,v in r.items() if not k.startswith("_")}
    # Suppress small bin-level counts in machine-readable public results, not only figures.
    clean["nonvital_record_by_bin"]={name:[{**q,"n_stays":None if q["n_stays"]<MIN_CELL else q["n_stays"]}
       for q in series] for name,series in clean["nonvital_record_by_bin"].items()}
    clean["evaluation_applicability"]=metric_status()
    clean["figure_ids"]={"V01":"implemented_as_aggregated_observation_matrix",
        "V02":"not_applicable_no_validated_embedding",
        "V03":"implemented_as_aggregated_record_linkage_flow",
        "V04":"not_applicable_no_fitted_prediction_model",
        "V05":"not_applicable_no_attention_model"}
    clean["quality_gate"]={"fabricated_patient_rows":False,"outcome_estimates":False,
        "small_heatmap_cells_suppressed":True,"publication_use":"exploratory_only"}
    (a.output/"aggregate_results.json").write_text(json.dumps(clean,indent=2,ensure_ascii=False)+"\n")
    names=figures(r,a.output/"figures")
    dashboard(r,names,a.output/"index.html")
    (a.output/"QA.md").write_text("""# Descriptive research atlas QA

- Origin: official public MIMIC-IV-ED Demo 2.2 and MIMIC-IV Clinical Demo 2.2; SHA256 verified during acquisition.
- Unit: ED encounter for temporal panels; vitalsign row for field completeness; laboratory record for recording delays.
- Time zero: ED arrival; no retrospectively inferred Sepsis-3 onset.
- Denominator: ED stays still eligible at each time-bin start, not all source rows.
- Small cells: suppressed if fewer than ten stays with a recorded observation.
- Patient-cluster 95% percentile intervals: 2,000 bootstrap replicates sampling patients (subject_id) with replacement, seed 2026; completeness is row-weighted within the selected demo. Not externally representative.
- Pyxis is medication dispensing, not verified administration.
- STORETIME is recording proxy and does not prove observation by a clinician.
- No trained predictive model, adjudicated sepsis outcome, valid counterfactual policy evaluation, or external validation.
- Primary source citations: https://doi.org/10.13026/jzz5-vs76 and https://doi.org/10.13026/dp1f-ex47.
- SVG and PNG are produced from the same real aggregate input; JSON is machine-readable and excludes patient identifiers.
""",encoding="utf-8")
    print(json.dumps({"n_figures":len(names),"n_ed_stays":r["n_ed_stays"],"matched":r["matched_ed_window"]}))

if __name__=="__main__":main()
