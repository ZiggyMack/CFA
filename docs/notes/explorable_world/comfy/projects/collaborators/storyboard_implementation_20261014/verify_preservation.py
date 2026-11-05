"""Read-only comparison against this assignment's frozen catalog and sources."""
from pathlib import Path
import hashlib,json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[6]
V=ROOT/'docs/notes/explorable_world/comfy/projects/visual_library'
def catalog(path):
    return json.loads(path.read_text(encoding='utf-8-sig').split('=',1)[1].strip().rstrip(';'))
before=catalog(HERE/'before_catalog.js');after=catalog(V/'catalog.js')
old={a['id']:a for a in before['assets']};new={a['id']:a for a in after['assets']}
assert old.keys()<=new.keys(),'Removed canonical assets'
changed={id:sorted(k for k in old[id].keys()|new[id].keys() if old[id].get(k)!=new[id].get(k)) for id in old if old[id]!=new[id]}
print(json.dumps({'assetsBefore':len(old),'assetsAfter':len(new),'added':len(new.keys()-old.keys()),'changed':changed},ensure_ascii=False))
writer=json.loads((V/'writer_development.json').read_text(encoding='utf-8'))
excerpt_ids={item['project']+':doc:'+item['path'] for item in writer['documents'] if item.get('publication')}
assert set(changed)==excerpt_ids, 'Unexpected existing-asset changes'
for id in changed:
    assert old[id]['kind']=='document'
    assert set(changed[id])<={'src','repoPath','historicalRepoPath','filename','text','note','sha256','bytes','sourceStatus'},changed[id]
for key in ['reviewDecisions','sceneReviews','sourceComparisons','referenceValidation','assistantLikenessAssessments','reviewRequests','characterReferenceBoard','characterBOM']:
    assert before.get(key)==after.get(key),'Changed canonical protection: '+key
for seq in before['storyboardSequences']:
    assert seq==next(s for s in after['storyboardSequences'] if s['id']==seq['id'])
old_shots={s['id']:s for s in before['shotMaterials']['shots']}
new_shots={s['id']:s for s in after['shotMaterials']['shots']}
assert old_shots.keys()==new_shots.keys()
for id,shot in old_shots.items():
    current=dict(new_shots[id])
    if id=='LAG-FLOW-SW2-001':
        assert current.pop('independentSequenceID')=='LAG-STORY-01-THE-GLOVED-HAND'
        assert current.pop('storyShotID')=='S01-4.1'
    assert current==shot,id
for project,count in [('hon',36),('lisan',50)]:
    panels=lambda data: [(a['id'],a.get('storyboardOrder'),a.get('storyboardPosition'),a.get('timing')) for a in data['assets'] if a['project']==project and a.get('storyboardOrder') and not a.get('storySequenceID')]
    assert panels(before)==panels(after)
    assert len(panels(after))==count
    assert after['storyboardMetadata'][project]['panelCount']==count
preservation=json.loads((HERE/'PRESERVATION_BEFORE.json').read_text(encoding='utf-8'))
for pin in preservation['files']:
    if Path(pin['path']).name in ['catalog.js','build_catalog.py','writer_development.json']:continue
    raw=(ROOT/pin['path']).read_bytes()
    assert len(raw)==pin['bytes'] and hashlib.sha256(raw).hexdigest()==pin['sha256'],pin['path']
for entry in writer['documents']:
    original=(ROOT/entry['path']).read_bytes()
    assert len(original)==entry['bytes'] and hashlib.sha256(original).hexdigest()==entry['sha256']
    if not entry.get('publication'):continue
    pub=entry['publication'];raw=(ROOT/pub['path']).read_bytes();asset=new[entry['project']+':doc:'+entry['path']]
    assert asset['repoPath']==asset['historicalRepoPath']==pub['path']
    assert asset['sha256']==hashlib.sha256(raw).hexdigest()==pub['sha256']
    assert asset['bytes']==len(raw)==pub['bytes']
    assert asset['text']==raw.decode('utf-8-sig').replace('\r\n','\n').replace('\r','\n')
print('PASS: all existing media, review records, source choices, validation and song timing/order preserved; only two approved site excerpts and the explicit SW2 navigation binding differ.')
