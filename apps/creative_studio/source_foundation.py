"""Read-only source maturity. Never writes a stage, selection, review or gate."""
from copy import deepcopy

LABELS={'detailed':'Detailed foundation','preliminary':'Preliminary foundation','unrecorded':'Maturity not recorded','no_frame':'No starting frame selected','from_scratch':'From scratch','not_required':'Not required','mixed':'Mixed input maturity','unresolved':'Unresolved input','changed':'Changed input · review dependencies'}
STAGES={'preliminary':'Preliminary','detailed_design':'Detailed design','verification':'Verification','production':'Production'}
ROLE_SCOPES={'start_frame':{'scene'},'source_frame':{'scene'},'source_video':{'scene'},'scene':{'scene'},'identity_reference':{'identity','complete_look'},'character_reference':{'identity','complete_look'},'outfit':{'outfit'},'dental_mouth_only':{'detail','dental_mouth_only'},'detail_reference':{'detail'},'tattoo':{'detail','tattoo'}}

def binding_key(binding):return ':'.join(str(binding.get(k,'')) for k in ['project','storyID','shotID'])

def checkpoint(bindings,assets,previous=None):
    """Compare persisted snapshots, including asset changes after rebinding."""
    by_id={a['id']:a for a in assets}; old={x['key']:x for x in (previous or {}).get('checkpoints',[])}; rows=[]
    for b in bindings:
        key=binding_key(b)
        signature={'binding':deepcopy(b),'resolved':[{k:by_id.get(i.get('assetID'),{}).get(k) for k in ['id','sha256','bytes']} for i in b.get('inputs',[])]}
        prior=old.get(key)
        changed=bool(prior and (prior['signature']!=signature or prior.get('dependencyReviewNeeded')))
        row={'key':key,'signature':signature,'dependencyReviewNeeded':changed}
        if changed:row['priorSignature']=deepcopy(prior.get('priorSignature',prior['signature']))
        rows.append(row)
    # Removing a selection also makes dependent evidence stale.
    for key,prior in old.items():
        if not any(r['key']==key for r in rows):rows.append({'key':key,'signature':{'binding':None,'resolved':[]},'dependencyReviewNeeded':True,'priorSignature':deepcopy(prior.get('priorSignature',prior['signature']))})
    return rows

def selected_binding(model,shot,project,story_id,scene_reviews=()):
    matches=[b for b in model.get('bindings',[]) if b.get('project')==project and b.get('storyID')==story_id and b.get('shotID')==shot['shotID']]
    # Only actual saved exact-shot start/source frame roles; never seed from art.
    def selection(b):
        return (b.get('mode'),sorted((str(i.get('role')),str(i.get('assetID')),str(i.get('sha256'))) for i in b.get('inputs',[]) if i.get('required') is True))
    for r in scene_reviews:
        if r.get('project')!=project or r.get('storyID')!=story_id or r.get('shotID')!=shot['shotID']:continue
        inputs=[deepcopy(i) for i in r.get('ingredients',[]) if i.get('kind')=='reference' and i.get('required') is True and i.get('role') in {'start_frame','source_frame'}]
        if inputs:
            b={'project':project,'storyID':story_id,'shotID':shot['shotID'],'mode':'first_frame','inputs':inputs,'evidence':{'source':'Saved exact-shot scene review','updatedAt':r.get('updatedAt')}}
            if not any(selection(m)==selection(b) for m in matches):matches.append(b)
    return matches

