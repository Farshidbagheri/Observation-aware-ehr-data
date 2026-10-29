"""Render a self-contained HTML dashboard from aggregate-only evidence (NO patient rows)."""
from __future__ import annotations
import argparse
import html
import json
from pathlib import Path

def render(data, destination:Path):
    charts=[]
    def add(name,typ,labels,values,title):
        charts.append({'id':name,'type':typ,'labels':labels,'values':values,'title':title})
    for name,k,title in [('ed-tables','ed_table_rows','ED source tables'),('hosp-tables','hospital_table_rows','Hospital source tables'),('acuity','triage_acuity','Triage acuity codes'),('vitals','vital_field_nonmissing','Vital-field availability'),('hour','vital_chart_hour','Clock-hour charting'),('kinds','normalized_events_by_type','Canonical ledger categories'),('availability','normalized_events_by_availability_assumption','Availability semantics'),('matches','hospital_ed_window_matches','ED-window hospital joins'),('fraction','hospital_ed_window_join_fraction','Joined share of hospital records'),('landmarks','available_event_counts_across_ed_landmarks_minutes','Stored records by ED landmark')]:
        d=data[k]
        add(name,'line' if name in ('hour','landmarks') else 'bar',list(d),list(d.values()),title)
    for name,k,title in [('durations','ed_stay_hours_hist','ED duration bins'),('lag','hospital_lab_store_lag_bins','Lab chart-to-store lag bins')]:
        d=data[k];add(name,'bar',d['bins'],d['counts'],title)
    cfg=json.dumps(charts,ensure_ascii=False).replace('<','\\u003c')
    stats=[('ED stays',data['unique_ed_stays']),('ED patients',data['unique_ed_patients']),('Canonical events',sum(data['normalized_events_by_type'].values())),('Lab records',data['hospital_table_rows']['labevents'])]
    metric=''.join(f'<div class="metric"><small>{html.escape(k)}</small><strong>{v:,}</strong></div>' for k,v in stats)
    doc='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Observation-Aware EHR | Research Audit</title>
<script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
<style>
:root{color-scheme:dark;font-family:Inter,system-ui,Segoe UI,Arial,sans-serif;background:#0b1220;color:#eef2fa}
body{margin:0;line-height:1.5}header{padding:46px max(28px,5vw);background:linear-gradient(130deg,#172846,#101b2c)}
header p{max-width:760px;color:#c1cce0}h1{font-size:clamp(1.8rem,4vw,3rem);margin:.3rem 0}
.eyebrow{letter-spacing:.15em;color:#89c3ff;text-transform:uppercase;font-size:.8rem}
main{max-width:1450px;margin:0 auto;padding:30px}
.metrics{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:16px;margin-bottom:30px}
.metric{padding:22px;background:#142238;border:1px solid #2b3b57;border-radius:14px}
.metric small{display:block;color:#a5b6d2}.metric strong{display:block;font-size:2.1rem}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,490px),1fr));gap:18px}
.panel{background:#111f33;border:1px solid #2d4160;border-radius:14px;padding:18px;min-width:0}
.panel h2{font-size:1rem;letter-spacing:.01em;color:#d6e2f8}.plot{height:350px}
footer{padding:22px max(28px,5vw);color:#a4b2c9;font-size:.85rem}
.important{padding:16px 20px;background:#192838;border-left:3px solid #76b7e7;color:#cad9e9;margin-bottom:24px}
</style></head><body><header><div class="eyebrow">Research engineering · public MIMIC v2.2 demos</div>
<h1>Observation-Aware EHR</h1><p>12 reproducible descriptive visualizations from the uploaded real-world deidentified public demonstration datasets. Strict availability logic; no synthetic patient records; no clinical treatment-effect claims.</p></header>
<main><div class="metrics">__METRICS__</div><div class="important">CHARTTIME ≠ clinician observation. STORETIME ≠ verified clinician access. Pyxis ≠ confirmed administration. Demo distributions are not representative clinical effect estimates.</div><section class="grid" id="panels"></section></main>
<footer>Data: MIMIC-IV-ED Demo 2.2 + MIMIC-IV Clinical Demo 2.2 · ODbL 1.0 attribution retained in repository. All graphs display aggregate statistics only. Plotly charting library loads from CDN; raw patient-level tables are excluded.</footer>
<script>
const charts=__DATA__;
const root=document.getElementById('panels');
for(const chart of charts){const panel=document.createElement('section');panel.className='panel';const title=document.createElement('h2');title.textContent=chart.title;const vis=document.createElement('div');vis.className='plot';panel.append(title,vis);root.append(panel);
const trace=chart.type==='line'?{x:chart.labels,y:chart.values,type:'scatter',mode:'lines+markers',line:{width:3,color:'#69b1ff'}}:{x:chart.labels,y:chart.values,type:'bar',marker:{color:'#4e9de4'}};
Plotly.newPlot(vis,[trace],{paper_bgcolor:'rgba(0,0,0,0)',plot_bgcolor:'rgba(0,0,0,0)',font:{color:'#d9e5f5',size:11},margin:{l:56,r:16,t:12,b:75},xaxis:{tickangle:-35,gridcolor:'#253651'},yaxis:{gridcolor:'#253651'}},{responsive:true,displaylogo:false,modeBarButtonsToRemove:['lasso2d','select2d']});}
</script></body></html>'''.replace('__DATA__',cfg).replace('__METRICS__',metric)
    destination.parent.mkdir(parents=True,exist_ok=True)
    destination.write_text(doc,encoding='utf-8')
    return destination

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--report',type=Path,default=Path('evidence/real_mimic_demo_profile_v0.2.json'))
    p.add_argument('--output',type=Path,default=Path('evidence/verified_demo_dashboard.html'))
    args=p.parse_args();print(render(json.loads(args.report.read_text()),args.output))
