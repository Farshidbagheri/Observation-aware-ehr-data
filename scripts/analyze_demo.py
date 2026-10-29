"""Offline aggregate-only descriptive reporting from the original public MIMIC-IV demos."""
import argparse
import json
from pathlib import Path
from obs_ehr.analytics import profile,save_report,plot_gallery

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--ed-dir',type=Path,default=Path('data/raw/ed'))
    p.add_argument('--hosp-dir',type=Path,default=Path('data/raw/hosp'))
    p.add_argument('--events',type=Path,default=Path('outputs/events_strict.jsonl'))
    p.add_argument('--report',type=Path,default=Path('reports/local/mimic_demo_profile.json'))
    p.add_argument('--figures',type=Path,default=Path('reports/local/figures'))
    a=p.parse_args();r=profile(a.ed_dir,a.hosp_dir,a.events);save_report(r,a.report)
    charts=plot_gallery(r,a.figures)
    print(json.dumps({'report':str(a.report),'charts':len(charts),'names':charts,
                      'ed_stays':r['unique_ed_stays'],'lab_lag_records':r['hospital_lab_store_lag_sample_size']},indent=2))
if __name__=='__main__':main()
