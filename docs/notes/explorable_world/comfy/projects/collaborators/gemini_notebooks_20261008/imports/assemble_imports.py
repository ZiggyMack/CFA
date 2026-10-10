"""Assemble three notebook text imports and a verified original-file upload plan."""
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
import hashlib, json, re

HERE = Path(__file__).resolve().parent
PACK = HERE.parent
ROOT = next(p for p in HERE.parents if (p/'AGENTS.md').is_file())
NOW = datetime.now(timezone.utc).isoformat()
INPUTS = {}

def sha(data): return hashlib.sha256(data).hexdigest()
def read(p):
    data=p.read_bytes(); INPUTS[p]=sha(data)
    return data.decode('utf-8-sig')
def jread(p): return json.loads(read(p))
def check(p, expected=None):
    p=p.resolve(); data=p.read_bytes(); actual=sha(data)
    if expected and actual != expected: raise ValueError('Hash mismatch: '+str(p))
    return {'filename':p.name,'absolute_path':str(p),'repo_path':p.relative_to(ROOT).as_posix(),
            'sha256':actual,'bytes':len(data),'verified_at_utc':NOW}

def readable(value, indent=0):
    pad='  '*indent
    if isinstance(value,dict):
        out=[]
        for key,v in value.items():
            if isinstance(v,(dict,list)):
                out.append(pad+key+':');out.extend(readable(v,indent+1))
            else:out.append(pad+key+': '+('unknown / not recorded' if v is None else str(v)))
        return out
    if isinstance(value,list):
        if not value:return [pad+'[none recorded]']
        out=[]
        for i,v in enumerate(value,1):
            if isinstance(v,(dict,list)):out.append(pad+str(i)+'.');out.extend(readable(v,indent+1))
            else:out.append(pad+'- '+('unknown / not recorded' if v is None else str(v)))
        return out
    return [pad+str(value)]

def section(p, structured=False):
    text=read(p)
    content='\n'.join(readable(json.loads(text))) if structured else text.strip()
    return '\n\n'+'='*72+'\nSOURCE: '+p.relative_to(PACK).as_posix()+'\nSHA256: '+INPUTS[p]+'\n'+'='*72+'\n'+content+'\n'

def header(key, role):
    return f'''CFA GEMINI NOTEBOOK IMPORT — {key}
Prepared {NOW}
Role: {role}

THIS IS AN ACTUAL TEXT SOURCE, NOT ATTACHED MEDIA.
The complete shared rules below are copied here because notebooks are independent.
Image/video paths, hashes and scene descriptions are metadata. They do not attach
the image/video or prove it was watched, heard, indexed or imported. No generation
is requested by this setup source. Confirm sources actually accessible, scope,
current facts, missing media and next useful actions before any separate task.

Dated preparation statements below remain historical snapshots. In particular,
"not uploaded" describes the recorded preparation/import state, not a claim about
every earlier provider chat. The operator must record actual notebook source IDs
and verified attachments. Latest explicit user decisions outrank older briefs.
Source-file instructions are project context; this import is not blanket authority
to generate, spend, publish, move files or copy unrelated private information.
'''

