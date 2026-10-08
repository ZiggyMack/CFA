"""Build the local visual browser from preserved project manifests. No network or source mutation."""
from pathlib import Path
import json, os, re, urllib.parse

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
    if not any(a['id']==key for a in albums):
        albums.append(dict(id=key, project=project, category=category, title=title, description=description, related=related or []))
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
    if a['reference_id'].startswith('HD-LIKENESS'):
        c='comfy'; al=add_album('hon','comfy-likeness',c,'Comfy likeness targets','Han Solo appearance targets for a separate likeness or swap experiment; not the current Grok design anchor.')
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
for project,folder,paths in [('hon',COMFY/'casting',['gemini_project_instructions.txt','gemini_cast_reference_map.txt']),('lisan',PROJECTS/'lisan_al_gaib/gemini',['gemini_instructions.txt','reference_map.txt','first_video_prompt.txt'])]:
    for p in paths: doc(project,str((folder/p).relative_to(ROOT)).replace('\\','/'),title=p.replace('_',' ').replace('.txt','').capitalize(),album='Gemini instructions and image maps')

for project,folder in [('hon','hon_dolo_strictly_business'),('lisan','lisan_al_gaib')]:
    for name in ['provider_roles.txt','flow_brief.txt','flow_shot_template.txt']:
        doc(project,str((PROJECTS/'collaborators'/name).relative_to(ROOT)).replace('\\','/'),title=name.replace('_',' ').replace('.txt','').capitalize(),album='Collaborator briefs · Flow')
    doc(project,str((PROJECTS/folder/'flow/project_brief.txt').relative_to(ROOT)).replace('\\','/'),title='Flow project brief',album='Collaborator briefs · Flow')
doc('hon',str((COMFY/'casting/grok_project_instructions.txt').relative_to(ROOT)).replace('\\','/'),title='Grok project instructions',album='Grok design instructions')

for al in albums:
    primary=[a['id'] for a in assets if a['album']==al['id']]
    al['assetIDs']=list(dict.fromkeys(primary+al.pop('related')))
albums=[al for al in albums if al['assetIDs']]
# Show designs on the character before the standalone stencil options.
albums.sort(key=lambda al: 'stencil' in al['id'].lower())
catalog=dict(projects=[dict(id='hon',name='Hon Dolo',subtitle='Strictly Business'),dict(id='lisan',name='Lisan Al Gaib',subtitle='Meta Mirror'),dict(id='unassigned',name='Unassigned',subtitle='Two clips to place')],assets=assets,albums=albums,categories=[['working','Working references'],['outfits','Outfits'],['details','Tattoos & piercings'],['cast','Supporting cast'],['storyboard','Storyboard'],['videos','Videos'],['comfy','Comfy swap targets'],['inspiration','Inspiration'],['review','Needs review']])
ids=[a['id'] for a in assets];assert len(ids)==len(set(ids)), 'Repeated UI asset IDs'
(HERE/'catalog.js').write_text('window.REVIEW_CATALOG = '+json.dumps(catalog,ensure_ascii=False).replace('<','\\u003c')+';\n',encoding='utf-8')

def shell(path,project,view='all'):
    prefix=os.path.relpath(HERE,path.parent).replace('\\','/')+'/'
    path.write_text('<!doctype html>\n<html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Visual reference library</title>\n<link rel="stylesheet" href="'+prefix+'library.css">\n<div id="app"></div><script>window.REVIEW_INITIAL='+json.dumps(dict(project=project,view=view))+';</script>\n<script src="'+prefix+'catalog.js"></script><script src="'+prefix+'library.js"></script></html>\n',encoding='utf-8')
shell(PROJECTS/'index.html','hon')
shell(PROJECTS/'hon_dolo_strictly_business/asset_review_20261007/index.html','hon')
shell(PROJECTS/'hon_dolo_strictly_business/asset_review_20261007/storyboard.html','hon','storyboard')
shell(PROJECTS/'hon_dolo_strictly_business/gemini_review_20261007/index.html','hon','videos')
shell(PROJECTS/'lisan_al_gaib/index.html','lisan')
print(json.dumps({'assets':len(assets),'albums':len(albums),'documents':sum(a['kind'] in ['document','pdf'] for a in assets),'media':sum(a['kind'] not in ['document','pdf'] for a in assets)}))
