"""Build the local visual browser from preserved project manifests. No network or source mutation."""
from pathlib import Path
import hashlib, json, os, re, urllib.parse

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[5]
COMFY = ROOT / 'docs/notes/explorable_world/comfy'
PROJECTS = COMFY / 'projects'
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def url(p):
    p = Path(p) if Path(p).is_absolute() else ROOT / p
    assert p.is_file(), p
    return urllib.parse.quote(os.path.relpath(p, HERE).replace('\\', '/'), safe='/')
previews = read(HERE / 'preview_paths.json')['by_path']
grouping = read(HERE / 'collections.json')
story = read(HERE / 'story_notes.json')
def thumb(p): return url(previews.get(str(p).replace('\\','/'), {}).get('thumbnail_path', p))
assets = []; albums = []
def add_album(project, id, category, title, description='', related=None):
    key = project + ':' + id
    existing=next((a for a in albums if a['id']==key),None)
    if existing is None:
        albums.append(dict(id=key, project=project, category=category, title=title, description=description, related=related or []))
    elif related:
        existing['related']=list(dict.fromkeys(existing['related']+related))
    return key
def image(project, id, p, title, category, album, **kw):
    a=dict(id=id, project=project, src=url(p), thumb=thumb(p), filename=Path(p).name,
           repoPath=str(p).replace('\\','/'), title=title, category=category, album=album, kind='image', **kw)
    assets.append(a); return a
def doc(project, p, title=None, album='Project notes'):
    ext=Path(p).suffix.lower()
    if ext not in ['.txt','.md','.json','.csv','.py','.pdf']: return
    content = '' if ext=='.pdf' else (ROOT / p).read_text(encoding='utf-8-sig',errors='replace')
    assets.append(dict(id=project+':doc:'+str(p),project=project,src=url(p),filename=Path(p).name,title=title or Path(p).name,
        repoPath=str(p),category='documents',album=album,kind='pdf' if ext=='.pdf' else 'document',text=content[:40000],
        note='Preview shortened; open the original for the full text.' if len(content)>40000 else '',inert=ext=='.py'))

hon = read(PROJECTS / 'hon_dolo_strictly_business/asset_review_20261007/manifest.json')
meta={a['asset_id']:a for a in grouping['assets']}
for g in grouping['albums']:
    if g['collection_id']=='storyboard':continue
    add_album('hon',g['id'],g['collection_id'],g['title'],g['short_description'],g.get('related_asset_ids',[]))
for g in story['hon_groups']: add_album('hon','story-'+g['id'],'storyboard',g['title'],g['description'])
for a in hon['assets']:
    p=a['review_path']
    if not a.get('image'):
        pack=a['sources'][0].get('archive_label','Drop notes')
        label=pack.replace('hon-dolo-ref-sheet-','').replace('hon-dolo-','').replace('-',' ').title()
        label=('Helper scripts (kept as text)' if Path(p).suffix=='.py' else
               'Storyboard notes' if 'storyboard' in pack else
               'Reference maps and drop notes' if any(x in pack for x in ['consolidation','since-last']) else
               'Design and outfit notes · '+label)
        doc('hon',p,album=label);continue
    m=meta[a['asset_id']]; c=m['collection_id']; al='hon:'+m['album_id']
    extra=dict(note=a.get('review_note',a.get('allowed_use','')),tags=m['tags'],sha256=a['sha256'],sourceStatus=a['category'])
    title=m['display_label']
    match=re.search(r'SB-\d+',a['filename'])
    if match:
        sid=match.group(); n=story['hon_panels'][sid]
        title=sid+' · '+n['beat_title']
        group=next(g for g in story['hon_groups'] if sid in g['panel_ids'])
        al='hon:story-'+group['id'];c='storyboard'
        extra.update(beat=n['lyric_connection'],lyric=n.get('lyric_cue',''),note=n['review_note'],sceneID=sid)
    image('hon',a['asset_id'],p,title,c,al,**extra)

