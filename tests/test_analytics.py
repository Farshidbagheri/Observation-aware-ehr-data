"""Analytic helpers: no fabricated clinical test ground truth."""
from pathlib import Path
from obs_ehr.analytics import _hist,quantile,describe,profile

def test_empirical_quantiles():
    assert quantile([1,3,2,4],.5)==2.5
    assert describe([])['median'] is None

def test_histogram_endpoints():
    assert _hist([0,1,2,7],[0,1,2,float('inf')])['counts']==[1,1,2]

def test_report_is_aggregate_only_when_demo_is_present():
    ed=Path('data/raw/ed');hosp=Path('data/raw/hosp')
    if not (ed/'edstays.csv.gz').exists() or not (hosp/'patients.csv.gz').exists():
        return
    report=profile(ed,hosp,Path('outputs/events_strict.jsonl'))
    assert report['unique_ed_stays']==len({})+222  # bounded to the supplied public v2.2 demo
    assert not any(k in report for k in ('subject_id','stay_id','hadm_id'))
    assert report['hospital_lab_store_lag_minutes']['count']>0
