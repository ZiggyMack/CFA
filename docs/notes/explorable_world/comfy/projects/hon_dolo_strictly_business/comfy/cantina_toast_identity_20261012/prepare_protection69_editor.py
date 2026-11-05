from pathlib import Path
import json, hashlib, copy, datetime, shutil
ROOT=Path('D:/Documents/CFA').resolve()
FOLDER=ROOT/'docs/notes/explorable_world/comfy/projects/hon_dolo_strictly_business/comfy/cantina_toast_identity_20261012'
SOURCE=ROOT/'docs/notes/downloads/WAN_BOUND_EDITOR_AUDIO_PLACEHOLDER_20261012.json'
ARCHIVE=FOLDER/'WAN_BOUND_EDITOR_AUDIO_PLACEHOLDER_ACTUAL_20261012.json'
OUT=FOLDER/'WAN_FACE_PROTECTION69_PREFLIGHT_EDITOR_v002.json'
REPORT=FOLDER/'WAN_FACE_PROTECTION69_PREFLIGHT_STRUCTURE_v002.json'
for p in [SOURCE,ARCHIVE,OUT,REPORT]:
    if not p.resolve().is_relative_to(ROOT):raise ValueError('Path outside workspace')
if ARCHIVE.exists() or OUT.exists() or REPORT.exists():raise FileExistsError('Preserve existing artifacts')
raw=SOURCE.read_bytes()
original=json.loads(raw)
d=copy.deepcopy(original)
N={n['id']:n for n in d['nodes']}
S=d['definitions']['subgraphs'][0]
SN={n['id']:n for n in S['nodes']}

def core(nid,typ,title,pos,inputs,outputs,values=None,named=None):
    n={'id':nid,'type':typ,'pos':pos,'size':[290,150],'flags':{},'order':0,'mode':0,
       'inputs':[{'name':name,'type':tp,'link':None} for name,tp in inputs],
       'outputs':[{'name':name,'type':tp,'links':[]} for name,tp in outputs],
       'title':title,'properties':{'Node name for S&R':typ,'cnr_id':'comfy-core'}}
    if values is not None:n['widgets_values']=values
    if named is not None:n['widgets_values_named']=named
    d['nodes'].append(n);N[nid]=n
    return n

def detach(nid,name):
    i=next(x for x in N[nid]['inputs'] if x['name']==name)
    lid=i.get('link')
    if lid is None:return
    l=next(x for x in d['links'] if x[0]==lid)
    o=N[l[1]]['outputs'][l[2]]
    o['links']=[v for v in (o.get('links') or []) if v!=lid]
    d['links']=[x for x in d['links'] if x[0]!=lid]
    i['link']=None

def connect(lid,src,outslot,dst,name):
    detach(dst,name)
    idx=next(i for i,x in enumerate(N[dst]['inputs']) if x['name']==name)
    tp=N[dst]['inputs'][idx]['type']
    assert N[src]['outputs'][outslot]['type']==tp,(src,dst,name)
    N[src]['outputs'][outslot]['links']=(N[src]['outputs'][outslot].get('links') or [])+[lid]
    N[dst]['inputs'][idx]['link']=lid
    d['links'].append([lid,src,outslot,dst,idx,tp])

