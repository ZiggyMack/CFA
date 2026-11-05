"""Evidence-backed storyboard structure, independent of media and human reviews.

This adapter reads posted writing; it never upgrades a draft to acceptance, picks
a source frame, assigns timing, or writes a review. Rebuilds are deterministic.
"""
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import re

BASE = 'docs/notes/explorable_world/comfy/projects/'
WRITER = BASE + 'hon_dolo_strictly_business/story/writer_pass_20261010/'
KITCHEN = WRITER + 'kitchen_block_20261029/'
MAP = WRITER + 'HON_COVERAGE_MAP_20261028.json'
TEMPLATE = BASE + 'lisan_al_gaib/story/writer_pass_20261012/SHOT_DIRECTION_TEMPLATE.md'
ADDENDUM = KITCHEN + 'KITCHEN_BLOCK_ADDENDUM_A_20261029.md'
SPEC = KITCHEN + 'KITCHEN_BLOCK_SPEC_20261029.md'

# Display labels are independent of the writer's numbered source headings.
# Stable field keys keep prior evidence and reviews connected.
FIELDS = [
 ('purpose','A','Purpose & story position','Writer','writing','Shot / take ID, title, story position and purpose.'),
 ('context','B','Before, after & cut','Writer','writing','Neighbouring shots, continuity, start/end state and cut boundaries.'),
 ('lineage','C','Source lineage & prior takes','CFA Nova','dispatch','Exact source file, hash, bytes, variant, repair history and parent revision.'),
 ('references','D','References & their roles','Writer / CFA Nova','route','Identity, design, inspiration and conditioning inputs; scoped selection is separate from scene acceptance.'),
 ('start_frame','0','Prepared starting frame','CFA Nova','route','Required when the chosen mode uses a starting frame; not required for writing or every route.'),
 ('lighting','1','Lighting','Writer','writing','Key, fill, rim, practicals and their changes; explicit none is valid.'),
 ('camera','2','Camera','Writer','writing','Frame, height, distance, lens feel, movement, axis and screen edges.'),
 ('character','3','Character direction','Writer','writing','Action, eyeline, face, hands, body, pace and intended audience reading; none can be intentional.'),
 ('background','4','Background action','Writer','writing','Other motion, light changes and exclusions; explicit none is valid.'),
 ('beats','5','Coordinated beats','Writer','writing','What lighting, camera, character and background do together; design beats are not accepted timing.'),
 ('cue','6','Song / score cue & placement','Writer / alignment owner','conditional','Cue or inherited master ID and revision; event/word/grid anchors, arc, placement evidence or explicit silence.'),
 ('prompt_still','7','Still / preparation prompt','Writer','route','Written prompt for preparation where needed; optional for existing footage.'),
 ('prompt_clip','8','Clip prompt','Writer','route','Prompt derived from the coordinated direction; readiness depends on the chosen route.'),
 ('settings','9','Dispatch & technical settings','CFA Nova','dispatch','Chosen provider, model, mode, resolution, aspect, native length, outputs, displayed cost and submitted prompt.'),
 ('results','10','Returned video & measurements','CFA Nova','return','Canonical result file, hash, bytes, duration, fps, dimensions, audio, frame sheet and observed defects.'),
 ('acceptance','11','Video review & acceptance','Ziggy','review','Human verdict on this exact result; attributed team observations remain separate.'),
]
KITCHEN_FIELDS = [
 ('11.1','Identity & provenance','Project, story, section, shot/take, parent revision and authority.'),
 ('11.2','Input manifest','Exact assets, hashes, bytes, roles and separate catalog / selection / human-review status.'),
 ('11.3','Inspiration','Panels and ideas; never silently treated as conditioning.'),
 ('11.4','Visible locks','What must match, what is hidden and what must not be forced into the frame.'),
 ('11.5','Cue, anchors & hold','Cue ID/revision/state, word/event/grid anchors, proposed hold, native length and trim rule.'),
 ('11.6','Audio & musical arc','Song, speech, ambience/effects, provider audio and score stay separate; musical change and visible consequence.'),
 ('11.7','Preserve / change / exclude','Allowed transformation, fixed details, exclusions and change class.'),
 ('11.8','Start / end / boundaries','Start state, end state, cut boundaries and nearby story context.'),
 ('11.9','Missing inputs & inherited defects','Known gaps, inherited issues and limits of current evidence.'),
 ('11.10','Prompt package','Prompt derived from this revision, repeated requirements and negatives.'),
 ('11.11','Review contract','Success checks, reviewer, evidence and relevant review fields.'),
 ('11.12','Ownership & route adapters','Writer preparation; operator binding, mode and cost; human choices; provider-specific handoff.'),
]

