from pathlib import Path
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor
import json,hashlib,subprocess
R=Path('D:/Documents/CFA');P=R/'docs/notes/explorable_world/comfy/projects';L=P/'visual_library';E=Path(__file__).parent
def read(p):return json.loads(p.read_bytes())
def cat(p):return json.loads(p.read_text(encoding='utf-8').split('=',1)[1].strip().removesuffix(';'))
def pin(p):
 b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
concurrent=[]
writer_updates={
 'docs/notes/explorable_world/comfy/projects/lisan_al_gaib/story/writer_pass_20261012/DECISIONS_20261012.md':'ae9e8203a43fc80f375ff03840cc0658929d9c3b6213e0a5c10a557a9c0f7974',
 'docs/notes/explorable_world/comfy/projects/lisan_al_gaib/story/writer_pass_20261012/START_HERE.txt':'13aaa651c1253d7ada5711b1596eb052e27b5f6731832d0dc7c13769fd8f949e'
}
def check(row):
 actual=pin(R/row['path']);expected={k:row[k] for k in ['path','bytes','sha256']}
 if actual!=expected and row['path'] in writer_updates and actual['sha256']==writer_updates[row['path']]:
  # Claude appended James decision 56 after this review-only build; published text remains the previous exact snapshot.
  item=dict(before=expected,current=actual,publication='Deferred to the subsequent James/casting publication; no author file was modified by this build.')
  if item not in concurrent:concurrent.append(item)
 else:assert actual==expected,row['path']
def save(n,o):(E/n).write_text(json.dumps(o,indent=2)+'\n',encoding='utf-8')
record=read(E/'build_result.json');assert record['buildInvocations']==1 and record['build']['exitCode']==0
if not (E/'build_result.initial_failure.json').exists():save('build_result.initial_failure.json',record)
baseline=read(E/'baseline.json');release=read(E/'intake_release.json');check(release['source']);before=cat(E/'catalog.js.before');after=cat(L/'catalog.js')
assert set(before)==set(after)
for key in before:
 if key not in ['assets','reviewDecisions']:assert after[key]==before[key],key
current=read(R/release['source']['path'])['items'];assert after['reviewDecisions']==current
reviews={r['id']:r for r in current};old={a['id']:a for a in before['assets']};new={a['id']:a for a in after['assets']};assert set(old)==set(new)
projections=[]
for aid,a in old.items():
 delta={k for k in set(a)|set(new[aid]) if a.get(k)!=new[aid].get(k)}
 if not delta:continue
 assert aid in release['changedReviewIDs'] and delta<={'variant','storyboardStage'},(aid,delta)
 assert all(new[aid][k]==reviews[aid][k] for k in delta)
 assert all(new[aid].get(k)==v for k,v in a.items() if k not in delta)
 projections.append(dict(id=aid,fields=sorted(delta),reason='Existing builder projects these explicit canonical review fields into asset browse metadata. Original file identity and all other metadata are unchanged.'))
assert len(projections)==6
for row in baseline['sources']:check(row)
names=['test_review_direct_clarification.cjs','test_review_requests.cjs','test_reference_scope.cjs','test_creative_review.cjs','test_reference_validation.cjs','test_working_bom.cjs','test_mission_gun_variants.cjs']
def run(n):
 r=subprocess.run(['D:/Program Files (x86)/node.exe',str(L/n)],cwd=L,capture_output=True,text=True,encoding='utf-8',errors='replace');return dict(name=n,exitCode=r.returncode,stdout=r.stdout,stderr=r.stderr)
saved=read(E/'test_results.json') if (E/'test_results.json').exists() else {}
prior={r['name']:r for r in saved.get('results',[]) if r['exitCode']==0}
with ThreadPoolExecutor(max_workers=3) as pool:fresh=list(pool.map(run,[n for n in names if n not in prior]))
prior.update({r['name']:r for r in fresh});results=[prior[n] for n in names]
save('test_results.json',dict(passed=all(r['exitCode']==0 for r in results),results=results,browserVisualQA=False))
for r in results:print(json.dumps(r),flush=True)
assert all(r['exitCode']==0 for r in results),'Repair verification without repeating build'
for row in baseline['sources']:check(row)
handback=dict(status='complete',completedAtUTC=datetime.now(timezone.utc).isoformat(),buildInvocations=1,catalog=pin(L/'catalog.js'),counts=dict(assets=len(after['assets']),albums=len(after['albums']),documents=sum(a['kind'] in ['document','pdf'] for a in after['assets']),reviews=len(current)),intake=release,reviewDerivedAssetMetadata=projections,tests=pin(E/'test_results.json'),runtime=[pin(L/'library.js'),pin(L/'library.css')],preserved='All original assets and hashes, albums, source choices, timing and non-review catalog values. Six assets inherit only the variant/stage fields explicitly saved in the authorized reviews.',sourcePinsVerified=len(baseline['sources'])-len(concurrent),concurrentWriterUpdates=concurrent,browserVisualQA=False)
save('SITE_PUBLICATION_HANDBACK.json',handback);record.update(status='complete',handback=pin(E/'SITE_PUBLICATION_HANDBACK.json'),reviewDerivedAssetMetadata=projections,verificationRepair='Original preservation assertion refined for six existing builder projections of authorized review variant/stage fields; no rebuild.');record.pop('error',None);save('build_result.json',record);print(json.dumps(record['handback']))