core(9001,'ImageFromBatch','Source F168-236: uploaded 77-frame batch, index 6, length 69',[-1310,390],[('image','IMAGE')],[('IMAGE','IMAGE')],[6,69],{'batch_index':6,'length':69})
core(9002,'GetVideoComponents','Generated post-trim 69 frames from CreateVideo (codec none)',[1700,580],[('video','VIDEO')],[('images','IMAGE'),('audio','AUDIO'),('fps','FLOAT'),('bit_depth','COMBO'),('color_space','COMBO')])
core(9003,'LoadVideo','UNBOUND: upload PROTECTION_FRONTAL_69_768x432_LOSSLESS.mp4',[900,520],[],[('VIDEO','VIDEO')],['PROTECTION_FRONTAL_69_768x432_LOSSLESS.mp4','image'],{'file':'PROTECTION_FRONTAL_69_768x432_LOSSLESS.mp4','upload':'image'})
core(9004,'GetVideoComponents','69 protection frames: same frame indices, dimensions and FPS',[1240,550],[('video','VIDEO')],[('images','IMAGE'),('audio','AUDIO'),('fps','FLOAT'),('bit_depth','COMBO'),('color_space','COMBO')])
core(9005,'ImageToMask','Red channel: WHITE protects, BLACK permits edit',[1540,460],[('image','IMAGE')],[('MASK','MASK')],['red'],{'channel':'red'})
core(9006,'MaskComposite','Editable mask = feathered face minus protected detail',[1780,-220],[('destination','MASK'),('source','MASK')],[('MASK','MASK')],[0,0,'subtract'],{'x':0,'y':0,'operation':'subtract'})
connect(93001,23,0,9001,'image')
connect(93002,9001,0,212,'image')
connect(93003,9001,0,158,'original_image')
connect(93004,232,0,9002,'video')
connect(93005,9002,0,548748812020021,'source')
connect(93006,9003,0,9004,'video')
connect(93007,9004,0,9005,'image')
connect(93008,1833034495877259,0,9006,'destination')
connect(93009,9005,0,9006,'source')
connect(93010,9006,0,275,'mask')
connect(93011,9006,0,232,'character_mask')
connect(93012,9006,0,548748812020021,'mask')
connect(93013,9006,0,1481734536190884,'mask')
# Final and subgraph audio use exact 69-frame PCM, not the 77-frame loader's absent audio.
N[4427161206989702]['widgets_values']=['SOURCE_FRONTAL_AUDIO_168_236_PCM.wav','']
N[4427161206989702]['widgets_values_named']={'audio':'SOURCE_FRONTAL_AUDIO_168_236_PCM.wav','upload':''}
N[4427161206989702]['title']='UNBOUND: upload SOURCE_FRONTAL_AUDIO_168_236_PCM.wav'
connect(93014,4427161206989702,0,4085252815952851,'audio')
connect(93015,4427161206989702,0,232,'audio')
# One redundant unconnected audio node is removed only from this derived graph.
assert not any(l[1]==126328811016242 or l[3]==126328811016242 for l in d['links'])
d['nodes']=[n for n in d['nodes'] if n['id']!=126328811016242]
N.pop(126328811016242)
# Retain actual uploaded source and actor filenames while clarifying their bound titles.
N[145]['title']='BOUND source 77 frames: local frame 0 = original F162'
N[10]['title']='BOUND actor identity crop HD-LIKENESS-03'
# Only identity-relevant face regions remain editable; mouth and hardware protected separately.
n=N[324475594538284]
for name in ['mouth','u_lip','l_lip']:n['widgets_values_named'][name]=False
n['widgets_values']=list(n['widgets_values_named'].values())
# Fix disconnected scalar boundary definitions by using the actual inner widgets.
# Old boundary inputs13-18 had no matching outer232 input sockets. Keep width/height links.
control_names={'fps','seed','steps','cfg','sampler_name','scheduler'}
control_lids={lid for x in S['inputs'] if x['name'] in control_names for lid in x.get('linkIds',[])}
S['inputs']=[x for x in S['inputs'] if x['name'] not in control_names]
S['links']=[x for x in S['links'] if x['id'] not in control_lids]
for n in S['nodes']:
    for i in n.get('inputs',[]):
        if i.get('link') in control_lids:i['link']=None
SN[62]['widgets_values']=[768,432,69,1,5,0]
SN[62]['widgets_values_named'].update({'width':768,'height':432,'length':69,'batch_size':1})
SN[63]['widgets_values']=[42,'fixed',6,1,'euler','simple',1]
SN[63]['widgets_values_named'].update({'seed':42,'control_after_generate':'fixed','steps':6,'cfg':1,'sampler_name':'euler','scheduler':'simple','denoise':1})
SN[15]['widgets_values']=[24,'auto','sRGB','none']
SN[15]['widgets_values_named'].update({'fps':24,'bit_depth':'auto','color_space':'sRGB','codec':'none'})
# Cap internal post-trim image batch length as well as requested generation length.
SN[230]['widgets_values'][1]=69
SN[230]['widgets_values_named']['length']=69
# Outer quarantined proxies are historical UI baggage, not source of sampling values.
N[232]['widgets_values']=[]
N[232]['widgets_values_named']={}
# Preflight has exactly two active terminal previews and no reachable sampling branch.
for nid in [19,127,3365632822813953,232,108,107,274,276,229]:N[nid]['mode']=2
SN[63]['mode']=2
N[124]['mode']=0
N[1481734536190884]['mode']=0
N[124]['title']='PREFLIGHT: source frames with only editable face region blacked out'
N[1481734536190884]['title']='PREFLIGHT: final editable mask after protection subtraction'
N[3365632822813953]['title']='DISABLED generation output: restore only after mask/alignment review'
N[232]['title']='DISABLED sampling: 69 frames, seed42 fixed,6 steps, CFG1'
N[4085252815952851]['widgets_values_named']['fps']=24
N[4085252815952851]['widgets_values'][0]=24
# Preserve all upstream remote-resource/model metadata exactly.
for old in original['nodes']:
    if old.get('properties',{}).get('models'):
        assert N[old['id']]['properties']==old['properties']
for nid in [145,10]:
    assert N[nid]['widgets_values']==next(x for x in original['nodes'] if x['id']==nid)['widgets_values']