def sha(raw): return hashlib.sha256(raw).hexdigest()
def read(root, path): return (root/path).read_text(encoding='utf-8-sig')
def source(root, path, start=None, end=None):
    raw=(root/path).read_bytes()
    return dict(path=path,assetID=('lisan' if '/lisan_' in path else 'hon')+':doc:'+path,
                sha256=sha(raw),bytes=len(raw),line=start,endLine=end)

def shot_blocks(text):
    matches=list(re.finditer(r'^###\s+((?:S\d{2}|P|E)-[\w.]+)\b[^\n]*',text,re.M))
    return {m[1]:(text[m.start():matches[i+1].start() if i+1<len(matches) else len(text)],
                   text[:m.start()].count('\n')+1) for i,m in enumerate(matches)}

def numbered(block):
    """Read section bodies, never count a heading itself as filled content."""
    pattern=r'^(?:\*\*)?(\d+(?:\.\d+|b)?)[.]?\s*(?:\*\*)?\s*[^\n]*'
    entries=[]
    for m in re.finditer(pattern,block,re.M):
        key=m[1]
        if key not in {str(x) for x in range(12)}|{'7b'}|{x[0] for x in KITCHEN_FIELDS}: continue
        line=m[0]
        if re.match(r'^8\.\s+to\s+10',line): continue
        # Numeric headings use bold labels; 11.x sometimes has only a bold number.
        cut=line.rfind('**') if '**' in line else -1
        body=line[cut+2:].strip() if cut>=0 else ''
        entries.append((key,m.start(),m.end(),body))
    result={}
    for i,(key,start,end,body) in enumerate(entries):
        tail=block[end:entries[i+1][1] if i+1<len(entries) else len(block)]
        # The next shot is already split. Adapter/source prose stays evidence.
        result[key]=(body+tail).strip()
    return result

def bullets(block):
    rows={}
    for m in re.finditer(r'^- ([\w /-]+):\s*(.*)(?:\n(?![-#]|\s*$).*)*',block,re.M):
        rows[m[1].lower()]=m[0].split(':',1)[1].strip()
    return rows

def content_status(text, absent='unknown'):
    value=re.sub(r'[*`#]','',text).strip()
    if not value: return absent
    if re.match(r'^(?:none yet|not yet|missing|no start frame|no (?:accepted |prepared )?start(?:ing)? frame|tbd|to be (?:written|filled)|unwritten)\b',value,re.I): return 'missing'
    if re.match(r'^(?:none\b(?! yet)|not needed\b|not applicable\b|silence\b)',value,re.I): return 'not_needed'
    if re.fullmatch(r'(?:CFA Nova.?s.*|Ziggy.?s.*|\.{3}|\[.*\])',value,re.I): return absent
    return 'draft'

def field(key,text,evidence,*,status=None,note=''):
    return dict(key=key,text=text,status=status or content_status(text),evidence=evidence,note=note)

