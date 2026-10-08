"""Bundle one existing identity reference and the planned Flow intake; no uploads or generation."""
from pathlib import Path
import hashlib
import json
import zipfile

HERE=Path(__file__).resolve().parent
PROJECTS=HERE.parent.parent
ROOT=next(p for p in HERE.parents if (p/'AGENTS.md').is_file() and (p/'apps').is_dir())
source=HERE.parent/'asset_review_20261007/reference_candidates/hon-dolo-armor-swap/HD-EXP-LOCK-FACE.jpg'
data=source.read_bytes()
digest=hashlib.sha256(data).hexdigest()
assert digest=='ef5d59a6402eaff568e30bb6a4432b14b90c692ea6758a761c7702c44d457978'
entries={
    'START_HERE.txt':(PROJECTS/'collaborators/flow_start_here.txt').read_bytes(),
    'EXPERIMENT.txt':(HERE/'first_experiment_20261008.txt').read_bytes(),
    'FLOW_BRIEF.txt':(PROJECTS/'collaborators/flow_brief.txt').read_bytes(),
    'PROJECT_BRIEF.txt':(HERE/'project_brief.txt').read_bytes(),
    'FLOW_INTAKE.txt':(PROJECTS/'collaborators/flow_intake_20261008.txt').read_bytes(),
    'Characters/Hon Dolo/HD-EXP-LOCK-FACE.jpg':data,
    'Images/READ_ME.txt':b'No outfit or scene pictures are attached for the first one-reference proof. Add selected, role-mapped images in a later package after sorting. Local folders do not automatically create Flow asset categories.\n',
}
manifest={'package_id':'FLOW-HD-STILL-001','status':'prepared_not_uploaded_or_generated','reference':{'id':'HD-DESIGN-01','asset_id':'HD-DROP-ef5d59a6402e','filename':source.name,'source_repo_path':source.relative_to(ROOT).as_posix(),'sha256':digest,'role':'current visible identity/design reference','flow_asset_id':None},'files':[{'path':name,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()} for name,raw in entries.items()]}
entries['PACKAGE_MAP.json']=json.dumps(manifest,indent=2).encode('utf-8')
target=HERE/'FLOW-HD-STILL-001.zip'
with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as archive:
    for name,raw in entries.items():
        info=zipfile.ZipInfo('FLOW-HD-STILL-001/'+name,date_time=(2026,10,8,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
        archive.writestr(info,raw)
with zipfile.ZipFile(target) as archive:
    assert archive.testzip() is None
    assert archive.read('FLOW-HD-STILL-001/Characters/Hon Dolo/HD-EXP-LOCK-FACE.jpg')==data
print(json.dumps({'file':target.name,'bytes':target.stat().st_size,'members':len(entries)}))
