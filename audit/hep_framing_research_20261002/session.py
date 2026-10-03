from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,platform,subprocess,sys
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def record(event,detail):
    p=HERE/'events.json';rows=json.loads(p.read_text()) if p.exists() else []
    row={'utc':datetime.now(timezone.utc).isoformat(),'event':event,'detail':detail};rows.append(row)
    p.write_text(json.dumps(rows,indent=2)+'\n',encoding='utf-8')
    prose='\n## '+event+'\n\n'+row['utc']+'\n\n```json\n'+json.dumps(detail,indent=2)+'\n```\n'
    for out in [HERE/'events.md',ROOT/'logs.md']:
        with out.open('a',encoding='utf-8') as f:f.write(prose)
def run(args):
    record('Command started',{'argv':args})
    p=subprocess.run(args,cwd=ROOT,capture_output=True,text=True,encoding='utf-8',errors='replace')
    out=HERE/('command_'+str(len(json.loads((HERE/'events.json').read_text()))).zfill(3)+'.txt')
    out.write_text(p.stdout+'\nSTDERR\n'+p.stderr,encoding='utf-8')
    record('Command completed',{'argv':args,'exit_code':p.returncode,'output':str(out.relative_to(ROOT)),'output_sha256':sha(out)})
    print(p.stdout[-6500:]);print(p.stderr[-1500:]);return p.returncode
if __name__=='__main__':
    if len(sys.argv)>1:sys.exit(run(sys.argv[1:]))
    record('HEP audience research and QC started',{'scope':'Title, abstract, discussion and conclusion, with full-manuscript regression and visual QA.','environment':{'platform':platform.platform(),'python':sys.version},'input_hashes':{name:sha(ROOT/name) for name in ['main.tex','references.bib','CITATION.cff','output/fast_mc_zdc_manuscript.pdf','audit/final_build_audit.json']},'commands_before_logger':['Read relevant implementation/operating rules already read completely earlier in this conversation','graft check: fresh; graft ask for paper framing: navigation only, no relevant scientific evidence','Read current title/abstract/discussion/conclusion, QA guards and claim register; git status preserves prior uncommitted work','Primary-source web research: APS and IOP guidance; ePIC ZDC, Kansal metrics, CaloDREAM and ALICE co-activation papers'],'failure':'CaloChallenge HTML returned internal error; use its already verified abstract and other full-text primary sources.','scientific_boundary':'No new data, test inspection, training, thresholds, graph choices, checkpoint selection or model evaluation. Editorial clarity is not a claim of HEP peer review or detector validation.'})