def build_hon(root,catalog):
    coverage=json.loads(read(root,MAP)); by_id={a['id']:a for a in catalog['assets']}
    paths=[WRITER+'OPENING_PACKET_20261028.md',KITCHEN+'S02_PACKET_20261029.md']
    blocks={}
    for path in paths:
        for sid,(block,line) in shot_blocks(read(root,path)).items(): blocks[sid]=(block,path,line)
    blocks['S01-1']=(read(root,KITCHEN+'EXAMPLE_S01-1_KITCHEN_BLOCK_20261029.md'),KITCHEN+'EXAMPLE_S01-1_KITCHEN_BLOCK_20261029.md',1)
    shots=[]
    for row in coverage['shots']:
        sid=row['shotID']; original=row.get('cardRepoPath')
        original_exists=bool(original and (root/original).is_file())
        if sid in blocks: block,path,line=blocks[sid]; structured=True
        else:
            block,line=shot_blocks(read(root,original)).get(sid,('',1)) if original_exists else ('',1)
            path=original if block else MAP; structured=False
        ev=source(root,path,line,line+block.count('\n')); map_ev=source(root,MAP)
        nums=numbered(block) if structured else {}; old=bullets(block)
        texts={
            'purpose':nums.get('0') or old.get('purpose') or row.get('purpose',''),
            'context':nums.get('11.8') or '\n'.join(filter(None,[old.get('start/end intent'),old.get('continuity'),row.get('transitionTo')])),
            'lineage':nums.get('1') or old.get('references',''),
            'references':nums.get('11.2') or old.get('references') or '\n'.join(row.get('otherReferences',[])),
            'lighting':nums.get('2') or old.get('lighting',''),
            'camera':nums.get('3') or old.get('camera',''),
            'character':nums.get('4') or old.get('direction',''),
            'background':nums.get('5',''), 'beats':nums.get('6',''),
            'prompt_still':nums.get('7',''), 'prompt_clip':nums.get('7b',''),
            'settings':'', 'results':'', 'acceptance':'',
        }
        # Section 7 is not always a still prompt. Preserve the writer's actual
        # type and explicit block instead of manufacturing an empty clip slot.
        prompt_heading=re.search(r'^7\.\s*\*\*(.*?)\*\*',block,re.M)
        if nums.get('7') and prompt_heading and 'still' not in prompt_heading[1].lower():
            texts['prompt_still']=''
            texts['prompt_clip']=nums.get('7b') or nums['7']
        if not texts['prompt_clip'] and content_status(nums.get('11.10',''))=='missing':
            texts['prompt_clip']=nums['11.10']
        cue=row.get('lyricCue')
        texts['cue']=nums.get('11.5') or (json.dumps(cue,ensure_ascii=False) if cue else '')
        texts['start_frame']=nums.get('1','') if re.search(r'\bno (?:\w+ )?start frame',nums.get('1',''),re.I) else ''
        fields=[field(k,texts.get(k,''),[ev if texts.get(k) else map_ev],status='draft' if k=='lineage' and texts.get(k) else None,
                      note='Prepared when this phase and the chosen mode require it.' if k in {'start_frame','settings'} else '') for k,*_ in FIELDS]
        if structured:
            for f in fields:
                if f['key'] in {'settings','results','acceptance'}: f['status']='unknown'; f['note']='No run / return / acceptance recorded by this writer packet. Not a writing defect.'
        materials=[]; seen=set()
        for item in row.get('originalPanels',[]):
            aid=item.get('assetID'); a=by_id.get(aid)
            if aid and aid not in seen:
                seen.add(aid); materials.append(dict(assetID=aid,role=item.get('role','inspiration'),availability='catalogued' if a else 'unresolved',note=item.get('note',''),source=map_ev))
        for aid in dict.fromkeys(re.findall(r'\b(?:HD|LAG|DJB|GEM|FLOW)-[A-Za-z0-9-]+',block)):
            if aid in by_id and aid not in seen:
                seen.add(aid); materials.append(dict(assetID=aid,role='named_reference',availability='catalogued',note='Named in writing; see the exact source for scope and role. Not automatically a starting frame.',source=ev))
        kitchen=[field(key,nums.get(key,''),[ev],status=content_status(nums.get(key,''),'missing')) for key,*_ in KITCHEN_FIELDS]
        parent=source(root,original) if original_exists else map_ev
        shot=dict(shotID=sid,sectionID=row['sectionID'],title=row['title'],stage='preliminary',
                  authoringStatus='Proposed detailed design' if block else 'Planned slot · card not written',fields=fields,kitchen=kitchen,materials=materials,
                  source=ev,parent=parent,coverageEvidence=map_ev,coverageAsOf='2026-10-28',
                  historicalArtState=row.get('artState'),missingArtReported=row.get('missingArt',[]),coverageUpdate=row.get('additionalCoverage',''),
                  sourceShotPlanIDs=row.get('shotPlanCandidateIDs',[]),settled=row.get('settled',[]),
                  revision='take 1' if structured else 'posted scene card' if block else 'unwritten',kitchenWritten=all(f['text'].strip() for f in kitchen),
                  dependencies=[ev,parent,map_ev],revisions=[])
        if sid=='S01-1':
            add=source(root,ADDENDUM)
            shot['revisions']=[dict(id='S01-1-take-2-proposed',status='draft',parent=ev,source=add,
                label='Proposed take 2 · grin pacing only',note='Addendum A proposes a later take. Take 1 and its prompt remain preserved; adoption and adapter refresh are not recorded.',needsReview=['prompt_clip','beats','cue'])]
            shot['dependencies'].append(add)
            for f in fields:
                if f['key'] in {'references','lineage'}:
                    f['note']="Addendum A supersedes the earlier unapproved-mouth wording: mouth B is the current scoped dental reference (dental_mouth_only). This does not approve a full scene or a prepared starting frame."
                    f['evidence'].append(add)
                if f['key']=='cue':
                    f['text']='Inherited fixed Hon master; EVT-HON-01 → EVT-HON-02 → TXT line 3. Master fixed; events proposed, not listened. The grin pacing revision remains proposed.'
                    f['evidence'].append(add)
            for f in kitchen:
                if f['key'] in {'11.2','11.5','11.9','11.12'}:
                    f['note']='Read Addendum A for the current correction: scoped mouth selection; Round M common prepared frame; Comfy still/motion split and actual observed settings. Earlier claims remain historical.'
                    f['evidence'].append(add)
        shot['unresolvedReferences']=[]
        if sid=='S02-8':
            named='SB-W04-S02-8-warship-v002.jpg'
            matches=[a for a in catalog['assets'] if a.get('filename','').lower()==named.lower()]
            for a in matches:
                if a['id'] not in seen: materials.append(dict(assetID=a['id'],role='named_reference',availability='catalogued',note='Matched by exact filename; still a staging candidate, not a selected starting frame.',source=ev))
            if not matches: shot['unresolvedReferences']=[named+' · mentioned by the writer; no exact catalog filename match established']
        shots.append(shot)
    assert len({s['shotID'] for s in shots})==len(shots), 'Duplicate authored shot ID'
    declared=[sid for section in coverage['sections'] for sid in section['shotIDs']]
    assert len(set(declared))==len(declared) and set(declared)=={s['shotID'] for s in shots}, 'Section/shot crosswalk differs'
    sections={sid:section['id'] for section in coverage['sections'] for sid in section['shotIDs']}
    assert all(s['sectionID']==sections[s['shotID']] for s in shots), 'Shot section differs'
    order={sid:i for i,sid in enumerate(sid for section in coverage['sections'] for sid in section['shotIDs'])}
    shots.sort(key=lambda shot:order[shot['shotID']])
    return dict(storyID='hon:strictly-business',project='hon',source=source(root,MAP),sections=coverage['sections'],shots=shots,
                note='Authored shots, independent of the 36 original panels. October 28 missing-art labels are dated writing evidence; current linked material is shown separately. No automatic production gate.')

