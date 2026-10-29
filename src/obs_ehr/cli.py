from __future__ import annotations
import argparse
import json
from pathlib import Path
from .core import load_ed, add_hospital_events, read_jsonl, write_jsonl
from .benchmark import run_benchmark
from .toy import generate_toy

def main(argv=None):
    p=argparse.ArgumentParser(description="Observation-aware EHR data research demonstrator")
    sub=p.add_subparsers(dest="cmd",required=True)
    prep=sub.add_parser("prepare",help="Normalize real open-demo source files (not clinical-effect estimation)")
    prep.add_argument("--ed-dir",type=Path,default=Path("data/raw/ed"))
    prep.add_argument("--hosp-dir",type=Path,default=None)
    prep.add_argument("--mode",choices=["strict","proxy","synthetic"],default="strict")
    prep.add_argument("--seed",type=int,default=2026)
    prep.add_argument("--fixture",action="store_true",help="Label all input rows as fictional test fixtures, NEVER as MIMIC")
    prep.add_argument("--output",type=Path,default=Path("outputs/events.jsonl"))
    bench=sub.add_parser("benchmark",help="Run matched as-of queries; strict correctness checks")
    bench.add_argument("--input",type=Path,default=Path("outputs/events.jsonl"))
    bench.add_argument("--backend",choices=["sqlite","both"],default="sqlite")
    bench.add_argument("--repeats",type=int,default=5)
    bench.add_argument("--max-stays",type=int,default=25)
    bench.add_argument("--output",type=Path,default=Path("outputs/benchmark.json"))
    toy=sub.add_parser("toy",help="Separate artificial causal ground truth - NOT MIMIC")
    toy.add_argument("--n",type=int,default=1000)
    toy.add_argument("--output",type=Path,default=Path("outputs/toy_outcomes.jsonl"))
    args=p.parse_args(argv)
    if args.cmd=="prepare":
        records,meta=load_ed(args.ed_dir,mode=args.mode,seed=args.seed,
                             dataset_id="fictional-ed-fixture" if args.fixture else "mimic-iv-ed-demo-v2.2")
        if args.hosp_dir:
            records,hosp_meta=add_hospital_events(records,args.ed_dir,args.hosp_dir,
                                                  dataset_id="fictional-hospital-fixture" if args.fixture else "mimic-iv-clinical-demo-v2.2")
            meta["hospital_join"]=hosp_meta
        n=write_jsonl(args.output,records)
        print(json.dumps({"output":str(args.output),"events":n,"audit":meta},indent=2))
    elif args.cmd=="benchmark":
        report=run_benchmark(read_jsonl(args.input),backend=args.backend,repeats=args.repeats,max_stays=args.max_stays)
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(report,indent=2),encoding="utf-8")
        print(json.dumps(report,indent=2))
    elif args.cmd=="toy":
        n=write_jsonl(args.output,generate_toy(n=args.n))
        print(f"Wrote {n} known-truth *synthetic* rows to {args.output}")

if __name__ == "__main__":main()
