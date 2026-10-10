(() => {
  'use strict';
  const base = new URL('.', document.currentScript.src);
  const C = window.REVIEW_CATALOG;
  const byID = new Map(C.assets.map(a => [a.id, a]));
  const cats = Object.fromEntries(C.categories);
  const esc = v => String(v ?? '').replace(/[&<>"']/g, x => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[x]));
  const href = p => new URL(p, base).href;
  const isDoc = a => ['document','pdf'].includes(a.kind);
  const initial = window.REVIEW_INITIAL || {project:'hon', view:'all'};
  let state = {...initial, view:location.hash?initial.view:'mission_control', album:'', search:'', destination:'all', videoSort:'longest', videoLayout:'grouped', outfitLayout:'compact', collaborator:'ComfyUI',exportIntent:'prime',detailLayout:'approved',detailProfile:'',storyTheme:'all',storyStage:'all',storyStart:0,storyEnd:100}, currentID = '', displayed = [], toastTimer;
  const expandedOutfits = new Set();
  const expandedCollections = new Set();
  const collapsedBrowseBuckets = new Set();
  const REVIEW_KEY = 'cfa-visual-review-v1', EXPORT_KEY = 'cfa-visual-export-v1';
  const statusLabels = {keep:'Keep', needs_fixes:'Needs fixes', remove:'Marked for removal'};
  const workingScopes={complete_look:'Complete look',identity:'Identity',outfit:'Outfit',scene:'Scene',detail:'Detail only'};
  const storyboardStages={preliminary:'Preliminary',detailed_design:'Detailed design',verification:'Verification',production:'Production'};
  const bomDefinitions=C.characterBOM?.characters||[];
  const bomRoles=new Map(bomDefinitions.flatMap(c=>(c.entries||[]).map(e=>[e.assetID,e])));
  const referencePolicyPath=C.characterBOM?.policyPath||'docs/notes/explorable_world/comfy/projects/visual_library/REFERENCE_POLICY.txt';
  const referencePolicyText='An explicitly named reference is used for that scene only. Other scenes start from canonical scoped gold standards and the highest-rated suitable approved Prime references. A scene image does not replace identity; likeness is rated only against the gold standard for the recorded role.';
  const normalizedRating=value=>Number.isInteger(value)&&value>=1&&value<=5?value:null;
  let favorites = new Set(), basket = new Set(), storageOK = true, reviews = new Map(), sceneReviews = new Map();
  let reviewFileHandle = null, fileSaveTimer, fileWriteChain = Promise.resolve();
  let reviewRevision = 0, fileSavedRevision = 0, fileWriting = false;
  let fileMessage = 'Browser backup only · choose Save review file or export for Nova’s next sweep. Changes do not notify Nova automatically.';
  function matchingAsset(item) {
    if (!item || typeof item !== 'object' || typeof item.id !== 'string') return null;
    const a = byID.get(item.id);
    return a && (!item.sha256 || item.sha256 === a.sha256) ? a : null;
  }
  const destinations = ['undecided','Gemini','Flow','Grok'];
  function normalizedPlan(plan){
    if(!plan||typeof plan!=='object')return null;
    let targets=Array.isArray(plan.destinations)?[...new Set(plan.destinations.filter(d=>destinations.includes(d)))]:[];
    if(targets.length>1)targets=targets.filter(d=>d!=='undecided');if(!targets.length)targets=['undecided'];
    return {status:'planned',destinations:targets,idea:typeof plan.idea==='string'?plan.idea.slice(0,20000):'',prompt:typeof plan.prompt==='string'?plan.prompt.slice(0,30000):'',...(Array.isArray(plan.sceneIDs)?{sceneIDs:[...new Set(plan.sceneIDs.filter(id=>typeof id==='string'&&(C.shotMaterials?.shots||[]).some(shot=>shot.id===id)))]}:{})};
  }
  // Scene readiness is a separate human review. Available source files do not prove a finished scene.
  function normalizedShootPlan(plan){const p=plan&&typeof plan==='object'?plan:{};return {direction:typeof p.direction==='string'?p.direction.slice(0,12000):'',camera:typeof p.camera==='string'?p.camera.slice(0,12000):'',lighting:typeof p.lighting==='string'?p.lighting.slice(0,12000):'',reviewStatus:['unreviewed','needs_fixes','verified'].includes(p.reviewStatus)?p.reviewStatus:'unreviewed',reviewedBy:typeof p.reviewedBy==='string'?p.reviewedBy.slice(0,300):'',reviewedAt:typeof p.reviewedAt==='string'&&!Number.isNaN(Date.parse(p.reviewedAt))?p.reviewedAt:null,note:typeof p.note==='string'?p.note.slice(0,6000):''};}
  function normalizedSceneReview(item){
    if(!item||typeof item!=='object'||!(C.shotMaterials?.shots||[]).some(s=>s.project===item.project&&s.id===item.shotID))return null;
    const ingredients=Array.isArray(item.ingredients)?item.ingredients.slice(0,80).filter(i=>i&&typeof i==='object'&&typeof i.id==='string').map(i=>({id:i.id.slice(0,180),label:typeof i.label==='string'?i.label.slice(0,300):'Unnamed ingredient',role:typeof i.role==='string'?i.role.slice(0,180):'scene_detail',kind:i.kind==='criterion'?'criterion':'reference',required:i.required===true,status:['unreviewed','ready','needs_fixes','missing'].includes(i.status)?i.status:'unreviewed',assetID:typeof i.assetID==='string'?i.assetID:null,sha256:typeof i.sha256==='string'?i.sha256:null,note:typeof i.note==='string'?i.note.slice(0,6000):''})):[];
    return {project:item.project,shotID:item.shotID,grade:['A','B','C','D','F'].includes(item.grade)?item.grade:null,note:typeof item.note==='string'?item.note.slice(0,12000):'',criticalBlockers:Array.isArray(item.criticalBlockers)?item.criticalBlockers.filter(v=>typeof v==='string'&&v.trim()).map(v=>v.trim().slice(0,1000)).slice(0,40):[],ingredients,shootPlan:normalizedShootPlan(item.shootPlan),updatedAt:typeof item.updatedAt==='string'?item.updatedAt:null};
  }
  function sceneReviewRecord(project,shotID){
    const saved=sceneReviews.get(project+':'+shotID);if(saved)return saved;
    const shot=(C.shotMaterials?.shots||[]).find(s=>s.project===project&&s.id===shotID);if(!shot)return null;
    return {project,shotID,grade:null,note:'',criticalBlockers:[],ingredients:(shot.materials||[]).map((m,i)=>({id:'material:'+i+':'+(m.assetID||'missing'),label:byID.get(m.assetID)?.title||String(m.role||'Missing reference').replace(/_/g,' '),role:m.role||'scene_detail',kind:'reference',required:false,status:'unreviewed',assetID:m.assetID||null,sha256:m.sha256||byID.get(m.assetID)?.sha256||null,note:''})),shootPlan:normalizedShootPlan(null),updatedAt:null};
  }
  function sceneHandoffGate(record){
    const reasons=[];if(!record)return {productionEligible:false,targetGrade:'B or better',reasons:['Scene review is not linked.']};
    if(!['A','B'].includes(record.grade))reasons.push('Scene grade must be A or B.');
    const shoot=normalizedShootPlan(record.shootPlan);if(shoot.reviewStatus!=='verified')reasons.push('Shoot plan needs verification.');
    if(!shoot.direction.trim()||!shoot.camera.trim()||!shoot.lighting.trim())reasons.push('Complete direction, camera and lighting instructions.');
    if(!shoot.reviewedBy.trim()||!shoot.reviewedAt)reasons.push('Record who verified the shoot plan and when.');
    if(record.criticalBlockers.length)reasons.push(...record.criticalBlockers.map(b=>'Critical blocker: '+b));
    const required=record.ingredients.filter(i=>i.required);if(!required.length)reasons.push('Select and review the required ingredients.');
    for(const i of required){
      if(i.status!=='ready')reasons.push(i.label+': '+String(i.status||'unreviewed').replace(/_/g,' '));
      if(i.kind==='criterion'){if(i.status==='ready'&&!i.note.trim())reasons.push(i.label+': add the evidence for this check.');continue;}
      const a=byID.get(i.assetID);if(!a)reasons.push(i.label+': reference is missing.');
      else if(!normalVisible(a))reasons.push(i.label+': reference is archived or marked for removal.');
      else if(!i.sha256||i.sha256!==a.sha256)reasons.push(i.label+': reference hash does not match.');
    }
    return {productionEligible:reasons.length===0,targetGrade:'B or better',reasons};
  }
  function updateSceneReview(project,shotID,patch,redraw=true){
    const prior=sceneReviewRecord(project,shotID);if(!prior)return;
    const next={...prior,...patch,shootPlan:normalizedShootPlan({...prior.shootPlan,...patch.shootPlan})};
    const planChanged=['direction','camera','lighting','reviewedBy'].some(field=>next.shootPlan[field]!==prior.shootPlan[field]);
    const requiredSignature=ingredients=>JSON.stringify(ingredients.filter(i=>i.required).map(i=>[i.id,i.kind,i.role,i.assetID,i.sha256]).sort((a,b)=>String(a[0]).localeCompare(String(b[0]))));
    const bindingChanged=requiredSignature(next.ingredients)!==requiredSignature(prior.ingredients);
    const explicitFreshReview=patch.shootPlan?.reviewStatus==='verified'&&patch.shootPlan?.reviewedAt&&patch.shootPlan.reviewedAt!==prior.shootPlan.reviewedAt;
    if((planChanged||bindingChanged)&&!explicitFreshReview){next.shootPlan.reviewStatus='unreviewed';next.shootPlan.reviewedAt=null;}
    const record=normalizedSceneReview({...next,project,shotID,updatedAt:new Date().toISOString()});if(!record)return;
    sceneReviews.set(project+':'+shotID,record);reviewRevision++;saveBrowserReview();scheduleFileSave();
    if(redraw){renderMain();if(currentID&&dialog.open)openViewer(currentID);}
    document.querySelectorAll('.scene-readiness').forEach(panel=>{const identity=panel.querySelector('[data-scene-id]');if(identity?.dataset.sceneProject===project&&identity.dataset.sceneId===shotID){const status=panel.querySelector('[data-shoot-field="reviewStatus"]');if(status)status.value=record.shootPlan.reviewStatus;const time=panel.querySelector('[data-shoot-review-time]');if(time)time.textContent=record.shootPlan.reviewedAt?'Review recorded: '+record.shootPlan.reviewedAt:'No shoot plan verification recorded.';}});
    document.querySelectorAll('[data-scene-gate]').forEach(node=>{if(node.dataset.sceneGate===project+':'+shotID)node.textContent=sceneHandoffGate(record).productionEligible?'Meets B-or-better scene target; final result acceptance is separate.':'Planning / repair: '+sceneHandoffGate(record).reasons.join(' ');});
  }
  function normalizedReview(item, origin='import') {
    const a = matchingAsset(item);
    if (!a || (a.sha256 && item.sha256 !== a.sha256) || !(item.status == null || Object.hasOwn(statusLabels,item.status))) return null;
    const record={id:a.id,sha256:a.sha256||null,origin:item.origin||origin};
    if(Object.hasOwn(item,'status'))record.status=item.status||null;
    if(Object.hasOwn(item,'note'))record.note=typeof item.note==='string'?item.note.slice(0,20000):'';
    if(Object.hasOwn(item,'updatedAt'))record.updatedAt=typeof item.updatedAt==='string'?item.updatedAt:null;
    if(Object.hasOwn(item,'shotPlan'))record.shotPlan=normalizedPlan(item.shotPlan);
    if(['prime','multiverse'].includes(item.variant)&&(origin==='catalog'||(item.variantSource!=='catalog'&&item.origin!=='catalog'))){record.variant=item.variant;record.variantSource=origin==='catalog'?'catalog':'user';}
    if(Object.hasOwn(item,'workingReference'))record.workingReference=normalizedWorkingReference(item.workingReference);
    if(isWorkingScope(item.workingReferenceScope))record.workingReferenceScope=item.workingReferenceScope;
    if(Object.hasOwn(item,'storyboardStage'))record.storyboardStage=Object.hasOwn(storyboardStages,item.storyboardStage)?item.storyboardStage:null;
    if(Object.hasOwn(item,'likenessRating'))record.likenessRating=normalizedRating(item.likenessRating);
    return record;
  }
  function isWorkingScope(value){return typeof value==='string'&&Object.hasOwn(workingScopes,value);}
  function normalizedWorkingReference(value){return value&&['requested','approved'].includes(value.status)&&isWorkingScope(value.scope)?{status:value.status,scope:value.scope}:null;}
  // The saved dropdown choice is independent of a requested or approved reference.
  function selectedWorkingScope(record){return isWorkingScope(record.workingReferenceScope)?record.workingReferenceScope:record.workingReference?.scope||'complete_look';}
  function mergeReview(record){const merged={status:null,note:'',shotPlan:null,...reviews.get(record.id),...record};if(merged.variant==='multiverse')merged.workingReference=null;reviews.set(record.id,merged);}
  for (const item of C.reviewDecisions || []) {
    const record = normalizedReview(item,'catalog'); if(record)mergeReview(record);
  }
  for(const item of C.sceneReviews||[]){const record=normalizedSceneReview(item);if(record)sceneReviews.set(record.project+':'+record.shotID,record);}
  try {
    const saved = JSON.parse(localStorage.getItem(REVIEW_KEY) || 'null');
    if(saved?.format===REVIEW_KEY && Array.isArray(saved.items)) {
      for(const item of saved.items){const record=normalizedReview(item,'browser');if(record)mergeReview(record);}
      for(const item of saved.sceneReviews||[]){const record=normalizedSceneReview(item);if(record)sceneReviews.set(record.project+':'+record.shotID,record);}
    }
  } catch {storageOK=false;}

  try { const saved=JSON.parse(localStorage.getItem('cfa-visual-favorites-v1') || '[]'); if(Array.isArray(saved))favorites=new Set(saved.filter(id=>byID.has(id))); } catch {storageOK=false;}
  try{const saved=JSON.parse(localStorage.getItem(EXPORT_KEY)||'null');if(saved?.format===EXPORT_KEY&&Array.isArray(saved.items)){for(const item of saved.items){const a=matchingAsset(item);if(a&&(!a.sha256||item.sha256===a.sha256))basket.add(a.id);}}}catch{storageOK=false;}
  const iconStar = id => favorites.has(id) ? '★' : '☆';
  function notice(message) {let t=document.querySelector('.toast');if(!t){t=document.createElement('div');t.className='toast';t.setAttribute('role','status');document.body.append(t);}t.textContent=message;clearTimeout(toastTimer);toastTimer=setTimeout(()=>t.remove(),3500);}
  function assetReference(a){return {id:a.id,project:a.project,filename:a.filename,path:a.repoPath,sha256:a.sha256||null,role:a.category};}
  function exportAllowed(a){const r=reviewRecord(a.id);return !a.archived&&r.status!=='remove'&&(state.exportIntent==='multiverse_ingredients'||r.variant!=='multiverse');}
  function exportReference(a){const r=reviewRecord(a.id);return {...assetReference(a),variant:r.variant||'prime',workingReference:r.workingReference||null,...(isWorkingScope(r.workingReferenceScope)?{workingReferenceScope:r.workingReferenceScope}:{}),...(a.componentApprovals?.length?{componentApprovals:a.componentApprovals}:{}),referenceRole:effectiveReferenceRole(a),storyboardStage:storyboardStage(a),likenessRating:normalizedRating(r.likenessRating),note:r.note||'',knownDifferences:[bomRoles.get(a.id)?.knownDifferences,r.note].filter(Boolean).join(' '),referenceUsePolicy:referenceUsePolicy(a)};}
  function exportIntentControls(){return `<label class="export-intent">Export intent<select data-export-intent><option value="prime" ${state.exportIntent==='prime'?'selected':''}>Prime references</option><option value="multiverse_ingredients" ${state.exportIntent==='multiverse_ingredients'?'selected':''}>Multiverse creative ingredients</option></select></label><p class="export-intent-help">${state.exportIntent==='prime'?'Multiverse ideas and removal requests stay out of exports.':'Multiverse ideas may be included as creative ingredients; removal requests still stay out.'} Review backups keep everything.</p>`;}
  function reviewPayload(){return {format:REVIEW_KEY,exported:new Date().toISOString(),
    status:'review decisions and notes; removal is a queue, not a file deletion',
    items:[...reviews.values()].map(record=>({...assetReference(byID.get(record.id)),...record})),
    sceneReviews:[...sceneReviews.values()],
    favorites:[...favorites].map(id=>byID.get(id)).filter(Boolean).map(assetReference),
    exportBasket:[...basket].map(id=>byID.get(id)).filter(Boolean).map(assetReference)};}
  function fileStatus(message){fileMessage=message;document.querySelectorAll('[data-review-file-status]').forEach(e=>e.textContent=message);}
  function saveBrowserReview(){
    try {localStorage.setItem(REVIEW_KEY,JSON.stringify(reviewPayload()));localStorage.setItem('cfa-visual-favorites-v1',JSON.stringify([...favorites]));localStorage.setItem(EXPORT_KEY,JSON.stringify(basketPayload(true)));storageOK=true;}
    catch {storageOK=false;fileStatus('Browser backup unavailable. Export review to keep this session.');notice('Browser storage unavailable. Export review to keep your decisions.');}
  }
  function saveFavorites(){saveBrowserReview();reviewRevision++;scheduleFileSave();}
  function scheduleFileSave(){
    if(!reviewFileHandle)return;
    fileStatus(storageOK?'Changes saved in this browser · saving review file…':'Saving review file… browser backup unavailable.');
    clearTimeout(fileSaveTimer);fileSaveTimer=setTimeout(()=>{fileSaveTimer=null;writeReviewFile();},450);
  }
  function writeReviewFile(){
    const handle=reviewFileHandle;if(!handle)return Promise.resolve(false);
    const perform=async()=>{
      if(handle!==reviewFileHandle)return false;
      const revision=reviewRevision, contents=JSON.stringify(reviewPayload(),null,2);fileWriting=true;
      try {
        const writable=await handle.createWritable();
        try{await writable.write(contents);await writable.close();}catch(error){try{await writable.abort();}catch{}throw error;}
        if(handle===reviewFileHandle){fileSavedRevision=revision;fileStatus('Saved to '+handle.name+' · autosave on for this open page.');}
        return true;
      } catch {
        if(handle===reviewFileHandle)reviewFileHandle=null;
        fileStatus((storageOK?'Browser backup kept. ':'')+'File save unavailable; use Export review.');
        notice('Could not write the review file. Use Export review; your current choices remain in this page.');return false;
      } finally {fileWriting=false;}
    };
    fileWriteChain=fileWriteChain.then(perform,perform);return fileWriteChain;
  }
  async function chooseReviewFile(){
    if(typeof window.showSaveFilePicker!=='function'){
      fileStatus('This browser needs Export review. Save the download in docs/notes/downloads for the next review sweep.');
      exportReview();return;
    }
    try {
      const handle=await window.showSaveFilePicker({suggestedName:'cfa-review.json',types:[{description:'CFA review JSON',accept:{'application/json':['.json']}}]});
      reviewFileHandle=handle;clearTimeout(fileSaveTimer);fileSaveTimer=null;
      fileStatus('Saving chosen review file…');await writeReviewFile();
    } catch(error) {
      if(error?.name==='AbortError'){notice('No review file chosen. Your current review remains in this page; Export review is available.');return;}
      reviewFileHandle=null;fileStatus((storageOK?'Browser backup kept. ':'')+'File permission unavailable; use Export review.');
      notice('File permission was not available. Export review to save a portable copy.');
    }
  }
  function reviewRecord(id){
    const asset=byID.get(id), defaults={id,status:null,note:''};
    if(['prime','multiverse'].includes(asset?.variant))Object.assign(defaults,{variant:asset.variant,variantSource:'catalog'});
    if(asset&&Object.hasOwn(asset,'workingReference'))defaults.workingReference=normalizedWorkingReference(asset.workingReference);
    const record={...defaults,...reviews.get(id)};
    return record.variant==='multiverse'?{...record,workingReference:null}:record;
  }
  function inReviewQueue(a){const r=reviewRecord(a.id);return a.archived||['needs_fixes','remove'].includes(r.status)||r.workingReference?.status==='requested';}
  function refreshReviewUI(){
    const plansCount=document.querySelector('[data-view="shot_plans"] .count');if(plansCount)plansCount.textContent=projectAssets().filter(a=>reviewRecord(a.id).shotPlan).length;
    const count=document.querySelector('[data-view="review_queue"] .count');if(count)count.textContent=projectAssets(true).filter(inReviewQueue).length;
    document.querySelectorAll('[data-review-card]').forEach(card=>{
      card.querySelector('.review-chip')?.remove();const status=reviewRecord(card.dataset.reviewCard).status;
      if(status){const badge=document.createElement('span');badge.className='review-chip '+status;badge.textContent=statusLabels[status];card.append(badge);}
    });
    document.querySelectorAll('[data-review-status]').forEach(button=>{const active=reviewRecord(currentID).status===(button.dataset.reviewStatus||null);button.classList.toggle('selected',active);button.setAttribute('aria-pressed',String(active));});
    const status=document.querySelector('#review-current-status');if(status)status.textContent=statusLabels[reviewRecord(currentID).status]||'No triage decision';
    refreshCollaboratorUI();
    refreshReferenceUI();
  }
  function updateReview(id,patch){
    if(!byID.has(id))return;
    mergeReview({...reviewRecord(id),...patch,id,sha256:byID.get(id).sha256||null,updatedAt:new Date().toISOString(),origin:'user'});
    reviewRevision++;saveBrowserReview();
    if(['status','storyboardStage','variant','workingReferenceScope','likenessRating'].some(key=>Object.hasOwn(patch,key)))render();
    refreshReviewUI();scheduleFileSave();
  }
  function reviewControls(a){const record=reviewRecord(a.id);return `<section class="review-controls" aria-label="Review this reference"><h3>Your review</h3><p id="review-current-status" class="review-current">${esc(statusLabels[record.status]||'No triage decision')}</p><div class="review-actions">${[['keep','Keep'],['needs_fixes','Needs fixes'],['remove','Mark for removal'],['','Clear decision']].map(([value,label])=>`<button data-review-status="${value}" class="${record.status===(value||null)?'selected':''}" aria-pressed="${record.status===(value||null)}">${label}</button>`).join('')}</div><label for="review-note">Your note</label><textarea id="review-note" rows="4" maxlength="20000" placeholder="What should stay, change, or be removed from the working collection?">${esc(record.note)}</textarea><p class="review-help">Marking for removal queues a sorting request. It never deletes the source file. Clear removes the decision and keeps your note.</p><p class="review-file-status" data-review-file-status role="status">${esc(fileMessage)}</p><button class="small-link" id="viewer-save-review">Save review file</button><button class="small-link" id="viewer-export-review">Export review</button></section>`;}

  function toggleFavorite(id){favorites.has(id)?favorites.delete(id):favorites.add(id);saveFavorites();document.querySelectorAll('[data-favorite]').forEach(b=>{const on=favorites.has(b.dataset.favorite);b.classList.toggle('on',on);b.textContent=iconStar(b.dataset.favorite);b.setAttribute('aria-pressed',String(on));b.setAttribute('aria-label',(on?'Remove favorite: ':'Favorite: ')+byID.get(b.dataset.favorite).title);});const count=document.querySelector('[data-view="favorites"] .count');if(count)count.textContent=projectAssets().filter(a=>favorites.has(a.id)).length;if(state.view==='favorites'&&!currentID)renderMain();}
  function basketPayload(backup=false){const selected=[...basket].map(id=>byID.get(id)).filter(Boolean),items=backup?selected:selected.filter(exportAllowed);return {format:EXPORT_KEY,exported:new Date().toISOString(),status:backup?'browser selection backup; not an export handoff':'selected references; no approval implied',exportIntent:backup?'review_backup':state.exportIntent,excludedCount:selected.length-items.length,referencePolicy:{path:referencePolicyPath,instruction:referencePolicyText},referenceReminder:'This is a selection list. The actual images, clips, and documents are not bundled.',items:items.map(exportReference)};}
  function saveBasket(){reviewRevision++;saveBrowserReview();scheduleFileSave();document.querySelectorAll('[data-view="export_basket"] .count').forEach(e=>e.textContent=basketAssets().length);document.querySelectorAll('[data-basket]').forEach(button=>{const on=basket.has(button.dataset.basket);button.classList.toggle('on',on);button.textContent=button.id==='viewer-basket'?(on?'⇩ In export basket':'⇩ Add to export basket'):(on?'✓':'⇩');button.setAttribute('aria-pressed',String(on));button.setAttribute('aria-label',(on?'Remove from export basket: ':'Add to export basket: ')+byID.get(button.dataset.basket).title);});if(state.view==='export_basket'&&!currentID)renderMain();}
  function toggleBasket(id){if(!byID.has(id))return;basket.has(id)?basket.delete(id):basket.add(id);saveBasket();}
  function exportBasket(){const data=basketPayload();downloadJSON(data,'cfa-export-selection.json');notice(data.items.length+' references exported; '+data.excludedCount+' excluded by export intent. Media files are not bundled.');}
  function importBasket(items){let added=0,skipped=0;for(const item of items){const a=matchingAsset(item);if(a&&(!a.sha256||item.sha256===a.sha256)){basket.add(a.id);added++;}else skipped++;}return {added,skipped};}
  function queryMatch(a){const text=[a.title,a.filename,a.album,isDoc(a)?a.text:'',a.note,a.beat,a.lyric,reviewRecord(a.id).note,...(a.tags||[])].join(' ').toLowerCase();return text.includes(state.search.toLowerCase().trim());}
  function normalVisible(a){return !!a&&!a.archived&&reviewRecord(a.id).status!=='remove';}
  function projectAssets(includeArchived=false){return C.assets.filter(a=>a.project===state.project&&(includeArchived||normalVisible(a)));}
  const basketAssets=()=>C.assets.filter(a=>basket.has(a.id)&&normalVisible(a));
  function effectiveReferenceRole(a){
    const mapped=bomRoles.get(a.id);if(mapped)return mapped.role;
    const locked=(a.componentApprovals||[]).find(c=>c.sourceSHA256===a.sha256&&c.status==='user_selected_component');if(locked)return locked.scope;
    const r=reviewRecord(a.id);if(r.workingReference?.status==='approved')return r.workingReference.scope;const scope=r.workingReferenceScope;
    if(scope==='outfit')return 'outfit';if(scope==='detail')return 'detail';
    return 'scene';
  }
  function referenceUsePolicy(a){
    const role=effectiveReferenceRole(a),sceneSpecific=role==='scene'||!!reviewRecord(a.id).shotPlan;
    return {policyPath:referencePolicyPath,explicitSceneReference:sceneSpecific?{id:a.id,sha256:a.sha256||null,scope:'this_scene_only',instruction:'Use this explicitly named reference for this scene only; retain canonical scoped character components.'}:null,defaultReferenceSelection:{instruction:'For other scenes use canonical scoped gold standards and the highest-rated suitable approved Prime references.',requiredRole:role,sameRoleRequired:true,unratedIsNotFive:true},referenceRole:role,sceneSpecific,imageDoesNotReplaceIdentity:true,ratingDoesNotApprove:true};
  }
  function workingBOMEntries(project=state.project){
    return C.assets.filter(a=>a.project===project&&!isDoc(a)&&normalVisible(a)).flatMap(asset=>{
      const r=reviewRecord(asset.id),mapped=bomRoles.get(asset.id),lock=(asset.componentApprovals||[]).some(c=>c.sourceSHA256===asset.sha256&&c.status==='user_selected_component');
      const recordedSelection=mapped?.recordedSelection||(lock?'user_selected_component':null),approved=!!recordedSelection||r.workingReference?.status==='approved'||storyboardStage(asset)==='production';
      if(!approved||r.variant==='multiverse'||(r.status==='needs_fixes'&&!recordedSelection))return [];
      const role=effectiveReferenceRole(asset),section=mapped?.section||(role==='identity'||role==='complete_look'?'identity':role==='outfit'?'wardrobe':role==='detail'?'details':'scene');
      return [{asset,role,section,label:mapped?.label||asset.title,recordedSelection,optional:!!mapped?.optional,needsFixes:r.status==='needs_fixes',approved,likenessRating:normalizedRating(r.likenessRating)}];
    }).sort((a,b)=>Number(!!b.recordedSelection)-Number(!!a.recordedSelection));
  }
  function workingReferencesWorkspace(compact=false){
    const entries=workingBOMEntries().filter(e=>queryMatch(e.asset)),definition=bomDefinitions.find(c=>c.project===state.project),character=entries.filter(e=>e.section!=='scene'),scenes=entries.filter(e=>e.section==='scene');
    const sectionTitles={identity:'Default identity',details:'Approved details and placement',artwork:'Approved artwork options',wardrobe:'Approved wardrobe and prop options',optional:'Optional approved looks'};
    let html=`<section class="working-bom"><h2>${compact?'Working references':'Character bill of materials'}</h2><p class="intro">Open the character cover for its approved parts. Each part keeps its own role; optional looks and scene references stay separate.</p>`;
    if(character.length){
      const items=character.map(e=>e.asset),preferred=items.find(a=>a.id===definition?.coverAssetID),cover=preferred||character.find(e=>e.role==='identity')?.asset||items[0];
      const sections=Object.entries(sectionTitles).map(([section,title])=>({title,assetIDs:character.filter(e=>e.section===section).map(e=>e.asset.id),description:section==='artwork'?'Approved options remain distinct; a design sheet is not proof of an exact body transfer.':section==='optional'?'These selected alternatives do not replace the default face or mouth.':null}));
      html+=collectionCards([{id:definition?.id||state.project+':character-bom',project:state.project,title:definition?.title||'Approved character references',cover,items,assetIDs:items.map(a=>a.id),unit:'approved parts',textOnly:!preferred&&!character.some(e=>e.role==='identity'),sections,description:'Use only the selected role of each image. A scene can need a fix while independently locked character parts remain available.',notes:character.filter(e=>e.needsFixes).map(e=>e.label+': the recorded component remains selected; see its separate fix note.')}]);
    } else html+='<p class="empty">No approved character components match this search yet. Production applies to the role of the particular image.</p>';
    if(scenes.length)html+=`<section class="working-scene-references"><h3>Approved scene and motion references</h3><p class="intro">For the named shot or motion only. These images do not redefine the character.</p>${collectionCards([{id:state.project+':approved-scene-references',title:'Scene and motion references',project:state.project,assetIDs:scenes.map(e=>e.asset.id),items:scenes.map(e=>e.asset),cover:scenes[0].asset,unit:'scene references',sections:[{title:'Approved for scene use',assetIDs:scenes.map(e=>e.asset.id)}]}])}</section>`;
    const conflicts=projectAssets().filter(a=>storyboardStage(a)==='production'&&(reviewRecord(a.id).variant==='multiverse'||reviewRecord(a.id).status==='needs_fixes'));
    if(conflicts.length&&!compact)html+=`<details class="detail-drawer"><summary>Production choices with separate fixes or variants · ${conflicts.length}</summary><p class="intro">Their Production stage is retained. Pending fixes and Multiverse options do not replace the approved default components.</p>${mediaGroup('Review these scoped choices','',conflicts)}</details>`;
    if(!compact){const history=(definition?.historyAssetIDs||[]).map(id=>byID.get(id)).filter(Boolean);if(history.length)html+=`<details class="detail-drawer"><summary>Earlier design references · ${history.length}</summary><p class="intro">Design history is preserved separately from the current approved parts.</p>${mediaGroup('Earlier design anchors','',history)}</details>`;}
    return html+'</section>';
  }
  function libraryLocation(){return ['mission_control','collaborators'].includes(state.view)?null:{project:state.project,view:state.view,album:state.album};}
  function rememberLibrary(){const previous=libraryLocation();if(previous){state.lastLibrary=previous;try{sessionStorage.setItem('cfa-last-library',JSON.stringify(previous));}catch{}}}
  function libraryReturn(){let saved=state.lastLibrary;try{saved=saved||JSON.parse(sessionStorage.getItem('cfa-last-library')||'null');}catch{}return saved&&C.projects.some(p=>p.id===saved.project)&&!['mission_control','collaborators'].includes(saved.view)?saved:{project:'hon',view:'all',album:''};}
  function route(project,view='all',album=''){rememberLibrary();state={...state,project,view,album,search:'',...(view==='details'?{detailLayout:album?'all':'approved'}:{})};location.hash=[project,view,album].filter(Boolean).map(encodeURIComponent).join('/');render();window.scrollTo({top:0,behavior:'instant'});}
  function parseHash(){const [p,v,a]=location.hash.slice(1).split('/').map(decodeURIComponent);if(C.projects.some(x=>x.id===p)){if(v==='details'&&(state.project!==p||state.view!==v||state.album!==(a||'')))state.detailLayout=a?'all':'approved';state.project=p;state.view=['mission_control','collaborators','all','favorites','export_basket','review_queue','shot_plans','documents',...Object.keys(cats)].includes(v)?v:'all';state.album=a||'';}}
  function render(){
    const p=C.projects.find(p=>p.id===state.project);const all=projectAssets();
    document.title=p.name+' · Visual library';
    document.querySelector('#app').innerHTML=`<div class="shell"><aside class="sidebar"><p class="brand">CFA / VISUAL LIBRARY</p><div class="project-picker">${C.projects.map(x=>`<button data-project="${x.id}" class="${state.project===x.id?'active':''}">${esc(x.name)}<small>${esc(x.subtitle)}</small></button>`).join('')}</div><nav class="nav" aria-label="Studio navigation"><button data-view="mission_control" class="${state.view==='mission_control'?'active':''}">Ziggy’s Corner</button><button data-view="collaborators" class="${state.view==='collaborators'?'active':''}">Collaborators</button><button data-view="all" class="${state.view==='all'?'active':''}">All files <span class="count">${all.filter(a=>!isDoc(a)).length} visuals</span></button>${C.categories.map(([id,name])=>{const albums=C.albums.filter(x=>x.project===state.project&&x.category===id);const count=new Set(albums.flatMap(x=>x.assetIDs).filter(id=>normalVisible(byID.get(id)))).size;const visibleCount=id==='working'?workingBOMEntries().length:count;return visibleCount?`<button data-view="${id}" class="${state.view===id?'active':''}">${esc(name)}<span class="count">${visibleCount}</span></button>`:'';}).join('')}<button data-view="favorites" class="${state.view==='favorites'?'active':''}">☆ Favorites <span class="count">${all.filter(a=>favorites.has(a.id)).length}</span></button><button data-view="export_basket" class="${state.view==='export_basket'?'active':''}">⇩ Export basket <span class="count">${basketAssets().length}</span></button><button data-view="review_queue" class="${state.view==='review_queue'?'active':''}">Review queue <span class="count">${projectAssets(true).filter(inReviewQueue).length}</span></button><button data-view="shot_plans" class="${state.view==='shot_plans'?'active':''}">Shot plans <span class="count">${all.filter(a=>reviewRecord(a.id).shotPlan).length}</span></button><button data-view="documents" class="${state.view==='documents'?'active':''}">Documents <span class="count">${all.filter(isDoc).length}</span></button></nav><div class="sidebar-foot">${exportIntentControls()}<button id="save-review">Save review file</button><button id="export-review">↓ Export review & notes</button><button id="import">↑ Import review or selections</button><button id="export">↓ Export favorites only</button><p class="review-storage-hint">Review inbox: docs/notes/downloads. Export review uses your download folder; Save review file autosaves to the file you choose. Browser backup is local to this browser. Choose the file again after a refresh. Saved changes are available for Nova to read; they do not notify her automatically.</p><p class="review-file-status" data-review-file-status role="status">${esc(fileMessage)}</p><p class="build-stamp">Build ${esc(window.REVIEW_BUILD||'local preview')}</p></div></aside><div class="workspace"><div class="topbar"><span class="breadcrumb">${esc(p.name)} / ${esc(cats[state.view]||({'mission_control':'Mission Control','collaborators':'Collaborators','all':'All files','favorites':'Favorites','export_basket':'Export basket','review_queue':'Review queue','shot_plans':'Shot plans','documents':'Documents'}[state.view]))}</span><input class="search" id="search" type="search" placeholder="Search looks, scenes, details…" aria-label="Search library" value="${esc(state.search)}"></div><main class="main" id="main"></main></div></div>`;
    document.querySelectorAll('[data-project]').forEach(b=>b.onclick=()=>route(b.dataset.project,['mission_control','collaborators'].includes(state.view)?state.view:'all'));
    document.querySelectorAll('[data-view]').forEach(b=>b.onclick=()=>route(state.project,b.dataset.view));
    document.querySelector('#search').oninput=e=>{state.search=e.target.value;renderMain();};
    document.querySelector('#export').onclick=exportFavorites;document.querySelector('#import').onclick=()=>document.querySelector('#import-file').click();document.querySelector('#save-review').onclick=chooseReviewFile;document.querySelector('#export-review').onclick=exportReview;
    renderMain();
  }
  const videoSortLabels={longest:'Longest first',shortest:'Shortest first',alphabetical:'Alphabetical A–Z'};
  const clipTitleOrder=new Intl.Collator(undefined,{numeric:true,sensitivity:'base'});
  const isClip=a=>['video','gif'].includes(a.kind);
  function clipDuration(a){if(!['number','string'].includes(typeof a.duration))return null;const value=Number(a.duration);return Number.isFinite(value)&&value>0?value:null;}
  function sortClips(items){return [...items].sort((a,b)=>{
    const byTitle=clipTitleOrder.compare(a.title||a.filename,b.title||b.filename);
    if(state.videoSort==='alphabetical')return byTitle;
    const left=clipDuration(a),right=clipDuration(b);if(left===null||right===null)return left===right?byTitle:left===null?1:-1;
    return (state.videoSort==='shortest'?left-right:right-left)||byTitle;
  });}
  function card(a){if(!displayed.includes(a.id))displayed.push(a.id);return `<article class="media-card" data-review-card="${esc(a.id)}">${reviewRecord(a.id).status?`<span class="review-chip ${reviewRecord(a.id).status}">${esc(statusLabels[reviewRecord(a.id).status])}</span>`:''}<button class="favorite ${favorites.has(a.id)?'on':''}" data-favorite="${esc(a.id)}" aria-label="${favorites.has(a.id)?'Remove favorite: ':'Favorite: '}${esc(a.title)}" aria-pressed="${favorites.has(a.id)}">${iconStar(a.id)}</button><button class="basket-toggle ${basket.has(a.id)?'on':''}" data-basket="${esc(a.id)}" title="Export basket" aria-label="${basket.has(a.id)?'Remove from export basket: ':'Add to export basket: '}${esc(a.title)}" aria-pressed="${basket.has(a.id)}">${basket.has(a.id)?'✓':'⇩'}</button><button class="media-open" data-open="${esc(a.id)}"><div class="media-thumb"><img loading="lazy" src="${esc(href(a.thumb))}" alt="${esc(a.title)}">${a.kind==='video'||a.kind==='gif'?`<span class="play">${a.kind==='video'?'▶':'GIF'} ${clipDuration(a)===null?'Duration unknown':Math.round(clipDuration(a)*10)/10+'s'}</span>`:''}</div><div class="media-copy"><b>${esc(a.title)}</b><small>${esc(a.sceneID?a.lyric||'Storyboard idea':C.albums.find(x=>x.id===a.album)?.title||a.filename)}</small>${storyMaterialHint(a)}</div></button></article>`;}
  function mediaGroup(title,description,items,albumID=''){
    if(!items.length)return '';
    return `<section class="story-section"><div class="section-head"><h2>${esc(title)}</h2>${albumID?`<button class="subtle-button" data-album="${esc(albumID)}">Open group · ${items.length}</button>`:`<span class="muted">${items.length}</span>`}</div>${description?`<p>${esc(description)}</p>`:''}<div class="gallery">${items.map(card).join('')}</div></section>`;
  }
  function outfitGroups(media){
    const visible=new Set(media.map(a=>a.id));
    return C.albums.filter(al=>al.project===state.project&&al.category==='outfits').map(al=>{
      const items=[...new Set(al.assetIDs)].map(id=>byID.get(id)).filter(a=>a&&a.kind==='image'&&!a.archived&&reviewRecord(a.id).status!=='remove'&&visible.has(a.id));
      return {al,items};
    }).filter(x=>x.items.length);
  }
  function outfitCover(items){
    const rank=a=>{
      const label=[a.title,a.filename,a.viewRole,a.referenceRole].filter(Boolean).join(' ');
      const sheet=/contact|all.views|reference.sheet|[_-]sheet/i.test(label);
      const portrait=!sheet&&/portrait|head.?shot|chest.?up|bust/i.test(label);
      const viewRank=portrait?0:sheet?3:/front/i.test(label)?1:2;
      return viewRank*100+Number(reviewRecord(a.id).variant==='multiverse')*10+Number(reviewRecord(a.id).status==='needs_fixes');
    };
    return [...items].sort((a,b)=>rank(a)-rank(b))[0];
  }
  function sharedCharacterAlbums(){
    return C.albums.filter(al=>al.project===state.project&&al.category==='comfy'&&/head|mouth|viseme|breather/i.test(al.id+' '+al.title)&&al.assetIDs.some(id=>byID.has(id)&&!byID.get(id).archived));
  }
  function sharedCharacterReferences(){
    const definitions=(C.sharedReferenceCollections||[]).filter(g=>g.project===state.project),covered=new Set(definitions.flatMap(g=>g.sourceAlbumIDs||[]));
    const fallback=sharedCharacterAlbums().filter(al=>!covered.has(al.id)).map(al=>({...al,description:al.description,coverID:outfitCover(al.assetIDs.map(id=>byID.get(id)).filter(a=>a&&!isDoc(a)))?.id}));
    const groups=collectionGroups([...definitions,...fallback]);if(!groups.length)return '';
    return `<section class="shared-character-references" aria-label="Shared head and mouth references"><h2>Shared heads & mouths</h2><p>Reusable across outfits. Click a cover to expand the references here; each image keeps its own review.</p>${collectionCards(groups)}</section>`;
  }
  function collectionGroups(definitions,media=projectAssets()){
    const visible=new Set(media.filter(a=>!isDoc(a)).map(a=>a.id)),query=state.search.toLowerCase().trim();
    return definitions.filter(g=>g.project===state.project).map(g=>{
      const allItems=[...new Set(g.assetIDs||[])].map(id=>byID.get(id)).filter(a=>a&&visible.has(a.id)&&(g.includeArchived||!a.archived)&&(g.includeRemoved||reviewRecord(a.id).status!=='remove'));
      const groupMatch=query&&[g.title,g.role,...(g.aliases||[])].join(' ').toLowerCase().includes(query);
      const items=allItems.filter(a=>!query||groupMatch||queryMatch(a));
      return {...g,items,cover:items.find(a=>a.id===(g.coverID||g.coverAssetID))||outfitCover(items)};
    }).filter(g=>g.items.length);
  }
  function collectionCards(groups){
    return `<div class="gallery collection-catalog">${groups.map(g=>{
      const expanded=expandedCollections.has(g.id),panel='collection-'+g.id.replace(/[^a-z0-9_-]/gi,'-'),cover=g.cover,status=reviewRecord(cover.id).status;
      let views='';
      if(expanded){
        const remaining=new Map(g.items.map(a=>[a.id,a])),sections=g.sections||(g.preferredIDs?.length?[{title:'Your shortlist',assetIDs:g.preferredIDs},{title:'Other candidates',assetIDs:g.assetIDs.filter(id=>!g.preferredIDs.includes(id)),history:true}]:[{title:'Current references',assetIDs:g.currentIDs||g.assetIDs},{title:'Earlier studies',assetIDs:g.historyIDs||[],history:true}]);
        if(g.children?.length){views+=collectionCards(g.children);for(const child of g.children)for(const a of child.items)remaining.delete(a.id);}
        // Historical media stays under its character, not in a second top-level collection.
        if(!g.sections&&g.historyIDs?.length)for(const id of g.historyIDs)if(!g.currentIDs)sections[0].assetIDs=sections[0].assetIDs.filter(x=>x!==id);
        for(const section of sections){const items=(section.assetIDs||[]).map(id=>remaining.get(id)).filter(Boolean);for(const a of items)remaining.delete(a.id);if(!items.length)continue;
          const gallery=`<div class="gallery">${items.map(card).join('')}</div>`;
          views+=section.history?`<details class="collection-history" ${state.search.trim()?'open':''}><summary>${esc(section.title)} · ${items.length}</summary>${gallery}</details>`:`<section class="collection-section"><h3>${esc(section.title)}</h3>${section.description?`<p>${esc(section.description)}</p>`:''}${gallery}</section>`;
        }
        if(remaining.size)views+=`<section class="collection-section"><h3>Related references</h3><div class="gallery">${[...remaining.values()].map(card).join('')}</div></section>`;
      }
      const unit=g.unit||'references',count=g.children?.length||g.items.length;
      return `<article class="inline-collection ${expanded?'is-expanded':''} ${g.textOnly?'text-collection':''}" data-collection="${esc(g.id)}"><div class="collection-summary"><div class="media-card collection-cover" ${g.textOnly?'':`data-review-card="${esc(cover.id)}"`}>${status&&!g.textOnly?`<span class="review-chip ${status}">${esc(statusLabels[status])}</span>`:''}<button class="media-open" data-collection-toggle="${esc(g.id)}" aria-expanded="${expanded}" aria-controls="${esc(panel)}" aria-label="${expanded?'Collapse':'Expand'} ${esc(g.title)}">${g.textOnly?'':`<div class="media-thumb"><img loading="lazy" src="${esc(href(cover.thumb))}" alt="${esc(g.title)}">${isClip(cover)?`<span class="play">▶ ${clipDuration(cover)===null?'Video':Math.round(clipDuration(cover)*10)/10+'s'}</span>`:''}</div>`}<div class="media-copy"><b>${esc(g.title)}</b><small>${esc(g.role||'')} ${g.role?'· ':''}${count} ${esc(unit)}</small>${g.enhancementRequest?'<small class="collection-flag">Clarity improvement requested</small>':''}</div></button></div><button class="outfit-expand" data-collection-toggle="${esc(g.id)}" aria-expanded="${expanded}" aria-controls="${esc(panel)}">${expanded?'▾ Hide':'▸ Show'} ${esc(unit)}${expanded?'':' here'}</button></div><div id="${esc(panel)}" class="collection-inline-views" ${expanded?'':'hidden'}>${expanded?`${g.description?`<p>${esc(g.description)}</p>`:''}${g.notes?.length?`<ul class="collection-notes">${g.notes.map(note=>`<li>${esc(note)}</li>`).join('')}</ul>`:''}${views}`:''}</div></article>`;
    }).join('')}</div>`;
  }
  function castExplorer(){
    const definitions=(C.castCollections||[]).filter(g=>g.project===state.project),covered=new Set(definitions.flatMap(g=>g.assetIDs));
    const fallback=C.albums.filter(al=>al.project===state.project&&al.category==='cast').map(al=>({...al,assetIDs:al.assetIDs.filter(id=>!covered.has(id))}));
    const groups=collectionGroups([...definitions,...fallback]);
    return `<section class="cast-explorer"><div class="section-head"><h2>Supporting cast</h2><span class="muted">${groups.length} collections</span></div><p class="intro">One place per character. Click a portrait for current views and earlier studies.</p>${collectionCards(groups)}${groups.length?'':'<p class="empty">No characters match this search.</p>'}</section>`;
  }
  function accessoryExplorer(){
    const groups=collectionGroups(C.accessoryCollections||[]);return groups.length?`<section class="accessory-explorer"><h2>Dolo’s jewelry & hand details</h2><p class="intro">Permanent character references, carried across outfits and shots whenever visible.</p>${collectionCards(groups)}</section>`:'';
  }
  function detailAlbumGroups(al,items){
    const definitions=(C.detailDisplayGroups||[]).filter(g=>g.project===state.project&&g.albumID===al.id),covered=new Set(definitions.flatMap(g=>g.assetIDs));
    const groups=collectionGroups(definitions,items),other=items.filter(a=>!covered.has(a.id));
    return (groups.length?`<section class="story-section"><h2>${esc(al.title)}</h2><p class="intro">One card per design. Transparent copies and option sheets are inside.</p>${collectionCards(groups)}</section>`:'')+mediaGroup(groups.length?'Other details':al.title,'',other,al.id);
  }
  const browseLayout=()=>C.browseLayout?.projects?.[state.project]||{};
  function browseDisclosure(id,title,body,count,defaultOpen=false){
    const open=defaultOpen?!collapsedBrowseBuckets.has(id):expandedCollections.has(id),panel='browse-'+id.replace(/[^a-z0-9_-]/gi,'-');
    return `<section class="browse-bucket"><button class="browse-bucket-toggle" ${defaultOpen?'data-browse-bucket':'data-collection-toggle'}="${esc(id)}" aria-expanded="${open}" aria-controls="${esc(panel)}"><span>${open?'▾':'▸'} ${esc(title)}</span><small>${count} collections</small></button><div id="${panel}" ${open?'':'hidden'}>${open?body():''}</div></section>`;
  }
  function orderedStoryAssets(ids){return [...ids].sort((left,right)=>{
    const order=id=>{const a=byID.get(id);return Number(a?.storyboardOrder)||Number(/SB[- ]?(\d+)/i.exec(a?.sceneID||a?.title||'')?.[1])||9999;};
    return order(left)-order(right);
  });}
  function storyboardAlbumCollections(media=projectAssets()){
    const sequenceAlbums=new Set((C.storyboardSequences||[]).flatMap(s=>s.sourceAlbumIDs||[])),covers=browseLayout().storyCovers||{};
    const definitions=C.albums.filter(al=>al.project===state.project&&al.category==='storyboard'&&!sequenceAlbums.has(al.id)).map(al=>{
      const assetIDs=orderedStoryAssets(al.assetIDs);
      return {...al,assetIDs,coverID:covers[al.id]||assetIDs[0],unit:'shots',sections:[{title:'Shots · storyboard order',assetIDs}]};
    });
    return collectionGroups(definitions,media);
  }
  function videoAlbumCollections(media=projectAssets()){
    const covers=browseLayout().videoCovers||{},comfy=new Set(browseLayout().comfyAlbumIDs||[]);
    return collectionGroups(C.albums.filter(al=>al.project===state.project&&al.category==='videos'&&!comfy.has(al.id)).map(al=>{
      const assetIDs=sortClips(al.assetIDs.map(id=>byID.get(id)).filter(Boolean)).map(a=>a.id);
      return {...al,assetIDs,coverID:covers[al.id]||assetIDs[0],unit:'clips',sections:[{title:'Clips',assetIDs}]};
    }),media);
  }
  function tattooCollections(media=projectAssets()){
    let html='';
    for(const [bucket,title] of [['stencils','Tattoo stencils'],['skin','Tattoos on skin']]){
      const groups=collectionGroups((C.detailDisplayGroups||[]).filter(g=>g.bucket===bucket),media);
      if(groups.length)html+=browseDisclosure(state.project+':tattoo-'+bucket,title,()=>collectionCards(groups),groups.length,bucket!=='guides');
    }
    return html;
  }
  function comfyCollections(media=projectAssets()){
    const config=browseLayout(),albumIDs=new Set(config.comfyAlbumIDs||[]),covers=config.videoCovers||{};
    const children=collectionGroups(C.albums.filter(al=>al.project===state.project&&albumIDs.has(al.id)).map(al=>({...al,coverID:covers[al.id]||al.assetIDs[0]})),media);
    if(!children.length)return [];
    const assetIDs=[...new Set(children.flatMap(g=>g.items.map(a=>a.id)))];
    return collectionGroups([{id:state.project+':comfy-workspace',project:state.project,title:'Comfy',unit:'collections',assetIDs,coverID:covers[state.project+':video-comfy_experiments'],description:'Motion and lighting experiments, turnaround videos, likeness targets and their original source material.'}],media).map(g=>({...g,children}));
  }
  function processArchive(media=projectAssets(true)){
    const config=browseLayout(),albumIDs=new Set(config.archiveAlbumIDs||[]),groups=collectionGroups(C.albums.filter(al=>al.project===state.project&&(al.category==='review'||albumIDs.has(al.id))).map(al=>({...al,textOnly:true,includeArchived:true,includeRemoved:true})),media);
    groups.push(...collectionGroups((C.detailDisplayGroups||[]).filter(g=>g.bucket==='guides').map(g=>({...g,textOnly:true,includeArchived:true,includeRemoved:true})),media));
    const claimed=new Set(groups.flatMap(g=>g.items.map(a=>a.id))),other=media.filter(a=>!isDoc(a)&&!claimed.has(a.id)&&(a.archived||reviewRecord(a.id).status==='remove'||/reject/i.test(a.filename||'')));
    if(other.length)groups.push(...collectionGroups([{id:state.project+':other-archived',project:state.project,title:'Other archived references',assetIDs:other.map(a=>a.id),textOnly:true,includeArchived:true,includeRemoved:true}],media));
    if(!groups.length)return '';
    return browseDisclosure(state.project+':process-history','Process & history',()=>{
      const buckets=[['rejects','Rejected attempts',g=>/reject|mouth-b-archive|other-archived/i.test(g.id+' '+g.title)],['source-history','Source recovery & earlier process',g=>!/reject|mouth-b-archive|other-archived/i.test(g.id+' '+g.title)]];
      const parents=buckets.map(([id,title,match])=>{
        const children=groups.filter(match),assetIDs=[...new Set(children.flatMap(g=>g.items.map(a=>a.id)))];
        return {...collectionGroups([{id:state.project+':'+id,project:state.project,title,assetIDs,textOnly:true,includeArchived:true,includeRemoved:true,unit:'collections'}],media)[0],children};
      }).filter(g=>g.items?.length);
      return '<p class="intro">Recovery originals, rejected attempts and benchmark history remain available here. Their review decisions are preserved.</p>'+collectionCards(parents);
    },groups.length);
  }
  function compactAllFiles(media=projectAssets()){
    const config=browseLayout(),covered=new Set(),claim=ids=>ids.forEach(id=>covered.add(id));
    const archiveAlbums=new Set(config.archiveAlbumIDs||[]);
    const current=media.filter(a=>!isDoc(a)&&!a.archived&&reviewRecord(a.id).status!=='remove'&&!/reject/i.test(a.filename||'')&&!archiveAlbums.has(a.album));
    // Explicit subject collections may include recovered evidence. Batch labels stay in history.
    const subjectMedia=media.filter(a=>!isDoc(a)&&!a.archived&&reviewRecord(a.id).status!=='remove'&&!/reject/i.test(a.filename||''));
    let html='';
    html+=workingReferencesWorkspace(true);claim(workingBOMEntries().map(e=>e.asset.id));claim(current.filter(a=>a.category==='working').map(a=>a.id));
    html+=outfitExplorer(current.filter(queryMatch));claim(current.filter(a=>a.category==='outfits').map(a=>a.id));
    for(const g of [...(C.sharedReferenceCollections||[]),...(C.accessoryCollections||[])].filter(g=>g.project===state.project))claim(g.assetIDs||[]);
    for(const al of sharedCharacterAlbums())claim(al.assetIDs);
    html+=tattooCollections(subjectMedia);for(const g of (C.detailDisplayGroups||[]).filter(g=>g.project===state.project))claim(g.assetIDs||[]);
    const detailAlbums=C.albums.filter(al=>al.project===state.project&&al.category==='details').map(al=>({...al,assetIDs:al.assetIDs.filter(id=>!covered.has(id)&&byID.get(id)?.category==='details')}));
    const detailGroups=collectionGroups(detailAlbums,current);if(detailGroups.length)html+=`<section><h2>Other character details</h2>${collectionCards(detailGroups)}</section>`;claim(detailGroups.flatMap(g=>g.items.map(a=>a.id)));
    html+=castExplorer();claim(subjectMedia.filter(a=>a.category==='cast').map(a=>a.id));for(const g of (C.castCollections||[]).filter(g=>g.project===state.project))claim(g.assetIDs||[]);
    const story=storyboardAlbumCollections(subjectMedia),sequences=storySequenceGroups(subjectMedia);
    if(story.length||sequences.length)html+=`<section class="storyboard-collections"><h2>Storyboard</h2><p class="intro">One cover per section. Open it here for shots in storyboard order.</p>${collectionCards(story)}${sequences.length?`<h3>Separate scene drafts</h3>${collectionCards(sequences)}`:''}</section>`;
    claim([...story,...sequences].flatMap(g=>g.items.map(a=>a.id)));
    const videos=videoAlbumCollections(subjectMedia);if(videos.length)html+=`<section><h2>Videos</h2>${collectionCards(videos)}</section>`;claim(videos.flatMap(g=>g.items.map(a=>a.id)));
    const comfy=comfyCollections(subjectMedia);if(comfy.length)html+=`<section class="comfy-collections"><h2>Comfy</h2>${collectionCards(comfy)}</section>`;claim(comfy.flatMap(g=>g.items.map(a=>a.id)));
    const otherGroups=collectionGroups(C.albums.filter(al=>al.project===state.project&&al.category!=='review'&&!archiveAlbums.has(al.id)).map(al=>({...al,assetIDs:al.assetIDs.filter(id=>!covered.has(id))})),current);
    if(otherGroups.length)html+=`<section><h2>More references & inspiration</h2>${collectionCards(otherGroups)}</section>`;
    html+=processArchive();return html;
  }
  function outfitExplorer(media){
    const outfits=outfitGroups(media);
    let html=`<section class="outfit-explorer"><div class="section-head"><h2>Outfits</h2><span class="muted">${outfits.length} ${state.search?'matching ':''}collections</span></div><p class="intro">One portrait per outfit. Open a card for its views, or expand it here. Gun and no-gun versions stay together.</p><div class="tools outfit-layout-controls" role="group" aria-label="Outfit view">${[['compact','One per outfit'],['all','Show all views']].map(([value,label])=>`<button class="pill ${state.outfitLayout===value?'active':''}" data-outfit-layout="${value}" aria-pressed="${state.outfitLayout===value}">${label}</button>`).join('')}</div>`;
    if(state.outfitLayout==='all')html+=outfits.map(({al,items})=>mediaGroup(al.title,al.description,items,al.id)).join('');
    else html+=`<div class="gallery outfit-catalog">${outfits.map(({al,items})=>{
      const cover=outfitCover(items),expanded=expandedOutfits.has(al.id),panel='outfit-views-'+al.id.replace(/[^a-z0-9_-]/gi,'-'),status=reviewRecord(cover.id).status;
      const portrait=/portrait|head.?shot|chest.?up|bust/i.test([cover.title,cover.filename,cover.viewRole,cover.referenceRole].join(' '));
      return `<article class="outfit-collection ${expanded?'is-expanded':''}" data-outfit-collection="${esc(al.id)}"><div class="outfit-summary"><div class="media-card outfit-cover" data-review-card="${esc(cover.id)}">${status?`<span class="review-chip ${status}">${esc(statusLabels[status])}</span>`:''}<button class="media-open" data-album="${esc(al.id)}" aria-label="Open ${esc(al.title)} views"><div class="media-thumb"><img loading="lazy" src="${esc(href(cover.thumb))}" alt="${esc(al.title)} · ${portrait?'portrait':'available view'}"></div><div class="media-copy"><b>${esc(al.title)}</b><small>${items.length} ${state.search?'matching ':''}views · Open outfit</small>${portrait?'':'<small class="outfit-cover-fallback">Available view · portrait not supplied</small>'}</div></button></div><button class="outfit-expand" data-outfit-toggle="${esc(al.id)}" aria-expanded="${expanded}" aria-controls="${esc(panel)}">${expanded?'▾ Hide views':'▸ Show views here'} <span>${items.length}</span></button></div><div id="${esc(panel)}" class="outfit-inline-views" ${expanded?'':'hidden'}>${expanded?`<p class="muted">${esc(al.title)} · ${state.search?'matching ':''}views and variants</p><div class="gallery">${items.map(card).join('')}</div>`:''}</div></article>`;
    }).join('')}</div>`;
    return html+(outfits.length?'':'<p class="empty">No outfits match this search.</p>')+'</section>'+sharedCharacterReferences()+accessoryExplorer();
  }
  function documentGroups(items){
    if(!items.length)return '';
    const classify=a=>{
      const album=String(a.album||'Other notes'),lower=album.toLowerCase();let parent,child=album;
      if(a.documentGroup){parent=a.documentGroup;child=a.documentCategory||album;}
      else if(/design.*outfit|outfit|wardrobe/.test(lower)){parent='Design & outfit notes';child=album.replace(/^design and outfit notes\s*[·:—-]?\s*/i,'')||'General';}
      else if(/histor|helper|reference maps|drop notes/.test(lower))parent='Reference history & helpers';
      else if(/tattoo|piercing|stencil|detail/.test(lower))parent='Tattoos & details';
      else if(/storyboard|story and character/.test(lower))parent='Storyboards & story';
      else if(/collaborator|gemini|grok|flow/.test(lower)){parent='Collaborators';child=album.replace(/^collaborator (briefs|roles)\s*[·:—-]?\s*/i,'')||'Shared roles';}
      else if(/production|comfy|workflow|audio|music/.test(lower))parent='Production';
      else parent='Reference history & helpers';return {parent,child};
    };
    const parents=new Map();for(const a of items){const {parent,child}=classify(a);if(!parents.has(parent))parents.set(parent,new Map());const children=parents.get(parent);if(!children.has(child))children.set(child,[]);children.get(child).push(a);}
    const order=['Design & outfit notes','Tattoos & details','Storyboards & story','Collaborators','Production','Reference history & helpers'],searching=!!state.search.trim();
    return `<section class="documents-section"><div class="section-head"><h2>Documents & notes</h2><span class="muted">${items.length} files</span></div><p class="intro">Open a subject, then a collection. Search reveals matching files inside their groups.</p><div class="doc-list">${[...parents].sort((a,b)=>order.indexOf(a[0])-order.indexOf(b[0])).map(([parent,children])=>`<details class="doc-group doc-parent" ${searching?'open':''}><summary>${esc(parent)} <span class="muted">${[...children.values()].reduce((n,files)=>n+files.length,0)} files</span></summary><div>${[...children].map(([child,files])=>`<details class="doc-group doc-child" ${searching?'open':''}><summary>${esc(child)} <span class="muted">${files.length}</span></summary><div>${files.map(a=>`<button class="doc-row" data-open="${esc(a.id)}"><b>${esc(a.title)}</b><small>${esc(a.inert?'Helper script · text preview only':a.filename)}</small></button>`).join('')}</div></details>`).join('')}</div></details>`).join('')}</div></section>`;
  }
  function detailExplorer(){
    const profiles=(C.detailProfiles||[]).filter(p=>p.project===state.project),query=state.search.toLowerCase().trim();
    if(!profiles.some(p=>p.id===state.detailProfile))state.detailProfile=profiles[0]?.id||'';
    let html=`<div class="tools detail-browse" role="group" aria-label="Artwork view">${[['approved','Approved artwork'],['archive','Archive'],['all','All references']].map(([value,label])=>`<button class="pill ${state.detailLayout===value?'active':''}" data-detail-layout="${value}" aria-pressed="${state.detailLayout===value}">${label}</button>`).join('')}</div>`;
    if(state.detailLayout==='all')return html;
    if(!profiles.length)return html+'<p class="notice">No artwork catalog is available for this character yet. All references remains available.</p>';
    if(profiles.length>1)html+=`<div class="tools detail-profile-tabs" aria-label="Character profile">${profiles.map(p=>`<button class="pill ${state.detailProfile===p.id?'active':''}" data-detail-profile="${esc(p.id)}">${esc(p.character||p.title)}</button>`).join('')}</div>`;
    const profile=profiles.find(p=>p.id===state.detailProfile),objects=(profile.objects||[]).filter(o=>!query||[o.title,o.kind,o.location,o.status,o.summary].join(' ').toLowerCase().includes(query)||[...(o.artworkAssetIDs||[]),...(o.exampleAssetIDs||[])].some(id=>byID.has(id)&&queryMatch(byID.get(id))));
    const artwork=o=>[...new Set(o.artworkAssetIDs||[])].map(id=>byID.get(id)).filter(a=>a&&a.kind==='image'&&!a.archived&&reviewRecord(a.id).status!=='remove');
    const evidence=o=>`<details class="detail-evidence"><summary>Placement & references</summary>${o.location?`<p>${esc(o.location)}</p>`:''}<p>${esc(o.summary||'')}</p>${workflowReferences('Actor & placement examples',[...new Set([...(o.exampleAssetIDs||[]),...(o.assetIDs||[])])].filter(id=>!(o.artworkAssetIDs||[]).includes(id)))}${workflowReferences('Artwork options',[...new Set([...(o.artworkAssetIDs||[]),...(o.stencilAssetIDs||[])])])}</details>`;
    const seen=new Set(),items=[];
    for(const o of objects.filter(o=>!o.optional))for(const a of artwork(o)){
      const approved=(o.approvedArtworkAssetIDs||[]).includes(a.id);
      if(approved!==(state.detailLayout==='approved')||seen.has(a.id))continue;
      seen.add(a.id);items.push({o,a});
    }
    html+=`<div class="section-head"><h2>${esc(profile.character||profile.title)}</h2><span class="muted">${items.length} ${items.length===1?'drawing':'drawings'}</span></div><p class="intro">${state.detailLayout==='approved'?'Approved drawings first. Open the artwork to inspect it, or expand an item for placement examples.':'Earlier options and drawings awaiting selection. These stay separate from approved artwork.'}</p>`;
    html+=items.length?`<div class="detail-object-grid stencil-catalog">${items.map(({o,a})=>{
      if(!displayed.includes(a.id))displayed.push(a.id);
      return `<article class="detail-object" data-artwork-id="${esc(a.id)}"><button class="detail-object-cover" data-open="${esc(a.id)}" aria-label="Open artwork: ${esc(o.title)}"><img loading="lazy" src="${esc(href(a.thumb))}" alt="${esc(o.title)}"></button><div class="detail-object-copy"><p class="eyebrow">${esc(o.kind==='artwork_candidate'?'Tattoo artwork':o.kind)}</p><h3>${esc(o.title)}</h3>${artwork(o).length>1?`<p>${esc(a.title)}</p>`:''}<p class="detail-object-status">${state.detailLayout==='approved'?'Approved artwork':'Archive · not selected'}</p>${evidence(o)}</div></article>`;
    }).join('')}</div>`:`<p class="empty detail-empty">${query?'No drawings match this search.':state.detailLayout==='approved'?'No standalone artwork is confirmed approved here yet. Browse the archive to review the available drawings.':'No other standalone drawings are filed here yet.'}</p>`;
    const missing=objects.filter(o=>o.needsArtwork&&!o.optional&&!artwork(o).length),optional=objects.filter(o=>o.optional);
    if(missing.length)html+=`<details class="detail-drawer"><summary>Artwork still needed <span class="muted">${missing.length}</span></summary><p class="intro">These details have placement references, but their separate drawings have not been recovered.</p><div class="detail-missing-list">${missing.map(o=>`<article><h3>${esc(o.title)}</h3><p class="muted">${o.kind==='piercing'?'Standalone jewelry reference needed':'Stencil needed'}</p>${evidence(o)}</article>`).join('')}</div></details>`;
    if(optional.length)html+=`<details class="detail-drawer"><summary>Optional accessories <span class="muted">${optional.length}</span></summary><div class="detail-missing-list">${optional.map(o=>`<article><h3>${esc(o.title)}</h3><p>${esc(o.summary||'Use only when explicitly requested.')}</p>${artwork(o).length?workflowReferences('Accessory artwork',o.artworkAssetIDs):'<p class="muted">The available reference is an on-character example.</p>'}${evidence(o)}</article>`).join('')}</div></details>`;
    return html;
  }
  function storyThemes(a){
    const themes=C.albums.filter(al=>al.project===state.project&&al.category==='storyboard'&&al.assetIDs.includes(a.id)).map(al=>({id:al.id,title:al.title}));
    for(const tag of a.storyboardThemes||a.themes||a.tags||[])if(typeof tag==='string'&&!/^(storyboard|series\s*\d+)$/i.test(tag))themes.push({id:'tag:'+tag,title:tag});return themes;
  }
  function storyboardStage(a){return reviewRecord(a.id).storyboardStage||a.storyboardStage||(a.category==='storyboard'?'preliminary':null);}
  function storyWorkItems(project=state.project){return (C.shotMaterials?.shots||[]).filter(s=>s.project===project);}
  function storyWorkForAsset(a){return storyWorkItems(a.project).filter(s=>(s.panelAssetIDs||[]).includes(a.id)||(s.materials||[]).some(m=>m.assetID===a.id));}
  function storyMaterialHint(a){
    if(a.category!=='storyboard')return '';
    const shots=storyWorkForAsset(a),count=new Set(shots.flatMap(s=>(s.materials||[]).filter(m=>m.role!=='storyboard_concept').map(m=>m.assetID)).filter(id=>byID.has(id))).size;
    return shots.length?`<small class="story-material-hint">${count?count+' linked material'+(count===1?'':'s'):'Shot plan'} · open for next step</small>`:'';
  }
  function storyMaterialLinks(shot,current=''){
    return (shot.materials||[]).filter(m=>normalVisible(byID.get(m.assetID))&&m.assetID!==current&&m.role!=='storyboard_concept').map(m=>{const a=byID.get(m.assetID),r=reviewRecord(a.id);if(!displayed.includes(a.id))displayed.push(a.id);return `<li><button class="small-link" data-open="${esc(a.id)}">${esc(a.title)}</button><small>${esc(String(m.role||'reference').replace(/_/g,' '))} · ${esc(String(m.status||'candidate').replace(/_/g,' '))}${r.status?' · '+esc(statusLabels[r.status]):''}${r.variant==='multiverse'?' · Multiverse':''}</small>${m.note?`<p class="review-help">${esc(m.note)}</p>`:''}</li>`;}).join('');
  }
  function sceneReadinessControls(shot){
    const r=sceneReviewRecord(shot.project,shot.id),gate=sceneHandoffGate(r),key=shot.project+':'+shot.id;
    const pool=[...new Set([...(shot.materials||[]).map(m=>m.assetID),...(shot.panelAssetIDs||[]),...workingBOMEntries(shot.project).map(e=>e.asset.id),...[...basket].filter(id=>byID.get(id)?.project===shot.project)])].map(id=>byID.get(id)).filter(normalVisible);
    return `<details class="scene-readiness" ${r.updatedAt?'open':''}><summary>Scene grade: ${r.grade||'Ungraded'} · ${gate.productionEligible?'B target met':'Review ingredients'}</summary><p class="review-help">Grade this whole scene separately from the likeness of each reference. B or better is the production target; missing fingers, an unready boss or another critical defect must be resolved. A grade does not approve the generated result or change its design stage.</p><label>Whole scene grade<select data-scene-field="grade"><option value="" ${r.grade===null?'selected':''}>Ungraded</option>${['A','B','C','D','F'].map(g=>`<option value="${g}" ${r.grade===g?'selected':''}>${g}</option>`).join('')}</select></label><p data-scene-gate="${esc(key)}" role="status" class="scene-gate">${esc(gate.productionEligible?'Meets B-or-better scene target; final result acceptance is separate.':'Planning / repair: '+gate.reasons.join(' '))}</p><h4>Shoot plan verification</h4><p class="review-help">Review direction and cinematography before a production handoff. Save who performed the review; this form does not contact another AI. <a class="small-link" href="${esc(href('../collaborators/work_briefs_20261010/SHOOT_PLAN_VERIFICATION.txt'))}" target="_blank" rel="noopener">Shoot plan review guide</a></p>${[['direction','Director: action, blocking, eyelines and performance'],['camera','Camera: framing, angle and movement'],['lighting','Lighting: sources, contrast and continuity']].map(([field,label])=>`<label>${label}<textarea data-shoot-field="${field}" rows="3" maxlength="12000">${esc(r.shootPlan[field])}</textarea></label>`).join('')}<label>Reviewed by<input type="text" data-shoot-field="reviewedBy" maxlength="300" value="${esc(r.shootPlan.reviewedBy)}" placeholder="Name of the person or AI that actually reviewed it"></label><label>Shoot plan review<select data-shoot-field="reviewStatus">${[['unreviewed','Unreviewed'],['needs_fixes','Needs fixes'],['verified','Verified']].map(([v,l])=>`<option value="${v}" ${r.shootPlan.reviewStatus===v?'selected':''}>${l}</option>`).join('')}</select></label><label>Review findings<textarea data-shoot-field="note" rows="2" maxlength="6000">${esc(r.shootPlan.note)}</textarea></label><p class="review-help" data-shoot-review-time>${esc(r.shootPlan.reviewedAt?'Review recorded: '+r.shootPlan.reviewedAt:'No shoot plan verification recorded.')}</p><h4>Scene ingredients</h4><p class="review-help">Mark what this scene requires and review each part. Available files begin unreviewed. Add missing characters, props or checks by name.</p><div class="scene-ingredients">${r.ingredients.map(i=>`<div class="scene-ingredient" data-ingredient="${esc(i.id)}"><b>${esc(i.label)}</b><small>${esc(String(i.role).replace(/_/g,' '))}</small><label><input type="checkbox" data-ingredient-field="required" ${i.required?'checked':''}> Required in this scene</label><label>Ready for this scene<select data-ingredient-field="status">${[['unreviewed','Unreviewed'],['ready','Ready'],['needs_fixes','Needs fixes'],['missing','Missing']].map(([v,l])=>`<option value="${v}" ${i.status===v?'selected':''}>${l}</option>`).join('')}</select></label>${i.kind==='reference'?`<label>Exact reference<select data-ingredient-field="assetID"><option value="">Missing / no reference</option>${[...pool,...(byID.has(i.assetID)&&!pool.some(a=>a.id===i.assetID)?[byID.get(i.assetID)]:[])].map(a=>`<option value="${esc(a.id)}" ${i.assetID===a.id?'selected':''}>${esc(a.title)}</option>`).join('')}</select></label>`:'<p class="muted">Scene check · describe the evidence below.</p>'}<label>Evidence, differences or fix needed<textarea data-ingredient-field="note" rows="2" maxlength="6000">${esc(i.note)}</textarea></label></div>`).join('')}</div><div class="scene-add"><label>New ingredient or check<input type="text" data-new-ingredient maxlength="300" placeholder="Boss face, cigar, dartboard, complete hands…"></label><button class="pill" data-add-ingredient="reference">Add missing reference</button><button class="pill" data-add-ingredient="criterion">Add scene check</button></div><label>Critical blockers · one per line<textarea data-scene-field="criticalBlockers" rows="3" maxlength="12000" placeholder="Defects that must be resolved before this scene is production ready">${esc(r.criticalBlockers.join('\n'))}</textarea></label><label>Whole scene note<textarea data-scene-field="note" rows="3" maxlength="12000">${esc(r.note)}</textarea></label><p class="review-help">Draft and repair handoffs remain available while the scene is ungraded or blocked.</p><span hidden data-scene-project="${esc(shot.project)}" data-scene-id="${esc(shot.id)}"></span></details>`;
  }
  function bindSceneReadinessControls(){
    document.querySelectorAll('.scene-readiness').forEach(panel=>{
      const identity=panel.querySelector('[data-scene-id]'),project=identity?.dataset.sceneProject,shotID=identity?.dataset.sceneId;if(!project||!shotID)return;
      panel.querySelectorAll('[data-scene-field]').forEach(input=>{const field=input.dataset.sceneField,apply=()=>updateSceneReview(project,shotID,{[field]:field==='criticalBlockers'?input.value.split(/\r?\n/):field==='grade'?input.value||null:input.value},field==='grade');if(input.tagName==='TEXTAREA')input.oninput=apply;else input.onchange=apply;});
      panel.querySelectorAll('[data-shoot-field]').forEach(input=>{const field=input.dataset.shootField,apply=()=>{const current=sceneReviewRecord(project,shotID).shootPlan,shootPlan={...current,[field]:input.value};if(['direction','camera','lighting','reviewedBy'].includes(field)&&current[field]!==input.value){shootPlan.reviewStatus='unreviewed';shootPlan.reviewedAt=null;}if(field==='reviewStatus')shootPlan.reviewedAt=input.value==='verified'?new Date().toISOString():null;updateSceneReview(project,shotID,{shootPlan},field==='reviewStatus');};if(input.tagName==='SELECT')input.onchange=apply;else input.oninput=apply;});
      panel.querySelectorAll('[data-ingredient]').forEach(row=>row.querySelectorAll('[data-ingredient-field]').forEach(input=>{
        const field=input.dataset.ingredientField,apply=()=>{const r=sceneReviewRecord(project,shotID),ingredients=r.ingredients.map(i=>{if(i.id!==row.dataset.ingredient)return i;const value=field==='required'?input.checked:input.value;if(field==='assetID')return {...i,assetID:value||null,sha256:byID.get(value)?.sha256||null,status:'unreviewed'};return {...i,[field]:value};});updateSceneReview(project,shotID,{ingredients},field!=='note');};if(field==='note')input.oninput=apply;else input.onchange=apply;
      }));
      panel.querySelectorAll('[data-add-ingredient]').forEach(button=>button.onclick=()=>{const input=panel.querySelector('[data-new-ingredient]'),label=input.value.trim();if(!label)return;const r=sceneReviewRecord(project,shotID);updateSceneReview(project,shotID,{ingredients:[...r.ingredients,{id:'added:'+Date.now()+':'+r.ingredients.length,label,role:'scene_detail',kind:button.dataset.addIngredient,required:true,status:button.dataset.addIngredient==='reference'?'missing':'unreviewed',assetID:null,sha256:null,note:''}]});});
    });
  }
  function storyWorkCard(shot){
    const materials=storyMaterialLinks(shot);
    return `<article class="story-work-card" id="shot-work-${esc(shot.id)}"><p class="eyebrow">${esc(shot.id)} · ${esc(shot.sectionLabel||'Placement pending')}</p><h3>${esc(shot.title)}</h3><p class="story-work-next"><strong>Next · ${esc(shot.nextStep?.owner||'CFA')}</strong><br>${esc(shot.nextStep?.action||'Review material and choose the next task.')}</p>${materials?`<ul class="story-materials">${materials}</ul>`:'<p class="muted">No production material linked yet.</p>'}${sceneReadinessControls(shot)}<details><summary>Progress & placement</summary><ol class="story-pipeline">${(shot.pipeline||[]).map(p=>`<li><strong>${esc(p.label)}</strong><span>${esc(String(p.status||'pending').replace(/_/g,' '))}</span>${p.note?`<p>${esc(p.note)}</p>`:''}</li>`).join('')}</ol><p class="review-help">${esc(shot.note||'')} ${esc(shot.acceptance==='accepted'?'Accepted for the recorded scope.':'Shot acceptance is still open.')}</p><div class="tools">${(shot.panelAssetIDs||[]).map(id=>byID.get(id)).filter(normalVisible).map(a=>`<button class="pill" data-open="${esc(a.id)}">${esc(a.sceneID||a.title)}</button>`).join('')}</div></details></article>`;
  }
  function storyProgress(cards){
    const visible=new Set(cards.map(a=>a.id)),all=storyWorkItems(),mapped=all.filter(s=>!s.independentSequenceID&&(s.panelAssetIDs||[]).some(id=>visible.has(id))),unplaced=all.filter(s=>!(s.panelAssetIDs||[]).length||s.independentSequenceID);
    let html=`<section class="story-progress-section"><h2>Shot progress</h2><p class="intro">${mapped.length} shot plans linked to these panels. Open the existing material before commissioning more. Steps can be skipped when usable footage already exists.</p><div class="story-work-grid">${mapped.map(storyWorkCard).join('')}</div>`;
    if(!mapped.length)html+='<p class="empty">No shot-progress records are linked to this range yet.</p>';
    if(unplaced.length)html+=`<details class="detail-drawer"><summary>Placement still needed · ${unplaced.length}</summary><div class="story-work-grid">${unplaced.map(storyWorkCard).join('')}</div></details>`;
    const pending=(C.shotMaterials?.pendingIntake||[]).filter(item=>item.project===state.project);
    if(pending.length)html+=`<details class="detail-drawer"><summary>Returned packages · ${pending.length}</summary>${pending.map(item=>`<p>${esc((item.reportedPackets||[]).join(' · '))}</p><p class="muted">${esc(String(item.status||'pending').replace(/_/g,' '))}</p><p><strong>Next · ${esc(item.nextStep?.owner||'CFA')}</strong><br>${esc(item.nextStep?.action||'Verify the returned files, then link them to the affected shots.')}</p><p class="review-help">${esc(item.note||'')}</p>`).join('')}</details>`;
    return html+'</section>';
  }
  function storyConnections(a){
    const shots=storyWorkForAsset(a);if(!shots.length)return '';
    return `<section class="story-connections"><h3>Storyboard connections</h3>${shots.map(s=>`<details><summary>${esc(s.sectionLabel||s.id)} · ${esc(s.title)}</summary><p><strong>Next · ${esc(s.nextStep?.owner||'CFA')}</strong><br>${esc(s.nextStep?.action||'Review placement.')}</p><ul class="story-materials">${storyMaterialLinks(s,a.id)}</ul>${sceneReadinessControls(s)}<button class="pill" data-story-shot="${esc(s.id)}" data-story-project="${esc(s.project)}">Open shot progress</button></details>`).join('')}<p class="review-help">Candidate connections; placement and acceptance are tracked per shot.</p></section>`;
  }
  function storySequenceGroups(media=projectAssets()){
    const definitions=(C.storyboardSequences||[]).filter(s=>(!state.album||(s.sourceAlbumIDs||[]).includes(state.album))&&(state.view!=='storyboard'||!state.storyStage||state.storyStage==='all'||s.stage===state.storyStage));
    return collectionGroups(definitions,media);
  }
  function storySequenceSection(media=projectAssets()){
    const groups=storySequenceGroups(media);if(!groups.length)return '';
    return `<section class="story-independent-sequences"><h2>Separate scene drafts</h2><p class="intro">Each scene keeps its own panel order, look reference and earlier alternatives. Music placement is open; the main panel-range slider does not filter these drafts.</p>${collectionCards(groups)}</section>`;
  }
  function storyboardExplorer(media){
    const sequenceAlbums=new Set((C.storyboardSequences||[]).filter(s=>s.project===state.project).flatMap(s=>s.sourceAlbumIDs||[]));
    if(state.album&&sequenceAlbums.has(state.album))return storySequenceSection(media)||'<p class="empty">No scene drafts match this search and stage.</p>';
    const albums=C.albums.filter(al=>al.project===state.project&&al.category==='storyboard'&&!sequenceAlbums.has(al.id)&&(!state.album||al.id===state.album)),ids=new Set(albums.flatMap(al=>al.assetIDs)),all=media.filter(a=>ids.has(a.id));
    const position=a=>typeof a.storyboardPosition==='number'&&Number.isFinite(a.storyboardPosition)?a.storyboardPosition:null;
    const ranged=all.filter(a=>(!state.storyStage||state.storyStage==='all'||storyboardStage(a)===state.storyStage)&&(position(a)===null?state.storyStart===0&&state.storyEnd===100:position(a)>=state.storyStart&&position(a)<=state.storyEnd));
    const themes=new Map(ranged.flatMap(storyThemes).map(t=>[t.id,t.title]));if(state.storyTheme!=='all'&&!themes.has(state.storyTheme))state.storyTheme='all';
    const cards=ranged.filter(a=>state.storyTheme==='all'||storyThemes(a).some(t=>t.id===state.storyTheme)).sort((a,b)=>(a.storyboardOrder??Infinity)-(b.storyboardOrder??Infinity)||clipTitleOrder.compare(a.title,b.title));
    const meta=Array.isArray(C.storyboardMetadata)?C.storyboardMetadata.find(m=>m.project===state.project):C.storyboardMetadata?.[state.project];
    let html=`<section class="story-controls"><div class="story-stage"><label for="story-stage">Stage</label><select id="story-stage"><option value="all">All stages</option>${Object.entries(storyboardStages).map(([id,label])=>`<option value="${id}" ${state.storyStage===id?'selected':''}>${label}</option>`).join('')}</select></div><div class="story-theme"><label for="story-theme">Theme</label><select id="story-theme"><option value="all">All themes in this range</option>${[...themes].map(([id,title])=>`<option value="${esc(id)}" ${state.storyTheme===id?'selected':''}>${esc(title)}</option>`).join('')}</select></div><div class="story-range"><label for="story-start">From <output>${state.storyStart}%</output><input id="story-start" type="range" min="0" max="100" step="5" value="${state.storyStart}" aria-label="Start of source panel range"></label><label for="story-end">To <output>${state.storyEnd}%</output><input id="story-end" type="range" min="0" max="100" step="5" value="${state.storyEnd}" aria-label="End of source panel range"></label><button class="pill" id="story-reset">Full storyboard</button></div><p class="review-help">Source panel order, not song seconds. ${esc(meta?.timingStatus||'Song timing has not been aligned.')} Themes update with the selected range.</p></section><p class="video-sort-note">${cards.length} matching panels · ${themes.size} available themes in this range</p>`;
    const hasProgress=storyWorkItems().length>0;
    if(hasProgress)html+=`<div class="tools story-view-switch" aria-label="Storyboard view">${[['panels','Panels'],['progress','Shot progress']].map(([id,label])=>`<button class="pill" data-story-layout="${id}" aria-pressed="${(state.storyLayout||'panels')===id}">${label}</button>`).join('')}</div>`;
    if(hasProgress&&state.storyLayout==='progress')html+=storyProgress(cards);
    else html+=mediaGroup('Story panels','In source panel order. Open a panel for linked material and its next step.',cards);
    if(!cards.length)html+='<p class="empty">No panels match this range and theme.</p>';return html+storySequenceSection(media);
  }
  const missionProviders=[['Grok','Grok'],['Gemini','Gemini'],['Flow','Flow'],['PanhandlerNova','Claude / Pan_Handlers']];
  const missionProject=t=>C.projects.find(p=>p.id===t.project)?.name||'Across projects';
  const missionStatuses={ready:'Ready to send',needs_input:'Needs your input',planned:'Planned',in_progress:'In progress',done:'Done'};
  function providerKey(value){const key=String(value||'').toLowerCase().replace(/[^a-z]/g,'');if(key==='claude')return 'PanhandlerNova';return [...missionProviders,...(C.providerScorecards?.providers||[]).map(p=>[p.id,p.name])].find(([id])=>id.toLowerCase().replace(/[^a-z]/g,'')===key)?.[0]||'';}
  function safeMissionHref(value){
    if(typeof value!=='string'||!value.trim())return '';let decoded;
    try{decoded=decodeURIComponent(value.trim());}catch{return '';}
    if(/[\x00-\x1f\x7f\\]/.test(decoded)||/^(?:[a-z][a-z0-9+.-]*:|\/)/i.test(decoded))return '';
    try{const target=new URL(value,base);return target.protocol===base.protocol&&target.origin===base.origin?target.href:'';}catch{return '';}
  }
  function missionLinkGroup(asset,url){
    if(asset)return asset.kind==='image'?'images':asset.kind==='video'?'videos':isDoc(asset)?'reading':'other';
    const target=new URL(url),path=target.pathname.toLowerCase(),view=target.hash.slice(1).split('/')[1];
    if(/\.(?:png|jpe?g|webp|gif|svg|avif)$/.test(path)||['outfits','details','cast','storyboard'].includes(view))return 'images';
    if(/\.(?:mp4|webm|mov|m4v)$/.test(path)||view==='videos')return 'videos';
    if(/\.(?:txt|md|json|csv|tsv|pdf)$/.test(path))return 'reading';
    return /\.zip$/.test(path)?'downloads':'other';
  }
  function missionTaskLinks(task){
    const groups=new Map([['images','View images'],['videos','View video'],['reading','Read briefs and records'],['downloads','Download packages'],['other','Other links']].map(([id,label])=>[id,{label,links:[]}]));
    for(const link of Array.isArray(task.links)?task.links:[]){
      const asset=byID.get(link.assetID),url=asset?'':safeMissionHref(link.href);if(!asset&&!url)continue;
      const group=missionLinkGroup(asset,url),html=asset?`<button class="pill" data-open="${esc(link.assetID)}">${esc(link.label||'Open reference')}</button>`:`<a class="pill" href="${esc(url)}" ${/\.zip(?:[?#]|$)/i.test(url)?'download':''} target="_blank" rel="noopener">${esc(link.label||'Open prepared file')} ↗</a>`;
      groups.get(group).links.push(html);
    }
    const sections=[...groups].filter(([,group])=>group.links.length).map(([id,group])=>`<section class="mission-resource-group" data-resource-group="${id}"><h4>${group.label}</h4><div class="tools">${group.links.join('')}</div></section>`).join('');
    return sections?`<div class="mission-resources">${sections}</div>`:'';
  }
  function missionTaskCard(t){return `<details class="mission-task" ${['ready','needs_input'].includes(t.status)?'open':''}><summary><span class="mission-status ${esc(t.status)}">${esc(missionStatuses[t.status]||'Planned')}</span><b>${esc(t.title)}</b><small class="mission-project">${esc(missionProject(t))}</small></summary><p>${esc(t.summary||'')}</p>${t.nextAction?`<p class="mission-next-action"><strong>Next:</strong> ${esc(t.nextAction)}</p>`:''}${Array.isArray(t.missing)&&t.missing.length?`<div class="mission-missing"><strong>Still needed</strong><ul>${t.missing.map(item=>`<li>${esc(item)}</li>`).join('')}</ul></div>`:''}${missionTaskLinks(t)}</details>`;}
  function workflowReferences(title,ids){
    const references=(Array.isArray(ids)?ids:[]).map(id=>byID.get(id)).filter(a=>normalVisible(a)&&(title!=='Source references'||exportAllowed(a)));if(!references.length)return '';
    return `<section class="workflow-references"><h3>${esc(title)}</h3><div class="workflow-reference-grid">${references.map(a=>{if(!isDoc(a)&&!displayed.includes(a.id))displayed.push(a.id);return `<button data-open="${esc(a.id)}" class="workflow-reference">${!isDoc(a)?`<img loading="lazy" src="${esc(href(a.thumb))}" alt="">`:''}<span>${esc(a.title)}</span></button>`;}).join('')}</div></section>`;
  }
  function safeComfyURL(value){try{const url=new URL(value);return url.protocol==='https:'&&url.hostname==='cloud.comfy.org'&&!url.username&&!url.password&&!url.port?url.href:'';}catch{return '';}}
  function collaboratorFileLink(label,path){const url=safeMissionHref('../../../../../../'+String(path||''));return path&&url?`<a class="pill" href="${esc(url)}" target="_blank" rel="noopener">${esc(label)} ↗</a>`:'';}
  function collaboratorWorkLink(link){if(link?.path)return collaboratorFileLink(link.label||'Open file',link.path);try{const url=new URL(link?.url);return url.protocol==='https:'?`<a class="pill" href="${esc(url.href)}" target="_blank" rel="noopener">${esc(link.label||'Open resource')} ↗</a>`:'';}catch{return '';}}
  function collaboratorProfile(id){
    const roster=C.providerScorecards||{},p=(roster.providers||[]).find(p=>p.id===id);if(!p)return '';
    const list=value=>Array.isArray(value)?value.filter(v=>typeof v==='string'):typeof value==='string'&&value?[value]:[];
    const self=p.selfReported||{},roles=roster.roleDefinitions||[],metrics=roster.metricDefinitions||[];
    const roleName=value=>roles.find(r=>r.id===value)?.label||String(value||'Unassigned role').replace(/_/g,' ');
    const excerpt=typeof self.summary==='string'?self.summary:typeof p.identity?.summary==='string'?p.identity.summary:'';
    let html=`<section class="collaborator-profile" data-collaborator-profile="${esc(p.id)}"><p class="eyebrow">Collaborator profile</p><h2>${esc(p.name)}</h2><p>${esc(p.currentRole||'No current role assigned.')}</p><p class="muted">${esc(p.availability||'Current availability is unconfirmed.')}</p><div class="tools">${p.identity?.path?collaboratorFileLink('Read authored I_AM',p.identity.path):''}${collaboratorFileLink('Mailbox guide','docs/notes/explorable_world/comfy/projects/collaborators/MAILBOX.md')}${collaboratorFileLink('Mailbox registry','docs/notes/explorable_world/comfy/projects/collaborators/mailbox/registry.json')}${(p.workLinks||[]).map(collaboratorWorkLink).join('')}</div>${p.identity?.sha256?`<details><summary>Identity provenance</summary><p class="filename">${esc(p.identity.path)}<br>SHA-256 ${esc(p.identity.sha256)}</p></details>`:''}<p class="review-help">Communication: ${esc(p.communication?.route||'Unverified')} · ${esc(p.communication?.status||'Unknown')}. ${esc(p.communication?.note||'')}</p>`;
    html+=`<section class="collaborator-self-report"><h3>In their own introduction</h3><p class="review-help">${esc(self.basis||'No authored self-report is supplied.')}</p>${excerpt?`<blockquote>${esc(excerpt)}</blockquote>`:'<p class="muted">Read the authored introduction above. A concise self-description has not been supplied here.</p>'}${[['strengths','Self-reported strengths'],['limitations','Self-reported limits'],['preferences','Self-reported preferences']].map(([key,label])=>`<h4>${label}</h4>${list(self[key]).length?`<ul>${list(self[key]).map(v=>`<li>${esc(v)}</li>`).join('')}</ul>`:'<p class="muted">Not reported in this profile.</p>'}`).join('')}<p class="review-help">Preferred creative roles: ${esc(list(self.preferredCreativeRoles).map(roleName).join(', ')||'Not reported')}. Benchmark participation: ${esc(String(self.benchmarkWillingness||'Not reported').replace(/_/g,' '))}.</p><p class="review-help">Self-description is kept separate from observed capability and production results.</p></section>`;
    html+=`<section class="collaborator-capabilities"><h3>Recorded capability evidence</h3><p>${esc(p.capabilities?.summary||'No observed capability is recorded yet.')}</p><p class="muted">Basis: ${esc(p.capabilities?.basis||'Unverified')}. These observations do not establish an earned filmmaking grade.</p></section>`;
    html+=`<section class="collaborator-scorecards"><h3>Role scorecards</h3><p class="review-help">Roles rotate through real production work. Quality, consistency, speed, rework, cost and tool access are measured separately. Ready character parts do not mean a ready scene.</p><div class="role-scorecards">${(p.scorecards||[]).map(card=>`<article><h4>${esc(roleName(card.category))} <span class="role-grade">${esc(card.grade||'Ungraded')}</span></h4><p class="muted">${esc(card.status==='human_assessment'?'Human assessment':'No assessed result')}${card.assessedBy?' · '+esc(card.assessedBy):''}${card.assessmentDate?' · '+esc(card.assessmentDate):''}</p><p>${esc(card.note||'No production result has been assessed for this role.')}</p>${(card.evidenceRefs||[]).length?`<details><summary>Assessment evidence</summary>${card.evidenceRefs.map(ref=>typeof ref==='string'?`<p>${esc(ref)}</p>`:collaboratorWorkLink(ref)).join('')}</details>`:''}<ul class="metric-status">${metrics.map(metric=>{const value=card.metrics?.[metric.id];return `<li>${esc(metric.label||metric.id)}: ${esc(value==null?'Not measured':typeof value==='string'||typeof value==='number'?value:'Recorded in assessment evidence')}</li>`;}).join('')}</ul></article>`).join('')||'<p class="muted">No role assessments recorded.</p>'}</div></section>`;
    html+=`<details class="collaborator-roles"><summary>Roles · what each review covers</summary><p class="review-help">Use a writer, director, cinematographer and the other roles needed for the particular scene. These descriptions do not assign a model permanent superiority.</p><div class="role-definitions">${roles.map(role=>`<article><h4>${esc(role.label)}</h4><p>${esc(role.check||role.description||'')}</p></article>`).join('')}</div><div class="tools">${collaboratorFileLink('Shared roles brief',roster.rolesBriefPath)}${collaboratorFileLink('Shoot plan verification','docs/notes/explorable_world/comfy/projects/collaborators/work_briefs_20261010/SHOOT_PLAN_VERIFICATION.txt')}</div><p class="review-help">Production handoff targets B or better, reviewed required scene ingredients, no critical blockers and a verified shoot plan. Final result acceptance remains separate.</p></details>`;
    return html+'</section>';
  }
  function collaboratorsWorkspace(){
    const configured=C.providerScorecards?.providers||[],providers=configured.length?configured.map(p=>[p.id,p.name]):[['ComfyUI','ComfyUI'],['Flow','Flow'],['Gemini','Gemini'],['Grok','Grok'],['PanhandlerNova','Claude / Pan_Handlers']];
    const selected=state.collaborator,providerName=providers.find(([id])=>id===selected)?.[1]||'ComfyUI',query=state.search.toLowerCase().trim();
    let html=`<div class="tools collaborator-tabs" role="group" aria-label="Choose collaborator">${providers.map(([id,label])=>`<button class="pill ${selected===id?'active':''}" aria-pressed="${selected===id}" data-collaborator-provider="${esc(id)}">${esc(label)}</button>`).join('')}</div>`;
    if(selected==='ComfyUI'){
      const workflows=(Array.isArray(C.productionWorkflows)?C.productionWorkflows:[]).filter(w=>w.provider==='ComfyUI'&&[w.title,w.summary,w.nextAction,missionProject(w)].join(' ').toLowerCase().includes(query));
      html+=`<div class="workflow-list">${workflows.map(w=>{const cloud=safeComfyURL(w.cloudURL);return `<article class="production-workflow"><p class="eyebrow">${esc(missionProject(w))}</p><h2>${esc(w.title)}</h2><p class="workflow-status">${esc(w.statusLabel||String(w.status||'Planned').replace(/_/g,' '))}</p><p class="intro">${esc(w.summary||'')}</p>${w.nextAction?`<p class="mission-next-action"><strong>Next:</strong> ${esc(w.nextAction)}</p>`:''}${workflowReferences('Source references',w.sourceAssetIDs)}${workflowReferences('Outputs',w.outputAssetIDs)}${workflowReferences('Workflow & notes',w.documentAssetIDs)}${cloud?`<a class="pill cloud-workflow-link" href="${esc(cloud)}" target="_blank" rel="noopener">Open saved Comfy workflow ↗</a>`:''}</article>`;}).join('')}</div>`;
      if(!workflows.length)html+='<div class="empty">No matching ComfyUI workflow is listed yet.</div>';
    } else {
      const tasks=(C.missionControl?.tasks||[]).filter(t=>providerKey(t.provider)===selected&&[t.title,t.summary,t.nextAction,missionProject(t)].join(' ').toLowerCase().includes(query));
      html+=`<section class="collaborator-work"><h2>${esc(providerName)}</h2>${tasks.map(missionTaskCard).join('')}</section>`;
      const plans=C.assets.filter(a=>normalVisible(a)&&reviewRecord(a.id).shotPlan?.destinations.includes(selected)&&queryMatch(a));
      if(plans.length){html+=mediaGroup('Draft shot queue','Planned here; attach the actual files when you send your handoff.',plans.filter(a=>!isDoc(a)));html+=`<div class="tools"><button class="pill" data-mission-export="${selected}">Export ${esc(providerName)} shot handoff</button></div>`;}
      if(selected==='PanhandlerNova')html+='<div class="tools"><button class="pill" data-mission-export="PanhandlerNova">Export review for Claude</button></div>';
      if(!tasks.length){const briefs=C.assets.filter(a=>isDoc(a)&&/collaborator/i.test(a.album||'')&&(a.album+' '+a.title).toLowerCase().includes(providerName.toLowerCase())&&queryMatch(a));html+=documentGroups(briefs);if(!briefs.length&&!plans.length)html+='<p class="notice">No matching work card is listed here. Use the recorded work links and mailbox route below for the next bounded task.</p>';}
    }
    return html+collaboratorProfile(selected);
  }
  function missionControl(){
    const board=C.missionControl||{}, rank={ready:0,needs_input:1,in_progress:2,planned:3,done:4};
    const tasks=(Array.isArray(board.tasks)?board.tasks:[]).map(t=>({...t,status:Object.hasOwn(missionStatuses,t.status)?t.status:'planned'})).sort((a,b)=>rank[a.status]-rank[b.status]);
    const query=state.search.toLowerCase().trim(),visible=tasks.filter(t=>[t.provider,t.title,t.summary,t.nextAction,...(Array.isArray(t.missing)?t.missing:[])].join(' ').toLowerCase().includes(query));
    const assets=C.assets,queued=assets.filter(inReviewQueue),plans=assets.filter(a=>normalVisible(a)&&reviewRecord(a.id).shotPlan),count=status=>tasks.filter(t=>t.status===status).length;
    let html=`<div class="mission-counts">${[['Ready to send',count('ready')],['Needs your input',count('needs_input')],['In progress',count('in_progress')],['Shot plans',plans.length]].map(([label,n])=>`<div><strong>${n}</strong><span>${label}</span></div>`).join('')}</div><p class="mission-note">Tasks cover all projects and come from the prepared board. Review choices and shot plans reflect this browser; they have not been sent to a collaborator.</p><section class="mission-next"><h2>Current work</h2><button class="pill review-sweep" id="prepare-review-sweep">Prepare review sweep</button><p class="mission-note">Save your review, favorites, stages and reference roles, then ask Nova to run the sweep. This button does not start Codex or delete files.</p><p id="review-sweep-status" role="status"></p>${visible.filter(t=>t.status!=='done').slice(0,3).map(t=>`<div class="mission-next-row"><span class="mission-status ${t.status}">${esc(missionStatuses[t.status])}</span><div><b>${esc(t.title)}</b><small class="mission-project">${esc(missionProject(t))}</small><p>${esc(t.nextAction||t.summary||'Open the handoff below for the next step.')}</p></div></div>`).join('')||'<p>Choose a reference and plan a shot, or add a review note to shape the next pass.</p>'}<div class="tools"><button class="pill" data-mission-view="review_queue">Review ${esc(C.projects.find(p=>p.id===state.project)?.name)} · ${projectAssets(true).filter(inReviewQueue).length}</button><button class="pill" data-mission-view="shot_plans">This project’s shot plans · ${projectAssets().filter(a=>reviewRecord(a.id).shotPlan).length}</button><button class="pill" data-mission-view="all">Browse the library</button></div></section><div class="section-head"><h2>Collaborator handoffs</h2></div><div class="mission-providers">`;
    for(const [id,name] of missionProviders){
      const work=visible.filter(t=>providerKey(t.provider)===id), planned=plans.filter(a=>reviewRecord(a.id).shotPlan.destinations.includes(id));
      html+=`<article class="mission-provider"><h3>${name}</h3><p class="mission-provider-count">${work.length} prepared ${work.length===1?'task':'tasks'}${id==='PanhandlerNova'?` · ${queued.length} review items`:` · ${planned.length} planned shots`}</p>${work.map(missionTaskCard).join('')||'<p class="mission-note">No prepared handoff listed yet.</p>'}${id==='PanhandlerNova'?`<button class="pill" data-mission-export="${id}">Export review for Claude</button>`:planned.length?`<button class="pill" data-mission-export="${id}">Export ${name} shot handoff</button>`:''}</article>`;
    }
    html+='</div>';const undecided=plans.filter(a=>reviewRecord(a.id).shotPlan.destinations.includes('undecided')).length;
    if(undecided)html+=`<p class="notice">${undecided} shot ${undecided===1?'idea still needs':'ideas still need'} a destination. You can keep exploring before choosing a collaborator.</p>`;
    if(board.updated)html+=`<p class="mission-note">Prepared board updated ${esc(board.updated)}. A prepared handoff is ready for you to send; this library does not send it automatically.</p>`;
    return html;
  }
  function renderMain(){
    displayed=[];const p=C.projects.find(p=>p.id===state.project);const all=projectAssets(state.view==='review_queue').filter(queryMatch);const docs=all.filter(isDoc);const media=all.filter(a=>!isDoc(a));
    const heading=state.album?C.albums.find(a=>a.id===state.album)?.title:cats[state.view]||{mission_control:'Mission Control',collaborators:'Collaborators',all:p.name+' reference library',favorites:'Your favorites',export_basket:'Export basket',review_queue:'Review queue',shot_plans:'Shot plans',documents:'Documents & notes'}[state.view];
    let html=`<p class="eyebrow">${esc(p.subtitle)}</p><div class="library-heading"><h1>${esc(heading)}</h1>${state.view==='videos'?`<div class="video-controls"><label class="video-sort" for="video-layout"><span>Layout</span><select id="video-layout"><option value="grouped" ${state.videoLayout==='grouped'?'selected':''}>Grouped</option><option value="all" ${state.videoLayout==='all'?'selected':''}>All clips</option></select></label><label class="video-sort" for="video-sort"><span>Sort</span><select id="video-sort">${Object.entries(videoSortLabels).map(([value,label])=>`<option value="${value}" ${state.videoSort===value?'selected':''}>${label}</option>`).join('')}</select></label></div>`:''}</div><p class="intro">${state.view==='collaborators'?'Workflows, source references, and prepared handoffs across your projects.':state.view==='mission_control'?'Your next moves, prepared handoffs, and ideas waiting for their next pass.':state.view==='all'?'Artwork first, grouped by purpose. Open a cover to browse its references here; select an image inside to review it.':state.view==='export_basket'?'A separate selection from across all projects. Add or remove references with ⇩; your favorites stay unchanged. The export is a file list, not a media bundle.':state.view==='favorites'?'Your review shortlist. These stars do not change the character locks or original files.':state.view==='shot_plans'?'Collect shot ideas and draft prompts, then export a handoff for your chosen collaborator. These plans have not been sent or generated.':state.view==='review_queue'?'Needs-fix notes and removal requests gathered for the next sorting pass. Source files remain in place.':state.view==='details'?'Standalone artwork first. Placement examples are inside each item.':state.view==='documents'?'Notes are grouped by subject. Click a file to read a preview without leaving the library.':'Choose a group or browse the previews below.'}</p>`;
    if(['mission_control','collaborators'].includes(state.view)){const back=libraryReturn();html=`<a class="library-back" href="#${[back.project,back.view,back.album].filter(Boolean).map(encodeURIComponent).join('/')}">← Back to library</a>`+html;}
    if(!storageOK)html+='<p class="notice">Browser storage is unavailable. Export your review to keep decisions, notes, and favorites.</p>';
    if(state.album)html+=`<p><button class="subtle-button" id="back-group">← Back to ${esc(cats[state.view]||'all files')}</button></p>`;
    if(state.view==='mission_control')html+=missionControl()+documentGroups(docs);
    else if(state.view==='collaborators')html+=collaboratorsWorkspace();
    else if(state.view==='export_basket'){
      const selected=basketAssets().filter(queryMatch);html+=`<div class="tools"><span>${selected.length} references shown · ${basketAssets().length} in basket</span><button class="pill" id="export-basket-list" ${basket.size?'':'disabled'}>Export selection list</button><button class="pill" id="clear-basket" ${basket.size?'':'disabled'}>Clear basket</button></div><p class="notice">Imports add matching references to this basket. Clearing it only clears this selection; it does not change stars, review notes, or files.</p>`;
      html+=mediaGroup('Selected pictures & clips','References from all projects, ready for your next package.',selected.filter(a=>!isDoc(a)));html+=documentGroups(selected.filter(isDoc));if(!selected.length)html+='<div class="empty">Your basket is empty, or no selections match the search. Use ⇩ on a preview to collect a subset.</div>';
    } else if(state.view==='favorites'){

      const fav=media.filter(a=>favorites.has(a.id));html+=fav.length?`<div class="tools"><span>${fav.length} selected</span><button class="pill" id="export-main">Export favorites</button></div><div class="gallery">${fav.map(card).join('')}</div>`:'<div class="empty">No favorites yet. Click ☆ on an image or video to add it here.</div>';
    } else if(state.view==='shot_plans'){
      const plans=all.filter(a=>reviewRecord(a.id).shotPlan&&(state.destination==='all'||reviewRecord(a.id).shotPlan.destinations.includes(state.destination)));
      html+=`<div class="tools"><label for="plan-destination">Destination</label><select id="plan-destination">${['all',...destinations].map(d=>`<option value="${d}" ${state.destination===d?'selected':''}>${esc(d==='all'?'All collaborators':d==='undecided'?'Undecided':d)}</option>`).join('')}</select><button class="pill" id="export-handoff-txt">Export handoff TXT</button><button class="pill" id="export-handoff-json">Export handoff JSON</button></div><p class="notice">Handoffs include exact reference IDs and filenames, plus your notes and prompt. Attach the actual images or clips yourself; media files are not bundled in the export.</p>`;
      html+=mediaGroup('Planned shots','Open a reference to refine its idea, prompt, or destinations.',plans.filter(a=>!isDoc(a)));
      html+=documentGroups(plans.filter(isDoc));if(!plans.length)html+='<div class="empty">No shots planned here yet. Open a reference and choose Plan a shot.</div>';
    } else if(state.view==='review_queue'){
      const queued=all.filter(inReviewQueue), promotions=queued.filter(a=>reviewRecord(a.id).workingReference?.status==='requested'), fixes=queued.filter(a=>reviewRecord(a.id).status==='needs_fixes'), removals=queued.filter(a=>a.archived||reviewRecord(a.id).status==='remove');
      html+=`<div class="tools"><span>${fixes.length} need fixes · ${removals.length} marked for removal</span><button class="pill" id="export-review-main">Export review</button></div>`;
      if(promotions.length)html+=`<details class="detail-drawer"><summary>Earlier saved reference requests · ${promotions.length}</summary>${mediaGroup('Earlier requests','Preserved from the previous controls. Production and the reference role now describe approved use.',promotions.filter(a=>!isDoc(a)))}</details>`;
      html+=mediaGroup('Needs fixes','Open a reference to read or update the correction note.',fixes.filter(a=>!isDoc(a)));
      html+=mediaGroup('Marked for removal','Queued for a later sorting pass. Nothing has been deleted.',removals.filter(a=>!isDoc(a)));
      html+=documentGroups(queued.filter(isDoc));if(!queued.length)html+='<div class="empty">Your review queue is clear. Open a reference and choose Needs fixes or Mark for removal to add it.</div>';
    } else if(state.view==='working')html+=workingReferencesWorkspace();
    else if(state.view==='documents')html+=documentGroups(docs);
    else if(state.view==='details'&&state.detailLayout!=='all')html+=detailExplorer();
    else if(state.view==='outfits'&&!state.album)html+=outfitExplorer(media);
    else if(state.view==='cast'&&!state.album)html+=castExplorer();
    else if(state.view==='storyboard')html+=storyboardExplorer(media);
    else if(state.view==='all'&&!state.album&&C.browseLayout?.projects?.[state.project])html+=compactAllFiles(projectAssets())+documentGroups(docs);
    else {
      let albums=C.albums.filter(a=>a.project===state.project&&(state.view==='all'||a.category===state.view)&&(!state.album||a.id===state.album));
      if(state.view==='storyboard')html+='<p class="notice">Story ideas grouped by beat. Panel numbers identify the source; song timings are still to be aligned.</p>';
      if(state.view==='details')html+=detailExplorer()+'<p class="notice">Use each reference for its selected detail. A tattoo or piercing example does not replace the whole character.</p>';
      if(state.view!=='all'&&!state.album&&albums.length>1)html+=`<div class="video-filter">${albums.map(a=>`<button class="pill" data-album="${esc(a.id)}">${esc(a.title)}</button>`).join('')}</div>`;
      const categoryOrder=Object.keys(cats);
      albums.sort((a,b)=>categoryOrder.indexOf(a.category)-categoryOrder.indexOf(b.category));
       let shown=0,outfitsShown=false,castShown=false,sequencesShown=false;
       const sequenceAlbumIDs=new Set((C.storyboardSequences||[]).filter(s=>s.project===state.project).flatMap(s=>s.sourceAlbumIDs||[]));
       const sharedAlbumIDs=new Set(sharedCharacterAlbums().map(al=>al.id));
      if(state.view==='videos'&&state.videoLayout==='all'){
        const ids=new Set(albums.flatMap(a=>a.assetIDs)),clips=sortClips(media.filter(a=>isClip(a)&&ids.has(a.id)));shown=clips.length;
        html+=`<p class="video-sort-note">${clips.length} matching clips · ${esc(videoSortLabels[state.videoSort])}${state.videoSort==='alphabetical'?' by clip title':'; unknown durations last'}. Collection names stay on the cards.</p>`;
        html+=mediaGroup(state.album?'Sorted clips':'All matching clips','',clips);
      } else {
        if(state.view==='videos'){
          const turnaround=album=>Number(/turnaround/i.test(album.id+' '+album.title));
          albums.sort((a,b)=>turnaround(a)-turnaround(b));html+=`<p class="video-sort-note">${esc(videoSortLabels[state.videoSort])} within each collection${state.videoSort==='alphabetical'?'':'; unknown durations last'}. ${state.album?'Showing this collection only.':'Turnaround studies stay at the end.'}</p>`;
        }
         const visibleIDs=new Set(media.map(a=>a.id));
         for(const al of albums){
           if(state.view==='all'&&sequenceAlbumIDs.has(al.id)){
             if(!sequencesShown){const groups=storySequenceGroups(media);shown+=groups.reduce((n,g)=>n+g.items.length,0);html+=storySequenceSection(media);sequencesShown=true;}continue;
           }
           if(state.view==='all'&&!state.album&&al.category==='outfits'){
             if(!outfitsShown){const groups=outfitGroups(media);shown+=groups.reduce((n,g)=>n+g.items.length,0);html+=outfitExplorer(media);outfitsShown=true;}
             continue;
           }
           if(state.view==='all'&&!state.album&&al.category==='cast'){
             if(!castShown){html+=castExplorer();castShown=true;shown+=media.filter(a=>a.category==='cast').length;}continue;
           }
           if(state.view==='all'&&!state.album&&sharedAlbumIDs.has(al.id)){
             if(!outfitsShown&&!albums.some(a=>a.category==='outfits')){html+=sharedCharacterReferences();outfitsShown=true;}
             shown+=al.assetIDs.filter(id=>visibleIDs.has(id)).length;continue;
           }
          const items=state.view==='videos'?sortClips(al.assetIDs.map(id=>byID.get(id)).filter(a=>a&&isClip(a)&&visibleIDs.has(a.id))):media.filter(a=>state.view==='all'?a.album===al.id:al.assetIDs.includes(a.id));
          if(!items.length)continue;
          shown+=items.length;
           if(state.view==='outfits'&&state.album)html+=sharedCharacterReferences();
           if(state.view==='outfits'&&state.album&&items.some(a=>a.propState==='with_gun')){
            html+=mediaGroup('Gun variants','Received candidates. Compare side placement, clothing and character details with the source.',items.filter(a=>a.propState==='with_gun'));
            html+=mediaGroup('Other views & revisions',al.description,items.filter(a=>a.propState!=='with_gun'));
          } else if(state.view==='all'&&!state.album&&al.category==='details')html+=detailAlbumGroups(al,items);
          else html+=mediaGroup(al.title,state.view==='all'?'':al.description,items,al.id);
        }
      }
      if(!shown&&!html.includes('data-collection='))html+='<div class="empty">No matching previews. Try another category or search.</div>';
      if(state.view==='all'&&!state.album)html+=documentGroups(docs);
    }
    document.querySelector('#main').innerHTML=html;
    document.querySelectorAll('[data-open]').forEach(b=>b.onclick=()=>openViewer(b.dataset.open));
    document.querySelectorAll('[data-favorite]').forEach(b=>b.onclick=()=>toggleFavorite(b.dataset.favorite));
    document.querySelectorAll('[data-basket]').forEach(b=>b.onclick=()=>toggleBasket(b.dataset.basket));
    document.querySelector('#export-basket-list')?.addEventListener('click',exportBasket);document.querySelector('#clear-basket')?.addEventListener('click',()=>{basket.clear();saveBasket();notice('Export basket cleared. Favorites and review notes are unchanged.');});
     document.querySelectorAll('[data-album]').forEach(b=>b.onclick=()=>{const a=C.albums.find(x=>x.id===b.dataset.album);route(state.project,a.category,a.id);});
     document.querySelectorAll('[data-outfit-layout]').forEach(button=>button.onclick=()=>{state.outfitLayout=button.dataset.outfitLayout==='all'?'all':'compact';renderMain();});
     document.querySelectorAll('[data-outfit-toggle]').forEach(button=>button.onclick=()=>{
       const id=button.dataset.outfitToggle,top=button.getBoundingClientRect().top;
       expandedOutfits.has(id)?expandedOutfits.delete(id):expandedOutfits.add(id);renderMain();
       const replacement=[...document.querySelectorAll('[data-outfit-toggle]')].find(b=>b.dataset.outfitToggle===id);
       if(replacement){window.scrollBy({top:replacement.getBoundingClientRect().top-top,behavior:'instant'});replacement.focus({preventScroll:true});}
     });
    document.querySelectorAll('[data-collection-toggle]').forEach(button=>button.onclick=()=>{
      const id=button.dataset.collectionToggle,top=button.getBoundingClientRect().top,isCover=button.classList.contains('media-open');
      expandedCollections.has(id)?expandedCollections.delete(id):expandedCollections.add(id);renderMain();
      const replacement=[...document.querySelectorAll('[data-collection-toggle]')].find(b=>b.dataset.collectionToggle===id&&b.classList.contains('media-open')===isCover);
      if(replacement){window.scrollBy({top:replacement.getBoundingClientRect().top-top,behavior:'instant'});replacement.focus({preventScroll:true});}
    });
    document.querySelectorAll('[data-browse-bucket]').forEach(button=>button.onclick=()=>{
      const id=button.dataset.browseBucket,top=button.getBoundingClientRect().top;
      collapsedBrowseBuckets.has(id)?collapsedBrowseBuckets.delete(id):collapsedBrowseBuckets.add(id);renderMain();
      const replacement=[...document.querySelectorAll('[data-browse-bucket]')].find(b=>b.dataset.browseBucket===id);
      if(replacement){window.scrollBy({top:replacement.getBoundingClientRect().top-top,behavior:'instant'});replacement.focus({preventScroll:true});}
    });
    document.querySelectorAll('[data-mission-view]').forEach(button=>button.onclick=()=>route(state.project,button.dataset.missionView));
    document.querySelectorAll('[data-collaborator-provider]').forEach(button=>button.onclick=()=>{state.collaborator=button.dataset.collaboratorProvider;renderMain();});
    document.querySelectorAll('[data-export-intent]').forEach(select=>select.onchange=()=>{state.exportIntent=select.value==='multiverse_ingredients'?'multiverse_ingredients':'prime';render();});
    document.querySelector('#prepare-review-sweep')?.addEventListener('click',prepareReviewSweep);
    document.querySelectorAll('[data-detail-layout]').forEach(button=>button.onclick=()=>{state.detailLayout=['approved','archive','all'].includes(button.dataset.detailLayout)?button.dataset.detailLayout:'approved';renderMain();});
    document.querySelectorAll('[data-detail-profile]').forEach(button=>button.onclick=()=>{state.detailProfile=button.dataset.detailProfile;renderMain();});
    document.querySelectorAll('[data-story-layout]').forEach(button=>button.onclick=()=>{state.storyLayout=button.dataset.storyLayout==='progress'?'progress':'panels';renderMain();});
    document.querySelector('#story-stage')?.addEventListener('change',e=>{state.storyStage=Object.hasOwn(storyboardStages,e.target.value)?e.target.value:'all';renderMain();});
    document.querySelector('#story-theme')?.addEventListener('change',e=>{state.storyTheme=e.target.value;renderMain();});
    document.querySelector('#story-start')?.addEventListener('change',e=>{state.storyStart=Math.min(Number(e.target.value),state.storyEnd);renderMain();});
    document.querySelector('#story-end')?.addEventListener('change',e=>{state.storyEnd=Math.max(Number(e.target.value),state.storyStart);renderMain();});
    document.querySelector('#story-reset')?.addEventListener('click',()=>{state.storyStart=0;state.storyEnd=100;state.storyTheme='all';state.storyStage='all';renderMain();});
    document.querySelectorAll('[data-mission-export]').forEach(button=>button.onclick=()=>{if(button.dataset.missionExport==='PanhandlerNova'){exportReview();return;}const previous={destination:state.destination,search:state.search};state.destination=button.dataset.missionExport;state.search='';try{exportShotHandoff('txt','all');}finally{Object.assign(state,previous);}});
    document.querySelector('#video-sort')?.addEventListener('change',e=>{state.videoSort=Object.hasOwn(videoSortLabels,e.target.value)?e.target.value:'longest';renderMain();});
    document.querySelector('#video-layout')?.addEventListener('change',e=>{state.videoLayout=e.target.value==='all'?'all':'grouped';renderMain();});
    document.querySelector('#back-group')?.addEventListener('click',()=>route(state.project,state.view));
    document.querySelector('#plan-destination')?.addEventListener('change',e=>{state.destination=e.target.value;renderMain();});
    document.querySelector('#export-handoff-txt')?.addEventListener('click',()=>exportShotHandoff('txt'));
    document.querySelector('#export-handoff-json')?.addEventListener('click',()=>exportShotHandoff('json'));
    bindSceneReadinessControls();
    document.querySelector('#export-main')?.addEventListener('click',exportFavorites);document.querySelector('#export-review-main')?.addEventListener('click',exportReview);
  }
  const dialog=document.createElement('dialog');dialog.className='viewer';dialog.setAttribute('aria-label','Media preview');document.body.append(dialog);
  function openViewer(id){
    const a=byID.get(id);if(!a)return;currentID=id;const doc=isDoc(a),connections=doc?'':storyConnections(a),i=displayed.indexOf(id);
    const media=a.kind==='video'?`<video controls playsinline preload="metadata" poster="${esc(href(a.thumb))}" src="${esc(href(a.src))}"></video>`:a.kind==='pdf'?`<iframe title="PDF preview" src="${esc(href(a.src))}"></iframe>`:a.kind==='document'?`<pre>${esc(a.text)}</pre>`:`<img src="${esc(href(a.src))}" alt="${esc(a.title)}" id="full-image">`;
    dialog.innerHTML=`<div class="viewer-body"><div class="viewer-head"><span>${doc?'Document preview':`${Math.max(i+1,1)} / ${Math.max(displayed.length,1)} · ${a.kind==='video'?'Video':'Image'} preview`}</span><div class="view-nav">${!doc?`<button id="previous" aria-label="Previous image" ${i<=0?'disabled':''}>←</button><button id="next" aria-label="Next image" ${i<0||i>=displayed.length-1?'disabled':''}>→</button>`:''}${['image','gif'].includes(a.kind)?'<button id="zoom" aria-label="Toggle full-size zoom">Zoom</button>':''}<button id="close-viewer" aria-label="Close preview">✕</button></div></div><div class="stage">${media}</div><aside class="viewer-info"><p class="label">${esc(cats[a.category]||'Document')}</p><h2>${esc(a.title)}</h2><p class="filename">${esc(a.filename)}</p><div class="viewer-quick-actions">${!doc?`<button class="action" id="viewer-favorite">${favorites.has(id)?'★ Favorited':'☆ Add to favorites'}</button>`:''}<button class="action export-basket-action ${basket.has(id)?'on':''}" id="viewer-basket" data-basket="${esc(id)}" aria-pressed="${basket.has(id)}">${basket.has(id)?'⇩ In export basket':'⇩ Add to export basket'}</button></div>${!doc?collaboratorControls(a):''}${a.lyric?`<p class="label">Lyric connection</p><p>${esc(a.lyric)}</p>`:''}${a.beat?`<p>${esc(a.beat)}</p>`:''}${a.motion?`<p class="label">Motion idea</p><p>${esc(a.motion)}</p>`:''}${a.note?`<p class="label">Review note</p><p>${esc(a.note)}</p>`:''}${a.inert?'<p>Preserved helper script. This viewer only displays its text.</p>':''}${!doc?connections+referenceControls(a)+workflowStageControls(a):''}${reviewControls(a)}${shotPlanControls(a)}<a class="small-link" href="${esc(href(a.src))}" target="_blank" rel="noopener" ${a.inert?'download':''}>Open original file ↗</a><details><summary>File details</summary><p>${esc(a.repoPath)}</p>${a.sha256?`<p>SHA-256<br>${esc(a.sha256)}</p>`:''}<p>${esc(typeof a.sourceStatus==='string'?a.sourceStatus:'Source record retained')}</p></details></aside></div>`;
    document.querySelector('#close-viewer').onclick=()=>dialog.close();
    document.querySelector('#previous')?.addEventListener('click',()=>openViewer(displayed[i-1]));
    document.querySelector('#next')?.addEventListener('click',()=>openViewer(displayed[i+1]));
    document.querySelector('#zoom')?.addEventListener('click',()=>document.querySelector('#full-image').classList.toggle('zoomed'));
    document.querySelector('#viewer-favorite')?.addEventListener('click',e=>{toggleFavorite(id);e.target.textContent=favorites.has(id)?'★ Favorited':'☆ Add to favorites';});
    document.querySelector('#viewer-basket').onclick=()=>toggleBasket(id);
    document.querySelectorAll('[data-review-status]').forEach(button=>button.onclick=()=>updateReview(id,{status:button.dataset.reviewStatus||null}));
    document.querySelector('#review-note').oninput=e=>updateReview(id,{note:e.target.value});
    document.querySelector('#viewer-save-review').onclick=chooseReviewFile;document.querySelector('#viewer-export-review').onclick=exportReview;
    dialog.querySelectorAll('[data-open]').forEach(button=>button.onclick=()=>openViewer(button.dataset.open));
    dialog.querySelectorAll('[data-story-shot]').forEach(button=>button.onclick=()=>{dialog.close();Object.assign(state,{storyLayout:'progress',storyStart:0,storyEnd:100,storyStage:'all',storyTheme:'all'});route(button.dataset.storyProject,'storyboard');document.getElementById('shot-work-'+button.dataset.storyShot)?.scrollIntoView({block:'center'});});
    bindShotPlanControls(id);bindReferenceControls(id);bindSceneReadinessControls();
    document.querySelector('#reference-storyboard-stage')?.addEventListener('change',e=>{updateReview(id,{storyboardStage:Object.hasOwn(storyboardStages,e.target.value)?e.target.value:null});const label=document.querySelector('#reference-stage-status');if(label)label.textContent='Current stage: '+(storyboardStages[storyboardStage(byID.get(id))]||'not assigned')+'. This applies to this image and its role; separate character components keep their locks.';});
    document.querySelectorAll('[data-quick-collaborator]').forEach(button=>button.onclick=()=>{
      const plan=reviewRecord(id).shotPlan||normalizedPlan({}),provider=button.dataset.quickCollaborator;
      const targets=plan.destinations.filter(d=>d!=='undecided');
      updateReview(id,{shotPlan:normalizedPlan({...plan,destinations:targets.includes(provider)?targets.filter(d=>d!==provider):[...targets,provider]})});
      const updated=reviewRecord(id).shotPlan;document.querySelector('#shot-plan-enabled').checked=true;document.querySelector('#shot-plan-fields').hidden=false;
      document.querySelectorAll('[data-shot-destination]').forEach(input=>input.checked=updated.destinations.includes(input.dataset.shotDestination));
      document.querySelector('#shot-idea').value=updated.idea;document.querySelector('#shot-prompt').value=updated.prompt;
    });
    if(!dialog.open)dialog.showModal();
  }
  dialog.addEventListener('close',()=>{dialog.querySelector('video')?.pause();dialog.innerHTML='';currentID='';renderMain();});
  dialog.addEventListener('click',e=>{if(e.target===dialog)dialog.close();});
  document.addEventListener('keydown',e=>{if(!dialog.open||e.target.closest('input,textarea,select,[contenteditable="true"]'))return;const i=displayed.indexOf(currentID);if(e.key==='ArrowRight'&&i>=0&&i<displayed.length-1){e.preventDefault();openViewer(displayed[i+1]);}if(e.key==='ArrowLeft'&&i>0){e.preventDefault();openViewer(displayed[i-1]);}});
  function collaboratorControls(a){
    const plan=reviewRecord(a.id).shotPlan,targets=(plan?.destinations||[]).filter(d=>d!=='undecided');
    return `<section class="quick-collaborators" aria-label="Queue for a collaborator"><h3>Collaborator</h3><div class="quick-collaborator-buttons">${['Flow','Grok','Gemini'].map(provider=>`<button data-quick-collaborator="${provider}" aria-pressed="${targets.includes(provider)}" class="${targets.includes(provider)?'selected':''}">${provider}</button>`).join('')}</div><p id="quick-collaborator-status" role="status">${esc(targets.length?'Draft queued for '+targets.join(', ')+' · not sent':plan?'Draft saved · choose a collaborator':'Choose a collaborator to queue a draft.')}</p></section>`;
  }
  function refreshCollaboratorUI(){
    const plan=reviewRecord(currentID).shotPlan,targets=(plan?.destinations||[]).filter(d=>d!=='undecided');
    document.querySelectorAll('[data-quick-collaborator]').forEach(button=>{const on=targets.includes(button.dataset.quickCollaborator);button.classList.toggle('selected',on);button.setAttribute('aria-pressed',String(on));});
    const status=document.querySelector('#quick-collaborator-status');if(status)status.textContent=targets.length?'Draft queued for '+targets.join(', ')+' · not sent':plan?'Draft saved · choose a collaborator':'Choose a collaborator to queue a draft.';
  }
  function workflowStageControls(a){const r=reviewRecord(a.id),stage=storyboardStage(a),rating=normalizedRating(r.likenessRating);return `<section class="workflow-stage-controls"><h3>Design stage</h3><label for="reference-storyboard-stage">Stage for this image</label><select id="reference-storyboard-stage"><option value="">Use source stage</option>${Object.entries(storyboardStages).map(([id,label])=>`<option value="${id}" ${stage===id?'selected':''}>${label}</option>`).join('')}</select><label for="reference-likeness-rating">Likeness to the gold standard</label><select id="reference-likeness-rating"><option value="" ${rating===null?'selected':''}>Unrated</option>${[1,2,3,4,5].map(n=>`<option value="${n}" ${rating===n?'selected':''}>${n}/5 ${'★'.repeat(n)}</option>`).join('')}</select><p class="review-help">Rate only the pictured role against its gold standard. Your favorite star and notes record what you like. A rating does not approve an image or change the character.</p><p id="reference-stage-status" class="review-help">Current stage: ${esc(storyboardStages[stage]||'not assigned')}. Production approves this image for its role. A scene or prop can need a fix while separately locked character parts remain usable.</p></section>`;}
  function referenceControls(a){const r=reviewRecord(a.id);return `<section class="reference-controls" aria-label="Reference lane and role"><h3>Reference role</h3><label for="reference-variant">Creative lane</label><select id="reference-variant"><option value="prime" ${r.variant!=='multiverse'?'selected':''}>Prime / current direction</option><option value="multiverse" ${r.variant==='multiverse'?'selected':''}>Multiverse idea</option></select><p class="review-help">Prime can include a selected close variation. It keeps the same canonical face and mouth; Multiverse is a separate creative idea.</p><label for="working-reference-scope">Use this reference for</label><select id="working-reference-scope">${Object.entries(workingScopes).map(([id,label])=>`<option value="${id}" ${selectedWorkingScope(r)===id?'selected':''}>${label}</option>`).join('')}</select><p id="working-reference-status" class="review-help" role="status"></p></section>`;}
  function refreshReferenceUI(){
    const a=byID.get(currentID);if(!a)return;const r=reviewRecord(currentID),scope=selectedWorkingScope(r),select=document.querySelector('#working-reference-scope');if(select)select.value=scope;
    const role=effectiveReferenceRole(a).replace(/_/g,' '),selection=isWorkingScope(r.workingReferenceScope)?'Selected use: '+workingScopes[scope]+'. ':'';
    const status=document.querySelector('#working-reference-status');if(status)status.textContent=selection+(r.status==='remove'||a.archived?'Marked for removal from ordinary browsing. Original and history are retained.':r.variant==='multiverse'?'Multiverse idea; separate from Prime character parts.':'Recorded role: '+role+'. Production adds approved use for this image; an existing component lock keeps its narrower scope.')+(r.workingReference?.status==='requested'?' Earlier request retained for the review history.':'');
  }
  function bindReferenceControls(id){
    document.querySelector('#reference-variant')?.addEventListener('change',e=>updateReview(id,{variant:e.target.value==='multiverse'?'multiverse':'prime',variantSource:'user',...(e.target.value==='multiverse'?{workingReference:null}:{})}));
    document.querySelector('#working-reference-scope')?.addEventListener('change',e=>{if(isWorkingScope(e.target.value))updateReview(id,{workingReferenceScope:e.target.value});});
    document.querySelector('#reference-likeness-rating')?.addEventListener('change',e=>{const raw=e.target.value,value=raw===''?null:Number(raw);if(raw===''||normalizedRating(value)!==null)updateReview(id,{likenessRating:value});});
    refreshReferenceUI();
  }
  async function prepareReviewSweep(){
    const data=reviewPayload();downloadJSON({...data,reviewSweep:{status:'prepared; waiting for Nova',requestedAt:new Date().toISOString(),pendingWorkingReferences:data.items.filter(i=>i.workingReference?.status==='requested').map(i=>({id:i.id,sha256:i.sha256,scope:i.workingReference.scope}))}},'cfa-review-sweep.json');
    const saved=reviewFileHandle?await writeReviewFile():false;const status=document.querySelector('#review-sweep-status');if(status)status.textContent=(saved?'Chosen review file saved. ':'')+'Review sweep exported. Give it to Nova and ask her to review the queued changes. No files were deleted and no task was started.';
  }
  function shotPlanControls(a){
    const plan=reviewRecord(a.id).shotPlan, values=plan||normalizedPlan({});
    return `<section class="shot-plan-controls" aria-label="Shot planning"><label class="plan-toggle"><input type="checkbox" id="shot-plan-enabled" ${plan?'checked':''}> Plan a shot</label><p class="review-help">A creative plan is separate from your keep/fix/removal decision. Nothing is sent or generated here.</p><div id="shot-plan-fields" ${plan?'':'hidden'}><fieldset><legend>Where might this shot go?</legend>${destinations.map(d=>`<label><input type="checkbox" data-shot-destination="${d}" ${values.destinations.includes(d)?'checked':''}> ${d==='undecided'?'Undecided':d}</label>`).join('')}</fieldset><label for="shot-scene-binding">Scene for this plan (optional)</label><select id="shot-scene-binding"><option value="">Unbound draft / planning only</option>${storyWorkItems(a.project).map(shot=>`<option value="${esc(shot.id)}" ${values.sceneIDs?.includes(shot.id)?'selected':''}>${esc(shot.title)} · ${esc(shot.sectionLabel||shot.id)}</option>`).join('')}</select><label for="shot-idea">Shot idea</label><textarea id="shot-idea" rows="3" maxlength="20000" placeholder="The moment, action, or feeling to explore…">${esc(values.idea)}</textarea><label for="shot-prompt">Draft prompt (optional)</label><textarea id="shot-prompt" rows="5" maxlength="30000" placeholder="What the collaborator should create or preserve…">${esc(values.prompt)}</textarea><p class="review-help">Status: planned. Export a provider handoff from Shot plans when you are ready.</p></div></section>`;
  }
  function bindShotPlanControls(id){
    document.querySelector('#shot-scene-binding')?.addEventListener('change',e=>updateReview(id,{shotPlan:normalizedPlan({...reviewRecord(id).shotPlan,sceneIDs:e.target.value?[e.target.value]:[]})}));
    document.querySelector('#shot-plan-enabled').onchange=e=>{
      updateReview(id,{shotPlan:e.target.checked?normalizedPlan({}):null});
      document.querySelector('#shot-plan-fields').hidden=!e.target.checked;
      if(e.target.checked){document.querySelector('#shot-scene-binding').value='';document.querySelector('#shot-idea').value='';document.querySelector('#shot-prompt').value='';document.querySelectorAll('[data-shot-destination]').forEach(input=>input.checked=input.dataset.shotDestination==='undecided');}
    };
    document.querySelectorAll('[data-shot-destination]').forEach(input=>input.onchange=()=>{
      if(input.checked&&input.dataset.shotDestination==='undecided')document.querySelectorAll('[data-shot-destination]').forEach(x=>{if(x!==input)x.checked=false;});
      else if(input.checked)document.querySelector('[data-shot-destination="undecided"]').checked=false;
      let targets=[...document.querySelectorAll('[data-shot-destination]:checked')].map(x=>x.dataset.shotDestination);
      if(!targets.length){targets=['undecided'];document.querySelector('[data-shot-destination="undecided"]').checked=true;}
      updateReview(id,{shotPlan:normalizedPlan({...reviewRecord(id).shotPlan,destinations:targets})});
    });
    document.querySelector('#shot-idea').oninput=e=>updateReview(id,{shotPlan:normalizedPlan({...reviewRecord(id).shotPlan,idea:e.target.value})});
    document.querySelector('#shot-prompt').oninput=e=>updateReview(id,{shotPlan:normalizedPlan({...reviewRecord(id).shotPlan,prompt:e.target.value})});
  }
  function shotHandoffPayload(scope=state.project){
    const items=(scope==='all'?C.assets:projectAssets()).filter(exportAllowed).filter(queryMatch).filter(a=>reviewRecord(a.id).shotPlan&&(state.destination==='all'||reviewRecord(a.id).shotPlan.destinations.includes(state.destination))).map(a=>{
      const plan=reviewRecord(a.id).shotPlan,sceneReadiness=(plan.sceneIDs||[]).map(id=>sceneReviewRecord(a.project,id)).filter(Boolean).map(record=>({...record,...sceneHandoffGate(record)}));
      return {...exportReference(a),title:a.title,reviewStatus:reviewRecord(a.id).status,note:reviewRecord(a.id).note,shotPlan:plan,sceneReadiness,handoffPurpose:sceneReadiness.length&&sceneReadiness.every(r=>r.productionEligible)?'production_target':'planning_or_repair'};
    });
    const records=new Map([...sceneReviews.values()].filter(r=>scope==='all'||r.project===scope).map(r=>[r.project+':'+r.shotID,r]));for(const item of items)for(const r of item.sceneReadiness)records.set(r.project+':'+r.shotID,r);
    const scenes=[...records.values()].map(record=>({...record,title:(C.shotMaterials?.shots||[]).find(s=>s.project===record.project&&s.id===record.shotID)?.title||record.shotID,...sceneHandoffGate(record)}));
    return {format:'cfa-shot-handoff-v1',exported:new Date().toISOString(),project:scope,destination:state.destination,exportIntent:state.exportIntent,status:'planned; not sent or generated',referencePolicy:{path:referencePolicyPath,instruction:referencePolicyText},sceneReadinessReminder:'B or better plus all reviewed required ingredients, no critical blockers and a verified shoot plan is a production target. Final result acceptance is separate; blocked and unbound plans are planning or repair handoffs.',attachmentReminder:'Attach the actual images or clips identified below. This handoff contains references and text only; no media files are bundled.',scenes,items};
  }
  function exportShotHandoff(format,scope=state.project){
    const data=shotHandoffPayload(scope),filename='cfa-shot-handoff-'+scope+'-'+state.destination+'.'+format;
    if(format==='json')downloadJSON(data,filename);
    else {
      const text=['CFA SHOT HANDOFF',`Project: ${data.project} | Destination: ${state.destination}`,`Export intent: ${data.exportIntent==='prime'?'Prime references':'Multiverse creative ingredients'}`,data.status,data.attachmentReminder,`Reference policy: ${data.referencePolicy.path}`,data.referencePolicy.instruction,data.sceneReadinessReminder,'',...data.scenes.flatMap(r=>[`Scene: ${r.title} (${r.shotID})`,`Whole scene grade: ${r.grade||'Ungraded'} | ${r.productionEligible?'B target met':'Planning / repair'}`,`Blockers: ${r.criticalBlockers.join('; ')||'(none recorded)'}`,`Readiness: ${r.reasons.join('; ')||'Required ingredients reviewed ready'}`,`Scene note: ${r.note||'(none)'}`,`Shoot plan: ${r.shootPlan.reviewStatus} | Reviewed by: ${r.shootPlan.reviewedBy||'(none)'} | ${r.shootPlan.reviewedAt||'no verification time'}`,`Direction: ${r.shootPlan.direction||'(missing)'}`,`Camera: ${r.shootPlan.camera||'(missing)'}`,`Lighting: ${r.shootPlan.lighting||'(missing)'}`,`Shoot plan review note: ${r.shootPlan.note||'(none)'}`,...r.ingredients.map(i=>`${i.required?'Required':'Optional'}: ${i.label} | ${i.status} | ${i.assetID||'no file'} | ${i.sha256||'no hash'} | ${i.note||'no evidence note'}`),'']),...data.items.flatMap((a,i)=>[
        `${i+1}. ${a.title}`,`Reference ID: ${a.id}`,`SHA-256: ${a.sha256||'not recorded'}`,`File: ${a.filename}`,`Source path: ${a.path||'see source catalog'}`,
        `Destinations: ${a.shotPlan.destinations.join(', ')}`,`Lane: ${a.variant}`,`Reference role: ${a.referenceRole}`,`Likeness to gold standard: ${a.likenessRating===null?'Unrated':a.likenessRating+'/5'}`,`Review: ${a.reviewStatus||'unreviewed'}`,`Review note / known differences: ${a.knownDifferences||'(none)'}`,`Scene use: ${a.referenceUsePolicy.explicitSceneReference?.instruction||a.referenceUsePolicy.defaultReferenceSelection.instruction}`,
        `Handoff purpose: ${a.handoffPurpose} | Bound scenes: ${(a.shotPlan.sceneIDs||[]).join(', ')||'none; planning only'}`,`Shot idea: ${a.shotPlan.idea||'(to be written)'}`,`Draft prompt: ${a.shotPlan.prompt||'(not drafted)'}`,''])].join('\n');
      const url=URL.createObjectURL(new Blob([text],{type:'text/plain;charset=utf-8'})),link=document.createElement('a');link.href=url;link.download=filename;link.click();setTimeout(()=>URL.revokeObjectURL(url),3000);
    }
    notice(data.items.length+' planned shots exported. Attach the actual reference files when handing them over.');
  }
  function exportFavorites(){const selected=[...favorites].map(id=>byID.get(id)).filter(Boolean),items=selected.filter(exportAllowed).map(exportReference);downloadJSON({format:'cfa-visual-favorites-v1',exported:new Date().toISOString(),exportIntent:state.exportIntent,status:'user review shortlist; not automatic final approval',items},'CFA-favorites-'+new Date().toISOString().slice(0,10)+'.json');notice(items.length+' favorites exported; '+(selected.length-items.length)+' excluded by export intent. Full review backups retain every star.');}
  function downloadJSON(data,filename){const blob=new Blob([JSON.stringify(data,null,2)],{type:'application/json'}),url=URL.createObjectURL(blob),link=document.createElement('a');link.href=url;link.download=filename;link.click();setTimeout(()=>URL.revokeObjectURL(url),3000);}
  function exportReview(){downloadJSON(reviewPayload(),'cfa-review.json');notice('Review exported with decisions, notes, and favorites. Save it in docs/notes/downloads (or docs/notes/cfa-review.json) for the next sweep.');}
  function importReview(data){
    if(!data||typeof data!=='object')throw Error('Choose an exported CFA review, favorites, or selection-list file.');
    if(data.format===EXPORT_KEY&&Array.isArray(data.items)){const result=importBasket(data.items);saveBasket();render();notice(`${result.added} matching references added to the export basket; ${result.skipped} unmatched entries skipped.`);return;}
    let records=[],starItems=[];
    if(data.format===REVIEW_KEY){records=data.items||data.reviewDecisions||data.decisions;starItems=data.favorites||[];if(!Array.isArray(records)||!Array.isArray(starItems))throw Error('The review file has invalid lists.');}
    else if(data.format==='cfa-visual-favorites-v1'&&Array.isArray(data.items))starItems=data.items;
    else throw Error('Choose an exported CFA review, favorites, or selection-list file.');
    let imported=0,stars=0,skipped=0;
    for(const item of records){const record=normalizedReview(item);if(record){mergeReview(record);imported++;}else skipped++;}
    for(const item of starItems){const a=matchingAsset(item);if(a&&(data.format!=='cfa-visual-review-v1'||!a.sha256||item.sha256===a.sha256)){favorites.add(a.id);stars++;}else skipped++;}
    if(data.format==='cfa-visual-favorites-v1'&&data.notes&&typeof data.notes==='object'){
      for(const [id,note] of Object.entries(data.notes)){if(typeof note!=='string')continue;const a=matchingAsset({id,sha256:data.note_refs?.[id]});if(a){reviews.set(id,{...reviewRecord(id),id,sha256:a.sha256||null,note:note.slice(0,20000),origin:'import'});imported++;}}
    }
    if(data.format===REVIEW_KEY&&Array.isArray(data.sceneReviews)){for(const item of data.sceneReviews){const record=normalizedSceneReview(item);if(record){sceneReviews.set(record.project+':'+record.shotID,record);imported++;}else skipped++;}}
    if(data.format===REVIEW_KEY&&Array.isArray(data.exportBasket)){const result=importBasket(data.exportBasket);skipped+=result.skipped;}
    reviewRevision++;saveBrowserReview();scheduleFileSave();render();notice(`${imported} review records and ${stars} favorites imported; ${skipped} unmatched entries skipped.`);
  }
  const input=document.createElement('input');input.type='file';input.accept='.json,application/json';input.id='import-file';input.hidden=true;document.body.append(input);
  input.onchange=async()=>{try{const file=input.files?.[0];if(!file)return;if(file.size>5*1024*1024)throw Error('Choose a review file smaller than 5 MB.');importReview(JSON.parse(await file.text()));}catch(error){notice(error instanceof SyntaxError?'That file is not valid JSON.':error.message||'Could not import that review file.');}finally{input.value='';}};
  window.addEventListener('beforeunload',e=>{if(reviewFileHandle&&(fileSaveTimer||fileWriting||reviewRevision!==fileSavedRevision)){e.preventDefault();e.returnValue='';}});
  window.addEventListener('hashchange',()=>{rememberLibrary();parseHash();render();});parseHash();render();
})();