cast=read(COMFY/'casting/gemini_cast_reference_map.json')
existing={a.get('sha256') for a in assets if a['project']=='hon'}
for a in cast['references']:
    if a['sha256'] in existing: continue
    char=a['character_id']; islead=char=='HON-DOLO'
    if 'LIKENESS' in a['reference_id']:
        c='comfy'
        label={'HON-DOLO':'Han Solo','LEIA':'Princess Leia','LUKE':'Luke Skywalker'}.get(char,char)
        source_group=a['reference_id']=='HD-LIKENESS-02'
        al=add_album('hon','source-group-photo' if source_group else 'comfy-likeness-'+char,c,'Original group photograph' if source_group else label+' · likeness targets','Source preserved; individual character crops are available for separate inputs.' if source_group else 'Appearance targets for a separate likeness or swap experiment; not a wardrobe or tattoo standard.')
    elif islead:
        c='details'; al=add_album('hon','optional-finish',c,'Optional photographic finish','A finish study only. Keep the current design anchor as the working reference.')
    else:
        c='cast'; al=add_album('hon','cast-existing-'+char,c,char.replace('-',' ').title()+' · earlier studies')
    image('hon',a['reference_id'],a['original_path'],a['role'].capitalize(),c,al,note=a['use_limits'],sha256=a['sha256'],tags=[char,a['role']],sourceStatus=a['selection_status'])
    existing.add(a['sha256'])

lm=read(PROJECTS/'lisan_al_gaib/manifest.json')
ls=read(PROJECTS/'lisan_al_gaib/scene_map.json')['scenes']; ls={s['scene_id']:s for s in ls}
for g in story['lisan_groups']: add_album('lisan','story-'+g['id'],'storyboard',g['title'],g['description'])
seen=set()
for a in lm['files']:
    if a['sha256'] in seen:continue
    seen.add(a['sha256']);p=a['review_path'];name=Path(p).name
    if not a.get('image'):
        doc('lisan',p,album='Story and character notes' if Path(p).suffix!='.csv' else 'Storyboard table');continue
    c='inspiration'; aid='history';title=Path(p).stem.replace('-',' ').title();note=a['role'];tags=[]
    if '/01_Flagship_References/' in p:
        c='details' if 'ARM' in name else 'working';aid='current-arm' if c=='details' else 'current-face'
        title={'LAG-LOCK-FACE-NATURAL.jpg':'Current face · natural teeth','LAG-LOCK-ARM-SH13.jpg':'Left arm · sandworm artwork','LAG-LOOK-V3-01.jpg':'Signature stillsuit and cloak'}[name]
        note='Arm tattoo only. The teeth, piercings and neck design in this image are retired.' if 'ARM' in name else 'Current working reference. Face portrait governs teeth and facial details; outfit picture supplies wardrobe.'
        add_album('lisan',aid,c,'Arm tattoo' if c=='details' else 'Face and signature look')
    elif '/02_Storyboard_Scenes/' in p:
        match=re.fullmatch(r'(LAG-SC-\d+)\.jpg',name)
        if not match: c='inspiration';aid='overview';add_album('lisan',aid,c,'Scene overview sheets')
        else:
            sid=match.group(1);s=ls[sid];n=int(sid[-2:]);g=next(g for g in story['lisan_groups'] if g['first_scene']<=n<=g['last_scene'])
            c='storyboard';aid='story-'+g['id'];title=sid+' · '+s['scene_outfit_reported'].split(',')[0].capitalize();note='Grok notes: '+s['grok_qa_reported'];tags=[s['lyric_cue_reported']]
    else:
        folder=Path(p).parent.name
        defs={'a-original-10-looks':('outfits','early-outfits','Early outfit ideas'), 'b-sandworm-stencils':('details','worm-stencils','Sandworm tattoo designs'), 'c-sandworm-neck-tryons':('details','neck-tryons','Neck tattoo placement'), 'd-looks-v2-iced-grill':('inspiration','grill-history','Retired grill exploration'), 'e-natural-teeth-face-tests':('inspiration','face-tests','Face studies'), 'f-first-12-scenes-old-spec':('inspiration','old-scenes','Earlier storyboard versions'), 'g-superseded-refs':('review','old-refs','Superseded references')}
        c,aid,label=defs.get(folder,('inspiration','history','Design history'));add_album('lisan',aid,c,label)
        note='Historical exploration. Current face and natural teeth take precedence.'
    extra=dict(note=note,tags=tags,sha256=a['sha256'],sourceStatus=a['role'])
    if c=='storyboard':extra.update(sceneID=sid,beat=s['scene_outfit_reported'],lyric=s['lyric_cue_reported'],motion=s['motion_suggestion'])
    image('lisan','LAG-'+a['sha256'][:16],p,title,c,'lisan:'+aid,**extra)