def derive(model,shot,project,story_id,assets,reviews=None,scene_reviews=()):
    by_id={a['id']:a for a in assets} if isinstance(assets,list) else assets;reviews=reviews or {}
    matches=selected_binding(model,shot,project,story_id,scene_reviews)
    key=binding_key({'project':project,'storyID':story_id,'shotID':shot['shotID']})
    prior=next((r for r in model.get('checkpoints',[]) if r['key']==key),None)
    current=checkpoint(matches,list(by_id.values()))
    stale=bool(prior and (prior.get('dependencyReviewNeeded') or len(current)!=1 or current[0]['signature']!=prior['signature']))
    result={'state':'no_frame','label':LABELS['no_frame'],'inputs':[],'notes':[],'dependencyReviewNeeded':stale,'bindingEvidence':None}
    def finish(state,note=''):
        result.update(state=state,label=LABELS[state])
        if note:result['notes'].append(note)
        if stale:result['notes'].append('Selected input changed since the recorded checkpoint. Dependent packs/checks need review; earlier decisions remain intact.')
        return result
    if not matches:return finish('no_frame','Linked references are not selected starting inputs.')
    if len(matches)!=1:return finish('unresolved','Conflicting selection records; no input chosen automatically.')
    b=matches[0];mode=b.get('mode');result['bindingEvidence']=b.get('evidence')
    if not b.get('evidence'):return finish('unresolved','Selection provenance is not recorded.')
    if mode in {'from_scratch','image_free'}:
        if any(i.get('required') for i in b.get('inputs',[])):return finish('unresolved','Image-free declaration conflicts with required media inputs.')
        return finish('from_scratch' if mode=='from_scratch' else 'not_required','Explicitly documented; not a quality failure or production gate.')
    if mode not in {'first_frame','ingredients','edit','extend'}:return finish('unresolved','Input mode is not recorded or supported by this display rule.')
    required=[i for i in b.get('inputs',[]) if i.get('required') is True]
    roles=[i.get('role') for i in required]
    if mode=='first_frame' and not any(r in {'start_frame','source_frame'} for r in roles):return finish('no_frame','No required scene starting frame is explicitly selected.')
    if not required:return finish('unresolved','Required inputs are not declared for this mode.')
    missing=[r for r in b.get('requiredRoles',[]) if r not in roles]
    if missing:result['notes'].append('Missing required roles: '+', '.join(missing))
    if mode=='extend' and 'source_video' not in roles:
        missing.append('source_video');result['notes'].append('Extend source video is not selected.')
    if mode=='edit' and not any(r in {'source_frame','start_frame','source_video'} for r in roles):
        missing.append('edit_source');result['notes'].append('Edit source still or video is not selected.')
    if mode=='first_frame' and sum(r in {'start_frame','source_frame'} for r in roles)>1:missing.append('conflicting_start_frames');result['notes'].append('More than one starting frame is marked required.')
    for i in required:
        a=by_id.get(i.get('assetID'));r=reviews.get(i.get('assetID'),{})
        if a and r.get('sha256')!=a.get('sha256'):r={}
        stage=r.get('storyboardStage') or (a or {}).get('storyboardStage')
        scope=r.get('workingReferenceScope') or (r.get('workingReference') or {}).get('scope') or (a or {}).get('workingReferenceScope') or ((a or {}).get('workingReference') or {}).get('scope') or (a or {}).get('defaultReferenceScope') or (a or {}).get('referenceScope')
        locks={c.get('scope') for c in (a or {}).get('componentApprovals',[]) if c.get('sourceSHA256')==(a or {}).get('sha256') and c.get('status')=='user_selected_component'}
        if not scope and len(locks)==1:scope=next(iter(locks))
        row={'assetID':i.get('assetID'),'role':i.get('role'),'stage':stage if stage in STAGES else None,'scope':scope or None,'expectedSHA256':i.get('sha256'),'actualSHA256':(a or {}).get('sha256'),'bytes':(a or {}).get('bytes'),'state':'unrecorded','notes':[],'stageSource':'Exact-hash review' if r.get('storyboardStage') else 'Asset metadata' if (a or {}).get('storyboardStage') else 'Not recorded'}
        if not a:row.update(state='unresolved');row['notes'].append('Selected asset is missing.')
        elif not i.get('sha256'):row.update(state='unresolved');row['notes'].append('Selection hash is not recorded.')
        elif i['sha256']!=a.get('sha256') or (i.get('bytes') is not None and i['bytes']!=a.get('bytes')):
            row.update(state='changed');row['notes'].append('Selected file changed; dependent checks are stale.');result['dependencyReviewNeeded']=True
        elif not stage and not scope:row['notes'].append('Maturity and review scope are not recorded.')
        elif i.get('role') not in ROLE_SCOPES or scope not in ROLE_SCOPES[i['role']]:
            row.update(state='unresolved');row['notes'].append('Scope does not establish maturity for this input role; scene use is unassessed.' if scope else 'Review scope is not recorded for this input role.')
        elif i.get('role') in {'start_frame','source_frame'} and a.get('kind')!='image':row.update(state='unresolved');row['notes'].append('Starting input is not an image.')
        elif i.get('role')=='source_video' and a.get('kind')!='video':row.update(state='unresolved');row['notes'].append('Source-video input is not a video.')
        elif stage=='preliminary':row['state']='preliminary'
        elif stage in {'detailed_design','verification','production'}:row['state']='detailed'
        for note in [i.get('note'),(a or {}).get('knownDifferences'),r.get('note')]:
            if note:row['notes'].append(str(note))
        if r.get('status'):row['notes'].append('Recorded disposition: '+r['status'].replace('_',' '))
        if r.get('collectionState')=='archived':row['notes'].append('Source is archived.')
        result['inputs'].append(row)
    states={r['state'] for r in result['inputs']}
    if 'changed' in states:return finish('changed')
    if missing or 'unresolved' in states:return finish('unresolved')
    if len(states)>1:return finish('mixed','Required inputs retain their own maturity and scope; no maximum-stage promotion.')
    return finish(next(iter(states)))
