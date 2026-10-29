import pytest
from pathlib import Path
from scripts.publication_atlas import wilson,ecdf,metric_status,build

def test_wilson_ci_valid():
    lo,hi=wilson(50,100)
    assert 0<lo<.5<hi<1
    assert wilson(0,20)[0]==0
    assert wilson(20,20)[1]==1

@pytest.mark.parametrize("success,total",[(-1,20),(21,20),(1,0)])
def test_invalid_wilson_rejected(success,total):
    with pytest.raises(ValueError):wilson(success,total)

def test_ecdf_rank_and_limits():
    x,y=ecdf([3,1,2])
    assert list(x)==[1.,2.,3.]
    assert y[0]==pytest.approx(1/3) and y[-1]==1

def test_no_fabricated_model_metrics():
    values=metric_status()
    assert len(values)==16
    assert all(v["status"]=="not_applicable" and v["value"] is None for v in values)

def test_mimic_demo_real_source_and_cross_system_join():
    ed,hosp=Path("data/raw/ed"),Path("data/raw/hosp")
    if not (ed/"edstays.csv.gz").exists() or not (hosp/"labevents.csv.gz").exists():
        pytest.skip("Official demo files are downloaded by the publication workflow")
    report=build(ed,hosp)
    assert report["n_ed_stays"]==222
    assert report["n_vitalsign_rows"]==1038
    assert report["n_hospital_labs"]==107727
    assert report["n_hospital_emar"]==35835
    assert report["matched_ed_window"]=={"labevents":1833,"emar":595}
    assert all(0<=n<=222 for n in report["at_risk_stays"])
    assert all(0<=v["fraction"]<=1 for arr in report["nonvital_record_by_bin"].values()
               for v in arr if v["fraction"] is not None)

def test_metric_registry_complete_and_nonduplicated():
    ids=[m["id"] for m in metric_status()]
    assert len(ids)==len(set(ids))==16
    assert set(ids)=={f"M{i:02d}" for i in range(1,11)} | {f"S{i:02d}" for i in range(1,7)}

def test_wilson_interval_symmetry_near_half():
    a,b=wilson(5,10)
    assert a==pytest.approx(1-b,abs=.00001)

def test_real_ed_subjects_and_at_risk_nonincreasing():
    ed,hosp=Path("data/raw/ed"),Path("data/raw/hosp")
    if not (ed/"edstays.csv.gz").exists() or not (hosp/"labevents.csv.gz").exists():
        pytest.skip("Requires verified real public-demo source")
    r=build(ed,hosp)
    assert r["n_ed_subjects"]==64
    assert r["at_risk_stays"]==sorted(r["at_risk_stays"],reverse=True)
    assert r["at_risk_stays"]==[222,221,221,210,170,63]

def test_real_recording_denominators_and_wilson_bounds():
    ed,hosp=Path("data/raw/ed"),Path("data/raw/hosp")
    if not (ed/"edstays.csv.gz").exists() or not (hosp/"labevents.csv.gz").exists():
        pytest.skip("Requires verified real public-demo source")
    r=build(ed,hosp)
    assert len(r["vital_field_coverage"])==6
    assert all(0<=x["fraction"]<=1 for x in r["vital_field_coverage"])
    assert all(x["wilson95"][0]<=x["fraction"]<=x["wilson95"][1] for x in r["vital_field_coverage"])
    assert all(sum(v is not None for v in row)>0 for row in r["vital_any_record_by_bin_rate"])
