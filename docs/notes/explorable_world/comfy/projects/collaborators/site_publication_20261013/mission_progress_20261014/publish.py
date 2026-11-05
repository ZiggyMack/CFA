from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,subprocess,sys
R=Path('D:/Documents/CFA');P=R/'docs/notes/explorable_world/comfy/projects';L=P/'visual_library';E=Path(__file__).parent
def cat(p):return json.loads(p.read_text(encoding='utf-8').split('=',1)[1].strip().removesuffix(';'))
def pin(p):
 b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def save(n,o):(E/n).write_text(json.dumps(o,indent=2)+'\n',encoding='utf-8')
attempts=1
if (E/'build_result.json').exists():
 prior=json.loads((E/'build_result.json').read_bytes())
 if '--restore-history-link' in sys.argv:
  assert prior['catalog']['sha256']=='7db24073a5a98c972608a4036b38bb5ea259bc76907a53f7f2fa48dc7902fb90' and pin(L/'catalog.js')==prior['catalog']
  assert not (E/'build_attempt_2.history_link_gap.json').exists()
  save('build_attempt_2.history_link_gap.json',prior);attempts=3
 else:
  assert prior['status']=='build_failed' and prior['catalog']['sha256']=='29e0ff04e59d3c7b2ddf7e1458928a4d9f7f0e4987fa9d3dbb940cb977bb14c7','Do not repeat a successful publication'
  assert not (E/'build_attempt_1.failed.json').exists(),'Only the verified cross-project writer-association repair is permitted'
  save('build_attempt_1.failed.json',prior);attempts=2
before=cat(E/'catalog.js.before')
if attempts<3:assert cat(L/'catalog.js')==before
review=P/'hon_dolo_strictly_business/feedback/review_decisions.json'
assert pin(review)['sha256']=='b37518b802a24d141a64933d13f61f5aad6462de9874f9a79319f26cfa0aa566'
record=dict(status='running',startedAtUTC=datetime.now(timezone.utc).isoformat(),buildInvocations=attempts,inputs=[pin(p) for p in [L/'build_catalog.py',L/'library.js',L/'library.css',L/'cast_collections.json',L/'cast_revisions.json',L/'writer_development.json',P/'collaborators/mission_control.json']],reviewSource=pin(review));save('build_result.json',record)
r=subprocess.run([sys.executable,'-B',str(L/'build_catalog.py')],cwd=L,capture_output=True,text=True,encoding='utf-8',errors='replace')
record.update(exitCode=r.returncode,stdout=r.stdout,stderr=r.stderr,status='built_pending_verification' if r.returncode==0 else 'build_failed',catalog=pin(L/'catalog.js'));save('build_result.json',record)
print(json.dumps(record),flush=True);assert r.returncode==0,r.stderr
after=cat(L/'catalog.js');allowed={'assets','albums','writerDevelopment','castCollections','missionControl'}
for k in before:
 if k not in allowed:assert after[k]==before[k],k
old={a['id']:a for a in before['assets']};new={a['id']:a for a in after['assets']};assert not set(old)-set(new)
diff={k:[field for field in set(old[k])|set(new[k]) if old[k].get(field)!=new[k].get(field)] for k in old if old[k]!=new[k]}
expected_boss={'HD-RETURN-8421e7cfa1a0','HD-RETURN-339cdbe1e03a','HD-RETURN-e18185bdab18','HD-RETURN-9143639db1cf'}
for aid,fields in diff.items():
 if aid in expected_boss:assert set(fields)<= {'note','sourceStatus','selectionStatus','referenceRole'},(aid,fields)
 elif aid=='hon:doc:docs/notes/explorable_world/comfy/projects/visual_library/cast_collections.json':assert fields==['text']
 else:assert any(aid.endswith('/'+n) for n in ['DECISIONS_20261012.md','START_HERE.txt']) and '/lisan_al_gaib/story/writer_pass_20261012/' in aid and set(fields)<={'note','text','bytes','sha256'},(aid,fields)
assert after['reviewDecisions']==before['reviewDecisions']
assert set(new)-set(old)=={a['id'] for a in after['assets'] if a['id'] not in old}
added=[new[k] for k in new if k not in old]
assert [a['id'] for a in added if a['kind'] not in ['document','pdf']]==['LAG-JAMES-NOGUN-0223fd8d0c6f']
assert old['HD-RETURN-957897bd45c4']==new['HD-RETURN-957897bd45c4']
save('catalog_verification.json',dict(passed=True,originalAssetsUnchangedExcept=diff,newAssets=[dict(id=a['id'],kind=a['kind'],repoPath=a['repoPath']) for a in added],unchangedCatalogRoots=sorted(set(before)-allowed),counts=dict(assets=len(new),albums=len(after['albums']),documents=sum(a['kind'] in ['document','pdf'] for a in after['assets']),reviews=len(after['reviewDecisions']))))
print('Bounded catalog verification passed.',flush=True)