d['revision']=original.get('revision',0)+1
# last IDs remain above newly reserved9001-9006/93001-93015.
d['last_node_id']=max(d['last_node_id'],max(N))
d['last_link_id']=max(d['last_link_id'],max(l[0] for l in d['links']))
S['state']['lastNodeId']=max(S['state']['lastNodeId'],max(SN))
# Bidirectional socket/link and type validation for the outer graph.
links={l[0]:l for l in d['links']}
assert len(links)==len(d['links'])
assert len(N)==len(d['nodes'])
for lid,src,os,dst,is_,tp in d['links']:
    assert src in N and dst in N
    assert N[src]['outputs'][os]['type']==tp
    assert N[dst]['inputs'][is_]['type']==tp
    assert N[dst]['inputs'][is_]['link']==lid
    assert lid in (N[src]['outputs'][os].get('links') or [])
for nid,n in N.items():
    for is_,i in enumerate(n.get('inputs',[])):
        if i.get('link') is not None:
            l=links[i['link']];assert l[3:5]==[nid,is_]
    for os,o in enumerate(n.get('outputs',[])):
        for lid in o.get('links') or []:assert links[lid][1:3]==[nid,os]
# Subgraph internal and boundary links: each actual socket maps to its link.
sl={l['id']:l for l in S['links']}
for l in S['links']:
    if l['origin_id']!=-10:
        assert l['id'] in (SN[l['origin_id']]['outputs'][l['origin_slot']].get('links') or [])
    else:
        assert l['id'] in S['inputs'][l['origin_slot']]['linkIds']
    if l['target_id']!=-20:
        assert SN[l['target_id']]['inputs'][l['target_slot']]['link']==l['id']
    else:
        assert l['id'] in S['outputs'][l['target_slot']]['linkIds']
for n in S['nodes']:
    for i in n.get('inputs',[]):assert i.get('link') is None or i['link'] in sl
    for o in n.get('outputs',[]):assert all(lid in sl for lid in o.get('links') or [])
# Trace ancestors of active terminal previews. No generation/model/pose/SAM branch is included.
reach=set()
def visit(nid):
    if nid in reach:return
    reach.add(nid)
    for i in N[nid].get('inputs',[]):
        if i.get('link') is not None:visit(links[i['link']][1])
for nid in [124,1481734536190884]:visit(nid)
for forbidden in [232,20,18,99,60,2,3,4,9,21,1,100,101,108,107,274,276,229]:assert forbidden not in reach
report={'status':'LOCAL_STRUCTURAL_CHECK_ONLY','source_sha256':hashlib.sha256(raw).hexdigest(),
 'archived_source':ARCHIVE.name,'editor':OUT.name,'active_terminal_outputs':[124,1481734536190884],
 'active_preflight_ancestors':sorted(reach),'sampling_reachable_from_preflight':False,
 'source_trim':{'node':9001,'batch_index':6,'length':69,'source_original_frames':[168,236]},
 'dimensions':[768,432],'fps':24,'sampling_plan':{'seed':42,'control_after_generate':'fixed','steps':6,'cfg':1,'sampler':'euler','scheduler':'simple','denoise':1,'batch_size':1,'length':69,'sampler_disabled':True},
 'conditioning_and_composite_mask':{'node':9006,'operation':'subtract','destination':1833034495877259,'source':9005,'outputs_to':[275,232,548748812020021,1481734536190884]},
 'composite_generated_source':{'node':9002,'input':'232.VIDEO','compiled_origin':'232:15 CreateVideo after232:230 ImageFromBatch','codec':'none'},
 'uploads_still_required':{'9003':'PROTECTION_FRONTAL_69_768x432_LOSSLESS.mp4','4427161206989702':'SOURCE_FRONTAL_AUDIO_168_236_PCM.wav'},
 'cloud_runtime_validated':False,'cloud_runs':0,
 'unknowns':['Cloud loaded schemas/exported compiled inputs for added nodes','Actual protection/video frame counts and alignment on Cloud','Face-parser coverage and protected-region boundary preview','Current remote model availability on generation branch','Actual GPU usage and costs'],
 'sources':['https://raw.githubusercontent.com/Comfy-Org/ComfyUI/master/comfy_extras/nodes_mask.py','https://raw.githubusercontent.com/Comfy-Org/ComfyUI/master/comfy_extras/nodes_video.py','../../../../../../../../Pan_Handlers/Help/content/video_routes.py:wan_mix']}
OUT.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
report['editor_sha256']=hashlib.sha256(OUT.read_bytes()).hexdigest()
REPORT.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
# Move only this known downloaded export within the workspace, verify original bytes after move.
shutil.move(str(SOURCE),str(ARCHIVE))
assert ARCHIVE.read_bytes()==raw
print(json.dumps({'archive':str(ARCHIVE),'editor':str(OUT),'report':str(REPORT),'editor_sha256':report['editor_sha256'],'nodes':len(d['nodes']),'links':len(d['links']),'preflight_ancestors':len(reach)}))
