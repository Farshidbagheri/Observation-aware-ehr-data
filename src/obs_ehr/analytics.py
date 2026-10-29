"""Descriptive, auditable analytics on PUBLIC MIMIC-IV v2.2 demos.

No inferred infection, sepsis, antibiotic administration, treatment effect, or
clinician observation time. All patient-level intermediates stay local.
"""
from __future__ import annotations
from collections import Counter, defaultdict
from datetime import timedelta
from pathlib import Path
import json
import math
import statistics

from .core import parse_time, read_table, resolve_csv, read_jsonl


def quantile(values, p):
    values = sorted(float(x) for x in values if math.isfinite(float(x)))
    if not values: return None
    i = (len(values)-1)*p
    lo, hi = math.floor(i), math.ceil(i)
    return round(values[lo]*(1-(i-lo)) + values[hi]*(i-lo),3)


def describe(values):
    x=[float(y) for y in values if math.isfinite(float(y))]
    return {'count':len(x),'p10':quantile(x,.1),'p25':quantile(x,.25),'median':quantile(x,.5),
            'p75':quantile(x,.75),'p90':quantile(x,.9),'p95':quantile(x,.95)}


def profile(ed_dir:Path,hosp_dir:Path,events_path:Path|None=None):
    """Produce aggregate summaries and chart inputs; exclude row-level records."""
    ed = {t: read_table(resolve_csv(ed_dir,t)) for t in
          ('edstays','vitalsign','pyxis','triage','diagnosis','medrecon')}
    hosp = {t: read_table(resolve_csv(hosp_dir,t)) for t in
            ('patients','admissions','labevents','emar')}
    stays=ed['edstays']
    duration=[]
    for s in stays:
        a,b=parse_time(s.get('intime')),parse_time(s.get('outtime'))
        if a and b and b>=a: duration.append((b-a).total_seconds()/3600)
    acuity=Counter(s.get('acuity') or 'unknown' for s in ed['triage'])
    # ED vital charts typically include measurements only sporadically.
    vital_cols=['temperature','heartrate','resprate','o2sat','sbp','dbp','pain']
    vital_presence={k:sum(bool(str(r.get(k,'')).strip()) for r in ed['vitalsign']) for k in vital_cols}
    measurement_hour=Counter()
    for r in ed['vitalsign']:
        t=parse_time(r.get('charttime'))
        if t:measurement_hour[str(t.hour).zfill(2)]+=1
    labs=[];lab_contradictory=0;lab_missing_storetime=0
    for r in hosp['labevents']:
        t,s=parse_time(r.get('charttime')),parse_time(r.get('storetime'))
        if not s: lab_missing_storetime+=1
        if t and s:
            if s<t: lab_contradictory+=1
            else: labs.append((s-t).total_seconds()/60)
    events = read_jsonl(events_path) if events_path and events_path.exists() else []
    kinds=Counter(e['kind'] for e in events)
    sources=Counter(e['availability_source'] for e in events)
    matchable=Counter(e['kind'] for e in events if e['kind'] in {'labevents','emar'})
    at_landmarks={}
    for m in [0,30,60,120,240]:
        n=0
        for s in stays:
            a=parse_time(s.get('intime'))
            if a:
                landmark=a+timedelta(minutes=m)
                n+=sum(e['stay_id']==s['stay_id'] and e.get('available_at') is not None and
                       parse_time(e['available_at'])<=landmark for e in events)
        at_landmarks[str(m)]=n
    return {
      'study':'mimic-iv-ed-demo-2.2+clinical-demo-2.2',
      'analysis_scope':'descriptive data quality and decision-time storage semantics only',
      'data_origins':'real-world deidentified public demo; no synthetic rows included',
      'ed_table_rows':{k:len(v) for k,v in ed.items()},
      'hospital_table_rows':{k:len(v) for k,v in hosp.items()},
      'unique_ed_patients':len({x['subject_id'] for x in stays}),
      'unique_ed_stays':len({x['stay_id'] for x in stays}),
      'ed_stay_hours':describe(duration),
      'ed_stay_hours_hist':_hist(duration,[0,1,2,4,6,8,12,24,float('inf')]),
      'triage_acuity':dict(sorted(acuity.items())),
      'vital_field_nonmissing':vital_presence,
      'vital_row_total':len(ed['vitalsign']),
      'vital_chart_hour':dict(sorted(measurement_hour.items())),
      'hospital_lab_store_lag_minutes':describe(labs),
      'hospital_lab_store_lag_bins':_hist(labs,[0,5,15,30,60,120,240,480,1440,float('inf')]),
      'hospital_lab_store_lag_sample_size':len(labs),
      'hospital_lab_missing_storetime':lab_missing_storetime,
      'hospital_lab_storetime_before_charttime':lab_contradictory,
      'normalized_events_by_type':dict(sorted(kinds.items())),
      'normalized_events_by_availability_assumption':dict(sorted(sources.items())),
      'hospital_ed_window_matches':dict(sorted(matchable.items())),
      'hospital_ed_window_join_fraction':{k:round(v/len(hosp[k]),6) for k,v in matchable.items()},
      'available_event_counts_across_ed_landmarks_minutes':at_landmarks,
      'landmark_scope':'sum across all ED stays; event release uses declared storage proxy only',
      'cautions':[
        'ED source charttime is not verified clinician access time',
        'Hospital storetime is data-storage proxy, not a clinician-observation timestamp',
        'Pyxis is dispensing, not confirmed medication administration',
        'Not a clinically validated sepsis cohort and no antibiotic effect estimates',
        'Individual patient rows and timestamps never enter this aggregate report'
      ]
    }


def _hist(x,bounds):
    counts=[];labels=[]
    for a,b in zip(bounds,bounds[1:]):
        labels.append(f'{a:g}–{b:g}' if math.isfinite(b) else f'≥{a:g}')
        counts.append(sum(a<=v<b for v in x))
    return {'bins':labels,'counts':counts}


def save_report(report:dict,out:Path):
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
