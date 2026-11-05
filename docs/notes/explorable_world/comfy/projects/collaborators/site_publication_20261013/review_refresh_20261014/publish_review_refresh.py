from pathlib import Path
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor
import hashlib,json,subprocess,sys
R=Path('D:/Documents/CFA');P=R/'docs/notes/explorable_world/comfy/projects';L=P/'visual_library';E=Path(__file__).parent
REVIEW=P/'hon_dolo_strictly_business/feedback/review_decisions.json'
def read(p):return json.loads(p.read_bytes())
def cat(p):return json.loads(p.read_text(encoding='utf-8').split('=',1)[1].strip().removesuffix(';'))
def pin(p):
 b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def check(row):assert pin(R/row['path'])=={k:row[k] for k in ['path','bytes','sha256']},row['path']
def save(name,obj):(E/name).write_text(json.dumps(obj,indent=2)+'\n',encoding='utf-8')
def now():return datetime.now(timezone.utc).isoformat()
def run(name,args):
 r=subprocess.run(args,cwd=L,capture_output=True,text=True,encoding='utf-8',errors='replace');return dict(name=name,exitCode=r.returncode,stdout=r.stdout,stderr=r.stderr)
assert not (E/'build_result.json').exists(),'Do not repeat a recorded build'
baseline=read(E/'baseline.json');before=cat(E/'catalog.js.before');assert cat(L/'catalog.js')==before
source=pin(REVIEW);assert source['bytes']==204969 and source['sha256']=='b37518b802a24d141a64933d13f61f5aad6462de9874f9a79319f26cfa0aa566'
auditRoot=P/'hon_dolo_strictly_business/feedback/review_intake_20261013_latest_624e40c2-5d58-477d-bb07-5825da914219'
audit=pin(auditRoot/'INTAKE_APPLIED_21.json');assert audit['sha256']=='7aedc1e7273863d98f0a45268f347fc01bd8334bf99a2a49d0ff410bbab39990'
verification=pin(auditRoot/'VERIFICATION_21.json');assert verification['sha256']=='8a7277bcc9f375af900e86718b0b4f381f57d5b17090c14fac2e04d47b581f98'
current=read(REVIEW)['items'];old={r['id']:r for r in before['reviewDecisions']};new={r['id']:r for r in current};assert len(current)==len(new)==199 and not set(old)-set(new)
changed=sorted(k for k,v in new.items() if old.get(k)!=v)
for row in baseline['sources']:check(row)
release=dict(source=source,intakeAudit=audit,verification=verification,changedReviewIDs=changed,sourceOfAuthority='CFA NOVA direct task-message final release in this chat; canonical intake of the user export21. No additional permission requested.',priorReviewCount=len(old),newReviewCount=len(new))
save('intake_release.json',release)
record=dict(status='running',startedAtUTC=now(),buildInvocations=1,catalogBefore=pin(L/'catalog.js'),canonicalSource=source,release=pin(E/'intake_release.json'));save('build_result.json',record)
try:
 record['build']=run('build_catalog.py',[sys.executable,'-B',str(L/'build_catalog.py')]);save('build_result.json',record);assert record['build']['exitCode']==0,record['build']['stderr']
 after=cat(L/'catalog.js');assert set(after)==set(before)
 for key in before:
  if key!='reviewDecisions':assert after[key]==before[key],key
 assert after['reviewDecisions']==current
 for row in baseline['sources']:check(row)
 names=['test_review_direct_clarification.cjs','test_review_requests.cjs','test_reference_scope.cjs','test_creative_review.cjs','test_reference_validation.cjs','test_working_bom.cjs','test_mission_gun_variants.cjs']
 with ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(lambda n:run(n,['D:/Program Files (x86)/node.exe',str(L/n)]),names))
 save('test_results.json',dict(passed=all(r['exitCode']==0 for r in results),results=results,browserVisualQA=False))
 for r in results:print(json.dumps(r),flush=True)
 assert all(r['exitCode']==0 for r in results),'Test failure: repair verification without repeating build'
 counts=dict(assets=len(after['assets']),albums=len(after['albums']),documents=sum(a['kind'] in ['document','pdf'] for a in after['assets']),reviews=len(current))
 handback=dict(status='complete',completedAtUTC=now(),buildInvocations=1,counts=counts,catalog=pin(L/'catalog.js'),intake=release,tests=pin(E/'test_results.json'),runtime=[pin(L/'library.js'),pin(L/'library.css')],preserved='Every non-review catalog root value, all asset metadata and original media pins, albums, source choices, scene timings and validation data are unchanged.',sourcePinsVerified=len(baseline['sources']),browserVisualQA=False)
 save('SITE_PUBLICATION_HANDBACK.json',handback);record.update(status='complete',completedAtUTC=now(),handback=pin(E/'SITE_PUBLICATION_HANDBACK.json'));save('build_result.json',record);print(json.dumps(record['handback']),flush=True)
except Exception as err:
 record.update(status='needs_attention',error=str(err));save('build_result.json',record);raise
