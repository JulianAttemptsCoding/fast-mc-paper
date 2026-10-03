from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, platform, subprocess, sys

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def record(event, detail):
    path = HERE / 'events.json'
    rows = json.loads(path.read_text()) if path.exists() else []
    row = {'utc': datetime.now(timezone.utc).isoformat(), 'event': event, 'detail': detail}
    rows.append(row)
    path.write_text(json.dumps(rows, indent=2)+'\n', encoding='utf-8')
    prose = '\n## '+event+'\n\n'+row['utc']+'\n\n```json\n'+json.dumps(detail,indent=2)+'\n```\n'
    for out in (HERE / 'events.md', ROOT / 'logs.md'):
        with out.open('a',encoding='utf-8') as f: f.write(prose)
def run(args):
    record('Command started', {'argv':args})
    p=subprocess.run(args,cwd=ROOT,capture_output=True,text=True,encoding='utf-8',errors='replace')
    n=len(json.loads((HERE/'events.json').read_text()))
    out=HERE/f'command_{n:03d}.txt'
    out.write_text(p.stdout+'\nSTDERR\n'+p.stderr,encoding='utf-8')
    record('Command completed',{'argv':args,'exit_code':p.returncode,'output':str(out.relative_to(ROOT)),'sha256':sha(out)})
    print(p.stdout[-7000:]); print(p.stderr[-2000:])
    return p.returncode
if __name__=='__main__':
    if len(sys.argv)>1: sys.exit(run(sys.argv[1:]))
    record('Comprehensive final review started',{
      'environment':{'platform':platform.platform(),'python':sys.version},
      'scope':'Entire 14-page manuscript, 14 equations, four figures, four tables, appendices and 25 references; editorial and aggregate-evidence review only.',
      'inputs':{str(p.relative_to(ROOT)):sha(p) for p in [ROOT/'main.tex',ROOT/'references.bib',ROOT/'output/fast_mc_zdc_manuscript.pdf',ROOT/'audit/final_build_audit.json']},
      'initial_reads':['Implementation guide (including separately recovered architecture lines)','Focused operating rules','Graft setup','PDF skill','README.md','STATUS.md','build.ps1','main.tex lines 1-247','references.bib','current release/QA/AI disclosure records'],
      'commands_before_logger':['Get-Content and Get-ChildItem read-only discovery','git status --short (clean)','graft check (current)','graft ask manuscript finalization evidence bibliography build PDF scientific claims --source'],
      'navigation':'Graft graph covers the simulation repository; paper source is a separate unindexed repository. Relevant paper files inspected directly.',
      'failures':['Two tool responses truncated; manuscript content being reread in bounded chunks.'],
      'boundary':'No remote dataset access, training, event evaluation, configuration changes, or checkpoint selection.'})