vid=read(PROJECTS/'hon_dolo_strictly_business/gemini_review_20261007/inventory.json')
for a in vid['items']:
    project='hon' if a['project']=='hon_dolo_strictly_business' else 'unassigned';p=a['review_copy_path'];cat=a['initial_scene_folder']
    al=add_album(project,'video-'+cat,'videos',cat.replace('_',' ').title()+' videos')
    assets.append(dict(id=a['reference_id'],project=project,src=url(p),thumb=thumb(p),filename=a['filename'],repoPath=p,title=a['title'],category='videos',album=al,kind='gif' if a['filename'].endswith('.gif') else 'video',duration=a['video_duration_seconds'],note=a['review_notes'],beat=a['observed_content'],sha256=a['sha256'],tags=[cat],sourceStatus=a.get('user_selection') or 'Candidate'))

# A production result has one asset ID. The project and collaborator workspace
# both point to it; experiments never become accepted references implicitly.
production=read(PROJECTS/'collaborators/comfy_workflows.json')
for item in production['media']:
    a=dict(item); p=a.pop('path'); group=a.pop('group'); title=a.pop('groupTitle')
    preview=a.pop('thumbnailPath',p)
    a.update(src=url(p),thumb=url(preview),repoPath=p,filename=Path(p).name,
             album=add_album(a['project'],group,a['category'],title))
    assets.append(a)
for d in production['documents']:
    doc('hon',d['path'],title=d['title'],album='ComfyUI production records')
# Provider output registries keep immutable originals separate from review state.
provider_outputs=PROJECTS/'lisan_al_gaib/gemini/outputs/registry.json'
if provider_outputs.exists():
    registry=read(provider_outputs)
    for item in registry.get('media',[]):
        a=dict(item); p=a.pop('path'); group=a.pop('group'); group_title=a.pop('groupTitle')
        preview=a.pop('thumbnailPath',p)
        a.update(src=url(p),thumb=url(preview),repoPath=p,filename=Path(p).name,
                 album=add_album(a['project'],group,a['category'],group_title))
        assets.append(a)
        if a.get('storyboardStage'):
            add_album(a['project'],'story-developed-takes','storyboard','Developed video takes',
                      'Selected footage beyond preliminary panels. Exact song placement and verification remain separate.',[a['id']])
        if a.get('workingReference',{}).get('status')=='approved':
            add_album(a['project'],'selected-video-references','working','Selected video references',
                      'Selected for scene and motion use; the current identity and tattoo references still govern.',[a['id']])
    for d in registry.get('documents',[]):
        doc('lisan',d['path'],title=d['title'],album='Gemini production records')
for project,folder,paths in [('hon',COMFY/'casting',['gemini_project_instructions.txt','gemini_cast_reference_map.txt']),('lisan',PROJECTS/'lisan_al_gaib/gemini',['gemini_instructions.txt','reference_map.txt','first_video_prompt.txt'])]:
    for p in paths: doc(project,str((folder/p).relative_to(ROOT)).replace('\\','/'),title=p.replace('_',' ').replace('.txt','').capitalize(),album='Gemini instructions and image maps')

for project,folder in [('hon','hon_dolo_strictly_business'),('lisan','lisan_al_gaib')]:
    for name in ['provider_roles.txt','flow_brief.txt','flow_shot_template.txt']:
        doc(project,str((PROJECTS/'collaborators'/name).relative_to(ROOT)).replace('\\','/'),title=name.replace('_',' ').replace('.txt','').capitalize(),album='Collaborator briefs · Flow')
    doc(project,str((PROJECTS/folder/'flow/project_brief.txt').relative_to(ROOT)).replace('\\','/'),title='Flow project brief',album='Collaborator briefs · Flow')
doc('hon',str((COMFY/'casting/grok_project_instructions.txt').relative_to(ROOT)).replace('\\','/'),title='Earlier Grok exploration brief (historical)',album='Historical collaborator briefs')
for project in ['hon','lisan']:
    doc(project,(PROJECTS/'collaborators/grok_design_instructions.txt').relative_to(ROOT).as_posix(),title='Grok design instructions · current',album='Collaborator briefs · Grok')