def document_asset(root,path):
    raw=(root/path).read_bytes(); project='lisan' if '/lisan_' in path else 'hon'
    return dict(id=project+':doc:'+path,project=project,category='documents',album=project+':writer-structure',kind='document',
                title=read(root,path).splitlines()[0].lstrip('# ') if path.endswith('.md') else Path(path).stem,
                filename=Path(path).name,repoPath=path,src=os.path.relpath(root/path,root/(BASE+'visual_library')).replace('\\','/'),
                thumb='',sha256=sha(raw),bytes=len(raw),text=read(root,path),author='Claude',sourceProvider='Claude',
                sourceStatus='received_writer_proposal',tags=['Storyboard','Structure','Writer proposal'])

def apply_storyboard_structure(catalog,root,previous_structure=None):
    root=Path(root)
    # Verify the posted Oct29 attachment receipts rather than trusting a summary.
    mailbox=BASE+'collaborators/mailbox/messages/'
    for name in ['fea8015a-b15d-42e3-a698-c9f1575a975e.json','e01c86af-d096-4e81-8b55-22b185055ec7.json']:
        for attachment in json.loads(read(root,mailbox+name))['attachments']:
            raw=(root/attachment['path']).read_bytes()
            assert sha(raw)==attachment['sha256'] and len(raw)==attachment['bytes'],attachment['path']
    structure=build_hon(root,catalog)
    checkpoint=previous_structure if previous_structure is not None else catalog.get('storyboardStructure',{})
    previous=next((s for s in checkpoint.get('stories',[]) if s['storyID']==structure['storyID']),{})
    previous_shots={s['shotID']:s for s in previous.get('shots',[])}
    for shot in structure['shots']:
        prior=previous_shots.get(shot['shotID'])
        shot['dependencyReviewNeeded']=bool(prior and prior.get('dependencies')!=shot['dependencies']) or bool(prior and prior.get('dependencyReviewNeeded'))
        if shot['dependencyReviewNeeded']:
            shot['priorDependencyEvidence']=deepcopy(prior.get('priorDependencyEvidence') or prior['dependencies'])
    definitions=[dict(key=k,section=s,label=label,owner=owner,phase=phase,hint=hint) for k,s,label,owner,phase,hint in FIELDS]
    catalog['storyboardStructure']=dict(format='cfa-storyboard-structure-v1',updated='2026-10-29',fields=definitions,
        kitchenFields=[dict(key=k,label=label,hint=hint) for k,label,hint in KITCHEN_FIELDS],stories=[structure],
        template=dict(label='Blank storyboard / shot template',demonstration=True,source=source(root,TEMPLATE),
                      kitchenSource=source(root,SPEC),addendum=source(root,ADDENDUM)),
        rules=['Structure records never create reviews, production eligibility, exports or generation requests.',
               'Required inputs depend on phase and the chosen route; optional art and unchosen modes are not global blockers.',
               'Changed source hashes require reconciliation. Earlier takes, timing and reviews stay intact.'])
    base_card=json.loads(read(root,WRITER+'review_queue_20261028/MISSION_CONTROL_CARD_PROPOSED_hon-coverage-review-queue-20261028.json'))['task']
    delta=json.loads(read(root,KITCHEN+'MISSION_CONTROL_CARD_DELTA_PROPOSED_20261029_v2.json'))
    base_card['missing']+=delta['missingAppend']; base_card['links']+=delta['linksAppend']
    base_card['previewAssetIDs']=list(dict.fromkeys(base_card['previewAssetIDs']+delta['previewAssetIDsAppend']))
    base_card.update(title='Strictly Business · storyboard structure and author choices',
        direction='inbound',workKind='planning',
        groupingBasis='The received authored storyboard package awaits Ziggy author choices through Structure & gaps; it is not a generation request.',
        summary=f"{len(structure['shots'])} authored shots are now visible in Structure & gaps. Opening direction and ten S02 cards are written; {sum(s['kitchenWritten'] for s in structure['shots'])} shots carry documented kitchen blocks, including gaps. These are proposals, separate from your image reviews and production acceptance.",
        nextAction='Open Structure & gaps to inspect a sequence or a missing field. Answer the author choices when ready; no generation or dispatch is authorized by this card.',
        laterReview='The optional 30-panel sweep remains proposed and is not queued by this intake.',
        updatedAtUTC=delta['updatedAtUTC'],sourceDelta=source(root,KITCHEN+'MISSION_CONTROL_CARD_DELTA_PROPOSED_20261029_v2.json'))
    base_card['userAction']=dict(title='For you now',description='Browse written shots and gaps, including shots without images. Use the blank template to inspect every field.',
        links=[dict(label='Storyboard · Structure & gaps',project='hon',view='storyboard',album='structure:hon:strictly-business')])
    tasks=catalog['missionControl']['tasks']; current=next((t for t in tasks if t['id']==base_card['id']),None)
    if current is None: tasks.append(base_card)
    else:
        # Preserve any later human status/action records on a repeated adapter run.
        for key,value in base_card.items():
            if key not in {'status','userDecision','completedAt','sentAt'}: current[key]=value
    requests=json.loads(read(root,WRITER+'review_queue_20261028/REVIEW_REQUESTS_PROPOSED_PARKED4_20261028.json'))['requests']
    existing={r['id'] for r in catalog['reviewRequests']}; by_id={a['id']:a for a in catalog['assets']}
    for request in requests:
        assert by_id[request['id']]['sha256']==request['sha256']
        if request['id'] not in existing: catalog['reviewRequests'].append(request)
    paths={MAP,TEMPLATE,SPEC,ADDENDUM,WRITER+'OPENING_PACKET_20261028.md',WRITER+'COVERAGE_CROSSWALK_20261028.md',WRITER+'HANDBACK_20261028.md',
           WRITER+'review_queue_20261028/REVIEW_QUEUE_PACKAGE_20261028.md',KITCHEN+'EXAMPLE_S01-1_KITCHEN_BLOCK_20261029.md',
           KITCHEN+'IMPROVEMENT_ROUND_OPENING_20261029.md',KITCHEN+'S02_PACKET_20261029.md'}
    paths.update(s['source']['path'] for s in structure['shots']); paths.update(s['parent']['path'] for s in structure['shots'])
    ids=[]
    for path in sorted(paths):
        a=document_asset(root,path); ids.append(a['id'])
        if a['id'] not in by_id: catalog['assets'].append(a); by_id[a['id']]=a
        else: assert by_id[a['id']]['sha256']==a['sha256'], 'Posted source changed; reconcile separately: '+path
    hon_ids=[id for id in ids if id.startswith('hon:')]
    story=next(s for s in catalog['storyboardStories'] if s['id']=='hon:strictly-business')
    story['documentIDs']=list(dict.fromkeys(story['documentIDs']+hon_ids))
    project=next(p for p in catalog['writerDevelopment']['projects'] if p['id']=='hon')
    group=next((g for g in project['groups'] if g.get('id')=='coverage'),None)
    if group is None:
        group=dict(id='coverage',title='Coverage & shot structure · October 28–29',description='Writer proposals, source crosswalk and kitchen blocks; intake is not acceptance.',storyboard=True,documentIDs=[]); project['groups'].append(group)
    group['documentIDs']=list(dict.fromkeys(group['documentIDs']+hon_ids))
    # User-selected footage is linked after rebuilding authored shots. These
    # additive references do not rewrite the writer's fields or imply acceptance.
    from user_video_references import apply_user_video_references
    apply_user_video_references(catalog, root)
    return catalog['storyboardStructure']
