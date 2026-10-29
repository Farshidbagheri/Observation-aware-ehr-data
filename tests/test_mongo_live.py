"""Only run in CI with real MongoDB service, or in local Docker environment."""
import os
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
import pytest
from obs_ehr.core import build_event,synthetic_delay
from obs_ehr.benchmark import run_benchmark

@pytest.mark.skipif(os.environ.get("RUN_MONGO_TEST")!="1",reason="Set RUN_MONGO_TEST=1 with a running MongoDB")
def test_mongo_vs_sqlite_live():
    data=[]
    for i in range(10):
        raw={"subject_id":"1", "stay_id":"1", "charttime":f"2026-01-01T10:{i:02d}:00", "heartrate":str(90+i)}
        ev=build_event("vitalsign",raw,i,stay_id="1",event_time=raw["charttime"],available_at=None,
                       availability_source="unknown",dataset="synthetic-fixture")
        data.append(synthetic_delay(ev,seed=12))
    r=run_benchmark(data,backend="both",repeats=2,db="obs_ehr_ci_test")
    assert r["correctness"]["mongodb"]["mismatched_queries"]==0
    assert r["correctness"]["sqlite"]["mismatched_queries"]==0
