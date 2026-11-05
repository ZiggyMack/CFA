"""Refresh one source-owned Mission card without ingesting unrelated revisions."""
from pathlib import Path
from copy import deepcopy
import ast, hashlib, json, os, sys
from urllib.parse import quote

R=Path(r'D:\Documents\CFA');P=R/'docs/notes/explorable_world/comfy/projects';V=P/'visual_library'
E=P/'collaborators/validator_status_20261021';B=R/'.cache/validator_status_20261021'
sha=lambda raw:hashlib.sha256(raw).hexdigest()
path=V/'catalog.js';raw=path.read_bytes()
receipt=json.loads((E/'RECONCILIATION.json').read_text(encoding='utf-8'))
assert sha(raw)==receipt['beforeFiles'][path.relative_to(R).as_posix()]
catalog=json.loads(raw.decode('utf-8').split('=',1)[1].strip().rstrip(';'))
mission=json.loads((P/'collaborators/mission_control.json').read_text(encoding='utf-8'))
target=next(t for t in mission['tasks'] if t['id']==receipt['taskID'])
sys.path.insert(0,str(V))
from source_relocations import resolve_source
from browser_media_paths import BrowserMediaPaths
browser=BrowserMediaPaths(R,P/'browser_media')
def url(p):
    p=Path(p) if Path(p).is_absolute() else R/p
    p=resolve_source(R,p)
    assert p.is_file()
    return quote(os.path.relpath(browser.resolve(p),V).replace('\\','/'),safe='/')

# Reuse the owner's doc and shell functions verbatim, without executing unrelated intakes.
tree=ast.parse((V/'build_catalog.py').read_text(encoding='utf-8'))
namespace={'Path':Path,'ROOT':R,'HERE':V,'assets':catalog['assets'],'url':url,
           'resolve_source':resolve_source,'os':os,'hashlib':hashlib,'json':json}
for node in tree.body:
    if isinstance(node,ast.FunctionDef) and node.name in {'doc','shell'}:
        exec(compile(ast.Module(body=[node],type_ignores=[]),str(V/'build_catalog.py'),'exec'),namespace)
known={a['id'] for a in catalog['assets']}
for link in target['links']:
    project,relative=link['assetID'].split(':doc:',1)
    if link['assetID'] not in known:
        namespace['doc'](project,relative,link['label'],album='Collaborator briefs · attachments')
        known.add(link['assetID'])
catalog['missionControl']=mission
text='window.REVIEW_CATALOG = '+json.dumps(catalog,ensure_ascii=False).replace('<','\\u003c')+';\n'
assert path.read_bytes()==raw
tmp=path.with_suffix('.validator.pending');tmp.write_text(text,encoding='utf-8');tmp.replace(path)
browser.write_manifest(V/'browser_media_paths.json')
for relative,project,view in [('index.html','hon','all'),('hon_dolo_strictly_business/asset_review_20261007/index.html','hon','all'),('hon_dolo_strictly_business/asset_review_20261007/storyboard.html','hon','storyboard'),('hon_dolo_strictly_business/gemini_review_20261007/index.html','hon','videos'),('lisan_al_gaib/index.html','lisan','all')]:
    namespace['shell'](P/relative,project,view)
receipt['fullBuildAttempt']={'result':'blocked_before_catalog_write','reason':'Unrelated writer revision differs from its registered hash','path':'docs/notes/explorable_world/comfy/projects/lisan_al_gaib/story/writer_pass_20261012/DECISIONS_20261012.md'}
receipt['localRefreshMethod']='Existing builder doc/shell functions; only canonical Mission source and its explicit attachments refreshed; unrelated frozen catalog preserved.'
(E/'RECONCILIATION.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Refreshed local card and explicit document links using existing builder functions.')