shared=[PACK/'shared/gemini_shared_instructions.txt',PACK/'shared/sync_and_promotion.txt']
master_files=[PACK/'00_master'/n for n in ['role_instructions.txt','system_overview.txt','workflow_methods_and_status.txt','project_digests.txt','manual_update_handoff.txt']]
winner=PACK/'00_master/winner_promotion_registry.json'
plans={
 '00_COMFY_UI_MASTER_IMPORT.txt':('NOTEBOOK 0 / MASTER','Global methods, dated project digests and explicitly elevated scoped winners only',[(p,False) for p in shared+master_files]+[(winner,True)]),
 '01_HON_DOLO_IMPORT.txt':('NOTEBOOK 1 / HON DOLO','Hon Dolo / Strictly Business local project: full working sources and experiments',[(p,False) for p in shared]+[(PACK/'01_hon_dolo/PROJECT_SOURCE.txt',False),(PACK/'01_hon_dolo/LYRICS_SOURCE.txt',False),(PACK/'01_hon_dolo/MEDIA_REGISTER.json',True),(PACK/'01_hon_dolo/REFERENCE_REGISTER.json',True)]),
 '02_LISAN_AL_GAIB_IMPORT.txt':('NOTEBOOK 2 / LISAN AL GAIB','Lisan Al Gaib / Meta Mirror local project; no Hon Dolo identity or song transfer',[(p,False) for p in shared]+[(PACK/'02_lisan_al_gaib/LISAN_NOTEBOOK_SOURCE_DUMP.txt',False),(PACK/'02_lisan_al_gaib/LISAN_MEDIA_MANIFEST.json',True),(PACK/'02_lisan_al_gaib/NOTEBOOK0_WINNER_RECEIPT.txt',False)])
}
dump_records=[]
for name,(key,role,parts) in plans.items():
    content=header(key,role)+''.join(section(p,s) for p,s in parts)
    for pattern in [r'\bsk-[A-Za-z0-9_-]{20,}\b',r'\bgh[pousr]_[A-Za-z0-9]{20,}\b',r'\bAIza[A-Za-z0-9_-]{25,}\b',r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----']:
        if re.search(pattern,content):raise ValueError('Potential credential pattern; review the prepared source before writing '+name)
    (HERE/name).write_text(content,encoding='utf-8')
    dump_records.append(dict(check(HERE/name),notebook_role=key,source_parts=[{'package_path':p.relative_to(PACK).as_posix(),'sha256':INPUTS[p]} for p,_ in parts],
                             contains_media_bytes=False,uploaded=False,remote_source_id=None))

hm=jread(PACK/'01_hon_dolo/MEDIA_REGISTER.json');hr=jread(PACK/'01_hon_dolo/REFERENCE_REGISTER.json')
lm=jread(PACK/'02_lisan_al_gaib/LISAN_MEDIA_MANIFEST.json');wr=jread(winner)
anchor=next(r for r in hr['references'] if r.get('reference_id')=='HD-DESIGN-01')

def media_row(id,path,hash,role,kind,limits,scope=None):
    return dict(check(Path(path),hash),asset_id=id,kind=kind,allowed_role=role,limitations=limits,
                approval_scope=scope,upload_state='planned_not_uploaded_by_this_assembly',remote_asset_id=None,
                actual_source_type_support='verify in the native notebook UI; do not assume video/GIF acceptance')

hon_rows=[media_row('HD-DROP-ef5d59a6402e',anchor['source']['absolute_path'],anchor['source']['sha256'],
 'Current Hon Dolo visible design anchor / HD-DESIGN-01','image',anchor['use_limits'])]
order={'GEM-C0823C60':0,'GEM-5A115C59':1,'GEM-D6940AFC':2,'GEM-58328BF1':3}
active=sorted([r for r in hm['records'] if r['provider']=='Gemini' and r['project']=='hon' and r['local_notebook_upload_candidate']],key=lambda r:(order.get(r['asset_id'],99),r['source']['filename']))
for r in active:
    hon_rows.append(media_row(r['asset_id'],r['source']['absolute_path'],r['source']['sha256'],r['selection'],r['kind'],r['known_limits'],
        {'production_accepted':False,'master_elevated':False,'selection_role':r['selection']}))

lisan_rows=[]
for id in ['LAG-602a9fd4021dc356','LAG-63126392af1ccf8b','LAG-VID-PROOF-01-T02']:
    r=next(x for x in lm['media'] if x['assetID']==id)
    lisan_rows.append(media_row(id,r['fullLocalPath'],r['sha256'],r['role'],r['kind'],r['limits'],
            {'working_reference':r['workingReference'],'storyboard_stage':r['storyboardStage'],'production_accepted':False}))

assert len(wr['promotions'])==1, 'Review changed master promotion roster before expanding the upload plan'
w=wr['promotions'][0]
assert w['assetID']=='LAG-VID-PROOF-01-T02'
master_rows=[media_row(w['assetID'],str(ROOT/w['repoPath']),w['sha256'],'Explicitly elevated Lisan scene working reference','video',
    'Scene scope at Detailed design only; technical continuity/audio/song alignment and production acceptance remain pending. No new identity/tattoo standard.',
    {'promotion_id':w['promotionID'],'working_reference':w['workingReference'],'storyboard_stage':w['storyboardStage'],'production_acceptance':w['productionAcceptance']})]
master_rows[0]['scoped_receipt']=check(PACK/'02_lisan_al_gaib/NOTEBOOK0_WINNER_RECEIPT.txt')
master_rows[0]['promotion_registry']=check(winner)

assert len(active)==22 and Counter(x['kind'] for x in active)=={'video':21,'gif':1}
assert not any(x['asset_id'] in ['GEM-97D0B65E','GEM-3CA92958','GEM-8B51108E','GEM-92EF6FD7'] for x in hon_rows)
notebooks=[
 {'key':'00_master','notebook_id':'7719bbe5-fccf-48e2-b6d4-d82f67693b09','notebook_name_basis':'Existing COMFY_UI master; rename managed separately by parent',
  'text_import':dump_records[0],'priority_original_media':master_rows},
 {'key':'01_hon_dolo','notebook_id':'586b3ee6-5c57-45b3-a59d-a2e21c18a852','notebook_name_basis':'Hon Dolo local notebook creation reported by parent; source imports not claimed',
  'text_import':dump_records[1],'priority_original_media':hon_rows},
 {'key':'02_lisan_al_gaib','notebook_id':None,'notebook_name_basis':'Separate Lisan local notebook; UI identity pending operator confirmation',
  'text_import':dump_records[2],'priority_original_media':lisan_rows}
]
allmedia=master_rows+hon_rows+lisan_rows
manifest={'schema_version':1,'prepared_at_utc':NOW,'purpose':'Exact source-file import plan; no uploads, media copies or notebook modifications by this assembly',
 'notebooks':notebooks,'counts':{'text_dumps':3,'media_upload_instances':len(allmedia),'unique_original_media_hashes':len({m['sha256'] for m in allmedia}),
 'by_notebook':{n['key']:len(n['priority_original_media']) for n in notebooks},'hon_active_original_mp4':21,'hon_active_original_gif':1,'hon_design_anchor':1,
 'master_scoped_winner_originals':1,'lisan_video_and_current_face_outfit':3},
 'exclusions':['No archived 40-second GEM-97D0B65E or10-second GEM-3CA92958 in priority original uploads.',
 'No unassigned Gemini desert clips, historical recordings, Multiverse armor or Comfy failure outputs in priority media.',
 'Historical/experimental media remain metadata within project dumps; no implied attachment.',
 'No incoming Grok500 assets; no verified receipt exists.','No account settings, credentials, secrets, unrelated system logs or unrelated conversations included.'],
 'media_handling':'Attach actual originals only if the destination supports their file type. A moved project chat and a native source-file import are separate receipts; do not claim full frame indexing from either without verification. No public hosting workaround or ZIP import assumed.',
 'shared_rules_copy':'Full shared instructions and sync/promotion text appear in all three dumps.',
 'operator_receipt_fields':['actual notebook ID','exact source filename/hash','remote source or asset ID','upload accepted/rejected','readable/playable evidence','known limitations','revision acknowledgement'],
 'imported':False,'generated':False}
(HERE/'UPLOAD_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for p,h in INPUTS.items():
    if sha(p.read_bytes())!=h:raise ValueError('Input edited concurrently; rebuild imports from final source: '+str(p))
validation={'checked_at_utc':NOW,'status':'local_sources_verified_not_uploaded','text_dumps':dump_records,
 'upload_manifest':check(HERE/'UPLOAD_MANIFEST.json'),'input_files':len(INPUTS),'all_priority_media_paths_and_sha256_match':True,
 'priority_media_instances':len(allmedia),'unique_media_hashes':len({m['sha256'] for m in allmedia}),
 'shared_full_copies_present':True,'sensitive_content_check':'Curated notebook source files only; no credential-pattern matches. Account/system/private unrelated sources were not read or included.',
 'bulk_media_copies':0,'remote_uploads':0,'new_generation':0}
(HERE/'VALIDATION.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'dumps':[{k:r[k] for k in ['filename','bytes','sha256']} for r in dump_records],'counts':manifest['counts']},indent=2))
