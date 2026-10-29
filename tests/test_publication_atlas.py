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
