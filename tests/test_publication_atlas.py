import pytest
from pathlib import Path
from scripts.publication_atlas import patient_cluster_interval, ecdf, metric_status, build


def test_patient_cluster_interval_is_deterministic():
    rows=[
        {"subject_id":"A","heartrate":"72"},
        {"subject_id":"A","heartrate":"75"},
        {"subject_id":"B","heartrate":""},
        {"subject_id":"C","heartrate":"83"},
    ]
    a,n=patient_cluster_interval(rows,"heartrate",replicates=1000,seed=41)
    b,m=patient_cluster_interval(rows,"heartrate",replicates=1000,seed=41)
    assert a==b and n==m==3
    assert 0<=a[0]<=a[1]<=1


def test_patient_cluster_extremes_and_invalid_request():
    rows=[{"subject_id":str(i),"o2sat":"98"} for i in range(12)]
    interval,n=patient_cluster_interval(rows,"o2sat",replicates=200,seed=11)
    assert interval==[1.,1.] and n==12
    with pytest.raises(ValueError):
        patient_cluster_interval(rows,"o2sat",replicates=10)


def test_ecdf_rank_and_limits():
    x,y=ecdf([3,1,2])
    assert list(x)==[1.,2.,3.]
    assert y[0]==pytest.approx(1/3) and y[-1]==1


def test_no_fabricated_model_metrics():
    values=metric_status()
    assert len(values)==16
    assert all(v["status"]=="not_applicable" and v["value"] is None for v in values)


def test_metric_registry_complete_and_nonduplicated():
    ids=[m["id"] for m in metric_status()]
    assert len(ids)==len(set(ids))==16
    assert set(ids)=={f"M{i:02d}" for i in range(1,11)} | {f"S{i:02d}" for i in range(1,7)}


def public_demo():
    ed,hosp=Path("data/raw/ed"),Path("data/raw/hosp")
    if not (ed/"edstays.csv.gz").exists() or not (hosp/"labevents.csv.gz").exists():
        pytest.skip("Requires verified real public-demo source")
    return build(ed,hosp)


def test_real_mimic_source_and_cross_system_join():
    r=public_demo()
    assert r["n_ed_stays"]==222
    assert r["n_ed_subjects"]==64
    assert r["n_vitalsign_rows"]==1038
    assert r["n_hospital_labs"]==107727
    assert r["n_hospital_emar"]==35835
    assert r["matched_ed_window"]=={"labevents":1833,"emar":595}
    assert r["at_risk_stays"]==[222,221,221,210,170,63]


def test_real_demo_clustered_interval_is_bounded_and_reproducible():
    r=public_demo()
    assert r["uncertainty_method"]["resamples"]==2000
    assert r["uncertainty_method"]["unit"]=="subject_id"
    assert len(r["vital_field_coverage"])==6
    for q in r["vital_field_coverage"]:
        assert q["patients_with_vital_rows"]==54
        assert 0<=q["fraction"]<=1
        lo,hi=q["patient_cluster_bootstrap95"]
        assert 0<=lo<=hi<=1


def test_real_recording_denominators_are_monotone():
    r=public_demo()
    assert r["at_risk_stays"]==sorted(r["at_risk_stays"],reverse=True)
    assert all(sum(v is not None for v in row)>0 for row in r["vital_any_record_by_bin_rate"])
    assert all(0<=v["fraction"]<=1 for arr in r["nonvital_record_by_bin"].values()
               for v in arr if v["fraction"] is not None)