for name,title in [('tattoo_audit_20261008.txt','Tattoo source recovery · visual audit'),('tattoo_audit_20261008.json','Tattoo source recovery · exact image map')]:
    p=HERE/name
    if p.exists():doc('hon',p.relative_to(ROOT).as_posix(),title=title,album='Tattoo source recovery')
handoff=PROJECTS/'hon_dolo_strictly_business/handoffs/grok_20261008'
for name, title in [('START_HERE.txt','Grok current care package · start here'),('requests.json','Grok requests and exact regions'),('asset_map.json','Grok package image map'),('panel_plan.txt','Boss and Caleb panel plans'),('return_manifest.template.json','Grok return manifest template')]:
    doc('hon',str((handoff/name).relative_to(ROOT)).replace('\\','/'),title=title,album='Grok care package · October 8')
for project in ['hon','lisan']:
    doc(project,str((PROJECTS/'collaborators/flow_start_here.txt').relative_to(ROOT)).replace('\\','/'),title='Start here · Flow',album='Collaborator briefs · Flow')
    doc(project,str((PROJECTS/'collaborators/flow_intake_20261008.txt').relative_to(ROOT)).replace('\\','/'),title='Flow upload roles and model choices',album='Collaborator briefs · Flow')
    doc(project,str((PROJECTS/'collaborators/panhandler_return_20261008.txt').relative_to(ROOT)).replace('\\','/'),title='Panhandler Nova · studio progress handoff',album='Collaborator handoffs')
doc('hon',str((PROJECTS/'hon_dolo_strictly_business/flow/first_experiment_20261008.txt').relative_to(ROOT)).replace('\\','/'),title='Flow first character experiment',album='Collaborator briefs · Flow')
doc('hon',str((PROJECTS/'hon_dolo_strictly_business/flow/second_video_experiment_20261008.txt').relative_to(ROOT)).replace('\\','/'),title='Flow second experiment · six-second video edit',album='Collaborator briefs · Flow')

# Panel order supplies navigation only. It is not fitted to the current song.
for project in ['hon','lisan']:
    panels=sorted([a for a in assets if a['project']==project and a['category']=='storyboard'],key=lambda a:int(re.search(r'(\d+)$',a['sceneID']).group()))
    for index,a in enumerate(panels):
        a['storyboardOrder']=index+1
        a['storyboardPosition']=round(index/max(1,len(panels)-1)*100,4)

review_path=PROJECTS/'hon_dolo_strictly_business/feedback/review_decisions.json'
review_decisions=read(review_path)['items'] if review_path.exists() else []
queue_path=PROJECTS/'hon_dolo_strictly_business/feedback/grok_revision_queue.txt'
if queue_path.exists():doc('hon',str(queue_path.relative_to(ROOT)).replace('\\','/'),title='Grok revision queue',album='Grok revisions and review notes')
for name,title in [('review_sweep_20261008.txt','Review sweep · saved favorites and decisions'),('grok_favorite_prop_sweep_20261008.txt','Grok · favorite-look hardware sweep'),('boss_discovery_20261008.txt','Boss discovery · select a character before turnarounds')]:
    p=PROJECTS/'hon_dolo_strictly_business/feedback'/name
    if p.exists():doc('hon',p.relative_to(ROOT).as_posix(),title=title,album='Grok revisions and review notes')

# Approved promotions are applied only by a recorded sweep. Requests remain
# requests; unresolved fixes/removals and Multiverse stay out of Prime references.
by_id={a['id']:a for a in assets}
for decision in review_decisions:
    a=by_id.get(decision['id'])
    if not a:continue
    if decision.get('variant'):a['variant']=decision['variant']
    if decision.get('collectionState')=='archived':a['archived']=True
    if decision.get('displayTitle'):a['title']=decision['displayTitle']
    if decision.get('storyboardStage'):a['storyboardStage']=decision['storyboardStage']
    wr=decision.get('workingReference') or {}
    if wr.get('status')=='approved' and not a.get('archived') and decision.get('variant')!='multiverse' and decision.get('status') not in ['needs_fixes','remove']:
        a['workingReference']=wr
        al=add_album(a['project'],'promoted-working','working','Selected working references','Selected for the recorded scope; a scene or outfit selection does not redefine facial details.',[a['id']])
        next(g for g in albums if g['id']==al)['related'].append(a['id'])

