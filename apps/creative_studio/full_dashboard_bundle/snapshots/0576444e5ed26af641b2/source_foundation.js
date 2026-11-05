/* Read-only source maturity. No stage, selection, review or production gate is written. */
(function(root,factory){
  'use strict';
  const api=factory();
  if(typeof module==='object'&&module.exports)module.exports=api;
  if(root)root.CFA_SOURCE_FOUNDATION=api;
})(typeof window!=='undefined'?window:null,function(){
  'use strict';
  const LABELS={detailed:'Detailed foundation',preliminary:'Preliminary foundation',unrecorded:'Maturity not recorded',no_frame:'No starting frame selected',from_scratch:'From scratch',not_required:'Not required',mixed:'Mixed input maturity',unresolved:'Unresolved input',changed:'Changed input · review dependencies'};
  const STAGES={preliminary:'Preliminary',detailed_design:'Detailed design',verification:'Verification',production:'Production'};
  const ROLE_SCOPES={start_frame:['scene'],source_frame:['scene'],source_video:['scene'],scene:['scene'],identity_reference:['identity','complete_look'],character_reference:['identity','complete_look'],outfit:['outfit'],dental_mouth_only:['detail','dental_mouth_only'],detail_reference:['detail'],tattoo:['detail','tattoo']};
  const copy=value=>JSON.parse(JSON.stringify(value));
  const list=value=>Array.isArray(value)?value:[];
  const present=value=>Boolean(value)&&(!(typeof value==='object')||Object.keys(value).length>0);
  const assetMap=assets=>assets instanceof Map?assets:new Map(Array.isArray(assets)?assets.map(a=>[a.id,a]):Object.entries(assets||{}));
  const reviewAt=(reviews,id)=>reviews instanceof Map?reviews.get(id)||{}:reviews?.[id]||{};
  const bindingKey=binding=>['project','storyID','shotID'].map(k=>String(binding[k]??'')).join(':');
  function same(left,right){
    if(left===right)return true;
    if(left===null||right===null||typeof left!=='object'||typeof right!=='object'||Array.isArray(left)!==Array.isArray(right))return false;
    const keys=Object.keys(left),other=Object.keys(right);
    return keys.length===other.length&&keys.every(k=>Object.prototype.hasOwnProperty.call(right,k)&&same(left[k],right[k]));
  }
  function checkpoint(bindings,assets,previous=null){
    const byID=assetMap(assets),old=new Map(list(previous?.checkpoints).map(row=>[row.key,row])),rows=[];
    for(const binding of list(bindings)){
      const key=bindingKey(binding),signature={binding:copy(binding),resolved:list(binding.inputs).map(input=>{
        const asset=byID.get(input.assetID)||{};
        return {id:asset.id??null,sha256:asset.sha256??null,bytes:asset.bytes??null};
      })};
      const prior=old.get(key),changed=Boolean(prior&&(!same(prior.signature,signature)||prior.dependencyReviewNeeded));
      const row={key,signature,dependencyReviewNeeded:changed};
      if(changed)row.priorSignature=copy(prior.priorSignature??prior.signature);
      rows.push(row);
    }
    // Removing a selection also makes dependent evidence stale.
    for(const [key,prior] of old){
      if(!rows.some(row=>row.key===key))rows.push({key,signature:{binding:null,resolved:[]},dependencyReviewNeeded:true,priorSignature:copy(prior.priorSignature??prior.signature)});
    }
    return rows;
  }
  function selectedBinding(model,shot,project,storyID,sceneReviews=[]){
    const matches=list(model.bindings).filter(binding=>binding.project===project&&binding.storyID===storyID&&binding.shotID===shot.shotID);
    // Saved exact-shot start/source roles are eligible. Linked artwork is never a selection.
    const text=value=>value==null?'None':value===true?'True':value===false?'False':String(value);
    const compare=(left,right)=>{for(let i=0;i<left.length;i++){if(left[i]!==right[i])return left[i]<right[i]?-1:1;}return 0;};
    const selection=binding=>[binding.mode??null,list(binding.inputs).filter(input=>input.required===true).map(input=>[text(input.role),text(input.assetID),text(input.sha256)]).sort(compare)];
    for(const review of list(sceneReviews)){
      if(review.project!==project||review.storyID!==storyID||review.shotID!==shot.shotID)continue;
      const inputs=list(review.ingredients).filter(input=>input.kind==='reference'&&input.required===true&&['start_frame','source_frame'].includes(input.role)).map(copy);
      if(inputs.length){
        const binding={project,storyID,shotID:shot.shotID,mode:'first_frame',inputs,evidence:{source:'Saved exact-shot scene review',updatedAt:review.updatedAt??null}};
        if(!matches.some(match=>same(selection(match),selection(binding))))matches.push(binding);
      }
    }
    return matches;
  }
  function derive(model,shot,project,storyID,assets,reviews={},sceneReviews=[]){
    const byID=assetMap(assets),matches=selectedBinding(model,shot,project,storyID,sceneReviews);
    const key=bindingKey({project,storyID,shotID:shot.shotID});
    const prior=list(model.checkpoints).find(row=>row.key===key),current=checkpoint(matches,[...byID.values()]);
    const stale=Boolean(prior&&(prior.dependencyReviewNeeded||current.length!==1||!same(current[0].signature,prior.signature)));
    const result={state:'no_frame',label:LABELS.no_frame,inputs:[],notes:[],dependencyReviewNeeded:stale,bindingEvidence:null};
    function finish(state,note=''){
      result.state=state;result.label=LABELS[state];
      if(note)result.notes.push(note);
      if(stale)result.notes.push('Selected input changed since the recorded checkpoint. Dependent packs/checks need review; earlier decisions remain intact.');
      return result;
    }
    if(!matches.length)return finish('no_frame','Linked references are not selected starting inputs.');
    if(matches.length!==1)return finish('unresolved','Conflicting selection records; no input chosen automatically.');
    const binding=matches[0],mode=binding.mode;
    result.bindingEvidence=binding.evidence??null;
    if(!present(binding.evidence))return finish('unresolved','Selection provenance is not recorded.');
    if(['from_scratch','image_free'].includes(mode)){
      if(list(binding.inputs).some(input=>present(input.required)))return finish('unresolved','Image-free declaration conflicts with required media inputs.');
      return finish(mode==='from_scratch'?'from_scratch':'not_required','Explicitly documented; not a quality failure or production gate.');
    }
    if(!['first_frame','ingredients','edit','extend'].includes(mode))return finish('unresolved','Input mode is not recorded or supported by this display rule.');
    const required=list(binding.inputs).filter(input=>input.required===true),roles=required.map(input=>input.role);
    if(mode==='first_frame'&&!roles.some(role=>['start_frame','source_frame'].includes(role)))return finish('no_frame','No required scene starting frame is explicitly selected.');
    if(!required.length)return finish('unresolved','Required inputs are not declared for this mode.');
    const missing=list(binding.requiredRoles).filter(role=>!roles.includes(role));
    if(missing.length)result.notes.push('Missing required roles: '+missing.join(', '));
    if(mode==='extend'&&!roles.includes('source_video')){missing.push('source_video');result.notes.push('Extend source video is not selected.');}
    if(mode==='edit'&&!roles.some(role=>['source_frame','start_frame','source_video'].includes(role))){missing.push('edit_source');result.notes.push('Edit source still or video is not selected.');}
    if(mode==='first_frame'&&roles.filter(role=>['start_frame','source_frame'].includes(role)).length>1){missing.push('conflicting_start_frames');result.notes.push('More than one starting frame is marked required.');}
    for(const input of required){
      const asset=byID.get(input.assetID);
      let review=reviewAt(reviews,input.assetID);
      if(asset&&(review.sha256??null)!==(asset.sha256??null))review={};
      const stage=review.storyboardStage||asset?.storyboardStage;
      let scope=review.workingReferenceScope||review.workingReference?.scope||asset?.workingReferenceScope||asset?.workingReference?.scope||asset?.defaultReferenceScope||asset?.referenceScope;
      const locks=new Set(list(asset?.componentApprovals).filter(approval=>(approval.sourceSHA256??null)===(asset?.sha256??null)&&approval.status==='user_selected_component').map(approval=>approval.scope??null));
      if(!scope&&locks.size===1)scope=locks.values().next().value;
      const row={assetID:input.assetID??null,role:input.role??null,stage:Object.hasOwn(STAGES,stage)?stage:null,scope:scope||null,expectedSHA256:input.sha256??null,actualSHA256:asset?.sha256??null,bytes:asset?.bytes??null,state:'unrecorded',notes:[],stageSource:review.storyboardStage?'Exact-hash review':asset?.storyboardStage?'Asset metadata':'Not recorded'};
      if(!asset){row.state='unresolved';row.notes.push('Selected asset is missing.');}
      else if(!input.sha256){row.state='unresolved';row.notes.push('Selection hash is not recorded.');}
      else if(input.sha256!==asset.sha256||(input.bytes!=null&&input.bytes!==asset.bytes)){
        row.state='changed';row.notes.push('Selected file changed; dependent checks are stale.');result.dependencyReviewNeeded=true;
      }else if(!stage&&!scope){
        row.notes.push('Maturity and review scope are not recorded.');
      }else if(!Object.hasOwn(ROLE_SCOPES,input.role)||!ROLE_SCOPES[input.role].includes(scope)){
        row.state='unresolved';row.notes.push(scope?'Scope does not establish maturity for this input role; scene use is unassessed.':'Review scope is not recorded for this input role.');
      }else if(['start_frame','source_frame'].includes(input.role)&&asset.kind!=='image'){
        row.state='unresolved';row.notes.push('Starting input is not an image.');
      }else if(input.role==='source_video'&&asset.kind!=='video'){
        row.state='unresolved';row.notes.push('Source-video input is not a video.');
      }else if(stage==='preliminary')row.state='preliminary';
      else if(['detailed_design','verification','production'].includes(stage))row.state='detailed';
      for(const note of [input.note,asset?.knownDifferences,review.note])if(note)row.notes.push(String(note));
      if(review.status)row.notes.push('Recorded disposition: '+review.status.replaceAll('_',' '));
      if(review.collectionState==='archived')row.notes.push('Source is archived.');
      result.inputs.push(row);
    }
    const states=new Set(result.inputs.map(input=>input.state));
    if(states.has('changed'))return finish('changed');
    if(missing.length||states.has('unresolved'))return finish('unresolved');
    if(states.size>1)return finish('mixed','Required inputs retain their own maturity and scope; no maximum-stage promotion.');
    return finish(states.values().next().value);
  }
  return {derive,checkpoint,selectedBinding,bindingKey,LABELS,STAGES,ROLE_SCOPES};
});
