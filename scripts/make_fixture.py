#!/usr/bin/env python3
"""Small, deliberately fabricated fixture, not a clinical data release."""
import csv
import gzip
from pathlib import Path

base=Path('data/fixture')
tables={
 'ed/edstays':[
  {'subject_id':'fake101','hadm_id':'h101','stay_id':'s101','intime':'2026-01-01 10:00:00','outtime':'2026-01-01 14:00:00'},
  {'subject_id':'fake102','hadm_id':'h102','stay_id':'s102','intime':'2026-01-02 10:00:00','outtime':'2026-01-02 14:00:00'}],
 'ed/vitalsign':[
  {'subject_id':'fake101','stay_id':'s101','charttime':'2026-01-01 10:05:00','heartrate':'102'},
  {'subject_id':'fake101','stay_id':'s101','charttime':'2026-01-01 10:45:00','heartrate':'110'},
  {'subject_id':'fake102','stay_id':'s102','charttime':'2026-01-02 11:05:00','heartrate':'99'}],
 'ed/pyxis':[
  {'subject_id':'fake101','stay_id':'s101','charttime':'2026-01-01 10:15:00','name':'FAKE MEDICATION DISPENSE (not administration)'}],
 'hosp/labevents':[
  {'subject_id':'fake101','hadm_id':'h101','charttime':'2026-01-01 10:10:00','storetime':'2026-01-01 11:05:00','valuenum':'2.4'}],
 'hosp/emar':[
  {'subject_id':'fake101','hadm_id':'h101','charttime':'2026-01-01 10:20:00','storetime':'2026-01-01 10:30:00','medication':'FAKE_MEDICATION'}]
}
for rel,rows in tables.items():
    p=base/f'{rel}.csv.gz'
    p.parent.mkdir(parents=True,exist_ok=True)
    with gzip.open(p,'wt',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
print(f'Generated {len(tables)} FICTIONAL small CSV files in {base}. NOT MIMIC.')