for al in albums:
    primary=[a['id'] for a in assets if a['album']==al['id']]
    if al['category']=='videos':
        by_id={a['id']:a for a in assets}
        primary.sort(key=lambda id: {'starting_source':0,'dinner_candidate':1}.get(by_id[id].get('sourceStatus'),2))
    al['assetIDs']=list(dict.fromkeys(primary+al.pop('related')))
albums=[al for al in albums if al['assetIDs']]
# Show designs on the character before the standalone stencil options.
category_order=['working','outfits','details','cast','storyboard','videos','comfy','inspiration','review']
video_order=['action','performance','gemini_approved','dinner','cockpit','supporting_cast','soundtrack_experiments','comfy_experiments','needs_review','turnaround']
def album_order(al):
    group=al['id'].split('video-',1)[-1]
    return (category_order.index(al['category']) if al['category'] in category_order else 99,
            (video_order.index(group) if group in video_order else len(video_order)-1) if al['category']=='videos' else int('stencil' in al['id'].lower()))
albums.sort(key=album_order)
catalog=dict(projects=[dict(id='hon',name='Hon Dolo',subtitle='Strictly Business'),dict(id='lisan',name='Lisan Al Gaib',subtitle='Meta Mirror'),dict(id='unassigned',name='Unassigned',subtitle='Two clips to place')],assets=assets,albums=albums,categories=[['working','Working references'],['outfits','Outfits'],['details','Tattoos & piercings'],['cast','Supporting cast'],['storyboard','Storyboard'],['videos','Videos'],['comfy','Comfy swap targets'],['inspiration','Inspiration'],['review','Needs review']])
ids=[a['id'] for a in assets];assert len(ids)==len(set(ids)), 'Repeated UI asset IDs'
catalog['reviewDecisions']=review_decisions
catalog['missionControl']=read(PROJECTS/'collaborators/mission_control.json')
catalog['productionWorkflows']=production['workflows']
profiles_path=PROJECTS/'collaborators/detail_profiles.json'
catalog['detailProfiles']=read(profiles_path) if profiles_path.exists() else []
catalog['storyboardMetadata']={p:dict(timingStatus='Source panel order only; not aligned to current song timings.',positionBasis='source_panel_order',panelCount=sum(a['project']==p and a['category']=='storyboard' for a in assets)) for p in ['hon','lisan']}
for workflow in catalog['productionWorkflows']:
    assert all(id in by_id for key in ['sourceAssetIDs','outputAssetIDs','documentAssetIDs'] for id in workflow[key]),workflow['id']
(HERE/'catalog.js').write_text('window.REVIEW_CATALOG = '+json.dumps(catalog,ensure_ascii=False).replace('<','\\u003c')+';\n',encoding='utf-8')

def shell(path,project,view='all'):
    prefix=os.path.relpath(HERE,path.parent).replace('\\','/')+'/'
    versions={name:hashlib.sha256((HERE/name).read_bytes()).hexdigest()[:10] for name in ['library.css','catalog.js','library.js']}
    build=hashlib.sha256(json.dumps(versions,sort_keys=True).encode()).hexdigest()[:10]
    path.write_text('<!doctype html>\n<html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Visual reference library</title>\n<link rel="stylesheet" href="'+prefix+'library.css?v='+versions['library.css']+'">\n<div id="app"></div><script>window.REVIEW_INITIAL='+json.dumps(dict(project=project,view=view))+';window.REVIEW_BUILD='+json.dumps(build)+';</script>\n<script src="'+prefix+'catalog.js?v='+versions['catalog.js']+'"></script><script src="'+prefix+'library.js?v='+versions['library.js']+'"></script></html>\n',encoding='utf-8')
shell(PROJECTS/'index.html','hon')
shell(PROJECTS/'hon_dolo_strictly_business/asset_review_20261007/index.html','hon')
shell(PROJECTS/'hon_dolo_strictly_business/asset_review_20261007/storyboard.html','hon','storyboard')
shell(PROJECTS/'hon_dolo_strictly_business/gemini_review_20261007/index.html','hon','videos')
shell(PROJECTS/'lisan_al_gaib/index.html','lisan')
print(json.dumps({'assets':len(assets),'albums':len(albums),'documents':sum(a['kind'] in ['document','pdf'] for a in assets),'media':sum(a['kind'] not in ['document','pdf'] for a in assets)}))
