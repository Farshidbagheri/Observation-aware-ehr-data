"""Matched query benchmark with correctness audit and explicit source/limitations."""
from __future__ import annotations
import json
import statistics
import time
from pathlib import Path
from .core import asof_reference,parse_time
from .storage import SQLiteStore,MongoStore


def percentile(samples:list[float],p:float) -> float | None:
    if not samples: return None
    s=sorted(samples)
    import math
    return s[min(len(s)-1,max(0,math.ceil(p*len(s))-1))]


def landmark_queries(records:list[dict],max_stays:int=25) -> list[tuple[str,str]]:
    """Take two deterministic decision landmarks per stay from *documented event times*."""
    by_stay={}
    for e in records:
        if e.get("event_time"):
            by_stay.setdefault(e["stay_id"],[]).append(e["event_time"])
    queries=[]
    for stay, times in sorted(by_stay.items())[:max_stays]:
        ordered=sorted(times)
        queries.append((stay,ordered[len(ordered)//3]))
        queries.append((stay,ordered[(2*len(ordered))//3]))
    return queries


def run_benchmark(records:list[dict],backend:str="sqlite",max_stays:int=25,repeats:int=5,db="obs_ehr_benchmark") -> dict:
    if backend not in {"sqlite","both"}:raise ValueError("backend must be sqlite or both")
    if repeats<1:raise ValueError("repeats must be >=1")
    queries=landmark_queries(records,max_stays=max_stays)
    stores={"sqlite":SQLiteStore()}
    if backend=="both":stores["mongodb"]=MongoStore(db=db)
    report={"bench_version":"0.1.0","dataset_provenance":sorted({r.get("dataset") for r in records}),
            "availability_source_counts":{},"queries":len(queries),"repetitions":repeats,
            "latency_ms":{},"correctness":{},"caveat":"No clinical effect, no timestamp-clinician-view verification, no universal backend speedup claim"}
    for e in records:
        src=e["availability_source"]
        report["availability_source_counts"][src]=report["availability_source_counts"].get(src,0)+1
    try:
        for name,store in stores.items():
            t=time.perf_counter_ns();store.replace(records)
            ingest_ms=(time.perf_counter_ns()-t)/1e6
            mismatch=0;future=0;null_visible=0;latencies=[];checked=0
            for _ in range(repeats):
                for stay,at in queries:
                    t=time.perf_counter_ns(); actual=store.asof(stay,at)
                    latencies.append((time.perf_counter_ns()-t)/1e6)
                    expected=asof_reference(records,stay,at)
                    if [e["event_id"] for e in actual] != [e["event_id"] for e in expected]: mismatch+=1
                    future+=sum(parse_time(e["available_at"])>parse_time(at) for e in actual if e.get("available_at"))
                    null_visible+=sum(not e.get("available_at") for e in actual)
                    checked+=len(actual)
            report["latency_ms"][name]={"ingest_ms":round(ingest_ms,3),"p50":round(statistics.median(latencies),4) if latencies else None,
                                          "p95":round(percentile(latencies,.95),4) if latencies else None,
                                          "n_measurements":len(latencies)}
            report["correctness"][name]={"mismatched_queries":mismatch,"future_available_leaks":future,"unknown_availability_visible":null_visible,"event_returns":checked}
            if mismatch or future or null_visible:raise AssertionError(f"As-of correctness failed: {name} {report['correctness'][name]}")
    finally:
        for store in stores.values():store.close()
    return report
