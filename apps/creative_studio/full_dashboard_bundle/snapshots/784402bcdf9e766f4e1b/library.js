(() => {
  'use strict';
  const base = new URL('.', document.currentScript.src);
  const C = window.REVIEW_CATALOG;
  const byID = new Map(C.assets.map(a => [a.id, a]));
  // Visual duplicates have distinct historical hashes. Resolve browsing/review
  // aliases separately; validation and scene evidence still use exact byID.
  const assetAliases=new Map(),conflictingAliasIDs=new Set();
  for(const alias of C.assetAliases||[]){
    const canonical=byID.get(alias?.canonicalID);
    if(alias?.kind!=='visual_duplicate_reencoding'||typeof alias.id!=='string'||!alias.id||byID.has(alias.id)||!/^[a-f0-9]{64}$/.test(alias.sha256||'')||!/^[a-f0-9]{64}$/.test(alias.canonicalSHA256||'')||canonical?.sha256!==alias.canonicalSHA256)continue;
    const prior=assetAliases.get(alias.id);
    if(prior&&(prior.sha256!==alias.sha256||prior.canonicalID!==alias.canonicalID||prior.canonicalSHA256!==alias.canonicalSHA256)){conflictingAliasIDs.add(alias.id);assetAliases.delete(alias.id);}
    else if(!conflictingAliasIDs.has(alias.id))assetAliases.set(alias.id,alias);
  }
  const aliasedCanonicalIDs=new Set([...assetAliases.values()].map(a=>a.canonicalID)),aliasedReviewRecords=new WeakSet();
  const aliasTarget=id=>{const alias=assetAliases.get(id),asset=byID.get(alias?.canonicalID);return alias&&asset?.sha256===alias.canonicalSHA256?asset:null;};
  const browseAsset=id=>byID.get(id)||aliasTarget(id);
  const cats = Object.fromEntries(C.categories);
  const esc = v => String(v ?? '').replace(/[&<>"']/g, x => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[x]));
  const href = p => new URL(p, base).href;
  const isDoc = a => ['document','pdf'].includes(a.kind);
  const initial = window.REVIEW_INITIAL || {project:'hon', view:'all'};
  let state = {...initial, view:location.hash?initial.view:'mission_control', album:'', search:'', destination:'all', videoSort:'longest', videoLayout:'grouped', intakeLayout:'evidence', intakeDecision:'pending', intakeBatch:'all', intakePage:0, castFilter:'all', castSource:'all', outfitLayout:'compact', collaborator:'ComfyUI',collaboratorSection:'work',exportIntent:'prime',detailLayout:initial.project==='hon'?'all':'approved',detailProfile:'',allPurpose:'all',storyTheme:'all',storyStage:'all',storyStart:0,storyEnd:100}, currentID = '', displayed = [], toastTimer;
  const intakeDisclosureState = new Map();
  const expandedOutfits = new Set();
  const expandedCollections = new Set();
  const collapsedBrowseBuckets = new Set();
  const closedMouthLooks = new Set();
  const REVIEW_KEY = 'cfa-visual-review-v1', EXPORT_KEY = 'cfa-visual-export-v1';
  const statusLabels = {keep:'Keep', needs_fixes:'Needs fixes', remove:'Marked for removal'};
  // Coordinator requests are hash-bound catalog metadata, independent of saved user reviews.
  const reviewRequests=new Map((C.reviewRequests||[]).filter(r=>{const a=byID.get(r?.id);return a?.sha256&&r.sha256===a.sha256&&r.type==='missing_decision'&&typeof r.reason==='string'&&typeof r.requestedBy==='string';}).map(r=>[r.id,r]));
  const workingScopes={complete_look:'Complete look',identity:'Identity',outfit:'Outfit',scene:'Scene',detail:'Detail only'};
  const storyboardStages={preliminary:'Preliminary',detailed_design:'Detailed design',verification:'Verification',production:'Production'};
  const bomDefinitions=C.characterBOM?.characters||[];
  const retiredInspirationIDs=new Set(C.albums.filter(al=>['hon:scene-ideas','hon:outfit-ideas'].includes(al.id)).flatMap(al=>al.assetIDs||[]));
  const historicalTattooReferenceIDs=['HD-RETURN-d55b97a3b322','HD-RETURN-78ad6c79615a','HD-RETURN-f88ff5ae511e','HD-TATGUIDE-b80e4d006917','HD-RETURN-d91685dd99cd','HD-TATGUIDE-d152270ab369','HD-TATGUIDE-ad54ba356e7c','HD-TATGUIDE-3046dd64faa8','HD-TATGUIDE-440a8cf5e911'];
  const historicalMouthLooks=new Set((C.mouthCoverage?.looks||[]).filter(l=>l.history===true||l.planStatus==='History only').map(l=>l.id));
  const protectedReferenceIDs=new Set([...bomDefinitions.flatMap(c=>[c.coverAssetID,...(c.entries||[]).filter(e=>e.recordedSelection).map(e=>e.assetID)]),...(C.castCollections||[]).flatMap(g=>[...(g.currentIDs||[]),...(g.workingReferenceIDs||[])]),...C.assets.filter(a=>(a.componentApprovals||[]).some(c=>c.sourceSHA256===a.sha256&&c.status==='user_selected_component')).map(a=>a.id)]);
  const historyArchiveIDs=new Set(['HD-LIKENESS-02',...retiredInspirationIDs,...historicalTattooReferenceIDs,...bomDefinitions.flatMap(c=>c.historyAssetIDs||[]),...(C.sharedReferenceCollections||[]).flatMap(g=>(g.sections||[]).filter(s=>s.history===true).flatMap(s=>s.assetIDs||[])),...(C.castCollections||[]).flatMap(g=>g.historicalReferenceIDs||g.historyIDs||[]),...(C.mouthCoverage?.items||[]).filter(row=>historicalMouthLooks.has(row.lookID)&&byID.get(row.exactAssetID||row.assetID)?.sha256===row.sha256).map(row=>row.assetID)].filter(id=>!protectedReferenceIDs.has(id)));
  const bomRoles=new Map(bomDefinitions.flatMap(c=>(c.entries||[]).map(e=>[e.assetID,e])));
  const referencePolicyPath=C.characterBOM?.policyPath||'docs/notes/explorable_world/comfy/projects/visual_library/REFERENCE_POLICY.txt';
  const referencePolicyText='An explicitly named reference is used for that scene only. Other scenes start from canonical scoped gold standards and the highest-rated suitable approved Prime references. A scene image does not replace identity. Character/component likeness is rated against its scoped gold standard; only likenessRating guides default reference ranking. Scene craft rates framing, lighting and staging separately; never average it with likeness or treat it as production readiness.';
  const normalizedRating=value=>Number.isInteger(value)&&value>=1&&value<=5?value:null;
  const assistantLikenessAssessments=new Map((C.assistantLikenessAssessments||[]).filter(p=>{const a=byID.get(p?.assetID);return a?.sha256&&p.sha256===a.sha256&&p.status==='proposal'&&p.assessedBy==='nova'&&(p.likenessRating===null||normalizedRating(p.likenessRating)!==null)&&Array.isArray(p.referenceAssets)&&p.referenceAssets.length&&p.referenceAssets.every(r=>byID.get(r.assetID)?.sha256&&r.sha256===byID.get(r.assetID).sha256);}).map(p=>[p.assetID,p]));
  let favorites = new Set(), basket = new Set(), storageOK = true, reviews = new Map(), sceneReviews = new Map();
  let reviewFileHandle = null, fileSaveTimer, fileWriteChain = Promise.resolve();
  let reviewRevision = 0, fileSavedRevision = 0, fileWriting = false;
  let fileMessage = 'Browser backup only · choose Save review file or export for Nova’s next sweep. Changes do not notify Nova automatically.';

  // Presets are writing aids. Only copied text becomes part of an asset's review.
  const NOTE_PRESETS_KEY='cfa-review-note-presets-v1';
  let notePresetsMessage='',notePresetsReadError='',notePresetSequence=0,clearedNotePresets=null;
  let notePresetDraft={id:'',label:'',text:''};
  let notePresets=readNotePresets();
  function readNotePresets(){
    try{
      const raw=localStorage.getItem(NOTE_PRESETS_KEY);if(!raw)return [];
      const data=JSON.parse(raw),ids=new Set();
      if(data?.format!==NOTE_PRESETS_KEY||!Array.isArray(data.items)||data.items.length>50)throw Error('Invalid preset list');
      for(const item of data.items){
        if(!item||typeof item.id!=='string'||!item.id||ids.has(item.id)||typeof item.label!=='string'||!item.label.trim()||item.label.length>80||typeof item.text!=='string'||!item.text.trim()||item.text.length>20000)throw Error('Invalid preset');
        ids.add(item.id);
      }
      return data.items.map(({id,label,text})=>({id,label,text}));
    }catch{
      notePresetsReadError='Saved presets could not be read. They have been left untouched. Clear the list to start again.';
      return [];
    }
  }
  function persistNotePresets(message){
    try{
      localStorage.setItem(NOTE_PRESETS_KEY,JSON.stringify({format:NOTE_PRESETS_KEY,items:notePresets}));
      notePresetsMessage=message;
    }catch{
      notePresetsMessage='Preset changes are available for this open page only; browser storage is unavailable.';
    }
    refreshNotePresetControls();
  }
  function notePresetFeedback(message){notePresetsMessage=message;refreshNotePresetControls();return false;}
  function saveNotePreset(id,label,text){
    if(notePresetsReadError)return notePresetFeedback(notePresetsReadError);
    if(typeof text!=='string'||!text.trim())return notePresetFeedback('Write a note before saving a preset.');
    if(text.length>20000||typeof label!=='string'||label.length>80)return notePresetFeedback('Use up to 80 characters for the name and 20,000 for the note.');
    if(id&&!notePresets.some(p=>p.id===id))return notePresetFeedback('That preset is no longer available. Choose New preset.');
    if(!id&&notePresets.length>=50)return notePresetFeedback('You have 50 presets. Edit or delete one to make room.');
    const editing=!!id;
    if(!id){do{id='note-'+Date.now().toString(36)+'-'+(++notePresetSequence);}while(notePresets.some(p=>p.id===id));}
    const preset={id,label:label.trim()||text.trim().replace(/\s+/g,' ').slice(0,60),text:text.trim()};
    notePresets=editing?notePresets.map(p=>p.id===id?preset:p):[...notePresets,preset];
    notePresetDraft={...preset};clearedNotePresets=null;
    persistNotePresets(editing?'Preset updated. Existing review notes are unchanged.':'Preset saved in this browser.');
    fillNotePresetEditor();return true;
  }
  function deleteNotePreset(id){
    if(!notePresets.some(p=>p.id===id))return false;
    notePresets=notePresets.filter(p=>p.id!==id);clearedNotePresets=null;
    if(notePresetDraft.id===id)notePresetDraft={id:'',label:'',text:''};
    persistNotePresets('Preset deleted. Existing review notes are unchanged.');fillNotePresetEditor();return true;
  }
  function clearNotePresets(){
    clearedNotePresets=notePresets.length?notePresets.map(p=>({...p})):null;
    notePresets=[];notePresetsReadError='';notePresetDraft={id:'',label:'',text:''};
    persistNotePresets('Preset list cleared. Existing review notes are unchanged.');fillNotePresetEditor();
  }
  function undoClearNotePresets(){
    if(!clearedNotePresets)return false;
    notePresets=clearedNotePresets;clearedNotePresets=null;
    persistNotePresets('Preset list restored.');return true;
  }
  function applyNotePreset(assetID,presetID){
    const preset=notePresets.find(p=>p.id===presetID),input=document.querySelector('#review-note');
    if(!preset||!input||currentID!==assetID||!byID.has(assetID))return false;
    const before=input.value,next=before+(before&&!before.endsWith('\n')?'\n':'')+preset.text;
    if(next.length>20000){notice('That preset would exceed the 20,000-character note limit. Your note is unchanged.');return false;}
    input.value=next;updateReview(assetID,{note:next});input.focus();
    input.setSelectionRange?.(next.length,next.length);
    return true;
  }
  function notePresetOptions(){return notePresets.map(p=>`<option value="${esc(p.id)}">${esc(p.label)}</option>`).join('');}
  function notePresetsControls(){
    return `<div class="note-presets"><select id="note-preset-select" aria-label="Add a saved note" ${notePresets.length?'':'disabled'}><option value="">${notePresets.length?'Add a saved note…':'No saved notes yet'}</option>${notePresetOptions()}</select><details class="note-preset-manager"><summary>Manage note presets</summary><p class="review-help">Choose a saved note to append its text. Presets stay in this browser; editing or clearing them leaves applied review notes intact.</p><label for="note-preset-editor-select">Create or edit</label><select id="note-preset-editor-select"><option value="">New preset</option>${notePresetOptions()}</select><button type="button" class="small-link" id="note-preset-from-note">Use current note as a starting point</button><label for="note-preset-label">Short name (optional)</label><input id="note-preset-label" type="text" maxlength="80" placeholder="e.g. Missing nose piercing"><label for="note-preset-text">Preset text</label><textarea id="note-preset-text" rows="3" maxlength="20000" placeholder="Write the comment you want to reuse…"></textarea><div class="note-preset-buttons"><button type="button" id="note-preset-save">Save preset</button><button type="button" id="note-preset-delete" disabled>Delete preset</button><button type="button" id="note-presets-clear">Clear list</button><button type="button" id="note-presets-undo" hidden>Undo clear</button></div><p class="review-help note-preset-status" id="note-preset-status" role="status">${esc(notePresetsReadError||notePresetsMessage)}</p></details></div>`;
  }
  function refreshNotePresetControls(){
    const insert=document.querySelector('#note-preset-select'),editor=document.querySelector('#note-preset-editor-select');
    if(insert){insert.innerHTML=`<option value="">${notePresets.length?'Add a saved note…':'No saved notes yet'}</option>${notePresetOptions()}`;insert.value='';insert.disabled=!notePresets.length;}
    if(editor){editor.innerHTML='<option value="">New preset</option>'+notePresetOptions();editor.value=notePresetDraft.id;}
    const status=document.querySelector('#note-preset-status');if(status)status.textContent=notePresetsReadError||notePresetsMessage;
    const clear=document.querySelector('#note-presets-clear');if(clear)clear.disabled=!notePresets.length&&!notePresetsReadError;
    const undo=document.querySelector('#note-presets-undo');if(undo)undo.hidden=!clearedNotePresets;
  }
  function fillNotePresetEditor(){
    const select=document.querySelector('#note-preset-editor-select'),label=document.querySelector('#note-preset-label'),text=document.querySelector('#note-preset-text'),remove=document.querySelector('#note-preset-delete');
    if(select)select.value=notePresetDraft.id;if(label)label.value=notePresetDraft.label;if(text)text.value=notePresetDraft.text;if(remove)remove.disabled=!notePresetDraft.id;
  }
  function bindNotePresets(assetID){
    refreshNotePresetControls();fillNotePresetEditor();
    document.querySelector('#note-preset-select').onchange=e=>{const id=e.target.value;e.target.value='';if(id)applyNotePreset(assetID,id);};
    document.querySelector('#note-preset-editor-select').onchange=e=>{notePresetDraft={...(notePresets.find(p=>p.id===e.target.value)||{id:'',label:'',text:''})};fillNotePresetEditor();};
    document.querySelector('#note-preset-label').oninput=e=>{notePresetDraft.label=e.target.value;};
    document.querySelector('#note-preset-text').oninput=e=>{notePresetDraft.text=e.target.value;};
    document.querySelector('#note-preset-save').onclick=()=>saveNotePreset(notePresetDraft.id,document.querySelector('#note-preset-label').value,document.querySelector('#note-preset-text').value);
    document.querySelector('#note-preset-delete').onclick=()=>deleteNotePreset(notePresetDraft.id);
    document.querySelector('#note-presets-clear').onclick=clearNotePresets;
    document.querySelector('#note-presets-undo').onclick=undoClearNotePresets;
    document.querySelector('#note-preset-from-note').onclick=()=>{notePresetDraft={id:'',label:'',text:document.querySelector('#review-note').value};fillNotePresetEditor();document.querySelector('#note-preset-text').focus();};
  }

  // BEGIN reference-validation-v1: separate evidence, never legacy review fields.
  const VALIDATION_KEY='cfa-reference-validation-v1';
  const validationData=C.referenceValidation||{criteriaSets:[],inventory:[],assessments:[],sceneUses:[]};
  const validationHistory=new Map(), legacyReviewArchive=new Map();
  let validationStorageError='', validationUnreadBackups=[];
  const vCopy=v=>JSON.parse(JSON.stringify(v));
  const vText=v=>typeof v==='string'&&v.trim().length>0;
  const vHash=v=>typeof v==='string'&&/^[a-f0-9]{64}$/.test(v);
  const vStable=v=>JSON.stringify(v,(key,value)=>value&&typeof value==='object'&&!Array.isArray(value)?Object.fromEntries(Object.keys(value).sort().map(k=>[k,value[k]])):value);
  const validationCriteriaSnapshots=new Map((validationData.criteriaSets||[]).map(c=>[c.id,vStable(c)]));
  const vVersion=a=>a?.referenceVersion||('sha256:'+a?.sha256);
  const vBinding=a=>({assetID:a.id,sha256:a.sha256,version:vVersion(a)});
  function archiveLegacy(items){for(const item of items||[])if(item&&typeof item==='object')legacyReviewArchive.set(vStable(item),vCopy(item));}
  function validationEnvelope(){return {format:VALIDATION_KEY,schemaVersion:1,assessments:[...validationHistory.values()].map(vCopy),legacyReviewArchive:[...legacyReviewArchive.values()].map(vCopy),...(validationUnreadBackups.length?{unreadBackups:validationUnreadBackups.map(vCopy)}:{})};}
  function checkValidationEnvelope(data){
    if(data?.format!==VALIDATION_KEY||data.schemaVersion!==1||!Array.isArray(data.assessments))throw Error('Unsupported validation evidence format; original backup retained.');
    const seen=new Map(validationHistory);
    for(const a of data.assessments){
      if(!a||a.schemaVersion!==1||!vText(a.id)||!['character','scene'].includes(a.axis)||!['required','optional','not_applicable'].includes(a.applicability)||!['not_checked','pass','fail','uncertain'].includes(a.status)||!vText(a.target?.assetID)||!vHash(a.target?.sha256)||!vText(a.target?.version)||!vText(a.scope?.id)||!vText(a.scope?.kind)||!vText(a.reviewer?.name)||!vText(a.reviewer?.model)||!vText(a.reviewer?.surface)||!Number.isFinite(Date.parse(a.reviewer?.reviewedAtUTC))||!vText(a.provenance?.source)||!Array.isArray(a.imagesSeen)||!Array.isArray(a.criteriaResults)||typeof a.evidence!=='string'||typeof a.uncertainty!=='string')throw Error('Invalid validation record. No records imported.');
      for(const image of a.imagesSeen)if(!image||!vText(image.assetID)||!vHash(image.sha256)||!vText(image.version)||typeof image.accessible!=='boolean'||!['original','full_size_frame','contact_sheet','thumbnail'].includes(image.view))throw Error('Invalid images-seen record. No records imported.');
      const criterionIDs=new Set();
      for(const row of a.criteriaResults){if(!row||!vText(row.criterionID)||criterionIDs.has(row.criterionID)||!['pass','fail','uncertain','not_checked'].includes(row.outcome)||!['visible','occluded','missing','unknown'].includes(row.visibility)||typeof row.observation!=='string'||(row.presence!==undefined&&!['present','absent','unknown'].includes(row.presence)))throw Error('Invalid criterion result. No records imported.');criterionIDs.add(row.criterionID);}
      if(seen.has(a.id)&&vStable(seen.get(a.id))!==vStable(a))throw Error('Conflicting immutable evidence ID: '+a.id+'. No records imported.');
      seen.set(a.id,a);
    }
    if(data.legacyReviewArchive!==undefined&&!Array.isArray(data.legacyReviewArchive))throw Error('Invalid preserved legacy archive.');
    if(data.unreadBackups!==undefined&&(!Array.isArray(data.unreadBackups)||data.unreadBackups.some(b=>!b||!vText(b.sourceKey)||typeof b.raw!=='string'||typeof b.error!=='string')))throw Error('Invalid unread-backup archive. No records imported.');
    return data;
  }
  function archiveUnread(backups){for(const backup of backups||[])if(!validationUnreadBackups.some(b=>vStable(b)===vStable(backup)))validationUnreadBackups.push(vCopy(backup));}
  function retainUnread(sourceKey,raw,error){archiveUnread([{sourceKey,raw:typeof raw==='string'?raw:'',error:error.message||String(error)}]);validationStorageError='Unread evidence backup retained. Export it before resolving the original storage.';}
  function mergeValidation(data){checkValidationEnvelope(data);for(const a of data.assessments)validationHistory.set(a.id,vCopy(a));archiveLegacy(data.legacyReviewArchive);archiveUnread(data.unreadBackups);}
  function validationAssessment(a){
    const reasons=[],staleReasons=[];
    const target=byID.get(a.target.assetID);
    if(!target)reasons.push('Target image is missing.');
    else if(target.sha256!==a.target.sha256||vVersion(target)!==a.target.version)staleReasons.push('Target hash or version changed.');
    const definition=(validationData.criteriaSets||[]).find(c=>c.id===a.criteria?.id);
    if(a.applicability==='not_applicable'){
      if(a.status==='pass')reasons.push('N/A cannot be a pass.');
      if(!vText(a.evidence))reasons.push('N/A needs a scoped explanation.');
      return {record:a,status:'not_checked',applicability:a.applicability,stale:!!staleReasons.length,reasons:[...staleReasons,...reasons],current:!!target&&!staleReasons.length&&!reasons.length};
    }
    if(!definition)reasons.push('Current scoped criteria are not available.');
    else {
      if(validationCriteriaSnapshots.get(definition.id)!==vStable(definition))staleReasons.push('Current criteria content changed since this catalog was loaded.');
      if(definition.version!==a.criteria.version||definition.sha256!==a.criteria.sha256)staleReasons.push('Criteria or tolerance version changed.');
      if(definition.axis!==a.axis||definition.scope.id!==a.scope.id||definition.scope.kind!==a.scope.kind)staleReasons.push('Comparison scope changed.');
      const nomination=(validationData.inventory||[]).find(n=>n.id===definition.nominationID);
      if(!nomination?.recordedSelection)reasons.push('Reference nomination is unresolved.');
      else if(vStable(nomination.reference)!==vStable(definition.reference)||nomination.project!==definition.project||nomination.scope!==definition.nominationScope)staleReasons.push('Reference nomination, project or scope changed.');
      if(!a.reference||a.reference.assetID!==definition.reference.assetID||a.reference.sha256!==definition.reference.sha256||a.reference.version!==definition.reference.version)staleReasons.push('Nominated reference binding changed.');
      const ref=byID.get(definition.reference.assetID);
      if(!ref)reasons.push('Reference image is missing.');
      else if(ref.sha256!==definition.reference.sha256||vVersion(ref)!==definition.reference.version)staleReasons.push('Reference hash or version changed.');
      if(definition.project!==target?.project)reasons.push('Reference belongs to a different project.');
    }
    for(const viewed of a.imagesSeen){const image=byID.get(viewed.assetID);if(!image)reasons.push('An inspected image is no longer available.');else if(image.sha256!==viewed.sha256||vVersion(image)!==viewed.version)staleReasons.push('An inspected image hash or version changed.');}
    const seen=b=>b&&a.imagesSeen.some(i=>i.assetID===b.assetID&&i.sha256===b.sha256&&i.version===b.version&&i.accessible===true&&['original','full_size_frame'].includes(i.view));
    if(!seen(a.target))reasons.push('Exact target pixels were not recorded as inspected.');
    if(!seen(a.reference))reasons.push('Exact reference pixels were not recorded as inspected.');
    if(!vText(a.evidence))reasons.push('Comparison evidence is missing.');
    const rows=definition?.criteria||[],required=rows.filter(r=>r.required);
    if(!required.length)reasons.push('Required criteria are not declared.');
    const results=new Map();
    for(const row of a.criteriaResults){
      if(!row||!vText(row.criterionID)||results.has(row.criterionID)){reasons.push('Duplicate or invalid criterion result.');continue;}
      results.set(row.criterionID,row);
    }
    let observedFail=false;
    for(const criterion of required){
      const result=results.get(criterion.id);
      if(!result||!vText(result.observation)){reasons.push(criterion.label+': observation missing.');continue;}
      if(result.visibility!=='visible'){reasons.push(criterion.label+': '+(result.visibility||'unknown visibility')+'.');continue;}
      if(criterion.presenceRequired&&!['present','absent'].includes(result.presence)){reasons.push(criterion.label+': presence not assessed.');continue;}
      if(criterion.presenceRequired&&result.presence==='absent'&&result.outcome==='pass'){reasons.push(criterion.label+': absent piercing cannot pass.');continue;}
      if(result.outcome==='fail')observedFail=true;
      else if(result.outcome!=='pass')reasons.push(criterion.label+': unresolved.');
    }
    const stale=staleReasons.length>0;
    let status=a.status;
    if(stale)status='uncertain';
    else if(observedFail)status='fail';
    else if(reasons.length&&status!=='not_checked')status='uncertain';
    else if(status==='fail')status='uncertain'; // A fail also needs an observed failed criterion.
    return {record:a,status,applicability:a.applicability,stale,reasons:[...staleReasons,...reasons],current:!stale&&!reasons.length,scope:a.scope,definition};
  }
  function validationLatest(id,axis,criteriaID=null){
    const candidates=[...validationHistory.values()].filter(a=>a.target.assetID===id&&a.axis===axis&&(!criteriaID||a.criteria?.id===criteriaID));
    return candidates.sort((a,b)=>Date.parse(b.reviewer.reviewedAtUTC)-Date.parse(a.reviewer.reviewedAtUTC)||b.id.localeCompare(a.id));
  }
  function validationSummary(asset,axis){
    const candidates=validationLatest(asset.id,axis);
    if(!candidates.length){
      const detail=(validationData.mouthAssetIDs||[]).includes(asset.id);
      return {status:'not_checked',applicability:axis==='scene'&&detail?'not_applicable':'required',stale:false,reasons:[axis==='scene'&&detail?'Mouth detail only; no scene assertion.':'No scoped evidence recorded.'],label:axis==='scene'&&detail?'N/A · mouth detail':'Not checked'};
    }
    const latestByScope=new Map();for(const candidate of candidates){const key=candidate.criteria?.id||candidate.scope.id;if(!latestByScope.has(key))latestByScope.set(key,validationAssessment(candidate));}
    const scopeResults=[...latestByScope.values()],applicable=scopeResults.filter(r=>r.applicability!=='not_applicable'),priority=applicable.find(r=>r.stale)||applicable.find(r=>r.status==='fail')||applicable.find(r=>r.status==='uncertain')||applicable.find(r=>r.status==='not_checked')||applicable[0]||scopeResults[0];
    const result={...priority,scopeResults,reasons:[...new Set(scopeResults.flatMap(r=>r.reasons))]};
    const label=result.stale?'Stale · recheck':result.applicability==='not_applicable'?'N/A':({pass:'Scoped pass',fail:'Needs repair',uncertain:'Uncertain',not_checked:'Not checked'}[result.status]);
    return {...result,label:label+' · '+(scopeResults.length===1?(candidates[0].scope.label||candidates[0].scope.id):scopeResults.length+' scopes')};
  }
  function validationSceneBinding(record){return {project:record?.project,shotID:record?.shotID,ingredients:(record?.ingredients||[]).filter(i=>i.required).map(i=>({id:i.id,kind:i.kind,role:i.role,assetID:i.assetID||null,sha256:i.sha256||null})).sort((a,b)=>a.id.localeCompare(b.id)),shootPlan:normalizedShootPlan(record?.shootPlan)};}
  function validationTechnicalGate(record){
    const manual=sceneHandoffGate(record), reasons=[...manual.reasons];
    const plan=(validationData.sceneUses||[]).find(p=>p.project===record?.project&&p.shotID===record?.shotID);
    if(!plan||!vText(plan.version)||!vText(plan.provenance?.source)||!Array.isArray(plan.requiredChecks)||!plan.requiredChecks.length)reasons.push('Required validation scopes for this scene/use have not been declared.');
    else {
      if(vStable(plan.binding)!==vStable(validationSceneBinding(record)))reasons.push('Required ingredients or shoot-plan binding changed; recheck the validation declaration.');
      for(const ingredient of record.ingredients.filter(i=>i.required&&i.kind==='reference'))if(!plan.requiredChecks.some(c=>c.ingredientID===ingredient.id&&c.assetID===ingredient.assetID))reasons.push(ingredient.label+': required validation scope is undeclared.');
      for(const check of plan.requiredChecks){
      const latest=validationLatest(check.assetID,check.axis,check.criteriaID)[0],result=latest&&validationAssessment(latest);
      if(!result||result.status!=='pass'||!result.current||result.applicability!=='required'||latest.scope.id!==check.scopeID)reasons.push(check.label||check.scopeID||check.assetID+': current required evidence is missing.');
    }
    }
    return {technicalReady:reasons.length===0,manualSceneGate:manual,reasons,scope:'Declared scene/use only; final video judgment and execution authorization remain separate.'};
  }
  function validationForExport(a){return {format:VALIDATION_KEY,character:validationSummary(a,'character'),scene:validationSummary(a,'scene'),assessmentIDs:[...validationHistory.values()].filter(r=>r.target.assetID===a.id).map(r=>r.id),evidenceIsScoped:true};}
  function persistValidation(){
    if(validationStorageError)throw Error('Existing evidence backup could not be read. Export it before replacing it.');
    const data=validationEnvelope();let durable=true;
    try{localStorage.setItem(VALIDATION_KEY,JSON.stringify(data));}
    catch{durable=false;}
    reviewRevision++;scheduleFileSave();return durable;
  }
  function importValidation(data){if(validationStorageError)throw Error('Resolve the unread evidence backup before importing.');mergeValidation(data);const durable=persistValidation();render();if(currentID&&dialog.open)openViewer(currentID);notice(durable?'Validation evidence merged; stars and manual stages unchanged.':'Evidence remains in this page. Export validation evidence to keep it; browser evidence backup failed.');}
  function validationBadge(a,axis){
    const result=validationSummary(a,axis);
    return '<span class="validation-badge '+esc(result.stale?'stale':result.applicability==='not_applicable'?'na':result.status)+'" data-validation-axis="'+axis+'" title="'+esc(result.reasons.join(' '))+'">'+(axis==='character'?'CHARACTER':'SCENE')+' · '+esc(result.label)+'</span>';
  }
  function validationPanel(a,axis){
    const history=validationLatest(a.id,axis),sets=(validationData.criteriaSets||[]).filter(c=>c.axis===axis&&c.project===a.project&&!(validationData.inactiveCriteriaSetIDs||[]).includes(c.id));
    let html='<details class="validation-panel"><summary>'+validationBadge(a,axis)+' · Evidence ('+history.length+')</summary><p class="review-help">Each result covers its named scope. Stars, manual Verification, and Production retain their existing meaning.</p>';
    if(validationStorageError)html+='<p role="alert">'+esc(validationStorageError)+'</p>';
    for(const assessment of history){
      const r=validationAssessment(assessment);
      html+='<details class="validation-record"><summary>'+esc(assessment.scope.label||assessment.scope.id)+' · '+esc(r.stale?'Stale':r.applicability==='not_applicable'?'N/A':r.status)+' · '+esc(assessment.reviewer.name)+'</summary><p>'+esc(assessment.evidence)+'</p><p>'+esc(assessment.uncertainty)+'</p><ul>'+r.reasons.map(s=>'<li>'+esc(s)+'</li>').join('')+'</ul><p>'+esc(assessment.reviewer.reviewedAtUTC)+' · '+esc(assessment.reviewer.model)+' · '+esc(assessment.reviewer.surface)+'</p><p>Target '+esc(assessment.target.assetID)+' · '+esc(assessment.target.sha256)+'</p><p>Reference '+esc(assessment.reference?.assetID||'None')+' · '+esc(assessment.reference?.sha256||'None')+'</p><p>Criteria '+esc(assessment.criteria?.id||'N/A')+' · '+esc(assessment.criteria?.version||'N/A')+'</p><p>Provenance: '+esc(assessment.provenance.source)+'</p><ul>'+assessment.criteriaResults.map(c=>'<li>'+esc(c.criterionID)+' · '+esc(c.visibility)+(c.presence?' · '+esc(c.presence):'')+' · '+esc(c.outcome)+': '+esc(c.observation)+'</li>').join('')+'</ul></details>';
    }
    html+='<details><summary>Record a scoped comparison</summary><div data-validation-form="'+axis+'"><label>Reference and criteria<select data-v-field="criteria" data-v-axis="'+axis+'"><option value="">Choose a documented scope</option>'+sets.map(c=>'<option value="'+esc(c.id)+'">'+esc(c.title)+'</option>').join('')+'</select></label><div data-v-criteria="'+axis+'"></div><label>Applicability<select data-v-field="applicability" data-v-axis="'+axis+'"><option value="required">Required for this scope</option><option value="optional">Optional</option><option value="not_applicable">N/A</option></select></label><label>Recorded result<select data-v-field="status" data-v-axis="'+axis+'">'+['not_checked','uncertain','fail','pass'].map(v=>'<option value="'+v+'">'+esc(v.replace('_',' '))+'</option>').join('')+'</select></label><label>Reviewer<input data-v-field="reviewer" data-v-axis="'+axis+'" placeholder="Your name"></label><label>Reviewer model or human<input data-v-field="model" data-v-axis="'+axis+'" placeholder="human, or actual model/version"></label><label>Evidence / N/A explanation<textarea data-v-field="evidence" data-v-axis="'+axis+'"></textarea></label><label>Uncertainty<textarea data-v-field="uncertainty" data-v-axis="'+axis+'"></textarea></label><label><input type="checkbox" data-v-field="seen" data-v-axis="'+axis+'"> I inspected these exact target and reference originals.</label><button data-v-save="'+axis+'" data-v-target="'+esc(a.id)+'">Save evidence</button><p class="review-help">Missing or hidden required features cannot pass. A detail result never validates the whole actor or scene.</p></div></details><button data-v-export>Export validation evidence</button><button data-v-import>Import validation evidence</button></details>';
    return html;
  }
  function validationCriterionFields(axis,c){
    const presence=c.presenceRequired?'<label>Presence<select data-v-axis="'+axis+'" data-v-presence="'+esc(c.id)+'"><option value="unknown">Not assessed</option><option value="present">Present</option><option value="absent">Absent</option></select></label><p class="review-help">Hidden or cropped: leave presence unassessed. Present does not automatically mean Pass.</p>':'';
    return '<fieldset><legend>'+esc(c.label)+(c.required?' · required':' · optional')+'</legend>'+(c.presenceRequired?'<details class="validation-rule"><summary>Reference guidance</summary><p>'+esc(c.rule)+'</p></details>':'<p>'+esc(c.rule)+'</p>')+'<label>'+(c.presenceRequired?'Area visibility':'Visibility')+'<select data-v-axis="'+axis+'" data-v-visibility="'+esc(c.id)+'"><option value="unknown">Unknown</option><option value="visible">'+(c.presenceRequired?'Area visible':'Visible')+'</option><option value="occluded">Hidden / cropped</option><option value="missing">Image unavailable</option></select></label>'+presence+'<label>Outcome<select data-v-axis="'+axis+'" data-v-outcome="'+esc(c.id)+'"><option value="not_checked">Not checked</option><option value="pass">'+(c.presenceRequired?'Pass · looks right':'Pass')+'</option><option value="fail">'+(c.presenceRequired?'Fail · needs a change':'Fail')+'</option><option value="uncertain">Uncertain</option></select></label><label>Observation<textarea data-v-axis="'+axis+'" data-v-observation="'+esc(c.id)+'"></textarea></label></fieldset>';
  }
  function bindValidationControls(a){
    const field=(axis,key)=>[...document.querySelectorAll('[data-v-field]')].find(n=>n.dataset.vAxis===axis&&n.dataset.vField===key);
    document.querySelectorAll('[data-v-field]').forEach(node=>{if(node.dataset.vField==='criteria')node.addEventListener('change',()=>{
      const axis=node.dataset.vAxis,def=(validationData.criteriaSets||[]).find(c=>c.id===node.value),box=[...document.querySelectorAll('[data-v-criteria]')].find(n=>n.dataset.vCriteria===axis);
      if(!box)return;const ref=def&&byID.get(def.reference.assetID);
      box.innerHTML=!def?'<p>Choose a reference, or record an explained N/A.</p>':'<p>'+esc(def.scope.label)+' · '+esc(def.allowedVariation)+'</p>'+(ref?'<a href="'+esc(href(ref.src))+'" target="_blank" rel="noopener"><img class="validation-reference" src="'+esc(href(ref.src))+'" alt="'+esc(ref.title)+'">Open exact reference</a>':'<p>Reference image missing.</p>')+def.criteria.map(c=>validationCriterionFields(axis,c)).join('');
    });});
    document.querySelectorAll('[data-v-save]').forEach(button=>button.addEventListener('click',()=>{
      try{
        const axis=button.dataset.vSave,def=(validationData.criteriaSets||[]).find(c=>c.id===field(axis,'criteria')?.value),applicability=field(axis,'applicability')?.value;
        if(!def&&applicability!=='not_applicable')throw Error('Choose documented criteria for an applicable comparison.');
        const form=[...document.querySelectorAll('[data-validation-form]')].find(n=>n.dataset.validationForm===axis);
        const find=(attribute,id)=>[...document.querySelectorAll('['+attribute+']')].filter(n=>n.dataset.vAxis===axis).find(n=>n.getAttribute?n.getAttribute(attribute)===id:n.attributes?.[attribute]===id);
        const ref=def&&byID.get(def.reference.assetID),stamp=new Date().toISOString(),record={schemaVersion:1,id:'local:'+stamp+':'+a.id+':'+axis+':'+Math.random().toString(36).slice(2),target:vBinding(a),axis,applicability,status:field(axis,'status')?.value||'not_checked',scope:def?.scope||{id:'not_applicable',kind:'none',label:'Explicit N/A'},criteria:def?{id:def.id,version:def.version,sha256:def.sha256}:null,reference:def?.reference||null,reviewer:{name:field(axis,'reviewer')?.value||'',model:field(axis,'model')?.value||'',surface:'CFA local review UI · user attestation',reviewedAtUTC:stamp},imagesSeen:field(axis,'seen')?.checked&&ref?[{...vBinding(a),accessible:true,view:'original'},{...vBinding(ref),accessible:true,view:'original'}]:[],criteriaResults:(def?.criteria||[]).map(c=>({criterionID:c.id,...(c.presenceRequired?{presence:find('data-v-presence',c.id)?.value||'unknown'}:{}),visibility:find('data-v-visibility',c.id)?.value||'unknown',outcome:find('data-v-outcome',c.id)?.value||'not_checked',observation:find('data-v-observation',c.id)?.value||''})),evidence:field(axis,'evidence')?.value||'',uncertainty:field(axis,'uncertainty')?.value||'',provenance:{source:'Explicit entry in CFA reference-validation UI'}};
        importValidation({format:VALIDATION_KEY,schemaVersion:1,assessments:[record]});
      }catch(error){notice(error.message);}
    }));
    document.querySelectorAll('[data-v-export]').forEach(b=>b.addEventListener('click',()=>downloadJSON(validationEnvelope(),'cfa-reference-validation.json')));
    document.querySelectorAll('[data-v-import]').forEach(b=>b.addEventListener('click',()=>input.click()));
  }
  archiveLegacy(C.reviewDecisions);
  mergeValidation({format:VALIDATION_KEY,schemaVersion:1,assessments:validationData.assessments||[]});
  let legacyValidationRaw=null,legacyValidationBackup=null;
  try{legacyValidationRaw=localStorage.getItem(REVIEW_KEY);if(legacyValidationRaw){legacyValidationBackup=JSON.parse(legacyValidationRaw);archiveLegacy(legacyValidationBackup.items);}}
  catch(error){retainUnread(REVIEW_KEY,legacyValidationRaw,error);}
  let sidecarValidationRaw=null;
  try{sidecarValidationRaw=localStorage.getItem(VALIDATION_KEY);if(sidecarValidationRaw)mergeValidation(JSON.parse(sidecarValidationRaw));}
  catch(error){retainUnread(VALIDATION_KEY,sidecarValidationRaw,error);}
  if(legacyValidationBackup?.validationEvidence){
    try{mergeValidation(legacyValidationBackup.validationEvidence);}
    catch(error){retainUnread(REVIEW_KEY,legacyValidationRaw,error);}
  }
  // END reference-validation-v1

  function matchingAsset(item,{requireHash=false,allowAliasID=false}={}) {
    if (!item || typeof item !== 'object' || typeof item.id !== 'string') return null;
    const a=byID.get(item.id);
    if(a)return (requireHash&&a.sha256?item.sha256===a.sha256:!item.sha256||item.sha256===a.sha256)?a:null;
    const alias=assetAliases.get(item.id);
    return alias&&(item.sha256===alias.sha256||allowAliasID&&item.sha256==null)?aliasTarget(item.id):null;
  }
  const destinations = ['undecided','Gemini','Flow','Grok','grok_video','ComfyUI'];
  const destinationLabel=d=>({undecided:'Undecided',Grok:'Grok stills',grok_video:'Grok video'}[d]||d);
  const providerDestinations=provider=>provider==='Grok'?['Grok','grok_video']:[provider];
  const planHasProvider=(plan,provider)=>providerDestinations(provider).some(d=>plan?.destinations?.includes(d));
  function providerShotExportControls(provider,plans){return providerDestinations(provider).filter(d=>plans.some(a=>reviewRecord(a.id).shotPlan?.destinations.includes(d))).map(d=>`<button class="pill" data-mission-export="${d}">Export ${esc(destinationLabel(d))} shot handoff</button>`).join('');}
  const creativeReviewRecipients=[['claude','Claude'],['grok_chief','Grok'],['gemini_chat','Gemini'],['flow','Flow']];
  function normalizedCreativeReview(value){
    if(!value||typeof value!=='object')return null;
    const recipients=Array.isArray(value.recipients)?[...new Set(value.recipients.filter(id=>creativeReviewRecipients.some(([known])=>id===known)))]:[];
    return recipients.length?{status:'queued',recipients,purpose:'find_story_use',scope:'music_video_and_interstitials',note:typeof value.note==='string'?value.note.slice(0,6000):''}:null;
  }
  function creativeReviewHandoffPayload(onlyID=null){
    const items=C.assets.filter(a=>!isDoc(a)&&normalVisible(a)&&(!onlyID||a.id===onlyID)&&normalizedCreativeReview(reviewRecord(a.id).creativeReview)).map(a=>({...exportReference(a),title:a.title,reviewStatus:reviewRecord(a.id).status,providerNote:a.note||'',creativeReview:normalizedCreativeReview(reviewRecord(a.id).creativeReview),instruction:'Find a useful story placement in the music video or stories between videos. Preserve the scene strengths; flag character differences against canonical references. This is a creative review, not a generation, production or identity-approval assignment.'}));
    return {format:'cfa-creative-review-handoff-v1',exported:new Date().toISOString(),status:'queued; not sent or generated',referencePolicy:{path:referencePolicyPath,instruction:referencePolicyText},attachmentReminder:'This file contains reference IDs, paths, hashes and review text. Attach actual images or verify local file access when delivering it. Only the named recipients should receive each request.',items};
  }
  function exportCreativeReviewRequests(onlyID=null){const data=creativeReviewHandoffPayload(onlyID);downloadJSON(data,'cfa-creative-review-requests.json');notice(data.items.length+' creative review requests exported. Give the file to Nova to relay to the named reviewers.');}
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
    document.querySelectorAll('[data-validation-scene]').forEach(node=>{if(node.dataset.validationScene===project+':'+shotID){const gate=validationTechnicalGate(record);node.textContent=gate.technicalReady?'Declared technical checks pass; final video judgment remains separate.':'Technical validation: '+gate.reasons.join(' ');}});
    document.querySelectorAll('[data-scene-gate]').forEach(node=>{if(node.dataset.sceneGate===project+':'+shotID)node.textContent=sceneHandoffGate(record).productionEligible?'Meets B-or-better scene target; final result acceptance is separate.':'Planning / repair: '+sceneHandoffGate(record).reasons.join(' ');});
  }
  function normalizedReview(item, origin='import') {
    const a=matchingAsset(item,{requireHash:true});
    if (!a || !(item.status == null || Object.hasOwn(statusLabels,item.status))) return null;
    const record={id:a.id,sha256:a.sha256||null,origin:item.origin||origin};
    if(item.id!==a.id)aliasedReviewRecords.add(record);
    if(Object.hasOwn(item,'status'))record.status=item.status||null;
    if(Object.hasOwn(item,'note'))record.note=typeof item.note==='string'?item.note.slice(0,20000):'';
    if(Object.hasOwn(item,'updatedAt'))record.updatedAt=typeof item.updatedAt==='string'?item.updatedAt:null;
    if(Object.hasOwn(item,'shotPlan'))record.shotPlan=normalizedPlan(item.shotPlan);
    if(['archived','working'].includes(item.collectionState))record.collectionState=item.collectionState;
    if(['candidate','approved'].includes(item.multiverseSelection))record.multiverseSelection=item.multiverseSelection;
    if(['prime','multiverse'].includes(item.variant)&&(origin==='catalog'||(item.variantSource!=='catalog'&&item.origin!=='catalog'))){record.variant=item.variant;record.variantSource=origin==='catalog'?'catalog':'user';}
    if(Object.hasOwn(item,'workingReference'))record.workingReference=normalizedWorkingReference(item.workingReference);
    if(isWorkingScope(item.workingReferenceScope))record.workingReferenceScope=item.workingReferenceScope;
    if(Object.hasOwn(item,'storyboardStage'))record.storyboardStage=Object.hasOwn(storyboardStages,item.storyboardStage)?item.storyboardStage:null;
    if(Object.hasOwn(item,'likenessRating'))record.likenessRating=normalizedRating(item.likenessRating);
    if(Object.hasOwn(item,'sceneQualityRating'))record.sceneQualityRating=normalizedRating(item.sceneQualityRating);
    if(Object.hasOwn(item,'creativeReview'))record.creativeReview=normalizedCreativeReview(item.creativeReview);
    if(origin==='browser'&&Object.hasOwn(record,'status')){
      const confirmed=(C.reviewDecisions||[]).find(r=>r.id===a.id&&r.sha256===a.sha256&&r.directUserClarification&&Object.hasOwn(statusLabels,r.status));
      const confirmedAt=Date.parse(confirmed?.directUserClarification?.recordedAtUTC),browserAt=Date.parse(record.updatedAt)||0;
      if(Number.isFinite(confirmedAt)&&browserAt<=confirmedAt)record.status=confirmed.status;
    }
    if(origin==='browser'&&Object.hasOwn(record,'likenessRating')){
      const confirmed=(C.reviewDecisions||[]).find(r=>r.id===a.id&&r.sha256===a.sha256&&r.humanRatingConfirmation?.field==='likenessRating');
      const receipt=confirmed?.humanRatingConfirmation,value=normalizedRating(confirmed?.likenessRating),confirmedAt=Date.parse(receipt?.decisionAtUTC||receipt?.recordedAtUTC),browserAt=Date.parse(record.updatedAt)||0;
      if(value!==null&&receipt.value===value&&Number.isFinite(confirmedAt)&&browserAt<=confirmedAt)record.likenessRating=value;
    }
    return record;
  }
  function isWorkingScope(value){return typeof value==='string'&&Object.hasOwn(workingScopes,value);}
  function normalizedWorkingReference(value){return value&&['requested','approved'].includes(value.status)&&isWorkingScope(value.scope)?{status:value.status,scope:value.scope}:null;}
  // The saved dropdown choice is independent of a requested or approved reference.
  function selectedWorkingScope(record){return isWorkingScope(record.workingReferenceScope)?record.workingReferenceScope:record.workingReference?.scope||'complete_look';}
  function mergeReview(record){
    const prior=reviews.get(record.id);
    if(prior&&aliasedCanonicalIDs.has(record.id)){
      const before=Date.parse(prior.updatedAt)||0,after=Date.parse(record.updatedAt)||0;
      if(after<before||after===before&&aliasedReviewRecords.has(record))return false;
    }
    const merged={status:null,note:'',shotPlan:null,...prior,...record};if(merged.variant==='multiverse')merged.workingReference=null;reviews.set(record.id,merged);return true;
  }
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

  try { const saved=JSON.parse(localStorage.getItem('cfa-visual-favorites-v1') || '[]'); if(Array.isArray(saved))favorites=new Set(saved.map(id=>typeof id==='string'?browseAsset(id)?.id:null).filter(Boolean)); } catch {storageOK=false;}
  try{const saved=JSON.parse(localStorage.getItem(EXPORT_KEY)||'null');if(saved?.format===EXPORT_KEY&&Array.isArray(saved.items)){for(const item of saved.items){const a=matchingAsset(item,{requireHash:true});if(a)basket.add(a.id);}}}catch{storageOK=false;}
  const iconStar = id => favorites.has(id) ? '★' : '☆';
  function notice(message) {let t=document.querySelector('.toast');if(!t){t=document.createElement('div');t.className='toast';t.setAttribute('role','status');document.body.append(t);}t.textContent=message;clearTimeout(toastTimer);toastTimer=setTimeout(()=>t.remove(),3500);}
  function assetReference(a){return {id:a.id,project:a.project,filename:a.filename,path:a.repoPath,sha256:a.sha256||null,role:a.category};}
  function exportAllowed(a){const r=reviewRecord(a.id);return !isArchived(a)&&r.status!=='remove'&&(state.exportIntent==='multiverse_ingredients'||r.variant!=='multiverse');}
  function exportReference(a){const r=reviewRecord(a.id);return {...assetReference(a),variant:r.variant||'prime',...(r.multiverseSelection?{multiverseSelection:r.multiverseSelection}:{}),workingReference:r.workingReference||null,...(isWorkingScope(r.workingReferenceScope)?{workingReferenceScope:r.workingReferenceScope}:{}),...(a.componentApprovals?.length?{componentApprovals:a.componentApprovals}:{}),referenceRole:effectiveReferenceRole(a),storyboardStage:storyboardStage(a),likenessRating:normalizedRating(r.likenessRating),sceneQualityRating:normalizedRating(r.sceneQualityRating),creativeReview:normalizedCreativeReview(r.creativeReview),note:r.note||'',knownDifferences:[bomRoles.get(a.id)?.knownDifferences,r.note].filter(Boolean).join(' '),referenceUsePolicy:referenceUsePolicy(a),validationEvidence:validationForExport(a)};}
  function exportIntentControls(){return `<label class="export-intent">Export intent<select data-export-intent><option value="prime" ${state.exportIntent==='prime'?'selected':''}>Prime references</option><option value="multiverse_ingredients" ${state.exportIntent==='multiverse_ingredients'?'selected':''}>Multiverse creative ingredients</option></select></label><p class="export-intent-help">${state.exportIntent==='prime'?'Multiverse ideas and removal requests stay out of exports.':'Multiverse ideas may be included as creative ingredients; removal requests still stay out.'} Review backups keep everything.</p>`;}
  function reviewPayload(){return {format:REVIEW_KEY,exported:new Date().toISOString(),
    status:'review decisions and notes; removal is a queue, not a file deletion',
    items:[...reviews.values()].map(record=>({...assetReference(byID.get(record.id)),...record})),
    sceneReviews:[...sceneReviews.values()],
    validationEvidence:validationEnvelope(),
    favorites:[...favorites].map(id=>byID.get(id)).filter(Boolean).map(assetReference),
    exportBasket:[...basket].map(id=>byID.get(id)).filter(Boolean).map(assetReference)};}
  function fileStatus(message){fileMessage=message;document.querySelectorAll('[data-review-file-status]').forEach(e=>e.textContent=message);}
  function saveBrowserReview(){
    if(!validationStorageError){try{localStorage.setItem(VALIDATION_KEY,JSON.stringify(validationEnvelope()));}catch{notice('Evidence backup unavailable; export validation evidence. Your manual review save will still be attempted.');}}
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
    if(isWorkingScope(asset?.defaultReferenceScope))defaults.workingReferenceScope=asset.defaultReferenceScope;
    if(['prime','multiverse'].includes(asset?.variant))Object.assign(defaults,{variant:asset.variant,variantSource:'catalog'});
    if(asset&&Object.hasOwn(asset,'workingReference'))defaults.workingReference=normalizedWorkingReference(asset.workingReference);
    const record={...defaults,...reviews.get(id)};
    return record.variant==='multiverse'?{...record,workingReference:null}:record;
  }
  function activeReviewRequest(a){return reviewRequests.get(a.id)&&!Object.hasOwn(statusLabels,reviewRecord(a.id).status)?reviewRequests.get(a.id):null;}
  function pendingReviewDecision(a){return normalVisible(a)&&!!activeReviewRequest(a);}
  function inReviewQueue(a){const r=reviewRecord(a.id);return !!activeReviewRequest(a)||isArchived(a)||['needs_fixes','remove'].includes(r.status)||r.workingReference?.status==='requested';}
  function refreshReviewUI(){
    const plansCount=document.querySelector('[data-view="shot_plans"] .count');if(plansCount)plansCount.textContent=projectAssets().filter(a=>reviewRecord(a.id).shotPlan).length;
    const count=document.querySelector('[data-view="review_queue"] .count');if(count)count.textContent=projectAssets(true).filter(pendingReviewDecision).length;
    document.querySelectorAll('[data-review-card]').forEach(card=>{
      card.querySelector('.review-chip')?.remove();const status=reviewRecord(card.dataset.reviewCard).status;
      if(status){const badge=document.createElement('span');badge.className='review-chip '+status;badge.textContent=statusLabels[status];card.append(badge);}
    });
    document.querySelectorAll('[data-review-status]').forEach(button=>{const active=reviewRecord(currentID).status===(button.dataset.reviewStatus||null);button.classList.toggle('selected',active);button.setAttribute('aria-pressed',String(active));});
    const status=document.querySelector('#review-current-status');if(status)status.textContent=statusLabels[reviewRecord(currentID).status]||'No triage decision';
    const archiveButton=document.querySelector('#viewer-archive');if(archiveButton){const archived=isArchived(byID.get(currentID));archiveButton.textContent=archived?'Restore from Archive':'Archive';archiveButton.setAttribute('aria-pressed',String(archived));}
    const archiveHelp=document.querySelector('[data-archive-help]');if(archiveHelp)archiveHelp.textContent=archiveHelpText(byID.get(currentID));
    document.querySelectorAll('[data-intake-live-progress]').forEach(el=>{el.textContent=intakeLiveProgress(byID.get(currentID)?.project||state.project);});
    refreshCollaboratorUI();
    refreshReferenceUI();
  }
  function updateReview(id,patch){
    if(!byID.has(id))return;
    const next={...reviewRecord(id),...patch,id,sha256:byID.get(id).sha256||null,updatedAt:new Date().toISOString(),origin:'user'};archiveLegacy([next]);mergeReview(next);
    reviewRevision++;saveBrowserReview();
    if(['status','storyboardStage','variant','workingReferenceScope','likenessRating','sceneQualityRating','creativeReview','collectionState','multiverseSelection'].some(key=>Object.hasOwn(patch,key)))render();
    refreshReviewUI();scheduleFileSave();
  }
  function archiveHelpText(a){return isArchived(a)?'In Archive. Review decisions, reference roles, favorites and shot plans are retained.':reviewRecord(a.id).status==='remove'?'Outside Archive; the separate removal decision still hides this reference.':'Archive hides this reference from ordinary browsing and media exports. Your review and source file stay intact.';}
  function toggleArchive(id){const a=byID.get(id);if(!a)return;const archived=!isArchived(a);updateReview(id,{collectionState:archived?'archived':'working'});notice(archived?'Moved to Archive. Your review and source file are retained.':reviewRecord(id).status==='remove'?'Restored from Archive. The separate removal decision is unchanged.':'Restored from Archive. Your saved review is unchanged.');}
  function reviewControls(a){const record=reviewRecord(a.id);return `<section class="review-controls" aria-label="Review this reference"><h3>Your review</h3>${state.view==='intake'?`<p class="review-help" data-intake-live-progress>${esc(intakeLiveProgress(a.project))}</p>`:''}<p id="review-current-status" class="review-current">${esc(statusLabels[record.status]||'No triage decision')}</p><div class="review-actions">${[['keep','Keep'],['needs_fixes','Needs fixes'],['remove','Mark for removal'],['','Clear decision']].map(([value,label])=>`<button data-review-status="${value}" class="${record.status===(value||null)?'selected':''}" aria-pressed="${record.status===(value||null)}">${label}</button>`).join('')}</div>${notePresetsControls()}<label for="review-note">Your note</label><textarea id="review-note" rows="4" maxlength="20000" placeholder="What should stay, change, or be removed from the working collection?">${esc(record.note)}</textarea>${a.note?`<p class="label">Image description</p><p>${esc(a.note)}</p>`:''}${activeReviewRequest(a)?`<p class="review-help">${esc(activeReviewRequest(a).requestedBy==='nova'?'Nova':activeReviewRequest(a).requestedBy)} requested your decision: ${esc(activeReviewRequest(a).reason)}</p>`:''}<p class="review-help">Marking for removal queues a sorting request. It never deletes the source file. Clear removes the decision and keeps your note.</p><p class="review-file-status" data-review-file-status role="status">${esc(fileMessage)}</p><button class="small-link" id="viewer-save-review">Save review file</button><button class="small-link" id="viewer-export-review">Export review</button><div class="collection-state-control"><button type="button" id="viewer-archive" aria-pressed="${isArchived(a)}">${isArchived(a)?'Restore from Archive':'Archive'}</button><p class="review-help" data-archive-help>${esc(archiveHelpText(a))}</p></div></section>`;}

  function toggleFavorite(id){favorites.has(id)?favorites.delete(id):favorites.add(id);saveFavorites();document.querySelectorAll('[data-favorite]').forEach(b=>{const on=favorites.has(b.dataset.favorite);b.classList.toggle('on',on);b.textContent=iconStar(b.dataset.favorite);b.setAttribute('aria-pressed',String(on));b.setAttribute('aria-label',(on?'Remove favorite: ':'Favorite: ')+byID.get(b.dataset.favorite).title);});const count=document.querySelector('[data-view="favorites"] .count');if(count)count.textContent=projectAssets().filter(a=>favorites.has(a.id)).length;if(state.view==='favorites'&&!currentID)renderMain();}
  function basketPayload(backup=false){const selected=[...basket].map(id=>byID.get(id)).filter(Boolean),items=backup?selected:selected.filter(exportAllowed);return {format:EXPORT_KEY,exported:new Date().toISOString(),status:backup?'browser selection backup; not an export handoff':'selected references; no approval implied',exportIntent:backup?'review_backup':state.exportIntent,excludedCount:selected.length-items.length,referencePolicy:{path:referencePolicyPath,instruction:referencePolicyText},referenceReminder:'This is a selection list. The actual images, clips, and documents are not bundled.',items:items.map(exportReference)};}
  function saveBasket(){reviewRevision++;saveBrowserReview();scheduleFileSave();document.querySelectorAll('[data-view="export_basket"] .count').forEach(e=>e.textContent=basketAssets().length);document.querySelectorAll('[data-basket]').forEach(button=>{const on=basket.has(button.dataset.basket);button.classList.toggle('on',on);button.textContent=button.id==='viewer-basket'?(on?'⇩ In export basket':'⇩ Add to export basket'):(on?'✓':'⇩');button.setAttribute('aria-pressed',String(on));button.setAttribute('aria-label',(on?'Remove from export basket: ':'Add to export basket: ')+byID.get(button.dataset.basket).title);});if(state.view==='export_basket'&&!currentID)renderMain();}
  function toggleBasket(id){if(!byID.has(id))return;basket.has(id)?basket.delete(id):basket.add(id);saveBasket();}
  function exportBasket(){const data=basketPayload();downloadJSON(data,'cfa-export-selection.json');notice(data.items.length+' references exported; '+data.excludedCount+' excluded by export intent. Media files are not bundled.');}
  function importBasket(items){let added=0,skipped=0;for(const item of items){const a=matchingAsset(item,{requireHash:true});if(a){basket.add(a.id);added++;}else skipped++;}return {added,skipped};}
  function queryMatch(a){if(isArchived(a)&&state.view!=='archive')return false;const text=[a.title,a.filename,a.album,isDoc(a)?a.text:'',a.note,a.beat,a.lyric,reviewRecord(a.id).note,...(a.tags||[])].join(' ').toLowerCase();return text.includes(state.search.toLowerCase().trim());}
  function isArchived(a){if(!a)return false;const r=reviewRecord(a.id),choice=r.collectionState,selectedInspiration=retiredInspirationIDs.has(a.id)&&(r.workingReference?.status==='approved'||r.status==='keep'&&(r.storyboardStage||a.storyboardStage)==='production');return choice==='archived'||choice!=='working'&&(!!a.archived||historyArchiveIDs.has(a.id)&&!selectedInspiration);}
  function normalVisible(a){return !!a&&!isArchived(a)&&reviewRecord(a.id).status!=='remove';}
  function archiveAssets(){return projectAssets(true).filter(isArchived);}
  function projectAssets(includeArchived=false){return C.assets.filter(a=>a.project===state.project&&(includeArchived||normalVisible(a)));}
  const basketAssets=()=>C.assets.filter(a=>basket.has(a.id)&&normalVisible(a));
  function effectiveReferenceRole(a){
    if(a.referenceRole==='Location guide only')return 'detail';
    const mapped=bomRoles.get(a.id);if(mapped)return mapped.role;
    const locked=(a.componentApprovals||[]).find(c=>c.sourceSHA256===a.sha256&&c.status==='user_selected_component');if(locked)return locked.scope;
    const r=reviewRecord(a.id);if(r.workingReference?.status==='approved')return r.workingReference.scope;const scope=r.workingReferenceScope;
    if(scope==='outfit')return 'outfit';if(scope==='detail')return 'detail';
    return 'scene';
  }
  function referenceUsePolicy(a){
    const role=effectiveReferenceRole(a),sceneSpecific=role==='scene'||!!reviewRecord(a.id).shotPlan;
    return {policyPath:referencePolicyPath,explicitSceneReference:sceneSpecific?{id:a.id,sha256:a.sha256||null,scope:'this_scene_only',instruction:'Use this explicitly named reference for this scene only; retain canonical scoped character components.'}:null,defaultReferenceSelection:{instruction:'For other scenes use canonical scoped gold standards and the highest-rated suitable approved Prime references.',requiredRole:role,sameRoleRequired:true,ratingField:'likenessRating',sceneCraftExcluded:true,unratedIsNotFive:true},referenceRole:role,sceneSpecific,imageDoesNotReplaceIdentity:true,ratingDoesNotApprove:true,sceneCraftDoesNotApprove:true};
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
  function castSetupIDs(){return new Set((C.castCollections||[]).filter(g=>g.project===state.project).flatMap(g=>[...(g.setupAssetIDs||[]),...(g.candidateSetupIDs||[]),...(g.referenceAssetIDs||[])].filter(id=>id!==(g.representativeID||g.coverID))));}
  function castWorkingGroups(collectionID=''){
    const approved=new Map(workingBOMEntries().filter(e=>['identity','complete_look'].includes(e.role)).map(e=>[e.asset.id,e]));
    const definitions=(C.castCollections||[]).filter(g=>g.project===state.project).map(g=>{
      const approvedIDs=(g.currentIDs||g.assetIDs||[]).filter(id=>approved.has(id)),selectedIDs=[...new Set(g.workingReferenceIDs||[])];
      const historyIDs=[...new Set(g.historicalReferenceIDs||g.historyIDs||[])],referenceIDs=[...new Set([...(g.referenceAssetIDs||[]),...(g.currentIDs||[])])],setupIDs=[...new Set([...(g.setupAssetIDs||[]),...(g.candidateSetupIDs||[])])];
      const claimed=new Set([...approvedIDs,...selectedIDs]),take=ids=>ids.filter(id=>{if(claimed.has(id))return false;claimed.add(id);return true;});
      const references=take(referenceIDs),setup=take(setupIDs),characterStudies=take(g.characterStudyIDs||[]),sceneStudies=take(g.sceneStudyIDs||[]),revisions=take(g.revisionStudyIDs||[]),history=take(historyIDs),assetIDs=[...new Set([...approvedIDs,...selectedIDs,...references,...setup,...characterStudies,...sceneStudies,...revisions,...history])];
      return {...g,id:g.id+'-working',castCollectionID:g.id,title:g.workingTitle||(g.title.split(' · ')[0]+' · '+(selectedIDs.length?'selected design references':'design & animation references')),assetIDs,role:selectedIDs.some(id=>!approved.has(id))?'Selected set · Approval not recorded':references.length||setup.length||history.length?'Reference candidates · Approval not recorded':'Approved design references',unit:'design & animation references',sections:[{title:'Approved design references',assetIDs:approvedIDs},{title:'Selected design references',assetIDs:selectedIDs.filter(id=>!approved.has(id)),description:'Selected for this character\'s working set. Per-image approval, stars and design stages remain as recorded.'},{title:'Design reference candidates',assetIDs:references,history:true},{title:'Animation/setup candidates',assetIDs:setup,history:true},{title:'Boss dais · character and staging candidates',assetIDs:characterStudies,description:'Returned studies of the selected boss. Individual reviews remain separate.'},{title:'Counting room · scene candidates',assetIDs:sceneStudies},{title:'Earlier repair versions',assetIDs:revisions,history:true},{title:'Earlier studies',assetIDs:history,history:true}],description:'Design, body angles, mouth shapes and setup material stay here. Candidate inclusion does not approve the design, validate animation or accept a new scene.',hubLinks:[{label:'Open character hub',href:castHubHref(g.project,'cast',g.id)}]};
    });
    return collectionGroups(definitions).filter(g=>!collectionID||collectionID===g.castCollectionID||collectionID===g.id);
  }
  function supportingWorkingReferences(){
    const groups=castWorkingGroups(state.view==='working'?state.album:'');return groups.length?collapsibleSection('supporting-working','Supporting-character design & animation references',()=>`<p class="intro">Selected working sets, setup candidates and recorded approvals keep their separate status.</p>${collectionCards(groups)}`,{className:'supporting-working-references',count:groups.length}):'';
  }
  function workingReferenceVisibleIDs(){
    const references=(C.castCollections||[]).filter(g=>g.project===state.project).flatMap(g=>[...(g.workingReferenceIDs||[]),...(g.referenceAssetIDs||[]),...(g.currentIDs||[]),...(g.setupAssetIDs||[]),...(g.candidateSetupIDs||[]),...(g.characterStudyIDs||[]),...(g.sceneStudyIDs||[]),...(g.revisionStudyIDs||[]),...(g.historicalReferenceIDs||g.historyIDs||[])]).filter(id=>{const a=byID.get(id);return a?.project===state.project&&!isDoc(a)&&normalVisible(a);});
    return [...new Set([...workingBOMEntries().map(e=>e.asset.id),...references])];
  }
  function multiverseCandidates(){return projectAssets().filter(a=>!isDoc(a)&&reviewRecord(a.id).variant==='multiverse'&&queryMatch(a));}
  function approvedMultiverse(a){const r=reviewRecord(a.id);return normalVisible(a)&&r.variant==='multiverse'&&r.multiverseSelection==='approved'&&normalizedRating(r.likenessRating)>=2;}
  function compactBOMEntries(entries){
    if(state.project!=='hon')return entries;
    const mouthAlbums=new Set(['hon:mouth-v003-candidates','hon:mouth-v003-sheets','hon:mouth-detail-updates','hon:mouth-reference-updates','hon:mouth-continuity-candidates','hon:mouth-b-archive','hon:mouth-continuity-rejected']);
    const mouthIDs=new Set((C.mouthCoverage?.items||[]).filter(row=>byID.get(row.exactAssetID||row.assetID)?.sha256===row.sha256).map(row=>row.assetID));
    return entries.filter(e=>e.section!=='details'||e.asset.id==='HD-B-91ef00348229'||!(mouthIDs.has(e.asset.id)||mouthAlbums.has(e.asset.album)||['dental_mouth_only','mouth_detail'].includes(e.role)));
  }
  function bomGallery(title,items,description='',emptyMessage=''){
    if(!items.length&&!emptyMessage)return '';
    return `<section class="bom-part"><h3>${esc(title)}</h3>${description?`<p class="review-help">${esc(description)}</p>`:''}${items.length?`<div class="gallery">${items.map(card).join('')}</div>`:`<p class="muted">${esc(emptyMessage)}</p>`}</section>`;
  }
  function leadBOMBody(entries,coverID,compact){
    const character=compactBOMEntries(entries.filter(e=>e.section!=='scene')),section=name=>character.filter(e=>e.section===name&&e.asset.id!==coverID).map(e=>e.asset);
    let html=C.characterReferenceBoard?.project===state.project?characterReferenceBoard(C.characterReferenceBoard):'';
    html+=bomGallery('Default identity',section('identity'));
    html+=bomGallery('Approved details and placement',section('details'),'Each image retains its selected component scope.');
    html+=bomGallery('Body art',section('artwork'),'Artwork options remain distinct; a design sheet is not proof of an exact body transfer.');
    const accessories=collectionGroups(C.accessoryCollections||[]).map(g=>({...g,sectionLayout:'grid'}));
    if(accessories.length)html+=`<section class="bom-part bom-bling"><h3>Bling bling</h3><p class="review-help">Jewelry and hand details for any outfit or shot. Each reference keeps its recorded scope and review.</p>${collectionCards(accessories)}</section>`;
    html+=bomGallery('Wardrobe',section('wardrobe'));
    html+=bomGallery('Optional accessories and looks',section('optional'),'Selected Prime options; these do not replace the default identity.');
    html+=bomGallery('Approved Multiverse',multiverseCandidates().filter(approvedMultiverse),'Explicitly selected alternatives with character/component likeness of at least 2/5. Selection does not approve production.','No approved Multiverse selections yet. Review candidates in Verbose BOM and choose a selection in the image viewer.');
    html+=bomGallery('Video production candidates',entries.filter(e=>e.section==='scene').map(e=>e.asset),'For the named shot or motion only. These references do not redefine the character or accept a finished video.');
    const conflicts=projectAssets().filter(a=>!isDoc(a)&&queryMatch(a)&&storyboardStage(a)==='production'&&(reviewRecord(a.id).variant==='multiverse'||reviewRecord(a.id).status==='needs_fixes'));
    if(conflicts.length&&!compact)html+=`<details class="detail-drawer bom-wip"><summary>WIP (work in progress) · ${conflicts.length}</summary><p class="review-help">Saved stages and scoped choices are retained alongside their fixes or alternative direction.</p><div class="gallery">${conflicts.map(card).join('')}</div></details>`;
    if(!compact)html+=sharedCharacterReferences();
    return html;
  }
  function workingReferencesWorkspace(compact=false){
    const castRoute=state.album&&(C.castCollections||[]).some(g=>g.project===state.project&&[g.id,g.id+'-working'].includes(state.album));
    if(castRoute){const groups=castWorkingGroups(state.album);return collapsibleSection('working-bom','Character bill of materials',()=>collectionCards(groups),{className:'working-bom',count:groups.length,unit:'characters'});}
    if(state.album&&grillSourceAlbumIDs().has(state.album))return collectionCards(collectionGroups(C.albums.filter(al=>al.id===state.album)));
    const castGroups=castWorkingGroups(),supportingIDs=new Set(castGroups.flatMap(g=>g.items.map(a=>a.id)));
    const entries=workingBOMEntries().filter(e=>queryMatch(e.asset)&&!supportingIDs.has(e.asset.id)),definition=bomDefinitions.find(c=>c.project===state.project);
    const visible=projectAssets().filter(a=>!isDoc(a)&&queryMatch(a)&&!supportingIDs.has(a.id)),preferred=byID.get(definition?.coverAssetID);
    const cover=preferred&&normalVisible(preferred)?preferred:entries.find(e=>e.role==='identity')?.asset||entries[0]?.asset||visible[0];
    const groups=[...castGroups];
    if(cover&&(entries.length||visible.length)){
      const nestedIDs=compact?[]:[...(C.sharedReferenceCollections||[]).filter(g=>g.project===state.project).flatMap(g=>g.assetIDs||[]),...(C.accessoryCollections||[]).filter(g=>g.project===state.project).flatMap(g=>g.assetIDs||[]),...sharedCharacterAlbums().flatMap(al=>al.assetIDs||[])];
      const items=[...new Map([cover,...entries.map(e=>e.asset),...multiverseCandidates(),...nestedIDs.map(id=>byID.get(id)).filter(a=>a&&!isDoc(a)&&normalVisible(a)&&queryMatch(a))].map(a=>[a.id,a])).values()];
      const leadID=definition?.id||state.project+':character-bom';
      groups.unshift({id:leadID,project:state.project,title:C.projects.find(p=>p.id===state.project)?.name||'Character',role:'Character parts and reference candidates',cover,coverPreviewOnly:true,representativeID:cover.id,items,assetIDs:items.map(a=>a.id),unit:'references',renderBody:()=>leadBOMBody(entries,cover.id,compact),description:'Open each part for its own scope, review and source. A selected component does not approve the entire image.'});
    }
    return collapsibleSection('working-bom',compact?'Working references':'Character bill of materials',()=>`<p class="intro">One card per character. Open a cover for their parts, options and reference candidates.</p>${collectionCards(groups)}${groups.length?'':'<p class="empty">No character references match this search.</p>'}`,{className:'working-bom',count:groups.length,unit:'characters'});
  }
  function libraryLocation(){return ['mission_control','collaborators'].includes(state.view)?null:{project:state.project,view:state.view,album:state.album};}
  function rememberLibrary(){const previous=libraryLocation();if(previous){state.lastLibrary=previous;try{sessionStorage.setItem('cfa-last-library',JSON.stringify(previous));}catch{}}}
  function libraryReturn(){let saved=state.lastLibrary;try{saved=saved||JSON.parse(sessionStorage.getItem('cfa-last-library')||'null');}catch{}return saved&&C.projects.some(p=>p.id===saved.project)&&!['mission_control','collaborators'].includes(saved.view)?saved:{project:'hon',view:'all',album:''};}
  function resetStoryFilters(){Object.assign(state,{storyTheme:'all',storyStage:'all',storyStart:0,storyEnd:100,storyLayout:'panels',structureFilter:'all',structureSequence:'all',structureFoundation:'all'});}
  function normalizedBrowseRoute(project,view,album=''){
    if(project==='unassigned'){
      const asset=browseAsset(album);
      if(asset?.placement?.original?.project==='unassigned')return {project:asset.project,view:'asset',album:asset.id};
      const moved=C.assets.find(a=>album&&a.placement?.original?.album===album);
      if(moved&&!C.albums.some(a=>a.id===album&&a.assetIDs.length))return {project:moved.project,view:moved.category,album:moved.album};
      if(!C.assets.some(a=>a.project==='unassigned'))return {project:'hon',view:'intake',album:''};
    }
    return project==='hon'&&view==='inspiration'?{project,view:album==='hon:creature-ideas'?'cast':'archive',album:album==='hon:creature-ideas'?album:''}:{project,view,album};
  }
  function route(project,view='all',album=''){({project,view,album}=normalizedBrowseRoute(project,view,album));rememberLibrary();if(project!==state.project){state.castFilter='all';state.castSource='all';}if(project!==state.project||view==='storyboard'&&(state.view!==view||state.album!==album))resetStoryFilters();state={...state,project,view,album,search:'',...(view==='details'?{detailLayout:album?'all':project==='hon'?'all':'approved'}:{})};location.hash=[project,view,album].filter(Boolean).map(encodeURIComponent).join('/');render();window.scrollTo({top:0,behavior:'instant'});}
  function parseHash(){const [rawProject,rawView,rawAlbum]=location.hash.slice(1).split('/').map(decodeURIComponent);const {project:p,view:v,album:a}=normalizedBrowseRoute(rawProject,rawView,rawAlbum);if(p!==rawProject||v!==rawView||a!==(rawAlbum||''))location.hash=[p,v,a].filter(Boolean).map(encodeURIComponent).join('/');if(C.projects.some(x=>x.id===p)){if(p!==state.project){state.castFilter='all';state.castSource='all';}if(p!==state.project||v==='storyboard'&&(state.view!==v||state.album!==(a||''))){resetStoryFilters();state.search='';}if(v==='details'&&(state.project!==p||state.view!==v||state.album!==(a||'')))state.detailLayout=a?'all':p==='hon'?'all':'approved';state.project=p;state.view=['mission_control','collaborators','all','favorites','export_basket','review_queue','archive','shot_plans','documents','intake',...Object.keys(cats)].includes(v)?v:'all';state.album=a||'';const asset=browseAsset(a);if(asset&&asset.project===p){state.view=v==='asset'?asset.category:state.view;state.album=asset.album;state.openAsset=asset.id;}else delete state.openAsset;const destination=normalizedBrowseRoute(state.project,state.view,state.album);if(destination.view!==state.view){Object.assign(state,destination);location.hash=[state.project,state.view,state.album].filter(Boolean).map(encodeURIComponent).join('/');}}}
  function render(){
    const p=C.projects.find(p=>p.id===state.project);const all=projectAssets();
    document.title=p.name+' · Visual library';
    document.querySelector('#app').innerHTML=`<div class="shell"><aside class="sidebar"><p class="brand">CFA / VISUAL LIBRARY</p><div class="project-picker">${C.projects.filter(x=>x.id!=='unassigned'||C.assets.some(a=>a.project==='unassigned')).map(x=>`<button data-project="${x.id}" class="${state.project===x.id?'active':''}">${esc(x.name)}<small>${esc(x.subtitle)}</small></button>`).join('')}</div><nav class="nav" aria-label="Studio navigation">${C.reviewIntake?`<button data-view="intake" data-nav-project="${state.project==='unassigned'?'hon':state.project}" class="${state.view==='intake'?'active':''}">Intake verification <span class="count">${intakeReviewTotals(intakeFamilies().filter(f=>f.project===(state.project==='unassigned'?'hon':state.project))).remaining} left</span></button>`:''}<button data-view="mission_control" class="${state.view==='mission_control'?'active':''}">Ziggy’s Corner</button><button data-view="collaborators" class="${state.view==='collaborators'?'active':''}">Collaborators</button><button data-view="all" class="${state.view==='all'?'active':''}">All files <span class="count">${all.filter(a=>!isDoc(a)).length} visuals</span></button>${C.categories.map(([id,name])=>{if(id==='intake'||state.project==='hon'&&id==='inspiration')return '';const albums=C.albums.filter(x=>x.project===state.project&&x.category===id&&!(state.project==='hon'&&id==='comfy'&&comfyMouthAlbum(x)));const count=new Set(albums.flatMap(x=>x.assetIDs).filter(id=>normalVisible(byID.get(id)))).size;const visibleCount=id==='intake'?intakeFamilies().filter(f=>f.project===state.project).length:id==='working'?workingReferenceVisibleIDs().length:id==='comfy'?comfyWorkspaceIDs().length:count;return (visibleCount||['review','comfy'].includes(id)?`<button data-view="${id}" class="${state.view===id?'active':''}">${esc(name)}<span class="count">${visibleCount}</span></button>`:'')+(id==='review'?`<button data-view="archive" class="${state.view==='archive'?'active':''}">Archive <span class="count">${archiveAssets().length}</span></button>`:'');}).join('')}<button data-view="review_queue" class="${state.view==='review_queue'?'active':''}">Review queue <span class="count">${projectAssets(true).filter(pendingReviewDecision).length}</span></button><button data-view="shot_plans" class="${state.view==='shot_plans'?'active':''}">Shot plans <span class="count">${all.filter(a=>reviewRecord(a.id).shotPlan).length}</span></button><button data-view="documents" class="${state.view==='documents'?'active':''}">Documents <span class="count">${all.filter(isDoc).length}</span></button><button data-view="export_basket" class="${state.view==='export_basket'?'active':''}">⇩ Export basket <span class="count">${basketAssets().length}</span></button><button data-view="favorites" class="${state.view==='favorites'?'active':''}">☆ Favorites <span class="count">${all.filter(a=>favorites.has(a.id)).length}</span></button></nav><div class="sidebar-foot">${exportIntentControls()}<button id="save-review">Save review file</button><button id="export-review">↓ Export review & notes</button><button id="import">↑ Import review or selections</button><button id="export">↓ Export favorites only</button><p class="review-storage-hint">Review inbox: docs/notes/downloads. Export review uses your download folder; Save review file autosaves to the file you choose. Browser backup is local to this browser. Choose the file again after a refresh. Saved changes are available for Nova to read; they do not notify her automatically.</p><p class="review-file-status" data-review-file-status role="status">${esc(fileMessage)}</p><p class="build-stamp">Build ${esc(window.REVIEW_BUILD||'local preview')}</p></div></aside><div class="workspace"><div class="topbar"><span class="breadcrumb">${state.view==='shot_plans'&&state.album==='all-projects'?'All projects':esc(p.name)} / ${esc(cats[state.view]||({'mission_control':'Mission Control','collaborators':'Collaborators','all':'All files','favorites':'Favorites','export_basket':'Export basket','review_queue':'Review queue','archive':'Archive','shot_plans':'Shot plans','documents':'Documents'}[state.view]))}</span><input class="search" id="search" type="search" placeholder="Search looks, scenes, details…" aria-label="Search library" value="${esc(state.search)}"></div><main class="main" id="main"></main></div></div>`;
    document.querySelectorAll('[data-project]').forEach(b=>b.onclick=()=>route(b.dataset.project,['mission_control','collaborators','storyboard','intake'].includes(state.view)?state.view:'all'));
    document.querySelectorAll('[data-view]').forEach(b=>b.onclick=()=>route(b.dataset.navProject||state.project,b.dataset.view));
    document.querySelector('#search').oninput=e=>{state.search=e.target.value;renderMain();};
    document.querySelector('#export').onclick=exportFavorites;document.querySelector('#import').onclick=()=>document.querySelector('#import-file').click();document.querySelector('#save-review').onclick=chooseReviewFile;document.querySelector('#export-review').onclick=exportReview;
    renderMain();
    if(state.openAsset){const id=state.openAsset;delete state.openAsset;openViewer(id);}
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
  function card(a){if(!displayed.includes(a.id))displayed.push(a.id);return `<article class="media-card" data-review-card="${esc(a.id)}">${reviewRecord(a.id).status?`<span class="review-chip ${reviewRecord(a.id).status}">${esc(statusLabels[reviewRecord(a.id).status])}</span>`:''}<button class="favorite ${favorites.has(a.id)?'on':''}" data-favorite="${esc(a.id)}" aria-label="${favorites.has(a.id)?'Remove favorite: ':'Favorite: '}${esc(a.title)}" aria-pressed="${favorites.has(a.id)}">${iconStar(a.id)}</button><button class="basket-toggle ${basket.has(a.id)?'on':''}" data-basket="${esc(a.id)}" title="Export basket" aria-label="${basket.has(a.id)?'Remove from export basket: ':'Add to export basket: '}${esc(a.title)}" aria-pressed="${basket.has(a.id)}">${basket.has(a.id)?'✓':'⇩'}</button><button class="media-open" data-open="${esc(a.id)}"><div class="media-thumb"><img loading="lazy" src="${esc(href(a.thumb))}" alt="${esc(a.title)}">${a.kind==='video'||a.kind==='gif'?`<span class="play">${a.kind==='video'?'▶':'GIF'} ${clipDuration(a)===null?'Duration unknown':Math.round(clipDuration(a)*10)/10+'s'}</span>`:''}</div><div class="media-copy"><b>${esc(a.title)}</b><small>${esc(a.sceneID?a.lyric||'Storyboard idea':C.albums.find(x=>x.id===a.album)?.title||a.filename)}</small>${storyMaterialHint(a)}${cardLikeness(a)}</div></button></article>`;}
  function cardLikeness(a){const r=reviewRecord(a.id),rating=normalizedRating(r.likenessRating);return `<small class="card-likeness">Character / component: ${rating===null?'unrated':`${rating}/5 <span aria-hidden="true">${'★'.repeat(rating)}${'☆'.repeat(5-rating)}</span>`}</small>${r.variant==='multiverse'?`<small class="card-multiverse">Multiverse · ${approvedMultiverse(a)?'approved selection':'candidate'}</small>`:''}`;}
  function mediaGroup(title,description,items,albumID=''){
    if(!items.length)return '';
    return collapsibleSection('media:'+(albumID||title),title,()=>`${description?`<p>${esc(description)}</p>`:''}${albumID?`<p><button class="subtle-button" data-album="${esc(albumID)}">Open group · ${items.length}</button></p>`:''}<div class="gallery">${items.map(card).join('')}</div>`,{className:'story-section',count:items.length,unit:'files'});
  }
  function outfitGroups(media){
    const visible=new Set(media.map(a=>a.id));
    return C.albums.filter(al=>al.project===state.project&&al.category==='outfits').map(al=>{
      const items=[...new Set(al.assetIDs)].map(id=>byID.get(id)).filter(a=>a&&a.kind==='image'&&normalVisible(a)&&visible.has(a.id));
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
    return C.albums.filter(al=>al.project===state.project&&(al.category==='comfy'&&/head|mouth|viseme|breather/i.test(al.id+' '+al.title)||grillSourceAlbumIDs().has(al.id))&&al.assetIDs.some(id=>normalVisible(byID.get(id))));
  }

  function mouthCoverageStats(look){
    const rows=(C.mouthCoverage?.items||[]).filter(i=>i.lookID===look.id&&byID.get(i.assetID)?.sha256===i.sha256&&normalVisible(byID.get(i.assetID))),numbers=new Set(rows.map(r=>r.number).filter(Number.isInteger));
    const reviewed=rows.filter(r=>reviews.has(r.assetID)),accepted=rows.filter(r=>{const q=reviewRecord(r.assetID);return q.status==='keep'&&storyboardStage(byID.get(r.assetID))==='production';});
    const validated=rows.filter(r=>{if(!r.validationScopeID)return false;const latest=validationLatest(r.assetID,'character',r.validationScopeID)[0],check=latest&&validationAssessment(latest);return check?.status==='pass'&&check.current;});
    return {rows,files:rows.length,distinctHashes:new Set(rows.map(r=>r.sha256)).size,labels:numbers.size,reviewed:reviewed.length,acceptedFiles:accepted.length,acceptedLabels:new Set(accepted.map(r=>r.number).filter(Number.isInteger)).size,validatedLabels:new Set(validated.map(r=>r.number).filter(Number.isInteger)).size,distinctUsable:null};
  }
  function mouthCoverageBoard(){
    const board=C.mouthCoverage;if(!board)return '';
    const looks=board.looks.filter(l=>l.project===state.project&&!historicalMouthLooks.has(l.id));
    let html='<section class="mouth-coverage" id="mouth-coverage-board"><h3>Mouth coverage board</h3><p>What the animation recipe needs and what the artwork library contains are separate counts.</p><details><summary>Recipe input readiness · '+board.recipe.requiredStillAtlasSlots+' still-atlas slots required by this saved graph</summary><p>'+esc(board.recipe.title)+' · '+esc(board.recipe.checkpoint)+'</p><p><b>Mouth bank not consumed.</b> '+esc(board.recipe.clipEvidence)+'</p><ul>'+board.recipe.inputs.map(x=>'<li>'+esc(x)+'</li>').join('')+'</ul><p>'+esc(board.recipe.result)+' '+esc(board.recipe.lisanStatus)+'</p><p>'+esc(board.recipe.faceDriverConcern)+'</p><p><a href="'+esc(href('../../../../../../'+board.recipe.graph.path))+'" target="_blank" rel="noopener">Exact saved graph</a> · SHA256 '+esc(board.recipe.graph.sha256)+'</p><p>'+esc(board.clipProofRequirements)+'</p></details><h4>Reference artwork coverage</h4><p>Provider labels mix articulation, expressions and actions. A repeated take, alias or view does not add a new mouth category. Usable distinct articulation remains unknown; still evidence never proves temporal speech.</p>';
    for(const look of looks){
      const stats=mouthCoverageStats(look),open=!closedMouthLooks.has(look.id);
      html+='<div class="mouth-look"><h4>'+esc(look.title)+'</h4><p>'+esc(look.stableLook)+'</p><p>'+esc(look.planStatus)+'. '+esc(look.note)+'</p>';
      if(look.referenceAssetID&&normalVisible(byID.get(look.referenceAssetID)))html+='<button class="pill" data-open="'+esc(look.referenceAssetID)+'">Open selected scoped look</button>';
      html+='<button class="pill" data-mouth-look="'+esc(look.id)+'" aria-expanded="'+open+'">'+(open?'Close':'Open')+' coverage grid</button>';
      if(open){
        const keys=look.plannedNumbers.length?look.plannedNumbers:[...new Set(stats.rows.map(r=>r.number||r.assetID))],kinds=[['articulation','Core articulation labels'],['extended','Extended delivery / phonetic labels'],['expression','Expression / action labels'],['other','Accessory, history and unnumbered references']];
        for(const [kind,title] of kinds){
          const slots=keys.filter(n=>kind===(typeof n!=='number'?'other':board.articulationNumbers.includes(n)?'articulation':board.extendedNumbers.includes(n)?'extended':'expression'));if(!slots.length)continue;
          html+='<details><summary>'+title+' · '+slots.length+'</summary><div class="mouth-board-grid">';
          for(const number of slots){
            const rows=stats.rows.filter(r=>(r.number||r.assetID)===number),first=rows[0]&&byID.get(rows[0].assetID);
            const failures=rows.filter(r=>validationSummary(byID.get(r.assetID),'character').status==='fail'||reviewRecord(r.assetID).status==='needs_fixes');
            html+='<article class="mouth-slot"><b>'+esc(typeof number==='number'?String(number).padStart(2,'0'):'Reference')+' · '+esc(rows[0]?.label||'Missing candidate')+'</b>'+(first?'<img loading="lazy" src="'+esc(href(first.thumb||first.src))+'" alt="'+esc(first.title)+'">':'')+'<p>'+rows.length+' takes · '+(rows.length?(failures.length?'Needs repair / unresolved':'Unchecked unless scoped evidence shown'):'Missing')+'</p>';
            for(const row of rows){
              const a=byID.get(row.exactAssetID||row.assetID),v=validationSummary(a,'character');
              html+='<button class="small-link" data-open="'+esc(a.id)+'">'+esc(a.id)+' · '+esc(row.revision)+'</button><p>'+esc(v.label)+' · '+esc(row.yaw)+' / '+esc(row.pitch)+'</p>';
              const notes=board.observations.filter(o=>o.assetID===a.id);for(const note of notes)html+='<details><summary>Attributed pixel observation</summary><p>'+esc(note.observation)+'</p><small>'+esc(note.reviewer.actor)+' · '+esc(note.documentAtUTC)+' · '+esc(note.surface)+' · source '+esc(note.source.sha256)+'</small></details>';
            }
            if(look.id==='hon-external-off'&&[9,10].includes(number))html+='<p>09/10: different bytes, overlapping teeth-baring poses. Distinct articulation uncertain; both original reviews retained.</p>';
            if(rows.length>1)html+='<p>Multiple takes share this provider label. Different bytes do not establish different articulation.</p>';
            html+='</article>';
          }
          html+='</div></details>';
        }
        html+='<details><summary>Yaw, pitch, stable look and jewelry are separate axes</summary><p>'+esc(board.headPlan.note)+'</p><p>Recorded head-state slots: '+board.headPlan.receivedSlots+' / '+board.headPlan.baseSlots+'. Optional expansion: '+board.headPlan.expandedUniqueSlots+' unique slots; key-state selection is not accepted.</p><p>Unknown angle/revision fields stay unknown. No opposite view is inferred by mirroring, and macros do not fill head slots.</p></details>';
      }
      html+='</div>';
    }
    html+='<details><summary>Reference inventory and remaining decisions</summary><p>18 existing BOM entries; eight explicit scoped nominations. Ten default/family choices remain unresolved without revoking their existing approvals.</p><ul>'+(validationData.inventory||[]).filter(r=>r.project===state.project&&normalVisible(byID.get(r.reference.assetID))).map(r=>'<li><button class="small-link" data-open="'+esc(r.reference.assetID)+'">'+esc(r.label)+'</button> · '+esc(r.recordedSelection||'Default nomination unresolved')+' · '+esc(r.scope)+' · family '+esc(r.familyID||'unreconciled')+'</li>').join('')+'</ul><p>'+validationData.gaps.map(esc).join(' ')+'</p>';
    for(const pet of (validationData.petCandidates||[]).filter(p=>byID.get(p.assetID)?.project===state.project&&normalVisible(byID.get(p.assetID))))html+='<button class="pill" data-open="'+esc(pet.assetID)+'">Existing dog candidate · not nominated</button>';
    const guide=C.assets.find(a=>a.kind==='document'&&a.repoPath?.endsWith('/visual_library/REFERENCE_VALIDATION_GUIDE.txt'));
    return html+'</details><p>'+(guide?'<button class="pill" data-open="'+esc(guide.id)+'">Read the evidence, reviewer and backup guide</button>':'')+'</p></section>';
  }

  function sharedCharacterReferences(){
    const definitions=(C.sharedReferenceCollections||[]).filter(g=>g.project===state.project).map(g=>({...g,sections:g.sections?.filter(s=>!s.history)})),covered=new Set(definitions.flatMap(g=>g.sourceAlbumIDs||[]));
    const fallback=sharedCharacterAlbums().filter(al=>!covered.has(al.id)&&(state.view==='working'||!grillSourceAlbumIDs().has(al.id))).map(al=>({...al,description:al.description,coverID:outfitCover(al.assetIDs.map(id=>byID.get(id)).filter(a=>a&&!isDoc(a)))?.id}));
    const groups=collectionGroups([...definitions,...fallback]),candidates=multiverseCandidates();if(!groups.length&&!candidates.length)return '';
    return collapsibleSection('shared-heads-mouths','Verbose BOM',()=>`<p>Reusable heads, mouths and broader options. Each reference keeps its own scope and review.</p>${collectionCards(groups)}${mouthCoverageBoard()}${candidates.length?`<details class="detail-drawer multiverse-candidates"><summary>Multiverse candidates · ${candidates.length}</summary><p class="review-help">All current alternatives, including unselected and low-rated ideas. Select an image to record a separate Multiverse choice.</p><div class="gallery">${candidates.map(card).join('')}</div></details>`:''}`,{className:'shared-character-references',count:groups.length,ariaLabel:'Verbose BOM'});
  }
  function archiveReferenceGroups(media){
    const available=new Map(media.map(a=>[a.id,a])),claimed=new Set(),definitions=state.project==='hon'?[{id:'hon:tattoo-source-history',title:'Earlier tattoo alternatives and source sheets',assetIDs:historicalTattooReferenceIDs}]:[];
    for(const group of C.sharedReferenceCollections||[])if(group.project===state.project)for(const section of group.sections||[])if(section.history)definitions.push({id:group.id+':archive:'+definitions.length,title:section.title,assetIDs:section.assetIDs});
    for(const look of C.mouthCoverage?.looks||[])if(look.project===state.project&&historicalMouthLooks.has(look.id))definitions.push({id:'archive:'+look.id,title:look.title,assetIDs:(C.mouthCoverage.items||[]).filter(row=>row.lookID===look.id&&byID.get(row.exactAssetID||row.assetID)?.sha256===row.sha256).map(row=>row.assetID)});
    const groups=definitions.map(g=>{const items=[...new Set(g.assetIDs||[])].map(id=>available.get(id)).filter(a=>a&&!claimed.has(a.id));for(const a of items)claimed.add(a.id);return {...g,items,cover:items[0],sections:[{title:'Historical references',assetIDs:items.map(a=>a.id)}]};}).filter(g=>g.items.length);
    return {html:groups.length?collapsibleSection('archive-verbose','Earlier reference collections',()=>collectionCards(groups),{count:groups.length}):'',remaining:media.filter(a=>!claimed.has(a.id))};
  }
  const hiddenBrowseCollections=new Set(['hon:face-neck-ink','hon:optional-finish']);
  function detailDisplayCollection(group){
    if(group.id==='hon:piercings'){
      const accessories=(C.accessoryCollections||[]).filter(g=>g.project==='hon'),assetIDs=[...new Set([...group.assetIDs,...accessories.flatMap(g=>g.assetIDs||[])])];
      return {...group,title:'Piercings and jewelry',assetIDs,textOnly:true,sectionLayout:'grid',role:'Display images pending',description:'Individual jewelry designs lead this collection. Character-specific examples are nested below; standalone display images have not arrived yet.',sections:[{title:'Jewelry on display',assetIDs:[],emptyMessage:'Display references are needed for the dice earring, hoop options and rings. The acceptable design variations still need to be selected.'},{title:'Dolo · earrings and facial piercings',assetIDs:group.assetIDs,collapsible:true},...accessories.flatMap(g=>(g.sections||[]).map(s=>({...s,title:'Dolo · '+s.title,collapsible:true})))]};
    }
    if(group.id==='hon:return-detail-art'&&group.assetIDs.length===1&&group.assetIDs[0]==='HD-RETURN-41b93f64e7ea')return {...group,title:'Guns',role:'On-character example · display images pending',coverPreviewOnly:true,representativeID:group.assetIDs[0],representativeLabel:'View the worn prop example',description:'Gun designs and their accepted variations belong here. Character and outfit images are examples of how the props are worn.',sections:[{title:'Guns on display',assetIDs:[],emptyMessage:'Standalone display images are needed for the existing gun variations. Different designs are welcome; they do not need to match one exact gun.'},{title:'On-character examples',assetIDs:group.assetIDs,collapsible:true}]};
    return group;
  }
  function sharedCollectionReference(group,asset){
    return !!asset&&!isDoc(asset)&&normalVisible(asset)&&(group.sharedReferences||[]).some(ref=>ref.assetID===asset.id&&ref.sha256===asset.sha256&&ref.sourceProject===asset.project);
  }
  function collectionGroups(definitions,media=projectAssets()){
    const visible=new Set(media.filter(a=>!isDoc(a)).map(a=>a.id)),query=state.search.toLowerCase().trim();
    return definitions.filter(g=>g.project===state.project&&!hiddenBrowseCollections.has(g.id)).map(detailDisplayCollection).map(g=>{
      const allItems=[...new Set(g.assetIDs||[])].map(id=>byID.get(id)).filter(a=>a&&(visible.has(a.id)||sharedCollectionReference(g,a))&&(g.includeArchived||!isArchived(a))&&(g.includeRemoved||reviewRecord(a.id).status!=='remove'));
      const groupMatch=query&&[g.title,g.role,...(g.aliases||[])].join(' ').toLowerCase().includes(query);
      const items=allItems.filter(a=>!query||groupMatch||queryMatch(a));
      return {...g,items,cover:items.find(a=>a.id===(g.coverID||g.coverAssetID))||outfitCover(items)};
    }).filter(g=>g.items.length);
  }
  function characterReferenceBoard(board){
    const rows=board.rows.filter(row=>{const a=byID.get(row.asset.id);return a&&a.sha256===row.asset.sha256&&normalVisible(a)&&(queryMatch(a)||[row.label,row.scope].join(' ').toLowerCase().includes(state.search.toLowerCase().trim()));});
    if(!rows.length)return '';
    return `<section class="character-reference-board" aria-label="Character reference purposes"><h3>${esc(board.title)}</h3><p>${esc(board.scopeNotice)}</p><p>${esc(board.portraitContext)}</p>${rows.map(row=>{
      const a=byID.get(row.asset.id);if(!displayed.includes(a.id))displayed.push(a.id);
      return `<article class="reference-purpose-row" data-reference-role="${esc(row.id)}"><button type="button" class="reference-purpose-preview" data-open="${esc(a.id)}" aria-label="Open ${esc(row.label)}"><img src="${esc(href(a.thumb||a.src))}" alt="${esc(row.label)}" loading="lazy" decoding="async"><span>Open reference</span></button><div class="reference-purpose-copy"><h4>${esc(row.label)}${row.id==='body-build-candidate'?' · Provisional':''}</h4><p>${esc(row.scope)}</p><div class="tools"><a class="pill" href="${esc(href(a.src))}" target="_blank" rel="noopener">Full-size original ↗</a></div><details><summary>Source, limits and recorded choices</summary><p>${esc(a.filename)} · ${row.asset.bytes.toLocaleString()} bytes</p><code class="reference-version">${esc(row.asset.version)}</code>${row.provenance.map(p=>`<p>${esc(p.summary)}</p>`).join('')}<ul>${row.limitations.map(s=>`<li>${esc(s)}</li>`).join('')}</ul>${row.unresolved?.summary?`<p>${esc(row.unresolved.summary)}</p>`:''}</details></div></article>`;
    }).join('')}</section>`;
  }
  function collectionCards(groups){
    return `<div class="gallery collection-catalog">${groups.map(g=>{
      if(g.directSingle&&g.items.length===1)return card({...g.items[0],title:g.title});
      const expanded=expandedCollections.has(g.id),panel='collection-'+g.id.replace(/[^a-z0-9_-]/gi,'-'),cover=g.cover,status=reviewRecord(cover.id).status;
      let views='';
      if(expanded){
        if(g.renderBody)views=g.renderBody();else{
        const remaining=new Map(g.items.filter(a=>!g.coverPreviewOnly||a.id!==g.representativeID).map(a=>[a.id,a])),sections=g.sections||(g.preferredIDs?.length?[{title:'Your shortlist',assetIDs:g.preferredIDs},{title:'Other candidates',assetIDs:g.assetIDs.filter(id=>!g.preferredIDs.includes(id)),history:true}]:[{title:'Current references',assetIDs:g.currentIDs||g.assetIDs},{title:'Earlier studies',assetIDs:g.historyIDs||[],history:true}]);
        if(g.children?.length){views+=collectionCards(g.children);for(const child of g.children)for(const a of child.items)remaining.delete(a.id);}
        // Historical media stays under its character, not in a second top-level collection.
        if(!g.sections&&g.historyIDs?.length)for(const id of g.historyIDs)if(!g.currentIDs)sections[0].assetIDs=sections[0].assetIDs.filter(x=>x!==id);
        for(const section of sections){const items=(section.assetIDs||[]).map(id=>remaining.get(id)).filter(Boolean);for(const a of items)remaining.delete(a.id);if(!items.length){if(section.emptyMessage)views+=`<section class="collection-section collection-pending"><h3>${esc(section.title)}</h3><p class="muted">${esc(section.emptyMessage)}</p></section>`;continue;}
          const gallery=`<div class="gallery">${items.map(card).join('')}</div>`;
          views+=section.history||section.collapsible?`<details class="${section.history?'collection-history':'collection-details'}" ${state.search.trim()?'open':''}><summary>${esc(section.title)} · ${items.length}</summary>${section.description?`<p class="review-help">${esc(section.description)}</p>`:''}${gallery}</details>`:`<section class="collection-section"><h3>${esc(section.title)}</h3>${section.description?`<p>${esc(section.description)}</p>`:''}${gallery}</section>`;
        }
        if(remaining.size)views+=`<section class="collection-section"><h3>Related references</h3><div class="gallery">${[...remaining.values()].map(card).join('')}</div></section>`;
        if(g.sectionLayout==='grid')views='<div class="collection-sections-grid">'+views+'</div>';
        }
      }
      const unit=g.unit||'references',count=g.children?.length||g.items.length;
      const representative=g.coverPreviewOnly?g.items.find(a=>a.id===g.representativeID):null;if(representative&&!displayed.includes(representative.id))displayed.push(representative.id);
      const hubNavigation=representative||g.hubLinks?.length?`<nav class="character-hub-links" aria-label="Character reference navigation">${representative?`<button class="pill" data-open="${esc(representative.id)}">${esc(g.representativeLabel||'View character cover')}</button>`:''}${(g.hubLinks||[]).map(link=>`<a class="pill" href="${esc(link.href)}">${esc(link.label)}</a>`).join('')}</nav>`:'';
      const provenance=`${g.description?`<p>${esc(g.description)}</p>`:''}${g.notes?.length?`<ul class="collection-notes">${g.notes.map(note=>`<li>${esc(note)}</li>`).join('')}</ul>`:''}`;
      return `<article class="inline-collection ${expanded?'is-expanded':''} ${g.textOnly?'text-collection':''}" data-collection="${esc(g.id)}"><div class="collection-summary"><div class="media-card collection-cover" ${g.textOnly?'':`data-review-card="${esc(cover.id)}"`}>${status&&!g.textOnly?`<span class="review-chip ${status}">${esc(statusLabels[status])}</span>`:''}<button class="media-open" data-collection-toggle="${esc(g.id)}" aria-expanded="${expanded}" aria-controls="${esc(panel)}" aria-label="${expanded?'Collapse':'Expand'} ${esc(g.title)}">${g.textOnly?'':`<div class="media-thumb"><img loading="lazy" src="${esc(href(cover.thumb))}" alt="${esc(g.title)}">${isClip(cover)?`<span class="play">▶ ${clipDuration(cover)===null?'Video':Math.round(clipDuration(cover)*10)/10+'s'}</span>`:''}</div>`}<div class="media-copy"><b>${esc(g.title)}</b><small>${esc(g.role||'')} ${g.role?'· ':''}${count} ${esc(unit)}</small>${g.enhancementRequest?'<small class="collection-flag">Clarity improvement requested</small>':''}</div></button></div>${g.browseContextHTML||''}<button class="outfit-expand" data-collection-toggle="${esc(g.id)}" aria-expanded="${expanded}" aria-controls="${esc(panel)}">${expanded?'▾ Hide':'▸ Show'} ${esc(unit)}${expanded?'':' here'}</button></div><div id="${esc(panel)}" class="collection-inline-views" ${expanded?'':'hidden'}>${expanded?`${hubNavigation}${g.browseEvidenceHTML||''}${g.deferProvenance?'':provenance}${g.referenceBoard?characterReferenceBoard(g.referenceBoard):''}${views}${g.deferProvenance&&provenance?`<details class="collection-provenance"><summary>Reference notes and provenance</summary>${provenance}</details>`:''}`:''}</div></article>`;
    }).join('')}</div>`;
  }
  const castHubHref=(project,view,id)=>'#'+[project,view,id].map(encodeURIComponent).join('/');
  function castHubGroups(collectionID=''){
    const definitions=(C.castCollections||[]).filter(g=>g.project===state.project&&g.id!=='hon:creature-ideas'),covered=new Set(definitions.flatMap(g=>g.assetIDs));
    const fallback=C.albums.filter(al=>al.project===state.project&&al.category==='cast'&&al.id!=='hon:creature-ideas').map(al=>({...al,assetIDs:al.assetIDs.filter(id=>!covered.has(id))}));
    const exactCharacter=definitions.some(g=>g.id===collectionID);
    const hubs=[...definitions,...fallback].filter(g=>!collectionID||g.id===collectionID||!exactCharacter&&(g.sourceAlbumIDs||[]).includes(collectionID)).map(g=>{
      const chosenRepresentativeID=g.representativeID||g.coverID||g.coverAssetID||(g.currentIDs||g.assetIDs||[])[0];
      const representativeID=[...new Set([chosenRepresentativeID,...(g.currentIDs||[]),...(g.workingReferenceIDs||[])])].find(id=>{const a=byID.get(id);return a&&(a.project===g.project||sharedCollectionReference(g,a))&&!isDoc(a)&&normalVisible(a);})||chosenRepresentativeID;
      const relatedIDs=[...new Set([...(g.sceneAssetIDs||[]),...(g.videoAssetIDs||[]),...(g.relatedAssetIDs||[])])].filter(id=>byID.get(id)?.project===g.project&&!isDoc(byID.get(id)));
      const scenes=(g.sceneAssetIDs||[]).filter(id=>byID.get(id)?.kind==='image'),videos=(g.videoAssetIDs||[]).filter(id=>byID.has(id)&&isClip(byID.get(id))),related=(g.relatedAssetIDs||[]).filter(id=>!scenes.includes(id)&&!videos.includes(id));
      const discovery=!!g.preferredIDs?.length,preserveSections=!!g.sections&&!g.currentIDs;
      const sections=preserveSections?[...g.sections]:discovery?[{title:'Your shortlist',assetIDs:g.preferredIDs},{title:'Other candidates',assetIDs:(g.assetIDs||[]).filter(id=>!g.preferredIDs.includes(id)),history:true}]:[];
      const studies=[...(g.characterStudyIDs||[]),...(g.sceneStudyIDs||[]),...(g.revisionStudyIDs||[])],studyIDs=new Set(studies);
      sections.push(...[{title:'Boss dais · character and staging candidates',assetIDs:g.characterStudyIDs||[]},{title:'Counting room · scene candidates',assetIDs:g.sceneStudyIDs||[]},{title:'Earlier repair versions',assetIDs:g.revisionStudyIDs||[],history:true},{title:'Scene appearances',assetIDs:scenes.filter(id=>!studyIDs.has(id)),history:true},{title:'Video appearances',assetIDs:videos,history:true},{title:'Related story material',assetIDs:related,history:true}].filter(section=>section.assetIDs.length));
      const workingIDs=[...new Set([...(g.workingReferenceIDs||[]),...(g.referenceAssetIDs||[]),...(g.currentIDs||[]),...(g.setupAssetIDs||[]),...(g.candidateSetupIDs||[]),...(g.characterStudyIDs||[]),...(g.sceneStudyIDs||[]),...(g.revisionStudyIDs||[]),...(g.historicalReferenceIDs||g.historyIDs||[])])].filter(id=>normalVisible(byID.get(id)));
      return {...g,representativeID,coverID:representativeID,coverPreviewOnly:!discovery&&!preserveSections,assetIDs:[...new Set([...(discovery||preserveSections?g.assetIDs||[]:[representativeID]),...relatedIDs])],sections,unit:'related references',description:[g.description,relatedIDs.length?'Scene and pose candidates and videos keep their individual reviews; grouping is not acceptance.':''].filter(Boolean).join(' '),hubLinks:[{label:'Design & animation references'+(workingIDs.length?' · '+workingIDs.length:''),href:castHubHref(g.project,'working',g.id)},...(collectionID?[]:[{label:'Open character hub',href:castHubHref(g.project,'cast',g.id)}])]};
    });
    return collectionGroups(hubs);
  }
  function creatureBossIdeasGroup(){
    if(state.project!=='hon')return null;
    const album=C.albums.find(al=>al.id==='hon:creature-ideas');
    return album?collectionGroups([album])[0]||null:null;
  }
  function creatureBossIdeasSection(){
    const group=creatureBossIdeasGroup();if(!group)return '';
    return collapsibleSection('creature-boss-ideas',group.title,()=>`<p class="intro">${esc(group.description)} Earlier options stay separate from the selected character hubs above.</p><div class="gallery">${group.items.map(card).join('')}</div>`,{className:'creature-boss-ideas',count:group.items.length,unit:'files'});
  }
  function castBrowseFacts(g){
    const sources=[...new Set(g.sourceAlbumIDs||[])].map(id=>C.albums.find(a=>a.project===g.project&&a.id===id)).filter(Boolean).map(a=>({id:a.id,title:a.title}));
    const identityIDs=[...new Set([g.representativeID,g.coverID,...(g.currentIDs||[]),...(g.workingReferenceIDs||[])].filter(Boolean))];
    const choices=identityIDs.map(id=>byID.get(id)).filter(a=>a&&(a.roleDecision==='user_assigned'||a.selectionStatus==='user_selected_visible_golden_reference'));
    const ids=new Set((g.items||[]).map(a=>a.id));
    const shots=storyWorkItems(g.project).filter(s=>s.characterCollectionID===g.id||(s.panelAssetIDs||[]).some(id=>ids.has(id))||(s.materials||[]).some(m=>ids.has(m.assetID)&&m.sha256&&byID.get(m.assetID)?.sha256===m.sha256));
    const planned=shots.filter(s=>!(s.panelAssetIDs||[]).length),linked=shots.filter(s=>(s.panelAssetIDs||[]).length);
    const sequences=(C.storyboardSequences||[]).filter(s=>s.project===g.project&&(s.assetIDs||[]).some(id=>ids.has(id)));
    return {sources,choices,planned,linked,sequences,roles:choices.length>0};
  }
  function castBrowseContext(g,f){
    const tags=[f.roles?'Role choice recorded':'',f.planned.length?'Planned for storyboard':'',f.linked.length||f.sequences.length?'Storyboard-linked':''].filter(Boolean);
    const contextHTML=`<div class="cast-card-context">${tags.map(t=>`<span>${esc(t)}</span>`).join('')}${f.sources.length?`<small>From ${esc(f.sources[0].title)}${f.sources.length>1?' · +'+(f.sources.length-1)+(f.sources.length===2?' source':' sources'):''}</small>`:''}</div>`;
    const choice=f.choices.map(a=>`<li>${esc(a.characterRole||'Selected boss')} · ${a.roleDecision==='user_assigned'?'role assigned by Ziggy':'visible likeness selected by Ziggy'}</li>`).join('');
    const planned=f.planned.map(s=>`<li><strong>${esc(s.title)}</strong><p>${esc(s.sourceTitle||s.sectionLabel||'Planned scene')} · placement ${esc(s.timing||'unassigned')}</p></li>`).join('');
    const linked=[...f.linked,...f.sequences].map(s=>`<li>${esc(s.title)}${s.stage?' · '+esc(s.stage):''}</li>`).join('');
    return {...g,browseContextHTML:contextHTML,browseEvidenceHTML:`<details class="cast-origin"><summary>Origin & story connections</summary>${f.sources.length?`<p>Source collections / runs</p><div class="tools">${f.sources.map(s=>`<button class="pill" data-cast-source="${esc(s.id)}">${esc(s.title)}</button>`).join('')}</div>`:'<p>No source collection is recorded.</p>'}${choice?`<p>Recorded character choices</p><ul>${choice}</ul><p class="review-help">These choices assign a role or reference scope; each image keeps its own review.</p>`:''}${planned?`<h4>Planned storyboard use</h4><ul>${planned}</ul><p class="review-help">Scene intentions are recorded; no storyboard panel is linked to these plans yet.</p>`:''}${linked?`<h4>Linked storyboard material</h4><ul>${linked}</ul><p class="review-help">These are recorded connections, including drafts. Placement and acceptance stay with each shot.</p>`:''}${planned||linked?`<a class="pill" href="${esc(castHubHref(g.project,'storyboard',''))}">Browse storyboards →</a>`:''}</details>`};
  }
  function castExplorer(collectionID=''){
    const creatureOnly=state.project==='hon'&&collectionID==='hon:creature-ideas',all=creatureOnly?[]:castHubGroups(collectionID),facts=new Map(all.map(g=>[g.id,castBrowseFacts(g)]));
    const filterable=state.view==='cast'&&!collectionID;
    let groups=all,controls='',filtered=false;
    if(filterable){
      const sources=new Map();for(const f of facts.values())for(const s of f.sources){if(!sources.has(s.id))sources.set(s.id,{...s,count:0});sources.get(s.id).count++;}
      if(!sources.has(state.castSource))state.castSource='all';
      const fromSource=all.filter(g=>state.castSource==='all'||facts.get(g.id).sources.some(s=>s.id===state.castSource));
      const matches=(g,value)=>{const f=facts.get(g.id);return value==='roles'?f.roles:value==='planned'?f.planned.length>0:value==='linked'?f.linked.length+f.sequences.length>0:true;};
      const filters=[['all','All characters'],['roles','Recorded role choices'],['planned','Planned for storyboard'],['linked','Storyboard-linked']];
      if(!filters.some(([id])=>id===state.castFilter))state.castFilter='all';
      groups=fromSource.filter(g=>matches(g,state.castFilter));filtered=state.castSource!=='all'||state.castFilter!=='all';
      controls=`<section class="cast-browse-tools" aria-label="Filter supporting cast"><div class="tools cast-filter-buttons" role="group" aria-label="Character connections">${filters.map(([id,label])=>`<button class="pill ${state.castFilter===id?'active':''}" data-cast-filter="${id}" aria-pressed="${state.castFilter===id}">${label} · ${fromSource.filter(g=>matches(g,id)).length}</button>`).join('')}</div><label>Source collection / run <select id="cast-source"><option value="all">All sources</option>${[...sources.values()].map(s=>`<option value="${esc(s.id)}" ${state.castSource===s.id?'selected':''}>${esc(s.title)} · ${s.count} ${s.count===1?'character':'characters'}</option>`).join('')}</select></label>${filtered?'<button class="pill" data-cast-reset>Clear filters</button>':''}<p>${groups.length} ${groups.length===1?'character':'characters'} shown${state.castSource!=='all'?' · From '+esc(sources.get(state.castSource).title):''}. Storyboard plans and linked drafts are shown separately.</p></section>`;
    }
    const cards=groups.map(g=>castBrowseContext(g,facts.get(g.id)));
    const characters=creatureOnly?'':collapsibleSection('cast:'+collectionID,collectionID?'Character hub':'Supporting cast',()=>`<p class="intro">One representative per character, with related scenes and videos. Design angles, mouth shapes and setup candidates are in Working references.</p>${collectionCards(cards)}${groups.length?'':'<p class="empty">No characters match these filters. Clear filters or change the search.</p>'}`,{className:'cast-explorer',count:groups.length});
    return controls+characters+((!collectionID&&!filtered||creatureOnly)?creatureBossIdeasSection():'');
  }
  function accessoryExplorer(){
    const groups=collectionGroups(C.accessoryCollections||[]).map(g=>({...g,sectionLayout:'grid'}));return groups.length?collapsibleSection('accessories','Dolo’s jewelry & hand details',()=>`<p class="intro">Choose jewelry and hand details independently for any outfit or shot.</p>${collectionCards(groups)}`,{className:'accessory-explorer',count:groups.length}):'';
  }
  function detailAlbumGroups(al,items){
    const definitions=(C.detailDisplayGroups||[]).filter(g=>g.project===state.project&&g.albumID===al.id),covered=new Set(definitions.flatMap(g=>g.assetIDs));
    const groups=collectionGroups(definitions,items),other=items.filter(a=>!covered.has(a.id));
    return (groups.length?collapsibleSection('details:'+al.id,al.title,()=>`<p class="intro">One card per design. Transparent copies and option sheets are inside.</p>${collectionCards(groups)}`,{className:'story-section',count:groups.length}):'')+mediaGroup(groups.length?'Other details':al.title,'',other,al.id);
  }
  const browseLayout=()=>C.browseLayout?.projects?.[state.project]||{};
  function collapsibleSection(key,title,body,{count,unit='collections',className='',ariaLabel=title}={}){
    const id=[state.project,state.view,state.album||'root',key].join(':'),open=!collapsedBrowseBuckets.has(id),panel='section-'+id.replace(/[^a-z0-9_-]/gi,'-');
    return `<section class="collapsible-section ${esc(className)}" aria-label="${esc(ariaLabel)}"><div class="section-head"><h2><button class="section-toggle" data-browse-bucket="${esc(id)}" aria-expanded="${open}" aria-controls="${esc(panel)}"><span aria-hidden="true">${open?'▾':'▸'}</span> ${esc(title)}</button></h2>${count===undefined?'':`<span class="muted">${count} ${esc(unit)}</span>`}</div><div class="section-body" id="${esc(panel)}" ${open?'':'hidden'}>${open?body():''}</div></section>`;
  }
  function browseDisclosure(id,title,body,count,defaultOpen=false){
    const open=defaultOpen?!collapsedBrowseBuckets.has(id):expandedCollections.has(id),panel='browse-'+id.replace(/[^a-z0-9_-]/gi,'-');
    return `<section class="browse-bucket"><button class="browse-bucket-toggle" ${defaultOpen?'data-browse-bucket':'data-collection-toggle'}="${esc(id)}" aria-expanded="${open}" aria-controls="${esc(panel)}"><span>${open?'▾':'▸'} ${esc(title)}</span><small>${count} collections</small></button><div id="${panel}" ${open?'':'hidden'}>${open?body():''}</div></section>`;
  }
  function orderedStoryAssets(ids){return [...ids].sort((left,right)=>{
    const order=id=>{const a=byID.get(id);return Number(a?.storyboardOrder)||Number(/SB[- ]?(\d+)/i.exec(a?.sceneID||a?.title||'')?.[1])||9999;};
    return order(left)-order(right);
  });}
  const isFalconAsset=a=>/^HON-FALCON-/i.test(a?.sourceIntake||'');
  const isFalconAlbum=al=>al.project==='hon'&&al.assetIDs.some(id=>isFalconAsset(byID.get(id)));
  function falconReferenceGroups(media=projectAssets(),albumID=''){
    const album=albumID?C.albums.find(al=>al.id===albumID):null,scope=album?new Set(album.assetIDs):null;
    const assets=media.filter(a=>a.project==='hon'&&isFalconAsset(a)&&(!scope||scope.has(a.id))&&(!state.storyStage||state.storyStage==='all'||storyboardStage(a)===state.storyStage));
    const categories=[...new Set(assets.map(a=>a.providerCategory))].sort();
    const definitions=categories.map(category=>{
      const items=assets.filter(a=>a.providerCategory===category).sort((a,b)=>clipTitleOrder.compare(a.filename,b.filename)),assetIDs=items.map(a=>a.id),code=category.split('-')[0];
      return {id:'hon:falcon-reference-'+code.toLowerCase(),project:'hon',title:items[0]?.title.replace(/^C\d+-\d+\s*[\u00b7-]\s*/,'')||category,role:code+' candidate batch',assetIDs,coverID:assetIDs[0],unit:'drafts',description:'Claude-directed scene/category concepts; Grok/swarm preliminary image exploration. '+code+' identifies a category; the final number identifies a candidate. These are untimed source drafts, with independent review decisions.',sections:[{title:'Candidates in file order',assetIDs}]};
    });
    const children=collectionGroups(definitions,assets);if(!children.length)return [];
    const assetIDs=[...new Set(children.flatMap(g=>g.items.map(a=>a.id)))];
    return collectionGroups([{id:albumID||'hon:falcon-reference-exploration',project:'hon',title:album?.title||'Falcon reference exploration',role:assetIDs.length+' drafts / '+children.length+' category batches',assetIDs,coverID:assetIDs[0],unit:'batches',description:'Claude directed the scene/category concepts; Grok and its swarm generated these preliminary image explorations. These are not individual final shots authored by Claude. Category and candidate numbers are not narrative chapters, shot order or song timing. Earlier and later intakes retain their original IDs and reviews.'}],assets).map(g=>({...g,children}));
  }
  function falconReferenceSection(media=projectAssets(),albumID=''){
    const groups=falconReferenceGroups(media,albumID);return groups.length?`<section class="falcon-reference-collections"><h2>Falcon reference exploration</h2><p class="intro">Category batches, separate from the original story panels. The source-panel range does not filter these untimed candidates.</p>${collectionCards(groups)}</section>`:'';
  }
  function storyboardAlbumCollections(media=projectAssets()){
    const sequenceAlbums=new Set((C.storyboardSequences||[]).flatMap(s=>s.sourceAlbumIDs||[])),covers=browseLayout().storyCovers||{};
    const definitions=C.albums.filter(al=>al.project===state.project&&al.category==='storyboard'&&!sequenceAlbums.has(al.id)&&!isFalconAlbum(al)).map(al=>{
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
  function videoPurposeExplorer(media){
    const albums=C.albums.filter(al=>al.project===state.project&&al.category==='videos'),experimentIDs=new Set(browseLayout().comfyAlbumIDs||[]);
    const exploratory=al=>experimentIDs.has(al.id)||/turnaround|flow-edit-experiments/i.test(al.id);
    let html='<p class="intro">Scene attempts and exploratory tests stay separate. Every clip retains its recorded design stage and review; grouping is not production acceptance.</p>';
    for(const [title,match] of [['Scene and performance attempts',al=>!exploratory(al)],['Exploratory tests and turnarounds',exploratory]]){
      const definitions=albums.filter(match).map(al=>{const clips=sortClips(media.filter(a=>isClip(a)&&al.assetIDs.includes(a.id))),assetIDs=clips.map(a=>a.id),role=Object.entries(storyboardStages).map(([stage,label])=>{const count=clips.filter(a=>storyboardStage(a)===stage).length;return count?label+' '+count:'';}).filter(Boolean).join(' / ');return {...al,assetIDs,role,coverID:browseLayout().videoCovers?.[al.id]||assetIDs[0],unit:'clips',sections:[{title:'Clips - each retains its own stage',assetIDs}]};}),groups=collectionGroups(definitions,media);
      if(groups.length)html+=collapsibleSection('video-purpose:'+title,title,()=>`${collectionCards(groups)}`,{className:'video-purpose-section',count:groups.length});
    }
    return html;
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
    media=media.filter(a=>!isArchived(a));
    const config=browseLayout(),albumIDs=new Set(config.archiveAlbumIDs||[]),groups=collectionGroups(C.albums.filter(al=>al.project===state.project&&(al.category==='review'||albumIDs.has(al.id))).map(al=>({...al,textOnly:true,includeArchived:true,includeRemoved:true})),media);
    groups.push(...collectionGroups((C.detailDisplayGroups||[]).filter(g=>g.bucket==='guides').map(g=>({...g,textOnly:true,includeArchived:true,includeRemoved:true})),media));
    const claimed=new Set(groups.flatMap(g=>g.items.map(a=>a.id))),other=media.filter(a=>!isDoc(a)&&!claimed.has(a.id)&&(isArchived(a)||reviewRecord(a.id).status==='remove'||/reject/i.test(a.filename||'')));
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
  function allPurposeControls(){
    const choices=[['all','All'],['outfits','Outfits'],['details','Details'],['cast','Supporting cast'],['storyboard','Storyboards'],['videos','Videos'],['comfy','Comfy'],['inspiration','Inspiration'],['history','History'],['documents','Documents']];
    if(!choices.some(([id])=>id===state.allPurpose))state.allPurpose='all';
    return `<div class="tools purpose-filters" role="group" aria-label="Filter All files by purpose">${choices.map(([id,label])=>`<button class="pill ${state.allPurpose===id?'active':''}" data-all-purpose="${id}" aria-pressed="${state.allPurpose===id}">${label}</button>`).join('')}</div>`;
  }
  function compactAllFiles(media=projectAssets()){
    const config=browseLayout(),covered=new Set(),claim=ids=>ids.forEach(id=>covered.add(id)),show=purpose=>state.allPurpose==='all'||state.allPurpose===purpose;
    const archiveAlbums=new Set(config.archiveAlbumIDs||[]);
    const setupIDs=castSetupIDs();
    const current=media.filter(a=>!setupIDs.has(a.id)&&!isDoc(a)&&normalVisible(a)&&!/reject/i.test(a.filename||'')&&!archiveAlbums.has(a.album));
    const subjectMedia=media.filter(a=>!setupIDs.has(a.id)&&!isDoc(a)&&normalVisible(a)&&!/reject/i.test(a.filename||''));
    let html=allPurposeControls();
    claim(workingBOMEntries().map(e=>e.asset.id));claim(current.filter(a=>a.category==='working').map(a=>a.id));
    if(show('outfits'))html+=outfitExplorer(current.filter(queryMatch),false);claim(current.filter(a=>a.category==='outfits').map(a=>a.id));
    if(show('details'))html+=sharedCharacterReferences()+accessoryExplorer()+tattooCollections(subjectMedia);
    for(const g of [...(C.sharedReferenceCollections||[]),...(C.accessoryCollections||[])].filter(g=>g.project===state.project))claim(g.assetIDs||[]);
    for(const al of sharedCharacterAlbums())claim(al.assetIDs);
    for(const g of (C.detailDisplayGroups||[]).filter(g=>g.project===state.project))claim(g.assetIDs||[]);
    const detailAlbums=C.albums.filter(al=>al.project===state.project&&al.category==='details'&&!grillSourceAlbumIDs().has(al.id)).map(al=>({...al,assetIDs:al.assetIDs.filter(id=>!covered.has(id)&&byID.get(id)?.category==='details')}));
    const detailGroups=[...grillDesignGroups(),...collectionGroups(detailAlbums,current)];if(show('details')&&detailGroups.length)html+=collapsibleSection('other-details','Other character details',()=>`${collectionCards(detailGroups)}`,{count:detailGroups.length});claim(detailGroups.flatMap(g=>g.items.map(a=>a.id)));
    if(show('cast'))html+=castExplorer();claim(subjectMedia.filter(a=>a.category==='cast').map(a=>a.id));claim(creatureBossIdeasGroup()?.items.map(a=>a.id)||[]);for(const g of (C.castCollections||[]).filter(g=>g.project===state.project))claim(g.assetIDs||[]);
    const story=storyboardAlbumCollections(subjectMedia),sequences=storySequenceGroups(subjectMedia),falcon=state.project==='hon'?falconReferenceGroups(subjectMedia):[];
    if(show('storyboard')&&(story.length||sequences.length||falcon.length))html+=collapsibleSection('storyboard',state.project==='hon'?'Original storyboard':'Storyboard',()=>`<p class="intro">Source panels stay in their own collections and order.</p>${collectionCards(story)}${falcon.length?falconReferenceSection(subjectMedia):''}${sequences.length?`<h3>Separate scene drafts</h3>${collectionCards(sequences)}`:''}`,{className:'storyboard-collections',count:story.length+sequences.length+falcon.length});
    claim([...story,...sequences,...falcon].flatMap(g=>g.items.map(a=>a.id)));
    const videos=videoAlbumCollections(subjectMedia);if(show('videos')&&videos.length)html+=collapsibleSection('videos','Videos',()=>`${collectionCards(videos)}`,{count:videos.length});claim(videos.flatMap(g=>g.items.map(a=>a.id)));
    const comfy=comfyCollections(subjectMedia);if(show('comfy')&&comfy.length)html+=collapsibleSection('comfy','Comfy',()=>`${collectionCards(comfy)}`,{className:'comfy-collections',count:comfy.length});claim(comfy.flatMap(g=>g.items.map(a=>a.id)));
    const otherGroups=collectionGroups(C.albums.filter(al=>al.project===state.project&&al.category!=='review'&&!archiveAlbums.has(al.id)).map(al=>({...al,assetIDs:al.assetIDs.filter(id=>!covered.has(id))})),current);
    if(show('inspiration')&&otherGroups.length)html+=collapsibleSection('inspiration','More references & inspiration',()=>`${collectionCards(otherGroups)}`,{count:otherGroups.length});
    if(show('history'))html+=processArchive();
    return `<div class="all-files-workspace" data-purpose="${esc(state.allPurpose)}">${html}</div>`;
  }
  const honOutfitCategories=[
    {id:'formal',title:'Formal attire',albums:['yellow','cream','fur','velvet','casino','pinstripe']},
    {id:'casual',title:'Casual',albums:['rain','baroque','letterman','bomber','dragon','parka','puffer','velour']},
    {id:'scoundrel',title:'Scoundrel gear',albums:['armor','vest','cash','coat','ice','vinyl','pilot','saloon']}
  ];
  const outfitCategorySearches=new Map();
  const outfitCategoryKey=id=>[state.project,state.view,state.album||'root','outfit-category:'+id].join(':');
  function outfitCategoryGroups(outfits){
    const categoryByAlbum=new Map(honOutfitCategories.flatMap(category=>category.albums.map(name=>['hon:outfit-'+name,category.id])));
    return honOutfitCategories.map(category=>({...category,outfits:outfits.filter(({al})=>(categoryByAlbum.get(al.id)||'casual')===category.id)}));
  }
  function selectOutfitCategory(id){
    if(state.project!=='hon'||state.view!=='outfits'||state.album||!honOutfitCategories.some(category=>category.id===id))return;
    for(const category of honOutfitCategories){const key=outfitCategoryKey(category.id);category.id===id?collapsedBrowseBuckets.delete(key):collapsedBrowseBuckets.add(key);}
    renderMain();document.querySelector('#outfit-category-tag-'+id)?.focus({preventScroll:true});
  }
  function outfitCollectionViews(outfits){
    if(state.outfitLayout==='all')return outfits.map(({al,items})=>mediaGroup(al.title,al.description,items,al.id)).join('');
    return `<div class="gallery outfit-catalog">${outfits.map(({al,items})=>{
      const cover=outfitCover(items),expanded=expandedOutfits.has(al.id),panel='outfit-views-'+al.id.replace(/[^a-z0-9_-]/gi,'-'),status=reviewRecord(cover.id).status;
      const portrait=/portrait|head.?shot|chest.?up|bust/i.test([cover.title,cover.filename,cover.viewRole,cover.referenceRole].join(' '));
      return `<article class="outfit-collection ${expanded?'is-expanded':''}" data-outfit-collection="${esc(al.id)}"><div class="outfit-summary"><div class="media-card outfit-cover" data-review-card="${esc(cover.id)}">${status?`<span class="review-chip ${status}">${esc(statusLabels[status])}</span>`:''}<button class="media-open" data-album="${esc(al.id)}" aria-label="Open ${esc(al.title)} views"><div class="media-thumb"><img loading="lazy" src="${esc(href(cover.thumb))}" alt="${esc(al.title)} · ${portrait?'portrait':'available view'}"></div><div class="media-copy"><b>${esc(al.title)}</b><small>${items.length} ${state.search?'matching ':''}views · Open outfit</small>${portrait?'':'<small class="outfit-cover-fallback">Available view · portrait not supplied</small>'}</div></button></div><button class="outfit-expand" data-outfit-toggle="${esc(al.id)}" aria-expanded="${expanded}" aria-controls="${esc(panel)}">${expanded?'▾ Hide views':'▸ Show views here'} <span>${items.length}</span></button></div><div id="${esc(panel)}" class="outfit-inline-views" ${expanded?'':'hidden'}>${expanded?`<p class="muted">${esc(al.title)} · ${state.search?'matching ':''}views and variants</p><div class="gallery">${items.map(card).join('')}</div>`:''}</div></article>`;
    }).join('')}</div>`;
  }
  function outfitExplorer(media,includeShared=false){
    const outfits=outfitGroups(media),categorized=state.project==='hon'&&state.view==='outfits'&&!state.album;
    return collapsibleSection('outfits','Outfits',()=>{
      let html=`<p class="intro">One portrait per outfit. Open a card for its views, or expand it here. Gun and no-gun versions stay together.</p>`;
      if(categorized){
        const search=state.search.trim().toLowerCase(),context=state.project+':'+state.view;
        if(outfitCategorySearches.get(context)!==search){for(const category of honOutfitCategories)collapsedBrowseBuckets.delete(outfitCategoryKey(category.id));outfitCategorySearches.set(context,search);}
        const groups=outfitCategoryGroups(outfits);
        html+=`<div class="tools outfit-category-controls" role="group" aria-label="Outfit categories">${groups.map(group=>{const key=outfitCategoryKey(group.id),open=!collapsedBrowseBuckets.has(key),panel='section-'+key.replace(/[^a-z0-9_-]/gi,'-');return `<button id="outfit-category-tag-${group.id}" class="pill ${open&&group.outfits.length?'active':''}" data-outfit-category="${group.id}" aria-expanded="${open&&!!group.outfits.length}" ${group.outfits.length?`aria-controls="${panel}"`:'disabled'}>${group.title} · ${group.outfits.length}</button>`;}).join('')}</div>`;
      }
      html+=`<div class="tools outfit-layout-controls" role="group" aria-label="Outfit view">${[['compact','One per outfit'],['all','Show all views']].map(([value,label])=>`<button class="pill ${state.outfitLayout===value?'active':''}" data-outfit-layout="${value}" aria-pressed="${state.outfitLayout===value}">${label}</button>`).join('')}</div>`;
      if(categorized)html+=outfitCategoryGroups(outfits).filter(group=>group.outfits.length).map(group=>collapsibleSection('outfit-category:'+group.id,group.title,()=>outfitCollectionViews(group.outfits),{className:'story-section outfit-category-bucket',count:group.outfits.length,unit:'outfits'})).join('');
      else html+=outfitCollectionViews(outfits);
      return html+(outfits.length?'':'<p class="empty">No outfits match this search.</p>');
    },{className:'outfit-explorer',count:outfits.length})+(includeShared?sharedCharacterReferences()+accessoryExplorer():'');
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
    return collapsibleSection('documents','Documents & notes',()=>`<p class="intro">Open a subject, then a collection. Search reveals matching files inside their groups.</p><div class="doc-list">${[...parents].sort((a,b)=>order.indexOf(a[0])-order.indexOf(b[0])).map(([parent,children])=>`<details class="doc-group doc-parent" ${searching?'open':''}><summary>${esc(parent)} <span class="muted">${[...children.values()].reduce((n,files)=>n+files.length,0)} files</span></summary><div>${[...children].map(([child,files])=>`<details class="doc-group doc-child" ${searching?'open':''}><summary>${esc(child)} <span class="muted">${files.length}</span></summary><div>${files.map(a=>`<button class="doc-row" data-open="${esc(a.id)}"><b>${esc(a.title)}</b><small>${esc(a.inert?'Helper script · text preview only':a.filename)}</small></button>`).join('')}</div></details>`).join('')}</div></details>`).join('')}</div>`,{className:'documents-section',count:items.length,unit:'files'});
  }
  function honTattooDefinitions(){
    const groups=(C.detailDisplayGroups||[]).filter(g=>g.project==='hon'),artwork=groups.filter(g=>g.bucket==='stencils'),skin=groups.filter(g=>g.bucket==='skin');
    const objects=(C.detailProfiles||[]).filter(p=>p.project==='hon').flatMap(p=>p.objects||[]);
    const keys=['ship','eye','know','blaster','leigh','scoundrel','optional-motifs'];
    const profiles={ship:['hon-chest-current','hon-ship-perspective','hon-ship-schematic'],eye:['hon-eye'],know:['hon-know'],blaster:['hon-neck-blaster'],leigh:['hon-hand-card'],scoundrel:['hon-forearm-scoundrel'],'optional-motifs':['hon-bird-optional']};
    const dedicatedAlbums={ship:['hon:ship-tattoo'],leigh:['hon:leigh-hand-options']};
    const relatedProofs={eye:['HD-RETURN-3fa3290e85db','HD-TATGUIDE-b6eb3258a6ae'],know:['HD-RETURN-3fa3290e85db','HD-TATGUIDE-b6eb3258a6ae'],scoundrel:['HD-TATGUIDE-1fd07b088244','HD-TATGUIDE-b6eb3258a6ae'],leigh:['HD-RETURN-831f6171619f','HD-RETURN-b8c9247bfe47'],'optional-motifs':['HD-TATGUIDE-1fd07b088244']};
    const generalGuideIDs=new Set(groups.filter(g=>g.bucket==='guides'&&!g.tattooKey).flatMap(g=>g.assetIDs||[]));
    const allPlacementGuides=[...(C.tattooPlacementGuides||[]),...groups.filter(g=>g.bucket==='guides'&&g.tattooKey)];
    const ordered=keys.map(key=>artwork.find(g=>g.id==='hon:detail-'+key+'-art')).filter(Boolean);
    ordered.push(...artwork.filter(g=>!ordered.includes(g)));
    return ordered.map(art=>{
      const key=art.id.replace(/^hon:detail-/,'').replace(/-art$/,''),body=skin.find(g=>g.id==='hon:detail-'+key+'-skin'),profileObjects=objects.filter(o=>(profiles[key]||[]).includes(o.id)||o.id===art.sourceObjectID);
      const guideRecords=allPlacementGuides.filter(g=>g.project==='hon'&&g.tattooKey===key),seen=new Set();
      // De-duplicate exact bytes within this subject only; originals and their reviews are untouched.
      const unique=ids=>[...new Set(ids)].filter(id=>{const a=byID.get(id);if(!a||isDoc(a)||a.project!=='hon'||!normalVisible(a))return false;const hash=a.sha256||id;if(seen.has(hash))return false;seen.add(hash);return true;});
      // Claim maps and the placement-only legacy proof before body/example lists so each appears once.
      const guideIDs=unique(guideRecords.flatMap(g=>g.assetIDs||[]));
      const legacyProofIDs=unique(['ship','eye','know','blaster','scoundrel','optional-motifs'].includes(key)?['HD-TATGUIDE-b6eb3258a6ae']:[]);
      const comparisonIDs=new Set((art.sections||[]).filter(section=>section.history).flatMap(section=>section.assetIDs||[]));
      const stencils=unique([...(art.assetIDs||[]).filter(id=>!comparisonIDs.has(id)),...profileObjects.flatMap(o=>[...(o.artworkAssetIDs||[]),...(o.stencilAssetIDs||[])])]);
      const comparisons=unique([...(art.assetIDs||[]).filter(id=>comparisonIDs.has(id)),...(relatedProofs[key]||[])]);
      const legacyBody=(dedicatedAlbums[key]||[]).flatMap(id=>C.albums.find(a=>a.id===id)?.assetIDs||[]);
      const bodyIDs=unique([...(body?.assetIDs||[]),...(art.relatedAssetIDs||[]).filter(id=>!generalGuideIDs.has(id)),...profileObjects.flatMap(o=>o.exampleAssetIDs||[]),...legacyBody]);
      const artworkID=[art.coverAssetID,art.coverID,...stencils].find(id=>stencils.includes(id)),assetIDs=[...stencils,...guideIDs,...legacyProofIDs,...bodyIDs,...comparisons];
      const sourceAlbumIDs=[...new Set([...(art.sourceAlbumIDs||[]),...(body?.sourceAlbumIDs||[]),art.albumID,body?.albumID,...(dedicatedAlbums[key]||[]),...(relatedProofs[key]||[]).map(id=>byID.get(id)?.album),...guideRecords.flatMap(g=>[...(g.sourceAlbumIDs||[]),g.albumID,...(g.assetIDs||[]).map(id=>byID.get(id)?.album)])].filter(Boolean))];
      const guideDescription=guideRecords.map(g=>g.description||g.status||'').filter(Boolean).join(' ');
      return {id:'hon:tattoo-'+key,project:'hon',tattooKey:key,deferProvenance:true,title:key==='ship'?'Ship tattoo':key==='eye'?'Eye lettering':key==='know'?'Know lettering':key==='blaster'?'Neck blaster':key==='leigh'?'Princess Leigh':key==='scoundrel'?'Scoundrel':key==='optional-motifs'?'Optional motifs':art.title,role:art.role||'Artwork, body appearances and placement',assetIDs,coverID:art.coverAssetID||art.coverID||stencils[0]||bodyIDs[0],unit:'references',sourceAlbumIDs,aliases:[art.title,body?.title,...sourceAlbumIDs],description:'Each section keeps its own reference role. Artwork options, body examples and placement aids are not interchangeable, and grouping grants no approval.',notes:[...(art.notes||[]),...(body?.notes||[])],sections:[
        {title:'Artwork / stencil',assetIDs:artworkID?[artworkID]:[],overview:true,description:art.description||'Artwork reference; see the image review for its recorded scope.',emptyMessage:'No separate artwork reference is available for this tattoo.'},
        {title:'Placement and mannequin guide',assetIDs:guideIDs,overview:true,description:guideDescription,emptyMessage:'Pending: no dedicated placement/mannequin guide is filed for this tattoo. Earlier mixed proofs remain source evidence.'},
        ...(legacyProofIDs.length?[{title:'Legacy placement proof · revision needed',assetIDs:legacyProofIDs,overview:true,description:'Placement-only proof with recorded defects. Revision needed; not accepted as character identity, teeth, complete look or an exact tattoo transfer.'}]:[]),
        {title:'More stencil and artwork options',assetIDs:stencils.filter(id=>id!==artworkID),description:'Additional artwork formats and variants; each keeps its recorded review.'},
        {title:'Body appearances',assetIDs:bodyIDs,description:body?.description||profileObjects.map(o=>o.location).filter(Boolean).join('; ')||'Appearance evidence only; an exact transfer and anatomical placement are not established.',emptyMessage:'No distinct body appearance is available for this motif.'},
        {title:'Source sheets and artwork comparison evidence',assetIDs:comparisons,description:'Earlier sheets and comparison images retain their recorded defects. A mixed sheet is not a standalone stencil or an approved placement. Dice shown in Scoundrel source context are an optional design, not the forearm lettering.'}
      ]};
    }).filter(g=>g.assetIDs.length);
  }
  function grillSourceAlbumIDs(){
    return new Set(C.albums.filter(al=>al.project===state.project&&al.category==='details'&&(state.project==='hon'?['hon:grillz','hon:mouth-detail-updates'].includes(al.id):state.project==='lisan'&&/mouth|grill/i.test(al.id))).map(al=>al.id));
  }
  const comfyMouthAlbum=al=>/mouth|head|viseme|breather/i.test(al.id+' '+al.title);
  function comfyWorkspaceConfig(){return browseLayout().comfyWorkspace||{};}
  function comfyWorkspaceIDs(){
    const c=comfyWorkspaceConfig(),targets=new Set(c.targetAlbumIDs||[]);
    return [...new Set([...(c.outputAssetIDs||[]),...(c.inputAssetIDs||[]),...(c.finishingAssetIDs||[]),...C.albums.filter(al=>al.project===state.project&&targets.has(al.id)).flatMap(al=>al.assetIDs)])].filter(id=>{const a=byID.get(id);return a&&a.project===state.project&&!isDoc(a)&&normalVisible(a);});
  }
  function comfyWorkflowRecipes(){
    const query=state.search.toLowerCase().trim();
    const families=(comfyWorkspaceConfig().workflowFamilies||[]).map(f=>({...f,workflows:(f.workflowIDs||[]).map(id=>(C.productionWorkflows||[]).find(w=>w.id===id&&[state.project,'shared'].includes(w.project))).filter(Boolean)})).filter(f=>!query||JSON.stringify(f).toLowerCase().includes(query)||[...(f.links||[]).map(l=>l.assetID),...f.workflows.flatMap(w=>[...(w.sourceAssetIDs||[]),...(w.outputAssetIDs||[]),...(w.documentAssetIDs||[])])].some(id=>byID.has(id)&&queryMatch(byID.get(id))));
    if(!families.length)return '';
    const links=rows=>rows.filter(r=>{const a=byID.get(r.assetID);return a&&a.project===state.project&&normalVisible(a);}).map(r=>`<button class="pill" data-open="${esc(r.assetID)}">${esc(r.label||byID.get(r.assetID).title)}</button>`).join('');
    const records=w=>`<section class="workflow-record"><h4>${esc(w.title)}</h4><p class="workflow-status">${esc(w.status)}</p><p>${esc(w.summary)}</p>${[['Parent inputs',w.sourceAssetIDs],['Results & technical guides',w.outputAssetIDs],['Saved records & graphs',w.documentAssetIDs]].map(([label,ids])=>{const buttons=links((ids||[]).map(assetID=>({assetID})));return buttons?`<p class="muted">${label}</p><div class="tools">${buttons}</div>`:'';}).join('')}</section>`;
    return `<section class="comfy-recipes"><h2>Workflow recipes</h2><p>Ingredients → operation → result. Open the records to see the exact inputs and each test’s status.</p><div class="workflow-family-grid">${families.map(f=>`<article class="workflow-family"><h3>${esc(f.title)}</h3><p class="workflow-status">${esc(f.status)}</p><div class="workflow-diagram" role="img" aria-label="${esc(f.inputLabel+' → '+f.operationLabel+' → '+f.outputLabel)}"><div class="workflow-node"><span aria-hidden="true">▧</span><small>Ingredients</small><strong>${esc(f.inputLabel)}</strong></div><span class="workflow-arrow" aria-hidden="true">→</span><div class="workflow-node workflow-operation"><span aria-hidden="true">⚙</span><small>Operation</small><strong>${esc(f.operationLabel)}</strong></div><span class="workflow-arrow" aria-hidden="true">→</span><div class="workflow-node"><span aria-hidden="true">▷</span><small>Result</small><strong>${esc(f.outputLabel)}</strong></div></div><p>${esc(f.description)}</p><details><summary>Ingredients and records</summary><div class="tools">${links(f.links||[])}</div>${f.workflows.map(records).join('')}</details></article>`).join('')}</div></section>`;
  }
  function comfyWorkspace(media){
    const config=comfyWorkspaceConfig(),visible=new Set(media.map(a=>a.id));
    const items=ids=>(ids||[]).map(id=>byID.get(id)).filter(a=>a&&a.project===state.project&&visible.has(a.id)&&normalVisible(a));
    const outputs=items(config.outputAssetIDs),inputs=items(config.inputAssetIDs),finishing=items(config.finishingAssetIDs);
    const targets=collectionGroups((config.targetAlbumIDs||[]).map(id=>C.albums.find(al=>al.id===id&&al.project===state.project)).filter(Boolean).map(al=>({...al,directSingle:true,unit:'targets',sections:[{title:'Likeness targets',assetIDs:al.assetIDs}]})),media);
    const gallery=rows=>`<div class="gallery">${rows.map(card).join('')}</div>`;
    const drawer=(title,description,rows)=>rows.length?`<details class="detail-drawer"><summary>${esc(title)} · ${rows.length}</summary><p>${esc(description)}</p>${gallery(rows)}</details>`:'';
    return `<div class="tools"><a class="pill" href="#${esc(state.project)}/working">Open Working references</a></div><section class="comfy-outputs"><h2>Comfy outputs</h2><p>Saved still and video results. These are candidates: the motion test awaits acceptance, and the relight tests failed character-detail preservation.</p>${outputs.length?gallery(outputs):`<p class="muted">${state.search.trim()?'No Comfy outputs match this search.':'No Comfy outputs saved for this project yet.'}</p>`}</section>`
      +(targets.length?`<section class="comfy-targets"><h2>Likeness targets</h2><p>Source likenesses for swap experiments. Open a single target directly, or expand a set.</p>${collectionCards(targets)}</section>`:'')
      +comfyWorkflowRecipes()
      +drawer('Source clips & control guides','Original footage and technical guides used by the saved experiments.',inputs)
      +drawer('Local finishing','Soundtrack replacement preview made locally. The related Comfy Cloud graph has not been executed.',finishing);
  }
  function grillDesignGroups(){
    if(!['hon','lisan'].includes(state.project)||state.album&&state.album!==state.project+':grill-designs'&&!(grillSourceAlbumIDs().has(state.album)&&(/grill/i.test(state.album)||state.album==='hon:mouth-detail-updates')))return [];
    const designs=state.project==='hon'?[{id:'HD-B-91ef00348229',label:'Natural grill · gold upper / silver lower'},{id:'HD-GRILLUP-40064d98db89',label:'Optional external iced grill'}]:[{id:'LAG-cb183973ed1fc70e',label:'Optional external iced grill · natural teeth are the default'}];
    const groups=collectionGroups([{id:state.project+':grill-designs',project:state.project,title:'Grills',coverID:designs[0].id,assetIDs:designs.map(d=>d.id),unit:'designs',description:'One clear reference per grill design. Mouth positions and articulation references are in Working references.',sections:designs.map(d=>({title:d.label,assetIDs:[d.id]}))}]);
    return groups.map(g=>({...g,coverPreviewOnly:true,representativeID:g.cover.id,representativeLabel:'View this grill reference',role:designs.find(d=>d.id===g.cover.id).label}));
  }
  function honTattooBody(group){
    const remaining=new Map(group.items.map(a=>[a.id,a]));
    const sectionHTML=section=>{
      const items=(section.assetIDs||[]).map(id=>remaining.get(id)).filter(Boolean);
      for(const a of items)remaining.delete(a.id);
      if(!items.length)return !(section.assetIDs||[]).length&&section.emptyMessage?`<section class="collection-section collection-pending"><h3>${esc(section.title)}</h3><p class="muted">${esc(section.emptyMessage)}</p></section>`:'';
      return `<section class="collection-section"><h3>${esc(section.title)}</h3><div class="gallery">${items.map(card).join('')}</div>${section.description?`<p>${esc(section.description)}</p>`:''}</section>`;
    };
    const overview=(group.sections||[]).filter(section=>section.overview).map(sectionHTML).join('');
    let body=overview?`<div class="tattoo-reference-overview">${overview}</div>`:'';
    body+=(group.sections||[]).filter(section=>!section.overview).map(sectionHTML).join('');
    if(remaining.size)body+=`<section class="collection-section"><h3>Related references</h3><div class="gallery">${[...remaining.values()].map(card).join('')}</div></section>`;
    return body;
  }
  function honTattooReferences(){
    const definitions=honTattooDefinitions(),matching=state.album?definitions.filter(g=>g.sourceAlbumIDs.includes(state.album)):definitions,groups=collectionGroups(matching),claimed=new Set(matching.flatMap(g=>g.assetIDs));
    let html=`<div class="tools detail-browse" role="group" aria-label="Artwork view">${[['all','All references'],['approved','Approved artwork'],['archive','Archive']].map(([id,label])=>`<button class="pill ${id==='all'?'active':''}" data-detail-layout="${id}" aria-pressed="${id==='all'}">${label}</button>`).join('')}</div><p class="intro">One collection per tattoo. Open it to compare artwork and placement guides side by side, with body appearances below. Each reference keeps its recorded scope and review; earlier alternatives are in Archive.</p>`;
    if(groups.length)html+=collapsibleSection('tattoo-subjects','Tattoos',()=>collectionCards(groups.map(g=>({...g,role:'',renderBody:()=>honTattooBody(g),notes:['Character: '+(g.role.includes('Supporting-cast')?'Supporting cast':'Hon Dolo'),...(g.notes||[])]}))),{className:'tattoo-subject-collections',count:groups.length});
    const setupIDs=castSetupIDs(),retainedDetails=new Set(['hon:grillz','hon:piercings','hon:mouth-detail-updates']),generalGuideIDs=new Set((C.detailDisplayGroups||[]).filter(g=>g.project==='hon'&&g.bucket==='guides'&&!g.tattooKey).flatMap(g=>g.assetIDs||[]));
    const otherAlbums=C.albums.filter(al=>al.project==='hon'&&al.category==='details'&&!hiddenBrowseCollections.has(al.id)&&(!state.album||al.id===state.album)).map(al=>({...al,assetIDs:al.assetIDs.filter(id=>!setupIDs.has(id)&&(retainedDetails.has(al.id)||!generalGuideIDs.has(id)&&!claimed.has(id)&&!definitions.some(g=>g.assetIDs.includes(id))))}));
    const others=[...grillDesignGroups(),...collectionGroups(otherAlbums.filter(al=>!['hon:grillz','hon:mouth-detail-updates'].includes(al.id)))];
    if(others.length)html+=collapsibleSection('other-character-details','Piercings, grills and props',()=>`${collectionCards(others)}`,{className:'other-detail-collections',count:others.length});
    if(!groups.length&&!others.length)html+='<p class="empty">No references match this subject or search.</p>';
    return html;
  }
  function detailExplorer(){
    const profiles=(C.detailProfiles||[]).filter(p=>p.project===state.project),query=state.search.toLowerCase().trim();
    if(!profiles.some(p=>p.id===state.detailProfile))state.detailProfile=profiles[0]?.id||'';
    let html=`<div class="tools detail-browse" role="group" aria-label="Artwork view">${[['all','All references'],['approved','Approved artwork'],['archive','Archive']].map(([value,label])=>`<button class="pill ${state.detailLayout===value?'active':''}" data-detail-layout="${value}" aria-pressed="${state.detailLayout===value}">${label}</button>`).join('')}</div>`;
    if(state.detailLayout==='all')return html;
    if(!profiles.length)return html+'<p class="notice">No artwork catalog is available for this character yet. All references remains available.</p>';
    if(profiles.length>1)html+=`<div class="tools detail-profile-tabs" aria-label="Character profile">${profiles.map(p=>`<button class="pill ${state.detailProfile===p.id?'active':''}" data-detail-profile="${esc(p.id)}">${esc(p.character||p.title)}</button>`).join('')}</div>`;
    const profile=profiles.find(p=>p.id===state.detailProfile),objects=(profile.objects||[]).filter(o=>!query||[o.title,o.kind,o.location,o.status,o.summary].join(' ').toLowerCase().includes(query)||[...(o.artworkAssetIDs||[]),...(o.exampleAssetIDs||[])].some(id=>byID.has(id)&&queryMatch(byID.get(id))));
    const artwork=o=>[...new Set(o.artworkAssetIDs||[])].map(id=>byID.get(id)).filter(a=>a&&a.kind==='image'&&normalVisible(a));
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
    const missing=objects.filter(o=>o.needsArtwork&&!o.optional&&!artwork(o).length),optional=objects.filter(o=>o.optional&&o.kind!=='grillz');
    if(missing.length)html+=`<details class="detail-drawer"><summary>Artwork still needed <span class="muted">${missing.length}</span></summary><p class="intro">These details have placement references, but their separate drawings have not been recovered.</p><div class="detail-missing-list">${missing.map(o=>`<article><h3>${esc(o.title)}</h3><p class="muted">${o.kind==='piercing'?'Standalone jewelry reference needed':'Stencil needed'}</p>${evidence(o)}</article>`).join('')}</div></details>`;
    if(optional.length)html+=`<details class="detail-drawer"><summary>Optional accessories <span class="muted">${optional.length}</span></summary><div class="detail-missing-list">${optional.map(o=>`<article><h3>${esc(o.title)}</h3><p>${esc(o.summary||'Use only when explicitly requested.')}</p>${artwork(o).length?workflowReferences('Accessory artwork',o.artworkAssetIDs):'<p class="muted">The available reference is an on-character example.</p>'}${evidence(o)}</article>`).join('')}</div></details>`;
    if(state.detailLayout==='approved')html+=collectionCards(grillDesignGroups());
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
    return `<details class="scene-readiness" ${r.updatedAt?'open':''}><summary>Scene grade: ${r.grade||'Ungraded'} · ${gate.productionEligible?'B target met':'Review ingredients'}</summary><p class="review-help">Grade this whole scene separately from the likeness of each reference. B or better is the production target; missing fingers, an unready boss or another critical defect must be resolved. A grade does not approve the generated result or change its design stage.</p><label>Whole scene grade<select data-scene-field="grade"><option value="" ${r.grade===null?'selected':''}>Ungraded</option>${['A','B','C','D','F'].map(g=>`<option value="${g}" ${r.grade===g?'selected':''}>${g}</option>`).join('')}</select></label><p data-scene-gate="${esc(key)}" role="status" class="scene-gate">${esc(gate.productionEligible?'Meets B-or-better scene target; final result acceptance is separate.':'Planning / repair: '+gate.reasons.join(' '))}</p><p class="scene-gate" data-validation-scene="${esc(key)}">${esc(validationTechnicalGate(r).technicalReady?'Declared technical checks pass; final video judgment remains separate.':'Technical validation: '+validationTechnicalGate(r).reasons.join(' '))}</p><h4>Shoot plan verification</h4><p class="review-help">Review direction and cinematography before a production handoff. Save who performed the review; this form does not contact another AI. <a class="small-link" href="${esc(href('../collaborators/work_briefs_20261010/SHOOT_PLAN_VERIFICATION.txt'))}" target="_blank" rel="noopener">Shoot plan review guide</a></p>${[['direction','Director: action, blocking, eyelines and performance'],['camera','Camera: framing, angle and movement'],['lighting','Lighting: sources, contrast and continuity']].map(([field,label])=>`<label>${label}<textarea data-shoot-field="${field}" rows="3" maxlength="12000">${esc(r.shootPlan[field])}</textarea></label>`).join('')}<label>Reviewed by<input type="text" data-shoot-field="reviewedBy" maxlength="300" value="${esc(r.shootPlan.reviewedBy)}" placeholder="Name of the person or AI that actually reviewed it"></label><label>Shoot plan review<select data-shoot-field="reviewStatus">${[['unreviewed','Unreviewed'],['needs_fixes','Needs fixes'],['verified','Verified']].map(([v,l])=>`<option value="${v}" ${r.shootPlan.reviewStatus===v?'selected':''}>${l}</option>`).join('')}</select></label><label>Review findings<textarea data-shoot-field="note" rows="2" maxlength="6000">${esc(r.shootPlan.note)}</textarea></label><p class="review-help" data-shoot-review-time>${esc(r.shootPlan.reviewedAt?'Review recorded: '+r.shootPlan.reviewedAt:'No shoot plan verification recorded.')}</p><h4>Scene ingredients</h4><p class="review-help">Mark what this scene requires and review each part. Available files begin unreviewed. Add missing characters, props or checks by name.</p><div class="scene-ingredients">${r.ingredients.map(i=>`<div class="scene-ingredient" data-ingredient="${esc(i.id)}"><b>${esc(i.label)}</b><small>${esc(String(i.role).replace(/_/g,' '))}</small><label><input type="checkbox" data-ingredient-field="required" ${i.required?'checked':''}> Required in this scene</label><label>Ready for this scene<select data-ingredient-field="status">${[['unreviewed','Unreviewed'],['ready','Ready'],['needs_fixes','Needs fixes'],['missing','Missing']].map(([v,l])=>`<option value="${v}" ${i.status===v?'selected':''}>${l}</option>`).join('')}</select></label>${i.kind==='reference'?`<label>Exact reference<select data-ingredient-field="assetID"><option value="">Missing / no reference</option>${[...pool,...(byID.has(i.assetID)&&!pool.some(a=>a.id===i.assetID)?[byID.get(i.assetID)]:[])].map(a=>`<option value="${esc(a.id)}" ${i.assetID===a.id?'selected':''}>${esc(a.title)}</option>`).join('')}</select></label>`:'<p class="muted">Scene check · describe the evidence below.</p>'}<label>Evidence, differences or fix needed<textarea data-ingredient-field="note" rows="2" maxlength="6000">${esc(i.note)}</textarea></label></div>`).join('')}</div><div class="scene-add"><label>New ingredient or check<input type="text" data-new-ingredient maxlength="300" placeholder="Boss face, cigar, dartboard, complete hands…"></label><button class="pill" data-add-ingredient="reference">Add missing reference</button><button class="pill" data-add-ingredient="criterion">Add scene check</button></div><label>Critical blockers · one per line<textarea data-scene-field="criticalBlockers" rows="3" maxlength="12000" placeholder="Defects that must be resolved before this scene is production ready">${esc(r.criticalBlockers.join('\n'))}</textarea></label><label>Whole scene note<textarea data-scene-field="note" rows="3" maxlength="12000">${esc(r.note)}</textarea></label><p class="review-help">Draft and repair handoffs remain available while the scene is ungraded or blocked.</p><span hidden data-scene-project="${esc(shot.project)}" data-scene-id="${esc(shot.id)}"></span></details>`;
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
    const visible=new Set(cards.map(a=>a.id)),all=storyWorkItems().filter(s=>!s.independentSequenceID),mapped=all.filter(s=>(s.panelAssetIDs||[]).some(id=>visible.has(id))),unplaced=all.filter(s=>!(s.panelAssetIDs||[]).length);
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
  function writerDevelopment(project=state.project,allGroups=false){
    const record=(C.writerDevelopment?.projects||[]).find(p=>p.id===project);if(!record)return '';
    const matching=id=>{const a=byID.get(id);return normalVisible(a)&&queryMatch(a);};
    const groups=record.groups.filter(g=>allGroups||g.storyboard).map(g=>({...g,documentIDs:g.documentIDs.filter(matching)})).filter(g=>g.documentIDs.length);
    if(!groups.length)return '';
    const button=id=>{const a=byID.get(id);return '<button class="doc-row" data-open="'+esc(id)+'"><b>'+esc(a.title)+'</b><small>'+esc(a.author||'Writer document')+' · '+esc(a.filename)+'</small></button>';};
    return '<section class="writer-development" data-writer-project="'+esc(project)+'"><h2>'+esc(record.title)+'</h2><p class="intro">'+esc(record.description)+'</p><div class="tools">'+record.contextDocumentIDs.filter(id=>normalVisible(byID.get(id))).map(id=>'<button class="pill" data-open="'+esc(id)+'">'+esc(byID.get(id).title)+'</button>').join('')+'</div><div class="writer-featured">'+record.featuredDocumentIDs.filter(matching).map(button).join('')+'</div><div class="doc-list">'+groups.map(g=>'<details class="doc-group" '+(state.search.trim()?'open':'')+'><summary>'+esc(g.title)+' <span class="muted">'+g.documentIDs.length+' files</span></summary><div><p class="review-help">'+esc(g.description)+'</p>'+g.documentIDs.map(button).join('')+'</div></details>').join('')+'</div><p class="review-help"><a href="#'+esc(project)+'/documents">All '+esc(C.projects.find(p=>p.id===project)?.name||project)+' documents</a> · Writer plans and attributed assessments remain separate from the Grok visual groups and human reviews.</p></section>';
  }
  function writerConnections(a){
    const links=(C.writerDevelopment?.associations||[]).filter(link=>(isDoc(a)?link.documentID===a.id:link.assetID===a.id)&&normalVisible(byID.get(isDoc(a)?link.assetID:link.documentID)));
    if(!links.length)return '';
    return '<section class="story-connections writer-connections"><h3>'+ (isDoc(a)?'Related source references':'Related writer development')+'</h3><p class="review-help">Documented creative associations; source status, acceptance and song timing remain separate.</p>'+links.map(link=>{const id=isDoc(a)?link.assetID:link.documentID,target=byID.get(id);return '<button class="doc-row" data-open="'+esc(id)+'"><b>'+esc(isDoc(a)?link.label:target.title)+'</b><small>'+esc(link.evidence)+'</small></button>';}).join('')+'</section>';
  }
  function storyboardStories(project=state.project){
    const records=(C.storyboardStories||[]).filter(s=>s.project===project),songID=project==='lisan'?'lisan:meta-mirror':'hon:strictly-business';
    if(!records.some(s=>s.kind==='song')&&['hon','lisan'].includes(project))records.unshift({id:songID,project,title:project==='lisan'?'Meta Mirror':'Strictly Business',kind:'song',documentIDs:[],description:'Original song storyboard in source panel order.'});
    for(const sequence of (C.storyboardSequences||[]).filter(s=>s.project===project))if(!records.some(s=>s.sequenceID===sequence.id))records.push({id:sequence.id,project,title:sequence.title,kind:'sequence',sequenceID:sequence.id,coverID:sequence.coverID,documentIDs:[],description:sequence.description||''});
    return records;
  }
  function selectedStoryboardStory(){
    const stories=storyboardStories(),explicit=state.album.startsWith('structure:')?state.album.slice(10):state.album.startsWith('story:')?state.album.slice(6):'',legacy=(C.storyboardSequences||[]).find(s=>s.project===state.project&&(s.sourceAlbumIDs||[]).includes(state.album));
    return stories.find(s=>s.id===explicit)||stories.find(s=>legacy&&s.sequenceID===legacy.id)||stories.find(s=>s.kind==='song')||stories[0];
  }
  function storyURL(story){return '#'+[story.project,'storyboard','story:'+story.id].map(encodeURIComponent).join('/');}
  function songSourcePanels(project=state.project){
    const sequences=new Set((C.storyboardSequences||[]).filter(s=>s.project===project).flatMap(s=>s.sourceAlbumIDs||[])),ids=new Set(C.albums.filter(al=>al.project===project&&al.category==='storyboard'&&!sequences.has(al.id)&&!isFalconAlbum(al)).flatMap(al=>al.assetIDs));
    return C.assets.filter(a=>normalVisible(a)&&ids.has(a.id)&&typeof a.storyboardPosition==='number'&&Number.isFinite(a.storyboardPosition)).sort((a,b)=>(a.storyboardOrder??Infinity)-(b.storyboardOrder??Infinity));
  }
  function storySequenceCoverage(sequence){
    const shots=sequence.shots||[],available=(shot,roles)=>(shot.materials||[]).some(m=>roles.includes(m.role)&&normalVisible(byID.get(m.assetID)));
    return {shots:shots.length,scenes:(sequence.sections||[]).length,frames:shots.filter(s=>available(s,['setting_stand_in','source_frame'])).length,results:shots.filter(s=>available(s,['result_on_disk'])).length,pending:shots.filter(s=>s.pendingReferences?.length).length,characters:shots.filter(s=>(s.pendingReferences||[]).some(p=>pendingReferenceType(p,s)==='Character')).length,objects:shots.filter(s=>(s.pendingReferences||[]).some(p=>pendingReferenceType(p,s)==='Object / design')).length};
  }
  function pendingReferenceType(reference,shot={}){const kind=(shot.pendingReferenceDetails||[]).find(p=>p.label===reference)?.kind;return kind==='object_design'?'Object / design':kind==='character'?'Character':'Reference';}
  function storyLandingCards(stories,selected){
    const groups=new Map();for(const story of stories){const group=story.group||(story.kind==='prose'?'Series and seeds':'Stories');if(!groups.has(group))groups.set(group,[]);groups.get(group).push(story);}
    return `<section class="story-library" aria-label="Story library">${[...groups].map(([title,items])=>`<h2>${esc(title)}</h2><div class="story-landing-grid">${items.map(story=>{const sequence=(C.storyboardSequences||[]).find(s=>s.id===story.sequenceID&&s.project===story.project),panels=story.kind==='song'?songSourcePanels(story.project):[],cover=byID.get(story.coverID||sequence?.coverID)||panels[0],count=story.kind==='prose'?'No panels yet':sequence?.shots?`${sequence.shots.length} shots · ${(sequence.sections||[]).length} scenes`:sequence?`${(sequence.assetIDs||[]).filter(id=>normalVisible(byID.get(id))).length} source images`:`${panels.length} source panels`,documents=(story.documentIDs||[]).filter(id=>{const a=byID.get(id);return normalVisible(a)&&isDoc(a);}),coverage=sequence?.shots?storySequenceCoverage(sequence):null,stages=new Set(panels.map(storyboardStage)),stage=sequence?storyboardStages[sequence.stage]||'Preliminary':story.kind==='song'?(stages.size===1?storyboardStages[[...stages][0]]||'Preliminary':'Mixed stages'):'Writing development';return `<a class="story-landing-card${story.id===selected.id?' selected':''}" href="${esc(storyURL(story))}"${story.id===selected.id?' aria-current="page"':''} data-story-card="${esc(story.id)}">${cover&&normalVisible(cover)&&cover.thumb?`<img src="${esc(href(cover.thumb))}" alt="" loading="lazy">`:`<div class="story-prose-cover" aria-hidden="true">${story.kind==='prose'?'Writings':'Story'}</div>`}<div><p class="eyebrow">${esc(story.kind==='song'?'Song storyboard':story.kind==='sequence'?'Independent sequence':'Prose development')} · ${esc(stage)}</p><h3>${esc(story.title)}</h3><p>${esc(count)} · ${documents.length} writing${documents.length===1?'':'s'}</p>${coverage?`<p class="story-card-coverage">${coverage.frames} with frames · ${coverage.results} with results<br>${coverage.pending} with pending references · ${coverage.characters} need characters</p>`:''}${story.description?`<p class="story-card-description">${esc(story.description)}</p>`:''}</div></a>`;}).join('')}</div>`).join('')}</section>`;
  }
  function storyWritings(story){
    const documents=(story.documentIDs||[]).map(id=>byID.get(id)).filter(a=>a&&isDoc(a)&&queryMatch(a));
    if(!documents.length)return '';
    return `<section class="writer-development story-writings" data-story-writings="${esc(story.id)}"><h2>Writings · ${esc(story.title)}</h2><p class="review-help">Writer plans and source notes keep their attribution. They do not change image reviews or approve a shot.</p><div class="story-writing-grid">${documents.map(a=>`<button class="doc-row" data-open="${esc(a.id)}"><b>${esc(a.title)}</b><small>${esc(a.author||'Writer document')} · ${esc(a.filename)}</small></button>`).join('')}</div></section>`;
  }
  function storyStageControl(){return `<div class="story-stage"><label for="story-stage">Stage</label><select id="story-stage"><option value="all">All stages</option>${Object.entries(storyboardStages).map(([id,label])=>`<option value="${id}" ${state.storyStage===id?'selected':''}>${label}</option>`).join('')}</select></div>`;}
  const storyMaterialRoles={setting_stand_in:'Setting stand-in',source_frame:'Exact source frame',character_reference:'Character reference',storyboard_concept:'Storyboard concept',result_on_disk:'Result on disk'};
  function sequenceShotCard(shot,sequence){
    const materials=(shot.materials||[]).filter(m=>!isArchived(byID.get(m.assetID))),roles=new Map(),preview=materials.find(m=>['source_frame','setting_stand_in'].includes(m.role)&&normalVisible(byID.get(m.assetID)))||materials.find(m=>normalVisible(byID.get(m.assetID))),asset=byID.get(preview?.assetID);
    for(const material of materials){if(!roles.has(material.role))roles.set(material.role,[]);roles.get(material.role).push(material);}
    const pending=shot.pendingReferences||[],searchMatch=!state.search.trim()||queryMatch({title:[shot.shotID,shot.label,shot.line,...pending].join(' '),tags:[]})||materials.some(m=>byID.has(m.assetID)&&queryMatch(byID.get(m.assetID)));
    if(!searchMatch)return '';
    if(asset&&!displayed.includes(asset.id))displayed.push(asset.id);
    return `<article class="story-sequence-shot" id="story-shot-${esc(shot.shotID)}" data-story-shot-id="${esc(shot.shotID)}"><div class="story-shot-heading"><p class="eyebrow">${esc(shot.shotID)} · ${esc(storyboardStages[sequence.stage]||'Preliminary')}</p><h3>${esc(shot.label||shot.shotID)}</h3></div>${asset?.thumb?`<button class="story-shot-preview" data-open="${esc(asset.id)}" aria-label="Open ${esc(storyMaterialRoles[preview.role]||preview.role)} for ${esc(shot.shotID)}"><img src="${esc(href(asset.thumb))}" alt="${esc(asset.title)}" loading="lazy"><span>${esc(storyMaterialRoles[preview.role]||String(preview.role).replace(/_/g,' '))}</span></button>`:'<p class="story-shot-empty">No frame linked yet.</p>'}${shot.line?`<p class="story-shot-line">${esc(shot.line)}</p>`:''}${pending.length?`<div class="story-pending"><h4>Pending references</h4><ul>${pending.map(p=>`<li><span>${esc(pendingReferenceType(p,shot))}</span> ${esc(p)}</li>`).join('')}</ul></div>`:'<p class="review-help">No pending reference names recorded. Shot review and acceptance remain separate.</p>'}<details class="story-shot-materials"><summary>Source material · ${materials.length} linked file${materials.length===1?'':'s'}</summary>${[...roles].map(([role,items])=>`<section class="story-material-role"><h4>${esc(storyMaterialRoles[role]||String(role).replace(/_/g,' '))} · ${items.length}</h4>${role==='setting_stand_in'?'<p class="review-help">Place and lighting only. The figure is Lisan; this frame does not establish the story character or action.</p>':role==='result_on_disk'?'<p class="review-help">Received result · preliminary. Availability does not mean accepted.</p>':''}<ul class="story-materials">${items.map(m=>{const a=byID.get(m.assetID);if(a&&!displayed.includes(a.id))displayed.push(a.id);return `<li>${a?`<button class="small-link" data-open="${esc(a.id)}">${esc(a.title)}</button>${!normalVisible(a)?'<small>Retained source · outside ordinary browsing</small>':''}`:`<span>${esc(m.repoPath||m.assetID||'Unresolved source')}</span><small>Not available in this catalog</small>`}${m.note?`<p class="review-help">${esc(m.note)}</p>`:''}<details class="story-source-record"><summary>Source record</summary><p>${esc(m.repoPath||a?.repoPath||'')}</p>${m.sha256?`<p>SHA-256 ${esc(m.sha256)}</p>`:''}${Number.isFinite(m.bytes)?`<p>${m.bytes.toLocaleString()} bytes</p>`:''}</details></li>`;}).join('')}</ul></section>`).join('')}</details></article>`;
  }
  function sequenceStoryboard(story,media){
    const sequence=(C.storyboardSequences||[]).find(s=>s.id===story.sequenceID&&s.project===state.project);if(!sequence)return '<p class="empty">This sequence has no registered panels yet.</p>';
    let html=`<section class="story-controls">${storyStageControl()}<p class="review-help">Independent sequence · ${esc(storyboardStages[sequence.stage]||'Preliminary')}. Shot order is separate from song timing.</p></section>`;
    if(state.storyStage!=='all'&&state.storyStage!==sequence.stage)return html+'<p class="empty">No shots match this stage.</p>';
    if(!Array.isArray(sequence.shots)){const work=storyWorkItems().filter(s=>s.independentSequenceID===sequence.id);return html+`<section class="story-independent-sequences">${collectionCards(collectionGroups([sequence],media))}</section>`+(work.length?`<details class="detail-drawer"><summary>Shot planning & progress · ${work.length}</summary><div class="story-work-grid">${work.map(storyWorkCard).join('')}</div></details>`:'');}
    const coverage=storySequenceCoverage(sequence),shots=new Map(sequence.shots.map(s=>[s.shotID,s]));
    html+=`<section class="story-sequence" data-story-sequence="${esc(sequence.id)}"><p class="story-coverage">${coverage.shots} shots · ${coverage.scenes} scenes · ${coverage.frames} shots with a setting or source frame · ${coverage.results} with a result on disk</p><p class="story-coverage">${coverage.pending} shots have pending references: ${coverage.characters} need characters; ${coverage.objects} need object or design references. These groups can overlap.</p><p class="notice">Available material is not shot readiness. Setting stand-ins supply place and light; every LAG-1K figure is Lisan. Writer picks and source self-scores are preliminary observations, separate from your reviews. No shot is accepted by this map.</p>`;
    let count=0;for(const section of sequence.sections||[]){const cards=(section.shotIDs||[]).map(id=>shots.get(id)).filter(Boolean).map(shot=>sequenceShotCard(shot,sequence)).filter(Boolean);if(!cards.length)continue;count+=cards.length;html+=`<section class="story-scene" data-story-scene="${esc(section.scene)}"><h2>Scene ${esc(section.scene)} · ${esc(section.title)}</h2><div class="story-shot-grid">${cards.join('')}</div></section>`;}
    return html+(count?'':'<p class="empty">No shots or linked materials match this search.</p>')+'</section>';
  }
  const structureStates={missing:'Missing',draft:'Draft',present:'Present · unreviewed',verified:'Verified for stated scope',accepted:'Accepted for stated scope',unknown:'Not assessed',not_needed:'Intentionally not needed'};
  function structureDefinition(){return C.storyboardStructure||{fields:[],kitchenFields:[],stories:[]};}
  function storyStructure(story){
    const declared=(structureDefinition().stories||[]).find(s=>s.storyID===story.id);if(declared)return declared;
    const sequence=(C.storyboardSequences||[]).find(s=>s.id===story.sequenceID),work=storyWorkItems().filter(s=>s.independentSequenceID===story.sequenceID);
    const raw=sequence?.shots||work;
    if(!raw?.length)return {storyID:story.id,project:story.project,sections:[],shots:[]};
    const shots=raw.map(s=>{const materials=(s.materials||[]).map(m=>({...m,availability:byID.has(m.assetID)?'catalogued':'unresolved'})),source=sequence?.sourceDocuments?.[0]||{};
      const fields=structureDefinition().fields.map(f=>({key:f.key,text:f.key==='purpose'?(s.line||s.title||s.label||''):f.key==='references'?materials.map(m=>(storyMaterialRoles[m.role]||m.role)+': '+(byID.get(m.assetID)?.title||m.assetID)).join('\n'):'',status:f.key==='purpose'?'draft':f.key==='references'&&materials.length?'present':'unknown',evidence:[]}));
      return {shotID:s.shotID||s.id,title:s.label||s.title||s.shotID,fields,kitchen:[],materials,source,parent:source,stage:sequence?.stage||s.stage||'preliminary',revision:'Existing sequence record',unresolvedReferences:s.pendingReferences||[],revisions:[]};});
    return {storyID:story.id,project:story.project,shots,sections:sequence?.sections?.map((s,i)=>({...s,id:s.id||String(s.scene||i+1)}))||[{id:'sequence',title:'Planned shots',shotIDs:shots.map(s=>s.shotID)}]};
  }
  function structureEvidence(records=[]){
    return records.filter(Boolean).map(record=>{if(typeof record==='string')record={path:record};const asset=byID.get(record.assetID)||C.assets.find(a=>a.repoPath===record.path),label=(record.path||asset?.filename||'Source').split('/').pop();
      if(!asset)return `<span class="review-help">${esc(label)} · source link not catalogued</span>`;
      const mismatch=record.sha256&&record.sha256!==asset.sha256;
      return `<button class="small-link" data-open="${esc(asset.id)}">${esc(label)}${record.line?' · line '+record.line:''}</button>${mismatch?'<strong class="structure-alert">Source changed · review dependencies</strong>':''}`;
    }).join(' ');
  }
  function structureGaps(shot){
    const f=Object.fromEntries((shot.fields||[]).map(f=>[f.key,f])),open=key=>['missing','unknown'].includes(f[key]?.status||'unknown');
    return {no_art:!(shot.materials||[]).some(m=>byID.has(m.assetID)&&!isDoc(byID.get(m.assetID))),start_frame:open('start_frame'),camera:open('camera'),prompt:open('prompt_clip'),cue:open('cue'),kitchen:!shot.kitchenWritten,changed:!!shot.dependencyReviewNeeded||!!shot.revisions?.length};
  }
  function structureField(def,value,shot,demonstration=false){
    const v=value||{status:'unknown',text:'',evidence:[]},status=structureStates[v.status]||structureStates.unknown;
    const applicability={writing:'Writing',route:'Depends on route',dispatch:'At dispatch',return:'On return',review:'At review',conditional:'As the story requires'}[def.phase]||'Handoff preparation';
    return `<section class="structure-field" data-structure-field="${esc(def.key)}"><div class="structure-field-head"><h4>${esc(def.section||def.key)} · ${esc(def.label)}</h4><span class="structure-status status-${esc(v.status||'unknown')}">${demonstration?'Empty template':esc(status)}</span></div><p class="review-help">${esc(def.hint)}</p>${v.text?`<div class="structure-text">${esc(v.text)}</div>`:`<p class="muted">${demonstration?'No content entered.':v.status==='not_needed'?'Explicitly not needed.':'No field-specific content recorded in this source.'}</p>`}${v.note?`<p class="structure-note">${esc(v.note)}</p>`:''}<p class="structure-owner">${esc(applicability)}${def.owner?' · '+esc(def.owner):''}</p>${demonstration?'':`<div class="structure-evidence">${structureEvidence(v.evidence?.length?v.evidence:[shot?.source])}</div>`}</section>`;
  }
  function structureLegacy(shot){
    const ids=shot.sourceShotPlanIDs||[];if(!ids.length)return '';
    const plans=new Map(storyWorkItems().map(s=>[s.id,s]));
    return `<details class="structure-sources"><summary>Earlier shot-plan crosswalk · ${ids.map(esc).join(', ')}</summary><p class="review-help">These source IDs remain distinct from ${esc(shot.shotID)}. Existing results and acceptance do not transfer to this authored shot.</p>${ids.map(id=>{const plan=plans.get(id);return `<h4>${esc(id)}${plan?' · '+esc(plan.title):' · source mapping only'}</h4><div class="tools">${(plan?.materials||[]).filter(m=>byID.has(m.assetID)).map(m=>`<button class="pill" data-open="${esc(m.assetID)}">${esc(byID.get(m.assetID).title)}</button>`).join('')}</div>`;}).join('')}</details>`;
  }
  function structureFoundation(shot,story){
    const source=window.CFA_SOURCE_FOUNDATION;
    if(!source)return {state:'unresolved',label:'Source indicator unavailable',inputs:[],notes:['Refresh this page to load the current source indicator.']};
    return source.derive(C.storyboardSourceFoundation||{},shot,story.project,story.id, C.assets,Object.fromEntries(reviews),[...sceneReviews.values()]);
  }
  function structureFoundationDetail(f){
    return `<details class="structure-sources source-foundation"><summary>Source foundation · ${esc(f.label)}${f.dependencyReviewNeeded?' · dependencies need review':''}</summary><p class="review-help">This describes selected inputs only. Storyboard maturity, direction checks and actual-video acceptance remain separate.</p>${(f.notes||[]).map(n=>`<p class="structure-note">${esc(n)}</p>`).join('')}${f.bindingEvidence?`<p class="review-help">Selection evidence: ${esc(JSON.stringify(f.bindingEvidence))}</p>`:''}${(f.inputs||[]).map(i=>`<section class="foundation-input"><h4>${esc(String(i.role||'Input').replace(/_/g,' '))} · ${esc(byID.get(i.assetID)?.title||i.assetID||'Missing asset')}</h4><p>Recorded source stage: ${esc(storyboardStages[i.stage]||'Not recorded')} · scope: ${esc(i.scope||'Not recorded')} · ${esc(window.CFA_SOURCE_FOUNDATION.LABELS[i.state]||i.state)}</p><p class="review-help">${esc(i.stageSource)} · ${Number.isFinite(i.bytes)?i.bytes.toLocaleString()+' bytes':'Size not recorded'}</p><p class="foundation-hash">Selected SHA-256: ${esc(i.expectedSHA256||'Not recorded')}<br>Current SHA-256: ${esc(i.actualSHA256||'Not available')}</p>${i.notes.map(n=>`<p class="structure-note">${esc(n)}</p>`).join('')}${byID.has(i.assetID)?`<button class="small-link" data-open="${esc(i.assetID)}">Open selected input</button>`:''}</section>`).join('')}</details>`;
  }
  function structureShot(shot,section,foundation){
    const defs=structureDefinition(),values=new Map((shot.fields||[]).map(f=>[f.key,f])),gaps=structureGaps(shot),material=(shot.materials||[]).filter(m=>byID.has(m.assetID)),known=(shot.fields||[]).filter(f=>f.text&&f.status!=='missing').length;
    return `<details class="structure-shot" data-structure-shot="${esc(shot.shotID)}"><summary><span><b>${esc(shot.shotID)} · ${esc(shot.title)}</b><small>${esc(shot.revision||'Draft')} · ${known}/${defs.fields.length} fields with content · ${material.length} linked references${shot.kitchenWritten?' · kitchen block documented':''}</small></span><span class="structure-shot-tags"><span data-foundation="${esc(foundation.state)}">Source foundation · ${esc(foundation.label)}</span>${foundation.dependencyReviewNeeded?'<span>Input dependencies need review</span>':''}${gaps.no_art?'<span>No linked art</span>':''}${values.get('prompt_clip')?.status==='missing'?'<span>Clip prompt missing</span>':''}${gaps.changed?'<span>Revision needs review</span>':''}</span></summary><div class="structure-shot-body"><p class="notice">${esc(shot.authoringStatus||'Source planning record')} · Storyboard maturity: ${esc(storyboardStages[shot.stage]||shot.stage||'Preliminary')}. Written content is separate from reviewed direction, accepted references and executed work.</p>${structureFoundationDetail(foundation)}<div class="structure-context"><b>${esc(section.title)}</b><p>${esc(section.spineBeat||'')}</p>${structureEvidence([shot.source])}</div><details class="structure-sources"><summary>Linked references · ${material.length}</summary><div class="tools">${material.map(m=>`<button class="pill" data-open="${esc(m.assetID)}">${esc(byID.get(m.assetID).title)} · ${esc(storyMaterialRoles[m.role]||String(m.role).replace(/_/g,' '))}</button>`).join('')}</div><p class="review-help">References keep their own reviews and scope. A concept or named reference is not a prepared starting frame.</p>${shot.unresolvedReferences?.length?`<ul>${shot.unresolvedReferences.map(p=>`<li>${esc(p)}</li>`).join('')}</ul>`:''}${shot.missingArtReported?.length?`<p class="review-help">Writer-reported gaps as of ${esc(shot.coverageAsOf)}: ${esc(shot.missingArtReported.join('; '))}. Check the linked library material before commissioning anything.</p>`:''}</details>${structureLegacy(shot)}<div class="structure-fields">${defs.fields.map(d=>structureField(d,values.get(d.key),shot)).join('')}</div><details class="structure-kitchen"><summary>Kitchen / handoff structure · ${shot.kitchenWritten?'12 documented parts · includes gaps':'incomplete or not yet assessed'}</summary><p class="review-help">Modes, models and cost are bound when a route is chosen. This list does not request a run.</p><div class="structure-fields">${defs.kitchenFields.map(d=>structureField(d,(shot.kitchen||[]).find(f=>f.key===d.key),shot)).join('')}</div></details><details class="structure-history"><summary>Prior take, revisions & dependency evidence</summary>${structureEvidence([shot.parent,...(shot.priorDependencyEvidence||[])])}${(shot.revisions||[]).map(r=>`<h4>${esc(r.label)}</h4><p>${esc(r.note)}</p>${structureEvidence([r.source,r.parent])}`).join('')}<p class="review-help">Changes to direction, cue, source or prompt require review of dependent packs. Earlier results and human reviews are retained; timings are never moved automatically.</p></details></div></details>`;
  }
  function blankStoryboardTemplate(){
    const defs=structureDefinition(),template=defs.template||{};
    return `<section class="structure-template" data-structure-demo="true"><h3>Blank storyboard / shot template</h3><p class="notice">Structural preview only. No real story, shot ID or media asset is created. Excluded from authored-shot counts, reviews, queues, production eligibility and exports.</p><p>Story → sequence → shot → take / revision</p><div class="structure-evidence">${structureEvidence([template.source,template.kitchenSource,template.addendum])}</div><div class="structure-fields">${defs.fields.map(d=>structureField(d,null,null,true)).join('')}</div><h3>11 · Kitchen / handoff structure</h3><div class="structure-fields">${defs.kitchenFields.map(d=>structureField(d,null,null,true)).join('')}</div><p class="notice">Intentionally empty is different from intentionally not needed. A real shot can explicitly use silence, no background action or no character. Required inputs depend on phase and the chosen route.</p></section>`;
  }
  function structureExplorer(story){
    if(state.album==='template')return blankStoryboardTemplate();
    const record=storyStructure(story),shots=record.shots||[],filter=state.structureFilter||'all',sequence=state.structureSequence||'all',foundationFilter=state.structureFoundation||'all',foundations=new Map(shots.map(s=>[s.shotID,structureFoundation(s,story)]));
    const filters=[['all','All planned shots'],['no_art','No linked art'],['start_frame','No starting frame recorded'],['camera','Camera missing / not assessed'],['prompt','Clip prompt missing / not assessed'],['cue','Cue missing / not assessed'],['kitchen','Kitchen block incomplete'],['changed','Revision / dependency review']];
    const selected=shots.filter(s=>(foundationFilter==='all'||foundations.get(s.shotID).state===foundationFilter)&&(filter==='all'||structureGaps(s)[filter]||filter==='changed'&&foundations.get(s.shotID).dependencyReviewNeeded)&&(!state.search.trim()||queryMatch({title:JSON.stringify(s),tags:[]}))),byShot=new Map(selected.map(s=>[s.shotID,s]));
    let html=`<section class="story-structure" aria-label="Storyboard structure and gaps"><h3>Structure & gaps</h3><p class="intro">${shots.length} planned shots · ${(record.sections||[]).length} sequences · ${shots.filter(s=>s.kitchenWritten).length} kitchen blocks documented · may contain gaps. Counts describe available writing, not acceptance or readiness to generate.</p><p class="review-help">${esc(record.note||'Every planned slot stays visible without an image. Not assessed means the source has not established that field; it is not a failure.')}</p><div class="structure-toolbar"><label>Sequence<select id="structure-sequence"><option value="all">All sequences</option>${(record.sections||[]).map(s=>`<option value="${esc(s.id)}" ${s.id===sequence?'selected':''}>${esc(s.id)} · ${esc(s.title)}</option>`).join('')}</select></label><label>Focus<select id="structure-filter">${filters.map(([k,label])=>`<option value="${k}" ${k===filter?'selected':''}>${label}${k==='all'?'':' · '+shots.filter(s=>structureGaps(s)[k]||k==='changed'&&foundations.get(s.shotID).dependencyReviewNeeded).length}</option>`).join('')}</select></label><label>Source foundation<select id="structure-foundation"><option value="all">All foundations</option>${Object.entries(window.CFA_SOURCE_FOUNDATION?.LABELS||{}).map(([k,label])=>`<option value="${k}" ${k===foundationFilter?'selected':''}>${esc(label)} · ${shots.filter(s=>foundations.get(s.shotID).state===k).length}</option>`).join('')}</select></label></div><div class="structure-legend">${Object.values(structureStates).map(label=>`<span>${esc(label)}</span>`).join('')}</div>`;
    let count=0;for(const section of record.sections||[]){if(sequence!=='all'&&sequence!==section.id)continue;const rows=(section.shotIDs||[]).map(id=>byShot.get(id)).filter(Boolean);if(!rows.length)continue;count+=rows.length;html+=`<section class="structure-sequence" data-structure-sequence="${esc(section.id)}"><h3>${esc(section.id)} · ${esc(section.title)} <small>${rows.length} shots</small></h3>${rows.map(s=>structureShot(s,section,foundations.get(s.shotID))).join('')}</section>`;}
    if(!count)html+=`<p class="empty">${shots.length?'No shots match this focus.':'No canonical shot slots are registered for this story yet. The blank template shows the full structure without inventing shots.'}</p>`;
    return html+'</section>';
  }
  function storyboardExplorer(media){
    const stories=storyboardStories(),story=selectedStoryboardStory();if(!story)return '<p class="empty">No stories registered yet.</p>';
    let html=`<section class="story-picker"><label for="story-select">Story</label><select id="story-select">${stories.map(s=>`<option value="${esc(s.id)}" ${s.id===story.id?'selected':''}>${esc(s.title)}${s.kind==='prose'?' · writings':''}</option>`).join('')}</select></section>`;
    const structure=state.album.startsWith('structure:')||state.album==='template';
    html+=`<nav class="tools structure-switch" aria-label="Storyboard views"><a class="pill" href="${esc(storyURL(story))}" ${!structure?'aria-current="page"':''}>Panels & writings</a><a class="pill" href="#${esc(story.project)}/storyboard/${encodeURIComponent('structure:'+story.id)}" ${state.album.startsWith('structure:')?'aria-current="page"':''}>Structure & gaps</a><a class="pill" href="#${esc(story.project)}/storyboard/template" ${state.album==='template'?'aria-current="page"':''}>Blank storyboard / shot template</a></nav>`;
    html+=(structure?'':storyLandingCards(stories,story))+`<section class="selected-story" data-selected-story="${esc(story.id)}"><h2>${state.album==='template'?'Storyboard structure demonstration':esc(story.title)}</h2>${story.description&&state.album!=='template'?`<p class="intro">${esc(story.description)}</p>`:''}`;
    html+=structure?structureExplorer(story):story.kind==='song'?songStoryboard(media):story.kind==='sequence'?sequenceStoryboard(story,media):'<p class="empty">No panels yet. This story is available as writings and development notes.</p>';
    return html+(state.album==='template'?'':storyWritings(story))+'</section>';
  }
  function songStoryboard(media){
    const album=state.album.startsWith('story:')?'':state.album;
    const sequenceAlbums=new Set((C.storyboardSequences||[]).filter(s=>s.project===state.project).flatMap(s=>s.sourceAlbumIDs||[]));
    if(state.project==='hon'&&album&&isFalconAlbum(C.albums.find(al=>al.id===album)||{project:'hon',assetIDs:[]}))return falconReferenceSection(media,album);
    const albums=C.albums.filter(al=>al.project===state.project&&al.category==='storyboard'&&!sequenceAlbums.has(al.id)&&!isFalconAlbum(al)&&(!album||al.id===album)),ids=new Set(albums.flatMap(al=>al.assetIDs));
    const position=a=>typeof a.storyboardPosition==='number'&&Number.isFinite(a.storyboardPosition)?a.storyboardPosition:null;
    const independentIDs=new Set((C.storyboardSequences||[]).filter(s=>s.project===state.project).flatMap(s=>s.assetIDs||[]));
    for(const shot of storyWorkItems().filter(s=>s.independentSequenceID))for(const m of shot.materials||[])independentIDs.add(m.assetID);
    const all=media.filter(a=>ids.has(a.id)&&(album||position(a)!==null)),related=album?[]:media.filter(a=>ids.has(a.id)&&position(a)===null&&!independentIDs.has(a.id));
    const ranged=all.filter(a=>(!state.storyStage||state.storyStage==='all'||storyboardStage(a)===state.storyStage)&&(position(a)===null?state.storyStart===0&&state.storyEnd===100:position(a)>=state.storyStart&&position(a)<=state.storyEnd));
    const themes=new Map(ranged.flatMap(storyThemes).map(t=>[t.id,t.title]));if(state.storyTheme!=='all'&&!themes.has(state.storyTheme))state.storyTheme='all';
    const cards=ranged.filter(a=>state.storyTheme==='all'||storyThemes(a).some(t=>t.id===state.storyTheme)).sort((a,b)=>(a.storyboardOrder??Infinity)-(b.storyboardOrder??Infinity)||clipTitleOrder.compare(a.title,b.title));
    const meta=Array.isArray(C.storyboardMetadata)?C.storyboardMetadata.find(m=>m.project===state.project):C.storyboardMetadata?.[state.project];
    let html=`<section class="story-controls"><div class="story-stage"><label for="story-stage">Stage</label><select id="story-stage"><option value="all">All stages</option>${Object.entries(storyboardStages).map(([id,label])=>`<option value="${id}" ${state.storyStage===id?'selected':''}>${label}</option>`).join('')}</select></div><div class="story-theme"><label for="story-theme">Theme</label><select id="story-theme"><option value="all">All themes in this range</option>${[...themes].map(([id,title])=>`<option value="${esc(id)}" ${state.storyTheme===id?'selected':''}>${esc(title)}</option>`).join('')}</select></div><div class="story-range"><label for="story-start">From <output>${state.storyStart}%</output><input id="story-start" type="range" min="0" max="100" step="5" value="${state.storyStart}" aria-label="Start of source panel range"></label><label for="story-end">To <output>${state.storyEnd}%</output><input id="story-end" type="range" min="0" max="100" step="5" value="${state.storyEnd}" aria-label="End of source panel range"></label><button class="pill" id="story-reset">Full storyboard</button></div><p class="review-help">Source panel order, not song seconds. ${esc(meta?.timingStatus||'Song timing has not been aligned.')} Themes update with the selected range.</p></section><p class="video-sort-note">${cards.length} matching panels · ${themes.size} available themes in this range</p>`;
    const hasProgress=storyWorkItems().some(s=>!s.independentSequenceID);
    if(hasProgress)html+=`<div class="tools story-view-switch" aria-label="Storyboard view">${[['panels','Panels'],['progress','Shot progress']].map(([id,label])=>`<button class="pill" data-story-layout="${id}" aria-pressed="${(state.storyLayout||'panels')===id}">${label}</button>`).join('')}</div>`;
    if(hasProgress&&state.storyLayout==='progress')html+=storyProgress(cards);
    else if(state.project==='hon')html+=`<section class="original-story-collections"><h2>Original storyboard - ${cards.length} source panels</h2><p class="intro">Original SB-series source images of Grok origin; the specific original bot author is unconfirmed. Open a section for its numbered panels; later planning does not change their source provenance.</p>${collectionCards(storyboardAlbumCollections(cards).filter(g=>!album||g.id===album))}</section>`;
    else html+=mediaGroup('Story panels','In source panel order. Open a panel for linked material and its next step.',cards);
    if(!cards.length)html+='<p class="empty">No panels match this range and theme.</p>';if(related.length)html+=`<details class="detail-drawer"><summary>Related song material · ${related.length}</summary>${mediaGroup('Developed frames and clips','Related song material; source panel order and timing stay unchanged.',related)}</details>`;return html+(state.project==='hon'&&!album?falconReferenceSection(media):'');
  }
  const missionProviders=[['Grok','Grok'],['Gemini','Gemini'],['Flow','Flow'],['PanhandlerNova','Claude / Pan_Handlers']];
  const missionProject=t=>C.projects.find(p=>p.id===t.project)?.name||'Across projects';
  const missionStatuses={ready:'Ready to send',needs_input:'Needs your input',planned:'Planned',in_progress:'In progress',done:'Done'};
  function providerKey(value){const key=String(value||'').toLowerCase().replace(/[^a-z]/g,'');if(key==='claude')return 'PanhandlerNova';return [...missionProviders,...(C.providerScorecards?.providers||[]).map(p=>[p.id,p.name])].find(([id])=>id.toLowerCase().replace(/[^a-z]/g,'')===key)?.[0]||'';}
  function safeMissionHref(value){
    if(typeof value!=='string'||!value.trim())return '';let decoded;
    try{decoded=decodeURIComponent(value.trim());}catch{return '';}
    if(/[\x00-\x1f\x7f\\]/.test(decoded)||/^(?:[a-z][a-z0-9+.-]*:|\/)/i.test(decoded))return '';
    try{const target=new URL(value,value.trim().startsWith('#')?(location.href||document.URL||base):base);return target.protocol===base.protocol&&target.origin===base.origin?target.href:'';}catch{return '';}
  }
  function missionLinkGroup(asset,url){
    if(asset)return asset.kind==='image'?'images':asset.kind==='video'?'videos':isDoc(asset)?'reading':'other';
    const target=new URL(url),path=target.pathname.toLowerCase(),view=target.hash.slice(1).split('/')[1];
    if(/\.(?:png|jpe?g|webp|gif|svg|avif)$/.test(path)||['outfits','details','cast','storyboard'].includes(view))return 'images';
    if(/\.(?:mp4|webm|mov|m4v)$/.test(path)||view==='videos')return 'videos';
    if(/\.(?:txt|md|json|csv|tsv|pdf)$/.test(path))return 'reading';
    return /\.zip$/.test(path)?'downloads':'other';
  }
  function sourceComparisonPairs(project,taskID){
    return (Array.isArray(C.sourceComparisons)?C.sourceComparisons:[]).filter(pair=>
      ['pending_comparison','source_selected'].includes(pair.status)&&(!project||pair.project===project)&&(!taskID||pair.missionTaskID===taskID)&&
      Array.isArray(pair.items)&&pair.items.length===2&&new Set(pair.items.map(item=>item.assetID)).size===2&&
      pair.items.every(item=>{const a=byID.get(item.assetID);return item.label&&a&&a.project===pair.project&&a.kind==='image'&&normalVisible(a);}));
  }
  function sourceComparisonChoice(pair){
    const choice=pair.sourceChoice,a=choice&&byID.get(choice.selectedAssetID);
    return pair.status==='source_selected'&&choice?.scope==='prototype_video_source'&&a?.sha256===choice.sha256&&a.bytes===choice.bytes&&pair.items.some(item=>item.assetID===a.id)?choice:null;
  }
  function sourceComparisonItemLabel(item){
    const label=String(item.label).replace(/ · (?:Keep|Needs fixes|Marked for removal)$/,'');
    const status=statusLabels[reviewRecord(item.assetID).status];
    return label+(status?' · '+status:'');
  }
  function sourceComparisonStatus(pair){
    const choice=sourceComparisonChoice(pair);
    return choice?'Saved video source: '+pair.items.find(item=>item.assetID===choice.selectedAssetID).label:pair.status==='pending_comparison'?(pair.items.every(item=>Object.hasOwn(statusLabels,reviewRecord(item.assetID).status))?'Reviews recorded · no source or replacement selected':'Pending comparison'):'Source choice needs verification';
  }
  function sourceComparisonPreviews(task){
    if(!task.id)return '';
    return sourceComparisonPairs(null,task.id).map(pair=>{
      const previews=pair.items.map(item=>{
        const a=byID.get(item.assetID);if(!displayed.includes(a.id))displayed.push(a.id);
        return '<button class="mission-priority-preview" data-open="'+esc(a.id)+'"><img loading="lazy" src="'+esc(href(a.thumb))+'" alt="'+esc(sourceComparisonItemLabel(item))+'"><span>'+esc(sourceComparisonItemLabel(item))+(sourceComparisonChoice(pair)?.selectedAssetID===a.id?' · Video source':'')+'</span></button>';
      }).join('');
      return '<section class="source-comparison-preview"><h4>'+esc(pair.title)+'</h4><p class="mission-note">'+esc(sourceComparisonStatus(pair))+'</p><div class="mission-priority-previews">'+previews+'</div><button class="pill" data-source-comparison="'+esc(pair.id)+'">Open paired full-size comparison</button></section>';
    }).join('');
  }
  function sourceComparisonPanels(){
    return sourceComparisonPairs(state.project).filter(pair=>!state.search||pair.items.some(item=>queryMatch(byID.get(item.assetID)))).map(pair=>{
      const figures=pair.items.map(item=>{
        const a=byID.get(item.assetID),full=esc(href(a.src));
        return '<figure data-comparison-asset="'+esc(a.id)+'"><figcaption><strong>'+esc(sourceComparisonItemLabel(item))+(sourceComparisonChoice(pair)?.selectedAssetID===a.id?' · Selected for video':'')+'</strong><span>'+esc(a.filename)+'</span></figcaption><a class="source-comparison-image" href="'+full+'" target="_blank" rel="noopener"><img src="'+full+'" alt="'+esc(sourceComparisonItemLabel(item))+' — '+esc(pair.title)+'" width="'+esc(a.width||1280)+'" height="'+esc(a.height||720)+'"></a><a class="pill" href="'+full+'" target="_blank" rel="noopener">Open '+esc(sourceComparisonItemLabel(item))+' full size ↗</a></figure>';
      }).join('');
      return '<section id="source-comparison-'+esc(pair.id)+'" class="source-comparison" aria-label="'+esc(pair.title)+'"><h2>'+esc(pair.title)+'</h2><p class="source-comparison-status">'+esc(sourceComparisonStatus(pair))+'</p><p>'+esc(pair.summary)+'</p><div class="source-comparison-pair">'+figures+'</div></section>';
    }).join('');
  }
  function missionTaskLinks(task){
    const groups=new Map([['images','View images'],['videos','View video'],['reading','Read briefs and records'],['downloads','Download packages'],['other','Other links']].map(([id,label])=>[id,{label,links:[]}]));
    const gatedIDs=new Set(task.reviewProgress&&task.reviewGate?(task.reviewGate.targets||[]).map(target=>target.assetID):[]);
    for(const link of Array.isArray(task.links)?task.links:[]){
      if(gatedIDs.has(link.assetID))continue;
      const asset=byID.get(link.assetID),url=asset?'':safeMissionHref(link.href);if(asset&&isArchived(asset)||!asset&&!url)continue;
      const group=missionLinkGroup(asset,url),html=asset?`<button class="pill" data-open="${esc(link.assetID)}">${esc(link.label||'Open reference')}</button>`:`<a class="pill" href="${esc(url)}" ${/\.zip(?:[?#]|$)/i.test(url)?'download':''} target="_blank" rel="noopener">${esc(link.label||'Open prepared file')} ↗</a>`;
      groups.get(group).links.push(html);
    }
    const sections=[...groups].filter(([,group])=>group.links.length).map(([id,group])=>`<section class="mission-resource-group" data-resource-group="${id}"><h4>${group.label}</h4><div class="tools">${group.links.join('')}</div></section>`).join('');
    const resources=sections?`<div class="mission-resources">${sections}</div>`:'',comparison=sourceComparisonPreviews(task);
    const reviewed=(task.reviewedPreviewAssetIDs||[]).map(id=>byID.get(id)).filter(a=>a&&['image','video'].includes(a.kind));
    const pending=task.reviewGate?(task.previewAssetIDs||[]).map(id=>byID.get(id)).filter(normalVisible):[];
    for(const a of [...pending,...reviewed])if(!displayed.includes(a.id))displayed.push(a.id);
    const reviewLinks=pending.length&&task.id!=='favorites-prop-sweep'?`<section class="mission-resource-group"><h4>Still to review · ${pending.length}</h4><div class="tools">${pending.map(a=>`<button class="pill" data-open="${esc(a.id)}">${esc(a.title)}</button>`).join('')}</div></section>`:'';
    const history=reviewed.length&&task.id!=='favorites-prop-sweep'?`<details class="mission-review-history"><summary>${task.reviewGate?'Recorded decisions':'Recorded shortlist decisions'} · ${reviewed.length}</summary><div class="tools">${reviewed.map(a=>`<button class="pill" data-open="${esc(a.id)}">${esc(a.title)} · ${esc(statusLabels[reviewRecord(a.id).status])}</button>`).join('')}</div></details>`:'';
    return task.comparisonInHistory?reviewLinks+resources+(comparison?`<details class="mission-review-history"><summary>Selected starting image and earlier comparison</summary>${comparison}</details>`:'')+history:comparison+outfitGunReviewLinks(task)+reviewLinks+resources+history;
  }
  function outfitGunReviewAssets(){
    return C.assets.filter(a=>a.project==='hon'&&a.kind==='image'&&a.sourceIntake==='HON-GROK-RETURN-20261009'&&a.propState==='with_gun'&&a.outfitAlbumID);
  }
  function missionReviewProgress(task){
    const ids=[...new Set(task.previewAssetIDs||[])],pendingIDs=[],reviewedIDs=[],unavailableIDs=[];
    for(const id of ids){const a=byID.get(id);if(!a||a.kind!=='image'){unavailableIDs.push(id);continue;}if(Object.hasOwn(statusLabels,reviewRecord(id).status))reviewedIDs.push(id);else if(normalVisible(a))pendingIDs.push(id);else unavailableIDs.push(id);}
    return {requested:ids.length,answered:reviewedIDs.length,pendingIDs,reviewedIDs,unavailableIDs};
  }
  function missionTaskPresentation(task){
    if(task.status!=='done'&&task.reviewGate){
      const gate=task.reviewGate,targets=gate.targets,seen=new Map();
      const valid=typeof gate.label==='string'&&gate.label.trim()&&(!gate.completed||(typeof gate.completed==='object'&&!Array.isArray(gate.completed)))&&Array.isArray(targets)&&targets.length&&targets.every(target=>{
        if(!target||typeof target.assetID!=='string'||!target.assetID.trim()||typeof target.sha256!=='string'||!/^[a-f0-9]{64}$/i.test(target.sha256))return false;
        const sha=target.sha256.toLowerCase();if(seen.has(target.assetID)&&seen.get(target.assetID)!==sha)return false;
        seen.set(target.assetID,sha);return true;
      });
      if(valid){
        const pendingIDs=[],reviewedIDs=[],unavailableIDs=[];
        for(const [id,sha] of seen){
          const asset=byID.get(id),review=reviewRecord(id);
          if(!asset||!['image','video'].includes(asset.kind)||asset.sha256!==sha||(review.sha256&&review.sha256!==sha))unavailableIDs.push(id);
          else if(Object.hasOwn(statusLabels,review.status))reviewedIDs.push(id);
          else if(normalVisible(asset))pendingIDs.push(id);
          else unavailableIDs.push(id);
        }
        const completed=gate.completed||{},pending=pendingIDs.length,unavailable=unavailableIDs.length;
        const progress={requested:seen.size,answered:reviewedIDs.length,pendingIDs,reviewedIDs,unavailableIDs};
        const counts={keep:0,needs_fixes:0,remove:0};for(const id of reviewedIDs)counts[reviewRecord(id).status]++;
        const summary=`${reviewedIDs.length} of ${seen.size} requested images or clips have recorded decisions (${counts.keep} Keep, ${counts.needs_fixes} Needs fixes, ${counts.remove} marked for removal). `;
        return {...task,status:pending?'needs_input':'in_progress',statusLabel:pending?'Needs your input':unavailable?'Reference check needed':completed.statusLabel||'Review recorded · team follow-up',
          title:pending?`${gate.label} · ${pending} awaiting review`:unavailable?`${gate.label} · reference check needed`:completed.title||`${gate.label} · review recorded`,
          priority:pending||unavailable?task.priority:'normal',previewAssetIDs:pendingIDs,reviewedPreviewAssetIDs:reviewedIDs,reviewProgress:progress,
          summary:summary+(pending?`${pending} still need a decision. Existing reviews do not need repeating.`:unavailable?`${unavailable} exact references are unavailable or do not match the requested version. The team must resolve these before the review can be called complete.`:completed.summary||'Your review step is complete. Repairs, replacement selection and feedback delivery remain separate.'),
          nextAction:pending?'Review only the remaining requested versions. Keep, Needs fixes and Mark for removal each complete the image review step.':unavailable?'Team: locate and verify the exact requested versions; do not transfer a decision from another image.':completed.nextAction||'Team: reconcile the recorded decisions with the handoff. Review completion does not establish that feedback was sent or a replacement was approved.',
          missing:pending?[`${pending} requested versions have no recorded decision.`]:unavailable?[`${unavailable} exact references need a source check.`]:Array.isArray(completed.missing)?completed.missing:[]};
      }
    }
    if(task.id==='grok-hon-neck-chains-and-props'&&task.status==='ready')return {...task,summary:'The authorized brief requests 24 chain designs: six choices in each of four styles. Grok confirms the brief is written but has not been sent for generation; no chain designs have returned. The separate 50-image cigar, cigarette and toothpick request was sent earlier, but Grok reports it is still pending with none generated.',nextAction:'CFA Nova coordinates the already-authorized chain brief and follows up on the existing mouth-prop request. No additional approval is needed from you to send the chain discovery brief.',enablers:[],deliverables:['24 necklace designs: six choices in each of four styles, with clear display images and a design manifest.','The separately requested cigar, cigarette and toothpick images, when Grok completes that existing request.'],laterReview:'Choose one favorite in each chain style after the 24 designs arrive. Additional winner angles wait for those selections.',missing:[]};
    if(['grok-lisan-mouth65-available','grok-falcon-extension40-available'].includes(task.id)){
      const progress=missionReviewProgress(task),pending=progress.pendingIDs.length,unavailable=progress.unavailableIDs.length;
      return {...task,priority:pending||unavailable?task.priority:'normal',status:pending?'needs_input':'in_progress',title:task.id==='grok-lisan-mouth65-available'?`Lisan mouth shortlist · ${pending} awaiting review`:`Falcon extension shortlist · ${pending} awaiting review`,summary:`${progress.answered} of ${progress.requested} shortlisted images have recorded decisions. ${pending} await your decision.${unavailable?' '+unavailable+' references are unavailable and need a source check.':''} The full collection remains available; images outside this shortlist are not added as new review requests.`,nextAction:pending?'Review the remaining shortlist. Existing decisions stay saved; recorded defects remain separate correction work.':'The shortlist decisions are saved. The team can follow up on recorded defects; the full collection and earlier decisions remain available below.',previewAssetIDs:progress.pendingIDs,reviewedPreviewAssetIDs:progress.reviewedIDs,reviewProgress:progress};
    }
    if(task.id!=='favorites-prop-sweep')return task;
    const received=outfitGunReviewAssets(),visible=received.filter(normalVisible),unreviewed=visible.filter(a=>!reviewRecord(a.id).status),kept=visible.filter(a=>reviewRecord(a.id).status==='keep'),fixes=visible.filter(a=>reviewRecord(a.id).status==='needs_fixes'),outfits=new Set(received.map(a=>a.outfitAlbumID));
    return {...task,title:unreviewed.length?`Review outfit gun variants · ${unreviewed.length} unreviewed`:'Outfit gun variant review',status:unreviewed.length?'needs_input':fixes.length?'in_progress':'done',summary:`${received.length} distinct gun variants were received across ${outfits.size} outfits. ${visible.length} are visible in this browser; ${received.length-visible.length} are hidden by removal or archive choices. Saved image reviews: ${unreviewed.length} unreviewed · ${kept.length} Keep · ${fixes.length} Needs fixes. A gun can be approved while the rest of its image needs fixes. Full outfit collections include original views; their counts are not additional gun variants.`,nextAction:unreviewed.length?'Review the remaining images for outfit and character preservation. Use the full outfit link to compare original views; existing gun approvals stay in each image’s notes.':fixes.length?'The recorded fixes remain open; accepted and removed variants retain their decisions.':'Every visible variant has a recorded review.',missing:unreviewed.length?[`${unreviewed.length} gun variants still have no Keep / Needs fixes / Remove decision in this browser.`]:[],links:(task.links||[]).filter(link=>{const a=byID.get(link.assetID),url=a?'':safeMissionHref(link.href);return (a||url)&&missionLinkGroup(a,url)!=='images';})};
  }
  function outfitGunReviewLinks(task){
    if(task.id!=='favorites-prop-sweep')return '';
    const progress=task.reviewGate&&task.reviewProgress;
    const visible=outfitGunReviewAssets().filter(normalVisible),pending=progress?progress.pendingIDs.map(id=>byID.get(id)).filter(Boolean):visible.filter(a=>!reviewRecord(a.id).status),reviewed=progress?progress.reviewedIDs.map(id=>byID.get(id)).filter(Boolean):visible.filter(a=>reviewRecord(a.id).status);
    const rows=items=>items.map(a=>{const album=C.albums.find(al=>al.id===a.outfitAlbumID),count=(album?.assetIDs||[]).filter(id=>normalVisible(byID.get(id))).length,status=reviewRecord(a.id).status;return `<div class="tools" data-gun-variant="${esc(a.id)}"><button class="pill" data-open="${esc(a.id)}">${esc(album?.title||a.title)} · gun variant${status?' · '+esc(statusLabels[status]):''}</button><a class="pill" href="${esc(castHubHref('hon','outfits',a.outfitAlbumID))}">Compare full outfit · ${count} images</a></div>`;}).join('');
    return `<section class="mission-resource-group" data-resource-group="gun-variants"><h4>Gun variants by outfit · ${progress?`${progress.requested} received · ${progress.answered} reviewed`:`${visible.length} visible`}</h4>${rows(pending)}${reviewed.length?`<details><summary>Already reviewed · ${reviewed.length}</summary>${rows(reviewed)}</details>`:''}${visible.length||progress?'':'<p>All received variants are currently hidden by your removal or archive choices.</p>'}</section>`;
  }
  function missionUserAction(task){
    const action=task.userAction;if(!action)return '';
    const links=(action.links||[]).filter(link=>C.projects.some(p=>p.id===link.project)&&['intake','working','review_queue'].includes(link.view));
    return `<section class="mission-user-action"><h4>${esc(action.title||'For you now')}</h4><p>${esc(action.description||'')}</p><div class="tools">${links.map(link=>`<button class="pill" data-mission-view="${esc(link.view)}" data-mission-project="${esc(link.project)}">${esc(link.label)}</button>`).join('')}</div></section>`;
  }
  function missionTaskBackground(task,content){
    return task.backgroundDetails?`<details class="mission-background"><summary>${esc(task.backgroundLabel||'Team progress and source records')}</summary>${content}</details>`:content;
  }
  function missionTaskCard(t){
    const lists=[['enablers','Before sending','mission-missing'],['deliverables','Deliverables','mission-deliverables'],['missing',t.missingLabel||'Other open items','mission-open-items']].map(([key,label,cls])=>Array.isArray(t[key])&&t[key].length?`<div class="${cls}"><strong>${esc(label)}</strong><ul>${t[key].map(item=>`<li>${esc(item)}</li>`).join('')}</ul></div>`:'').join('');
    const background=`${t.nextAction?`<p class="mission-next-action"><strong>${t.backgroundDetails?'Team next step:':'Next:'}</strong> ${esc(t.nextAction)}</p>`:''}${lists}${t.laterReview?`<p class="mission-note"><strong>Your later review:</strong> ${esc(t.laterReview)}</p>`:''}${missionTaskLinks(t)}`;
    return `<details class="mission-task"><summary><span class="mission-status ${esc(t.status)}">${esc(t.statusLabel||missionStatuses[t.status]||'Planned')}</span><b>${esc(t.title)}</b><small class="mission-project">${esc(missionProject(t))}</small></summary><p>${esc(t.summary||'')}</p>${missionUserAction(t)}${missionTaskBackground(t,background)}</details>`;
  }
  function missionPriorityCard(task){
    const references=[...new Set(Array.isArray(task.previewAssetIDs)?task.previewAssetIDs:[])].map(id=>byID.get(id)).filter(a=>normalVisible(a)&&a.kind==='image');
    const previews=items=>`<div class="mission-priority-previews">${items.map(a=>{if(!displayed.includes(a.id))displayed.push(a.id);return `<button class="mission-priority-preview" data-open="${esc(a.id)}"><img loading="lazy" src="${esc(href(a.thumb))}" alt=""><span>${esc(a.title)}</span></button>`;}).join('')}</div>`;
    const previewIDs=new Set(references.map(a=>a.id)),otherLinks={...task,links:(Array.isArray(task.links)?task.links:[]).filter(link=>!previewIDs.has(link.assetID))};
    const background=`${task.nextAction?`<p class="mission-next-action"><strong>${task.backgroundDetails?'Team next step:':'Next:'}</strong> ${esc(task.nextAction)}</p>`:''}${references.length?`<h4>Start with these images</h4>${previews(references.slice(0,7))}${references.length>7?`<details class="mission-priority-more"><summary>More shortlisted images · ${references.length-7}</summary>${previews(references.slice(7))}</details>`:''}`:''}${missionTaskLinks(otherLinks)}${Array.isArray(task.missing)&&task.missing.length?`<details class="mission-priority-notes"><summary>${esc(task.missingLabel||'Review notes & remaining checks')}</summary><ul>${task.missing.map(item=>`<li>${esc(item)}</li>`).join('')}</ul></details>`:''}`;
    return `<article class="mission-priority-card" data-task-id="${esc(task.id)}"><details class="mission-priority-task"><summary><div class="mission-priority-meta"><span class="mission-status ${esc(task.status)}">${esc(task.statusLabel||missionStatuses[task.status])}</span><span>${esc(task.provider)} · ${esc(missionProject(task))}</span></div><h3>${esc(task.title)}</h3></summary><p>${esc(task.summary||'')}</p>${missionUserAction(task)}${missionTaskBackground(task,background)}</details></article>`;
  }
  function missionPrioritySection(tasks,hasQuery){
    return `<details class="mission-priority" aria-labelledby="mission-priority-heading"><summary class="mission-priority-heading"><div><p class="mission-priority-label">Review first</p><h2 id="mission-priority-heading">Top priority</h2></div><span class="mission-priority-count">${tasks.length} ${tasks.length===1?'item':'items'}</span></summary>${tasks.length?tasks.map(missionPriorityCard).join(''):`<p class="mission-note">${hasQuery?'No top-priority items match this search.':'No top-priority reviews waiting.'}</p>`}</details>`;
  }
  function workflowReferences(title,ids){
    const references=(Array.isArray(ids)?ids:[]).map(id=>byID.get(id)).filter(a=>normalVisible(a)&&(title!=='Source references'||exportAllowed(a)));if(!references.length)return '';
    return `<section class="workflow-references"><h3>${esc(title)}</h3><div class="workflow-reference-grid">${references.map(a=>{if(!isDoc(a)&&!displayed.includes(a.id))displayed.push(a.id);return `<button data-open="${esc(a.id)}" class="workflow-reference">${!isDoc(a)?`<img loading="lazy" src="${esc(href(a.thumb))}" alt="">`:''}<span>${esc(a.title)}</span></button>`;}).join('')}</div></section>`;
  }
  function safeComfyURL(value){try{const url=new URL(value);return url.protocol==='https:'&&url.hostname==='cloud.comfy.org'&&!url.username&&!url.password&&!url.port?url.href:'';}catch{return '';}}
  function collaboratorFileLink(label,path,download=false){const url=safeMissionHref('../../../../../../'+String(path||''));return path&&url?`<a class="pill" href="${esc(url)}" ${download?'download':''} target="_blank" rel="noopener">${esc(label)} ↗</a>`:'';}
  function collaboratorWorkLink(link){if(link?.path)return collaboratorFileLink(link.label||'Open file',link.path);try{const url=new URL(link?.url);return url.protocol==='https:'?`<a class="pill" href="${esc(url.href)}" target="_blank" rel="noopener">${esc(link.label||'Open resource')} ↗</a>`:'';}catch{return '';}}
  function projectContextPackLink(label,path,bundledHref,download=false){
    if(bundledHref!==undefined){if(typeof bundledHref!=='string'||!/^media\/[0-9a-f]{64}\.(?:txt|zip)$/.test(bundledHref))return '';const url=safeMissionHref(bundledHref);return url?`<a class="pill" href="${esc(url)}" ${download?'download':''} target="_blank" rel="noopener">${esc(label)} ↗</a>`:'';}
    return collaboratorFileLink(label,path,download);
  }
  function collaboratorContextPacks(provider,profile){
    const index=C.projectContextPacks;if(!index||index.status!=='prepared_not_delivered')return '';
    const fallback={Gemini:['gemini_master','gemini_chat','gemini_studio'],Grok:['grok_chief','hal'],Flow:['flow'],Codex:['nova'],DeepSeek:['deepseek'],Kimi:['kimi'],Qwen:['qwen'],PanhandlerNova:['claude']};
    const recipients=profile?.mailboxIDs?.length?profile.mailboxIDs:fallback[provider]||[],packs=(index.packs||[]).filter(pack=>recipients.includes(pack.recipientID));
    return '<section class="collaborator-context-packs"><h3>Project context packs</h3><p class="review-help">Prepared snapshots · not sent. Load the listed files into the matching project or chat. Extract ZIP downloads first; a ZIP is transport, not a presumed model input.</p><div class="tools">'+projectContextPackLink('Which files to load',index.uploadMapPath,index.uploadMapHref)+projectContextPackLink('Download all project packs',index.allPacksZipPath,index.allPacksZipHref,true)+'</div>'+packs.map(pack=>'<details class="collaborator-detail" data-context-pack="'+esc(pack.recipientID)+'"><summary>'+esc(pack.label||pack.recipientID)+'</summary><p class="review-help">'+esc(pack.route||'Route unverified')+' · '+esc(pack.identityStatus||'Identity status unrecorded')+'</p><div class="tools">'+projectContextPackLink('Load guide',pack.loadGuidePath,pack.loadGuideHref)+projectContextPackLink('Download project pack',pack.zipPath,pack.zipHref,true)+'</div><p class="review-help">'+esc(pack.fileCount)+' files · '+esc(index.preparedAtUTC||'Date unrecorded')+'</p></details>').join('')+'</section>';
  }
  const collaboratorSections=[['work','Work & handoffs'],['profile','Profile'],['scorecard','Role scorecard'],['roles','Roles guide']];
  function collaboratorIdentityLink(p){
    if(!p.identity?.path)return '';
    const identityURL=safeMissionHref('../../../../../../'+p.identity.path),named=(p.workLinks||[]).find(link=>link?.label&&link?.path&&safeMissionHref('../../../../../../'+link.path)===identityURL);
    return named?collaboratorWorkLink(named):collaboratorFileLink('Read authored I_AM',p.identity.path);
  }
  function collaboratorProfile(id,section='profile'){
    const roster=C.providerScorecards||{},p=(roster.providers||[]).find(p=>p.id===id);if(!p)return '';
    const list=value=>Array.isArray(value)?value.filter(v=>typeof v==='string'):typeof value==='string'&&value?[value]:[];
    const self=p.selfReported||{},roles=roster.roleDefinitions||[],metrics=roster.metricDefinitions||[];
    const roleName=value=>roles.find(r=>r.id===value)?.label||String(value||'Unassigned role').replace(/_/g,' ');
    if(section==='scorecard'){
      const cards=p.scorecards||[];
      return '<section class="collaborator-scorecards"><h3>Role scorecard</h3><p class="review-help">Assessed work earns grades. Self-reports and untested roles stay separate.</p><div class="role-scorecard-wrap"><table class="role-scorecard-table"><caption class="sr-only">'+esc(p.name)+' role assessments</caption><thead><tr><th scope="col">Role</th><th scope="col">Grade</th><th scope="col">Assessment & evidence</th></tr></thead><tbody>'+cards.map(card=>{
        const assessed=card.status==='human_assessment'?'Human assessment':card.grade?'Recorded assessment':'No assessed result';
        const evidence=(card.evidenceRefs||[]).map(ref=>typeof ref==='string'?'<p>'+esc(ref)+'</p>':collaboratorWorkLink(ref)).join('');
        return '<tr><th scope="row">'+esc(roleName(card.category))+'</th><td><span class="role-grade '+(card.grade?'assessed':'ungraded')+'">'+esc(card.grade||'Ungraded')+'</span></td><td><span class="assessment-label">'+esc(assessed)+'</span>'+(card.assessedBy||card.assessmentDate?'<small class="assessment-by">'+esc([card.assessedBy,card.assessmentDate].filter(Boolean).join(' · '))+'</small>':'')+'<details class="scorecard-evidence"><summary>Details & dimensions</summary><p>'+esc(card.note||'No production result has been assessed for this role.')+'</p>'+(evidence?'<div class="assessment-evidence"><strong>Assessment evidence</strong>'+evidence+'</div>':'')+'<dl class="metric-status">'+metrics.map(metric=>{const value=card.metrics?.[metric.id];return '<div><dt>'+esc(metric.label||metric.id)+'</dt><dd>'+esc(value==null?'Not measured':typeof value==='string'||typeof value==='number'?value:'Recorded in assessment evidence')+'</dd></div>';}).join('')+'</dl></details></td></tr>';
      }).join('')+'</tbody></table></div>'+(cards.length?'':'<p class="muted">No role assessments recorded.</p>')+'<details class="collaborator-detail"><summary>How to compare results</summary><p>Compare the same role, task and inputs. Quality, consistency, speed, rework, cost and tool access are recorded separately. Unsupported execution does not automatically fail planning quality.</p><p>Roles rotate through real work; one role grade does not establish an overall winner.</p></details></section>';
    }
    if(section==='roles')return '<section class="collaborator-roles"><h3>Roles guide</h3><p class="review-help">Choose the roles this scene needs. Assignments rotate through real work.</p><div class="role-definitions">'+roles.map(role=>'<details class="collaborator-detail"><summary>'+esc(role.label)+'</summary><p>'+esc(role.check||role.description||'')+'</p></details>').join('')+'</div><div class="tools">'+collaboratorFileLink('Shared roles brief',roster.rolesBriefPath)+collaboratorFileLink('Shoot plan verification','docs/notes/explorable_world/comfy/projects/collaborators/work_briefs_20261010/SHOOT_PLAN_VERIFICATION.txt')+'</div><details class="collaborator-detail"><summary>Production readiness · B or better</summary><p>Required scene ingredients must be reviewed, critical blockers resolved and the shoot plan verified. Approved character parts do not make a scene ready. Final result acceptance remains separate.</p></details></section>';
    const excerpt=typeof self.summary==='string'?self.summary:typeof p.identity?.summary==='string'?p.identity.summary:'';
    const identity=collaboratorIdentityLink(p),preferred=list(self.preferredCreativeRoles);
    return '<section class="collaborator-profile"><h3>Profile</h3><div class="tools">'+identity+'</div>'+(excerpt?'<blockquote>'+esc(excerpt)+'</blockquote>':'')+'<dl class="profile-overview"><div><dt>Preferred roles</dt><dd>'+esc(preferred.map(roleName).join(', ')||'Not reported')+'</dd></div><div><dt>Benchmark participation</dt><dd>'+esc(String(self.benchmarkWillingness||'Not reported').replace(/_/g,' '))+'</dd></div><div><dt>Availability</dt><dd>'+esc(p.availability||'Unconfirmed')+'</dd></div></dl><p class="review-help">Role preferences are self-reported, not earned grades.</p><details class="collaborator-detail collaborator-self-report"><summary>In their own introduction</summary><p class="review-help">'+esc(self.basis||'No authored self-report is supplied.')+'</p>'+[['strengths','Self-reported strengths'],['limitations','Self-reported limits'],['preferences','Self-reported preferences']].map(([key,label])=>'<h4>'+label+'</h4>'+(list(self[key]).length?'<ul>'+list(self[key]).map(v=>'<li>'+esc(v)+'</li>').join('')+'</ul>':'<p class="muted">Not reported.</p>')).join('')+'</details><details class="collaborator-detail collaborator-capabilities"><summary>Recorded capability evidence</summary><p>'+esc(p.capabilities?.summary||'No observed capability is recorded yet.')+'</p><p class="review-help">Basis: '+esc(p.capabilities?.basis||'Unverified')+'. These observations do not establish an earned filmmaking grade.</p>'+((p.capabilities?.evidenceRefs||[]).map(ref=>typeof ref==='string'?'<p>'+esc(ref)+'</p>':collaboratorWorkLink(ref)).join(''))+'</details><details class="collaborator-detail"><summary>Communication & mailbox</summary><p>'+esc(p.communication?.route||'Unverified')+'</p><p class="review-help">'+esc(String(p.communication?.status||'Unknown').replace(/_/g,' '))+' · '+esc(p.communication?.note||'')+'</p><div class="tools">'+collaboratorFileLink('Mailbox guide','docs/notes/explorable_world/comfy/projects/collaborators/MAILBOX.md')+collaboratorFileLink('Mailbox registry','docs/notes/explorable_world/comfy/projects/collaborators/mailbox/registry.json')+'</div></details>'+(p.identity?.sha256?'<details class="collaborator-detail"><summary>Identity provenance</summary><p class="filename">'+esc(p.identity.path)+'<br>SHA-256 '+esc(p.identity.sha256)+'</p></details>':'')+'</section>';
  }
  function collaboratorsWorkspace(){
    const configured=C.providerScorecards?.providers||[],providers=configured.length?configured.map(p=>[p.id,p.name]):[['ComfyUI','ComfyUI'],['Flow','Flow'],['Gemini','Gemini'],['Grok','Grok'],['PanhandlerNova','Claude / Pan_Handlers']];
    const selected=providers.some(([id])=>id===state.collaborator)?state.collaborator:providers[0][0],p=configured.find(p=>p.id===selected),providerName=providers.find(([id])=>id===selected)?.[1]||'ComfyUI',query=state.search.toLowerCase().trim();
    const section=collaboratorSections.some(([id])=>id===state.collaboratorSection)?state.collaboratorSection:'work',tabID='collaborator-tab-'+selected+'-'+section,panelID='collaborator-panel-'+selected;
    let html=`<div class="tools collaborator-tabs" role="group" aria-label="Choose collaborator">${providers.map(([id,label])=>`<button class="pill ${selected===id?'active':''}" aria-pressed="${selected===id}" data-collaborator-provider="${esc(id)}">${esc(label)}</button>`).join('')}</div>`;
    html+='<section class="collaborator-provider" data-collaborator-profile="'+esc(selected)+'"><header class="collaborator-heading"><h2>'+esc(providerName)+'</h2>'+(p?.currentRole?'<p>'+esc(p.currentRole)+'</p>':'')+'</header><div class="collaborator-section-tabs" role="tablist" aria-label="'+esc(providerName)+' sections">'+collaboratorSections.map(([id,label])=>'<button role="tab" id="collaborator-tab-'+esc(selected)+'-'+id+'" data-collaborator-section="'+id+'" aria-selected="'+(section===id)+'" aria-controls="'+esc(panelID)+'" tabindex="'+(section===id?'0':'-1')+'">'+esc(label)+'</button>').join('')+'</div><section class="collaborator-section-panel" role="tabpanel" id="'+esc(panelID)+'" aria-labelledby="'+esc(tabID)+'" tabindex="0" data-collaborator-section-panel="'+section+'">';
    if(section==='work'){
    if(selected==='ComfyUI'){
      const workflows=(Array.isArray(C.productionWorkflows)?C.productionWorkflows:[]).filter(w=>w.provider==='ComfyUI'&&[w.title,w.summary,w.nextAction,missionProject(w)].join(' ').toLowerCase().includes(query));
      html+=`<div class="workflow-list">${workflows.map(w=>{const cloud=safeComfyURL(w.cloudURL);return `<article class="production-workflow"><p class="eyebrow">${esc(missionProject(w))}</p><h2>${esc(w.title)}</h2><p class="workflow-status">${esc(w.statusLabel||String(w.status||'Planned').replace(/_/g,' '))}</p><p class="intro">${esc(w.summary||'')}</p>${w.nextAction?`<p class="mission-next-action"><strong>Next:</strong> ${esc(w.nextAction)}</p>`:''}${workflowReferences('Source references',w.sourceAssetIDs)}${workflowReferences('Outputs',w.outputAssetIDs)}${workflowReferences('Workflow & notes',w.documentAssetIDs)}${cloud?`<a class="pill cloud-workflow-link" href="${esc(cloud)}" target="_blank" rel="noopener">Open saved Comfy workflow ↗</a>`:''}</article>`;}).join('')}</div>`;
      if(!workflows.length)html+='<div class="empty">No matching ComfyUI workflow is listed yet.</div>';
    } else {
      const tasks=(C.missionControl?.tasks||[]).map(missionTaskPresentation).filter(t=>providerKey(t.provider)===selected&&[t.title,t.summary,t.nextAction,missionProject(t)].join(' ').toLowerCase().includes(query));
      if(tasks.length)html+=`<section class="collaborator-work">${tasks.map(missionTaskCard).join('')}</section>`;
      const plans=C.assets.filter(a=>normalVisible(a)&&planHasProvider(reviewRecord(a.id).shotPlan,selected)&&queryMatch(a));
      if(plans.length){html+=mediaGroup('Draft shot queue','Planned here; attach the actual files when you send your handoff.',plans.filter(a=>!isDoc(a)));html+=`<div class="tools">${providerShotExportControls(selected,plans)}</div>`;}
      if(selected==='PanhandlerNova')html+='<div class="tools"><button class="pill" data-mission-export="PanhandlerNova">Export review for Claude</button></div>';
      if(!tasks.length){const briefs=C.assets.filter(a=>isDoc(a)&&/collaborator/i.test(a.album||'')&&(a.album+' '+a.title).toLowerCase().includes(providerName.toLowerCase())&&queryMatch(a));html+=documentGroups(briefs);if(!briefs.length&&!plans.length)html+='<p class="notice">No matching work card is listed. Use the project links below for the next bounded task.</p>';}
    }
    if(selected==='PanhandlerNova')html+=(C.writerDevelopment?.projects||[]).map(project=>writerDevelopment(project.id,true)).join('');
    html+=collaboratorContextPacks(selected,p);
    if(p)html+='<details class="collaborator-detail collaborator-work-links"><summary>Project links & mailbox</summary><div class="tools">'+(p.workLinks||[]).map(collaboratorWorkLink).join('')+collaboratorFileLink('Mailbox guide','docs/notes/explorable_world/comfy/projects/collaborators/MAILBOX.md')+collaboratorFileLink('Mailbox registry','docs/notes/explorable_world/comfy/projects/collaborators/mailbox/registry.json')+'</div><p class="review-help">'+esc(p.communication?.route||'Route unverified')+' · '+esc(p.communication?.note||'')+'</p></details>';
    } else html+=collaboratorProfile(selected,section);
    return html+'</section></section>';
  }
  function missionControl(){
    const board=C.missionControl||{}, rank={ready:0,needs_input:1,in_progress:2,planned:3,done:4};
    const tasks=(Array.isArray(board.tasks)?board.tasks:[]).map(missionTaskPresentation).map(t=>({...t,status:Object.hasOwn(missionStatuses,t.status)?t.status:'planned'})).sort((a,b)=>rank[a.status]-rank[b.status]);
    const query=state.search.toLowerCase().trim(),matching=tasks.filter(t=>[t.provider,t.title,t.summary,t.nextAction,...(Array.isArray(t.missing)?t.missing:[])].join(' ').toLowerCase().includes(query));
    const priority=matching.filter(t=>t.priority==='top'&&t.status!=='done'),visible=matching.filter(t=>t.priority!=='top'||t.status==='done');
    const assets=C.assets,queued=assets.filter(pendingReviewDecision),plans=assets.filter(a=>normalVisible(a)&&reviewRecord(a.id).shotPlan),count=status=>tasks.filter(t=>t.status===status).length;
    const pending=projectAssets(true).filter(pendingReviewDecision),projectName=C.projects.find(p=>p.id===state.project)?.name||state.project;
    let html=`<div class="mission-counts">${[['Ready to send',count('ready')],['Needs your input',count('needs_input')],['In progress',count('in_progress')]].map(([label,n])=>`<div><strong>${n}</strong><span>${label}</span></div>`).join('')}<button type="button" class="mission-count-link" data-mission-view="shot_plans" data-mission-scope="all" aria-label="Open all ${plans.length} shot plans"><strong>${plans.length}</strong><span>Shot plans <span aria-hidden="true">→</span></span></button></div><p class="mission-note">Tasks and shot plans cover all projects. Review choices reflect this browser; they have not been sent to a collaborator.</p>${missionPrioritySection(priority,Boolean(query))}<section class="mission-review" aria-labelledby="mission-review-heading"><div class="mission-review-summary"><div><h2 id="mission-review-heading">Image review</h2><p>${pending.length?`${pending.length} ${pending.length===1?'image is':'images are'} awaiting your decision · ${esc(projectName)}`:`No images awaiting your review · ${esc(projectName)}`}</p></div>${pending.length?`<button class="pill" data-mission-view="review_queue">Review images · ${pending.length}</button>`:''}</div><details class="mission-review-share"><summary>Prepare review sweep</summary><p class="mission-note">Export your decisions, favorites, stages and reference roles for Nova to pick up.</p><button class="pill review-sweep" id="prepare-review-sweep">Export review sweep</button><p id="review-sweep-status" role="status"></p></details></section><div class="section-head"><h2>Collaborator handoffs</h2></div><div class="mission-providers">`;
    for(const [id,name] of missionProviders){
      const work=visible.filter(t=>providerKey(t.provider)===id), planned=plans.filter(a=>planHasProvider(reviewRecord(a.id).shotPlan,id));
      html+=`<article class="mission-provider"><h3>${name}</h3><p class="mission-provider-count">${work.length} prepared ${work.length===1?'task':'tasks'}${id==='PanhandlerNova'?` · ${queued.length} review items`:` · ${planned.length} planned shots`}</p>${work.map(missionTaskCard).join('')||'<p class="mission-note">No prepared handoff listed yet.</p>'}${id==='PanhandlerNova'?`<button class="pill" data-mission-export="${id}">Export review for Claude</button>`:planned.length?providerShotExportControls(id,planned):''}</article>`;
    }
    html+='</div>';const undecided=plans.filter(a=>reviewRecord(a.id).shotPlan.destinations.includes('undecided')).length;
    if(undecided)html+=`<p class="notice">${undecided} shot ${undecided===1?'idea still needs':'ideas still need'} a destination. You can keep exploring before choosing a collaborator.</p>`;
    if(board.updated)html+=`<p class="mission-note">Prepared board updated ${esc(board.updated)}. A prepared handoff is ready for you to send; this library does not send it automatically.</p>`;
    return html;
  }

  const intakeFamilies=()=>C.reviewIntake?.families||[];
  let intakeViewerSequence=null;
  const intakeLabels={'GROK-HD-FALCON-1000':'Falcon scenes','LAG-1K':'Lisan scenes','LAG-VIS-NATURAL':'Lisan mouth updates','GROK-VIDEO-TEST':'Grok video tests'};
  const intakeName=value=>intakeLabels[value]||value;
  const intakeText=value=>value===null||value===undefined?'Unknown':typeof value==='object'?JSON.stringify(value,null,2):String(value);
  const supplementGroups=[['approved','Golden references','Your recorded selections and component approvals, with their original scope and source record. Existing site decisions are unchanged.'],['validated','V-Team scoped passes','V-Team checked the stated scope. Your saved choices appear on each card; advisory notes remain attached.'],['preliminary','Preliminary mouth picks','Your choices appear on each card. These remain preliminary team picks; V-Team has not validated them.']];
  const reviewSupplements=()=>Array.isArray(C.reviewSupplements)?C.reviewSupplements:[];
  function supplementURL(value){
    if(!value)return '';
    try{const url=new URL(value,base);return ['file:','http:','https:'].includes(url.protocol)?url.href:'';}catch{return '';}
  }
  function supplementLinks(s){
    const index=supplementURL(s.indexURL||s.sourceURL),manifest=supplementURL(s.csvURL),receipt=supplementURL(s.receiptURL);
    const delivery=s.mediaDelivery?`${s.mediaDelivery.fullImages} full images received and file-verified. The supplied review reports and version records are linked below each image.`:'This delivery lists the team’s selected references. Source records are available here for tracing the handoff.';
    return `${index?`<div class="tools"><a class="pill" href="${esc(index)}" target="_blank" rel="noopener">Supplied winners index ↗</a></div>`:''}<details class="supplement-source-details"><summary>Source details · optional</summary><p>${esc(delivery)}</p><p>These files document the delivery; they are not a review checklist.</p><div class="tools">${manifest?`<a class="pill" href="${esc(manifest)}" download="winners-source-manifest.csv">Download source manifest (.csv)</a>`:''}${receipt?`<a class="pill" href="${esc(receipt)}" target="_blank" rel="noopener">Original delivery receipt (text) ↗</a>`:''}</div></details>`;
  }
  function supplementReferenceNotice(s){
    if(s.mediaDelivery)return 'The delivered full images and review records are now connected. Some gold-reference assignments remain inferred; the team’s verdicts and your decisions stay separate.';
    return s.goldReferenceStatus==='provider_links_with_inferences'?'Some gold-reference assignments are inferred. The underlying V reports and full images for the new winners are still pending.':s.goldReferenceStatus==='pending'?'Gold-reference check pending.':'';
  }
  function supplementCard(item){
    const thumb=supplementURL(item.thumbURL),full=item.availability==='local_original_verified'?supplementURL(item.fullImageURL):'';
    const asset=byID.get(item.exactAssetID),reviewable=!!full&&asset?.sha256===item.sha256&&asset.kind==='image',decision=reviewable?reviewRecord(asset.id):null;
    if(reviewable&&!displayed.includes(asset.id))displayed.push(asset.id);
    const media=thumb?'<img loading="lazy" src="'+esc(thumb)+'" alt="'+esc(item.title)+'">':'<div class="empty">Preview unavailable</div>';
    const families=(item.familyIDs||[]).map(id=>intakeFamilies().find(f=>f.id===id)).filter(Boolean);
    const matchLabel=basis=>basis==='unique_hash_prefix_from_provider'?'Matched by the provider’s unique hash prefix':basis==='cited_hash_prefix'?'Matched to the cited hash prefix':['exact_version_hash','unique_version_hash_prefix'].includes(basis)?'Report identifies this exact image version':basis||'';
    const references=(item.referenceLinks||[]).map(ref=>{const url=supplementURL(ref.url),availability=ref.availability==='preview_only'?'Preview only':ref.availability==='local_original_verified'?'Full image local':'Availability not verified';return '<li>'+(url?'<a href="'+esc(url)+'" target="_blank" rel="noopener">'+esc(ref.label||'Local reference')+' ↗</a>':esc(ref.label||'Reference unavailable'))+'<p class="review-help">'+availability+' · '+esc(matchLabel(ref.matchBasis))+'</p><code>'+esc(ref.sha256||'')+'</code></li>';}).join('');
    const sources=(item.sourceLinks||[]).map(source=>{const url=supplementURL(source.url);return '<li>'+(url?'<a href="'+esc(url)+'" target="_blank" rel="noopener">'+esc(source.label||'Cited document')+' ↗</a>':esc(source.label||'Cited document unavailable'))+'<p class="review-help">'+esc(matchLabel(source.matchBasis))+'</p><code>'+esc(source.sha256||'')+'</code></li>';}).join('');
    const sourceLabel=item.group==='validated'?'V-Team scoped pass':item.group==='preliminary'?'Preliminary team pick':item.label;
    const reviewLink=reviewable?`<button class="pill supplement-review" data-open="${esc(asset.id)}">${decision.status?'Review saved decision':'Review image'}</button>`:'';
    const preview=reviewable?`<button class="supplement-preview" data-open="${esc(asset.id)}" aria-label="Review ${esc(item.title)}">${media}</button>`:full?`<a class="supplement-preview" href="${esc(full)}" target="_blank" rel="noopener" aria-label="Open verified local original: ${esc(item.title)}">${media}</a>`:`<div class="supplement-preview">${media}</div>`;
    const lineage=(item.lineage||[]).map(row=>{const older=byID.get(row.exactAssetID||row.assetID),canOpen=older?.sha256===row.sha256;return `<li>${canOpen?`<button class="pill" data-open="${esc(older.id)}">${esc(row.label||row.versionID||older.title)}</button>`:esc(row.label||row.versionID||row.imageID||'Recorded version')}<p class="review-help">${esc(row.status||'Version record')}${canOpen?' · Full image available':' · Full image not indexed'}</p><code>${esc(row.sha256||'')}</code></li>`;}).join('');
    return `<article class="supplement-card" data-supplement-item="${esc(item.id)}">${preview}<div class="supplement-copy"><p class="supplement-label">${esc(sourceLabel)}${item.vVerdict?' · '+esc(item.vVerdict):''}</p><h4>${esc(item.title)}</h4><p>${esc(item.version||'')} · <code>${esc(item.sha8||item.sha256?.slice(0,8)||'Hash unavailable')}</code></p><p class="review-help">${full?'Full image verified locally.':'Preview only · full image is not available locally.'}</p>${reviewable?`<p class="supplement-decision"><strong>Your decision:</strong> ${esc(statusLabels[decision.status]||'Not reviewed')}${decision.note?`<br>${esc(decision.note)}`:''}</p>`:''}${item.reviewScope?`<p class="review-help"><strong>Checked scope:</strong> ${esc(item.reviewScope)}</p>`:''}${item.advisories?`<p class="supplement-advisory"><strong>Advisory:</strong> ${esc(item.advisories)}</p>`:''}<div class="tools">${reviewLink}${full?`<a class="pill" href="${esc(full)}" target="_blank" rel="noopener">Open local original ↗</a>`:''}${families.map(f=>`<button class="pill" data-intake-family="${esc(f.id)}" data-intake-project="${esc(f.project)}">Earlier family · ${esc(f.frameID)}</button>`).join('')}</div><details><summary>Source and version evidence</summary>${intakeFields({sha256:item.sha256,thumbnailSHA256:item.thumbnailSHA256,reviewScope:item.reviewScope,goldReferences:item.goldReferences,source:item.sourceEvidence,'Provider note (as supplied)':item.notes,remoteImagePath:item.remoteImagePath,familyLinkBasis:item.familyLinkBasis,'Your recorded scoped choice':item.humanAcceptance})}${lineage?`<p>Version history · relationships supplied by the team</p><ul class="supplement-reference-links">${lineage}</ul>`:''}${references?`<p>Local gold-reference files</p><ul class="supplement-reference-links">${references}</ul>`:''}${sources?`<p>Cited source documents</p><ul class="supplement-reference-links">${sources}</ul>`:''}</details></div></article>`;
  }
  function supplementPanel(){
    const q=state.search.trim().toLowerCase();
    return reviewSupplements().map((s,index)=>{
      const projectItems=(s.items||[]).filter(item=>item.project===state.project),items=projectItems.filter(item=>!q||[item.title,item.version,item.sha256,item.label,item.notes].join(' ').toLowerCase().includes(q));
      if(!projectItems.length)return '';
      const key=state.project+':supplement:'+(s.id||index),open=intakeDisclosureState.get(key)??Boolean(q);
      return '<details class="intake-supplement" data-intake-disclosure="'+esc(key)+'"'+(open?' open':'')+'><summary><span>'+esc(s.title||'Winners supplement')+'</span><small>'+items.length+' entries · Golden references, scoped passes &amp; mouth picks</small></summary><div class="supplement-body"><p class="eyebrow">Later delivery · separate from frozen intake</p><p>'+items.length+' of '+projectItems.length+' entries for this project. Open a group, then choose Review saved decision to see the full image and its review controls.</p><p class="notice">'+esc(supplementReferenceNotice(s))+' Your saved choices are shown separately from the team’s findings. Preview-only entries cannot be reviewed as full images.</p>'+supplementLinks(s)+supplementGroups.map(([group,title,description])=>{const rows=items.filter(item=>item.group===group);return rows.length?'<details class="supplement-group"'+(q?' open':'')+'><summary>'+title+' · '+rows.length+'</summary><p>'+description+'</p><div class="supplement-grid">'+rows.map(item=>supplementCard(item)).join('')+'</div></details>':'';}).join('')+(!items.length?'<p class="empty">No supplement entries match this search.</p>':'')+'</div></details>';
    }).join('');
  }
  function familySupplementEvidence(f){
    return reviewSupplements().map(s=>{
      const items=(s.items||[]).filter(item=>(item.familyIDs||[]).includes(f.id));if(!items.length)return '';
      return '<aside class="family-supplement"><p class="notice">A later supplement has '+items.length+' '+(items.length===1?'entry':'entries')+' for this frame. The comparison below remains the frozen r002 handoff; it does not show a new final selection.</p><details class="supplement-group"><summary>Later supplement · '+items.length+'</summary><p>Family links associate the frame only. Each version retains its own hash, scope and availability. '+esc(supplementReferenceNotice(s))+'</p><div class="supplement-grid">'+items.map(item=>supplementCard(item)).join('')+'</div>'+supplementLinks(s)+'</details></aside>';
    }).join('');
  }
  function intakeFields(values){
    return '<dl class="intake-fields">'+Object.entries(values||{}).filter(([k,v])=>v!==null&&v!==undefined&&v!==''&&!(Array.isArray(v)&&!v.length)).map(([k,v])=>'<div><dt>'+esc(k.replace(/([a-z])([A-Z])/g,'$1 $2').replace(/_/g,' '))+'</dt><dd>'+esc(intakeText(v))+'</dd></div>').join('')+'</dl>';
  }
  function intakeVersion(v,label){
    const a=byID.get(v?.assetID),available=v?.availability==='available'&&a?.sha256===v.sha256;
    if(!v)return '<article class="intake-version"><h3>'+esc(label)+'</h3><p>No current scoped pass was nominated in this handoff. Review the original and version evidence.</p></article>';
    return '<article class="intake-version"><h3>'+esc(label)+'</h3>'+(available?card({...a,title:v.filename||a.title}):'<div class="empty">'+esc((v.availability||'unavailable').replace(/_/g,' '))+' · media is not included locally</div>')+'<p class="review-help">'+esc(v.role||'')+' · '+esc(v.filename||'Unspecified filename')+'</p>'+intakeFields(v.providerReview)+'<details><summary>Source and lineage</summary>'+intakeFields({sha256:v.sha256,path:v.repoPath,...(v.lineage||{})})+'</details></article>';
  }
  function intakeFamily(f){
    const original=f.versions.find(v=>v.sha256===f.original?.sha256),candidate=f.versions.find(v=>v.sha256===f.currentCandidate?.sha256);
    const shown=new Set([original?.sha256,candidate?.sha256].filter(Boolean)),history=f.versions.filter(v=>v!==original&&v!==candidate&&!shown.has(v.sha256));
    return '<section class="intake-family" data-intake-family-id="'+esc(f.id)+'" id="intake-'+esc(f.id)+'"><header><p class="eyebrow">'+esc(intakeName(f.dataset))+'</p><h2>'+esc(f.frameID)+'</h2><p>'+esc(f.category||'')+'</p>'+intakeFamilyProgress(f)+'</header>'+familySupplementEvidence(f)+'<div class="intake-compare">'+intakeVersion(original||f.versions.find(v=>v.role==='version_only_base'),'Original / delivered base')+(candidate&&candidate.sha256===original?.sha256?'<p class="notice">The provider current candidate is the original above.</p>':intakeVersion(candidate,'Provider current candidate'))+'</div><details class="detail-drawer"><summary>Provider review and open choices</summary><p>Reported by the production team. Your site decisions and formal reference validation remain separate.</p>'+intakeFields(f.providerReview)+intakeFields({duplicateEvidence:(C.reviewIntake?.duplicateGroups||[]).filter(g=>g.dataset===f.dataset&&g.id===f.providerReview?.duplicateGroup)})+(f.providerFinalPointer&&!f.currentCandidate?'<p class="notice">The provider final pointer is retained as evidence; it is not an available current scoped pass.</p>'+intakeFields(f.providerFinalPointer):'')+'</details>'+(history.length?'<details class="detail-drawer"><summary>Earlier versions and other candidates · '+history.length+'</summary><div class="intake-compare">'+history.map(v=>intakeVersion(v,'Version history')).join('')+'</div></details>':'')+'<details class="detail-drawer"><summary>Manifest evidence</summary>'+intakeFields({familyID:f.id,siteValidation:f.siteValidation,evidence:f.evidence})+'</details></section>';
  }
  const intakeBatchKey=f=>f.dataset+'::'+(f.category||'');
  const intakeBatchLabel=f=>f.category||'Unlabeled batch';
  const intakeAvailableAsset=v=>v?.availability==='available'&&byID.get(v.assetID)?.sha256===v.sha256?byID.get(v.assetID):null;
  function intakeReviewTargets(f){
    const original=f.versions.find(v=>v.sha256===f.original?.sha256)||f.versions.find(v=>v.role==='version_only_base');
    const current=f.versions.find(v=>v.sha256===f.currentCandidate?.sha256);
    let targets=[original,current].map(intakeAvailableAsset).filter(Boolean);
    if(!targets.length){const fallback=f.versions.map(intakeAvailableAsset).find(Boolean);if(fallback)targets=[fallback];}
    return [...new Map(targets.map(a=>[a.id+':'+a.sha256,a])).values()];
  }
  function intakeReviewProgress(f){
    const targets=intakeReviewTargets(f),reviewed=targets.filter(a=>Object.hasOwn(statusLabels,reviewRecord(a.id).status));
    const pending=targets.filter(a=>!Object.hasOwn(statusLabels,reviewRecord(a.id).status));
    return {targets,reviewed,pending,complete:targets.length>0&&!pending.length,unavailable:!targets.length};
  }
  function intakeReviewTotals(families){
    const progress=families.map(intakeReviewProgress),targets=[...new Map(progress.flatMap(p=>p.targets).map(a=>[a.id+':'+a.sha256,a])).values()];
    const done=targets.filter(a=>Object.hasOwn(statusLabels,reviewRecord(a.id).status)).length;
    return {total:targets.length,done,remaining:targets.length-done,familiesPending:progress.filter(p=>p.pending.length).length,familiesReviewed:progress.filter(p=>p.complete).length,unavailable:progress.filter(p=>p.unavailable).length};
  }
  function intakeFamilyProgress(f){const p=intakeReviewProgress(f);return `<p class="intake-family-progress">${p.unavailable?'Waiting for a full image':p.reviewed.length+' of '+p.targets.length+' review targets decided'}</p>`;}
  function intakeLiveProgress(project){const p=intakeReviewTotals(intakeFamilies().filter(f=>f.project===project));return 'Project intake: '+p.remaining+' images left · '+p.done+' reviewed';}
  function intakeGalleryFamily(f){
    const seen=new Set(),versions=f.versions.filter(v=>{const key=v.sha256||v.assetID||v.filename;if(seen.has(key))return false;seen.add(key);return true;});
    const original=versions.find(v=>v.sha256===f.original?.sha256)||versions.find(v=>v.role==='version_only_base');
    const pending=state.intakeDecision==='pending'?intakeReviewProgress(f).pending[0]:null;
    const cover=(pending&&versions.find(v=>v.assetID===pending.id&&v.sha256===pending.sha256))||(intakeAvailableAsset(original)&&original)||versions.find(intakeAvailableAsset)||original||versions[0];
    const asset=intakeAvailableAsset(cover),related=versions.filter(v=>v!==cover);
    const later=reviewSupplements().flatMap(s=>s.items||[]).filter(item=>(item.familyIDs||[]).includes(f.id));
    const preview=v=>{const a=intakeAvailableAsset(v);return a?card(a):'<p class="empty">'+esc(v?.filename||'Original')+' · media unavailable locally</p>';};
    return `<section class="intake-gallery-family" data-intake-family-id="${esc(f.id)}"><header><h3>${esc(f.frameID)}</h3><p>${cover===original?'Original / delivered base':cover?.sha256===f.currentCandidate?.sha256?'Provider current candidate':asset?'Available delivered version':'Media unavailable locally'}</p>${intakeFamilyProgress(f)}</header>${preview(cover)}${related.length?`<details class="intake-gallery-versions"><summary>Related versions · ${related.length}</summary>${related.map(v=>`<div class="intake-gallery-version"><p>${esc(v.role?.replace(/_/g,' ')||'Recorded version')}</p>${preview(v)}</div>`).join('')}</details>`:''}<footer>${later.length?`<p>Later supplement · ${later.length} ${later.length===1?'entry':'entries'}</p>`:''}<button class="pill" data-intake-detail="${esc(f.id)}" aria-label="View evidence for ${esc(f.frameID)}">View family evidence →</button></footer></section>`;
  }
  function intakeGallery(rows,allRows){
    const groups=new Map();for(const f of rows){const key=intakeBatchKey(f);if(!groups.has(key))groups.set(key,[]);groups.get(key).push(f);}
    return [...groups].map(([key,items])=>`<section class="intake-gallery-batch"><header class="section-head"><div><p class="eyebrow">${esc(intakeName(items[0].dataset))} · ${esc(items[0].dataset)}</p><h2>${esc(intakeBatchLabel(items[0]))}</h2></div><span>${items.length} shown · ${allRows.filter(f=>intakeBatchKey(f)===key).length} families</span></header><div class="gallery intake-gallery">${items.map(intakeGalleryFamily).join('')}</div></section>`).join('');
  }
  function intakeWorkspace(){
    const families=intakeFamilies().filter(f=>f.project===state.project),datasets=[...new Set(families.map(f=>f.dataset))],q=state.search.trim().toLowerCase();
    if(!datasets.includes(state.intakeDataset))state.intakeDataset='all';
    const focused=Boolean(state.album),layout=focused?'evidence':state.intakeLayout==='gallery'?'gallery':'evidence';
    const batchFamilies=families.filter(f=>state.intakeDataset==='all'||f.dataset===state.intakeDataset),batches=new Map();
    for(const f of batchFamilies){const key=intakeBatchKey(f);if(!batches.has(key))batches.set(key,{family:f,count:0});batches.get(key).count++;}
    if(!batches.has(state.intakeBatch))state.intakeBatch='all';
    let rows=focused?families.filter(f=>f.id===state.album):batchFamilies.filter(f=>(state.intakeBatch==='all'||intakeBatchKey(f)===state.intakeBatch)&&(!q||JSON.stringify([f.frameID,f.category,f.providerReview,f.versions.map(v=>[v.filename,v.sha256])]).toLowerCase().includes(q)));
    if(!focused&&state.intakeFilter==='repairs')rows=rows.filter(f=>f.versions.length>1);
    if(!focused&&state.intakeFilter==='unavailable')rows=rows.filter(f=>f.versions.some(v=>v.availability!=='available'));
    const progress=intakeReviewTotals(rows);
    if(!focused&&state.intakeDecision==='pending')rows=rows.filter(f=>intakeReviewProgress(f).pending.length);
    if(!focused&&state.intakeDecision==='reviewed')rows=rows.filter(f=>intakeReviewProgress(f).complete);
    const pageSize=layout==='gallery'?36:12,pages=Math.max(1,Math.ceil(rows.length/pageSize)),page=Math.max(0,Math.min(state.intakePage||0,pages-1));state.intakePage=page;
    let html='<div class="tools intake-view-tools"><label>View <select id="intake-layout"><option value="evidence" '+(layout==='evidence'?'selected':'')+'>Detailed evidence</option><option value="gallery" '+(layout==='gallery'?'selected':'')+'>Batch gallery</option></select></label><span>Same images and saved reviews in both views.</span></div>'+(!focused?supplementPanel():'')+'<p class="notice">Frozen handoff r002 · files verified. Provider grades, duplicate suggestions and scoped passes are evidence for your review; they do not set Keep, ratings, character defaults or approval.</p>';
    if(!focused)html+='<div class="tools"><label>Review <select id="intake-decision-filter">'+[['pending','Still to review'],['reviewed','Reviewed'],['all','All families']].map(([value,label])=>'<option value="'+value+'" '+(state.intakeDecision===value?'selected':'')+'>'+label+'</option>').join('')+'</select></label><label>Dataset <select id="intake-dataset"><option value="all">All received datasets</option>'+datasets.map(d=>'<option value="'+esc(d)+'" '+(state.intakeDataset===d?'selected':'')+'>'+esc(intakeName(d))+'</option>').join('')+'</select></label><label>Show <select id="intake-filter">'+[['all','All families'],['repairs','Families with versions'],['unavailable','Unavailable history or originals']].map(([v,l])=>'<option value="'+v+'" '+((state.intakeFilter||'all')===v?'selected':'')+'>'+l+'</option>').join('')+'</select></label></div><details class="intake-batches"><summary>Batch / run · '+esc(state.intakeBatch==='all'?'All batches':intakeBatchLabel(batches.get(state.intakeBatch).family))+' · '+batches.size+' available</summary><p>Original batch names from the delivery. Each family keeps its related versions and source evidence.</p><div class="intake-batch-options" role="group" aria-label="Filter by batch"><button class="pill '+(state.intakeBatch==='all'?'active':'')+'" data-intake-batch="all" aria-pressed="'+(state.intakeBatch==='all')+'">All batches · '+batchFamilies.length+'</button>'+[...batches].map(([key,b])=>'<button class="pill '+(state.intakeBatch===key?'active':'')+'" data-intake-batch="'+esc(key)+'" aria-pressed="'+(state.intakeBatch===key)+'" title="'+esc(b.family.dataset)+'">'+esc(intakeBatchLabel(b.family))+' · '+b.count+'</button>').join('')+'</div></details>';
    html+='<section class="intake-progress" aria-label="Intake review progress"><p><strong>'+progress.remaining+' images left</strong> · '+progress.done+' reviewed · '+progress.familiesPending+' families still to review'+(progress.unavailable?' · '+progress.unavailable+' awaiting files':'')+'</p><p class="review-help">Keep, Needs fixes or Mark for removal completes this pass for that image. Notes and ratings are optional. Each original and nominated current version has its own decision; earlier attempts stay in the evidence.</p></section>';
    html+='<p id="intake-results" class="intake-results-count">'+rows.length+' '+(rows.length===1?'family':'families')+' · page '+(page+1)+' of '+pages+(layout==='gallery'?' · Open an image to review; expand related versions to compare.':'')+'</p>';
    const pagination=pages===1?'':'<div class="tools"><button class="pill" data-intake-page="'+(page-1)+'" '+(page===0?'disabled':'')+'>Previous families</button><button class="pill" data-intake-page="'+(page+1)+'" '+(page===pages-1?'disabled':'')+'>Next families</button></div>';
    const coverageKey=state.project+':coverage',coverage='<details class="detail-drawer intake-coverage" data-intake-disclosure="'+esc(coverageKey)+'"'+(intakeDisclosureState.get(coverageKey)?' open':'')+'><summary>Handoff coverage and receipts · optional</summary>'+intakeFields(C.reviewIntake?.summary)+'<p>Unavailable versions stay linked here. Nothing has been deleted or inferred from a matching filename.</p>'+intakeFields(C.reviewIntake?.receipt)+'</details>';
    html+=pagination;
    const pageRows=rows.slice(page*pageSize,(page+1)*pageSize);
    return html+(rows.length?(layout==='gallery'?intakeGallery(pageRows,rows):pageRows.map(intakeFamily).join('')):'<p class="empty">No families match these filters. Choose All families to revisit saved decisions or unavailable files.</p>')+pagination+coverage;
  }
  function intakeEvidenceMatches(a){
    if(!a?.sha256)return {families:[],later:[]};
    const row=C.reviewIntake?.assetMetadata?.[a.id];
    const families=row?.sha256===a.sha256?intakeFamilies().filter(f=>(row.familyIDs||[]).includes(f.id)&&f.versions.some(v=>v.sha256===a.sha256)):[];
    const later=reviewSupplements().map(s=>({supplement:s,items:(s.items||[]).filter(item=>item.exactAssetID===a.id&&item.sha256===a.sha256)})).filter(match=>match.items.length);
    return {families,later};
  }
  function intakeAssetEvidence(a){
    const {families,later}=intakeEvidenceMatches(a);
    if(!families.length&&!later.length)return '';
    const laterCount=later.reduce((n,match)=>n+match.items.length,0);
    return `<section class="intake-asset-evidence intake-evidence-summary" aria-label="Received review evidence and related versions"><h3>Team review</h3><p>${families.length?`${families.length} ${families.length===1?'family record':'family records'} with related versions.`:''}${laterCount?`${families.length?' ':''}Later winners supplement · exact image match.`:''}</p><p>Read the findings and scope alongside your saved decision.</p><button class="pill" data-intake-evidence="${esc(a.id)}">Read full review</button></section>`;
  }
  function intakeEvidenceFindings(review){
    const r=review||{}, rows=[['Team result',r.validationLabel||r.verdict||r.technicalValidation],['Reported stage',r.stage],['QA grade',r.qaGrade],['Suggested score',r.qaScoreSuggestion],['Score basis',r.qaBasis],['Checked scope',r.scope],['Reason',r.reason],['Advisory',r.advisory],['Remaining defects',r.remainingDefects],['Superseded finding',r.staleReason],['Chest classification',r.chestClass],['Team question at delivery',r.humanQuestion]];
    const findings=rows.filter(([,value])=>value!==null&&value!==undefined&&value!=='');
    const scoped=(r.scopedChecks||[]).map(check=>`<li><strong>${esc(check.outcome||'Outcome not recorded')}</strong>${check.scope?' · '+esc(check.scope):''}<p class="review-help">${esc(check.reviewer||'Reviewer not recorded')}${check.targetSha256Recorded?' · Image '+esc(check.targetSha256Recorded.slice(0,12)):''}</p></li>`).join('');
    return (findings.length?'<dl class="evidence-findings">'+findings.map(([label,value])=>`<div><dt>${esc(label)}</dt><dd>${esc(intakeText(value))}</dd></div>`).join('')+'</dl>':'<p class="review-help">No separate findings were supplied for this exact version.</p>')+(scoped?'<h4>Scoped checks</h4><ul class="evidence-scoped-checks">'+scoped+'</ul>':'');
  }
  function intakeEvidenceVersion(version,label,currentSHA){
    if(!version)return `<article class="evidence-version"><h4>${esc(label)}</h4><p>No version nominated in this delivery.</p></article>`;
    const a=byID.get(version.assetID||version.exactAssetID),verified=a?.sha256===version.sha256&&(version.availability==='available'||version.availability==='local_original_verified');
    const url=verified?supplementURL(href(a.src)):'';
    return `<article class="evidence-version"><h4>${esc(label)}</h4>${url?`<img loading="lazy" src="${esc(url)}" alt="${esc(a.title)}">`:''}<p>${esc(version.filename||a?.title||version.versionID||'Recorded version')}</p><p class="review-help">${version.sha256===currentSHA?'Image currently open':verified?'Full image available':'Full image not available locally'} · ${esc((version.sha256||'Unknown hash').slice(0,12))}</p>${url?`<a class="pill" href="${esc(url)}" target="_blank" rel="noopener">Open full image ↗</a>`:''}</article>`;
  }
  function intakeEvidencePanel(a){
    const {families,later}=intakeEvidenceMatches(a),choice=reviewRecord(a.id);
    const frozen=families.map(f=>{
      const version=f.versions.find(v=>v.sha256===a.sha256),original=f.versions.find(v=>v.sha256===f.original?.sha256),candidate=f.versions.find(v=>v.sha256===f.currentCandidate?.sha256),history=f.versions.filter(v=>v!==original&&v!==candidate);
      const exact=Object.keys(version.providerReview||{}).length?`<section class="evidence-findings-block"><h4>This exact version</h4>${intakeEvidenceFindings(version.providerReview)}</section>`:'';
      return `<section class="evidence-report"><p class="eyebrow">Received family record</p><h3>${esc(f.frameID)}</h3>${exact}<section class="evidence-findings-block"><h4>Family / original findings</h4><p class="review-help">Recorded at delivery. These findings do not automatically apply to a repaired version or override your later choices.</p>${intakeEvidenceFindings(f.providerReview)}</section><details class="evidence-related"><summary>Original and related versions · ${f.versions.length}</summary><div class="evidence-version-grid">${intakeEvidenceVersion(original,'Original / delivered base',a.sha256)}${candidate&&candidate.sha256===original?.sha256?'<p>The provider current candidate is the original.</p>':intakeEvidenceVersion(candidate,'Provider current candidate',a.sha256)}</div>${history.length?`<details><summary>Other delivered versions</summary><div class="evidence-version-grid">${history.map(v=>intakeEvidenceVersion(v,'Other version',a.sha256)).join('')}</div></details>`:''}<button class="pill" data-evidence-family="${esc(f.id)}" data-evidence-project="${esc(f.project)}">Compare original and versions in intake</button></details><details class="evidence-source"><summary>Source details · optional</summary><h4>Exact-version source record</h4>${intakeFields({sha256:version.sha256,providerReview:version.providerReview,lineage:version.lineage,evidence:version.evidence})}<h4>Family source record</h4>${intakeFields({familyID:f.id,original:f.original,currentCandidate:f.currentCandidate,providerReview:f.providerReview,siteValidation:f.siteValidation,evidence:f.evidence})}</details></section>`;
    }).join('');
    const supplements=later.map(({supplement:s,items})=>items.map(item=>{
      const sourceLabel=item.group==='validated'?'V-Team scoped pass':item.group==='preliminary'?'Preliminary team pick':'Reported approval';
      const links=(item.sourceLinks||[]).map(link=>{const url=supplementURL(link.url);return url?`<li><a href="${esc(url)}" target="_blank" rel="noopener">${esc(link.label||'Source report')} ↗</a></li>`:'';}).join('');
      return `<section class="evidence-report"><p class="eyebrow">Later winners supplement · exact image match</p><h3>${esc(item.title)}</h3>${intakeEvidenceFindings({validationLabel:sourceLabel+(item.vVerdict?' · '+item.vVerdict:''),scope:item.reviewScope,advisory:item.advisories})}<p class="review-help">${item.group==='preliminary'?'Your choice does not turn this preliminary pick into a V-Team validation.':'The team’s finding applies only to the stated scope of this exact image.'}</p>${links?`<details class="evidence-source"><summary>Review reports · optional</summary><ul>${links}</ul></details>`:''}<details class="evidence-source"><summary>Source details · optional</summary>${intakeFields({sha256:item.sha256,version:item.version,source:item.sourceEvidence,providerNote:item.notes,goldReferences:item.goldReferences,referenceLinks:item.referenceLinks,sourceLinks:item.sourceLinks,versionHistory:item.lineage,familyLinkBasis:item.familyLinkBasis,humanAcceptance:item.humanAcceptance})}${supplementLinks(s)}</details></section>`;
    }).join('')).join('');
    return `<header class="evidence-reader-head"><div><p class="eyebrow">Team review · read only</p><h2 id="intake-evidence-title">${esc(a.title)}</h2><p>Exact image · ${esc(a.sha256.slice(0,12))}</p></div><button class="pill" data-evidence-close>Return to image</button></header><div class="evidence-reader-content"><aside class="evidence-your-choice"><h3>Your saved decision</h3><p>${esc(statusLabels[choice.status]||'Not reviewed')}${choice.note?` · ${esc(choice.note)}`:''}</p><p class="review-help">Team findings are separate from your choice. Reading this panel changes nothing.</p></aside>${supplements}${frozen}</div>`;
  }
  let intakeEvidenceDialog=null,intakeEvidenceReturnFocus=null;
  function openIntakeEvidence(id,trigger){
    const a=byID.get(id);if(!a)return;
    const matches=intakeEvidenceMatches(a);if(!matches.families.length&&!matches.later.length)return;
    if(!intakeEvidenceDialog){
      intakeEvidenceDialog=document.createElement('dialog');intakeEvidenceDialog.className='intake-evidence-reader';intakeEvidenceDialog.setAttribute('aria-labelledby','intake-evidence-title');document.body.append(intakeEvidenceDialog);
      intakeEvidenceDialog.addEventListener('close',()=>{intakeEvidenceDialog.innerHTML='';intakeEvidenceReturnFocus?.focus();intakeEvidenceReturnFocus=null;});
      intakeEvidenceDialog.addEventListener('click',e=>{if(e.target===intakeEvidenceDialog)intakeEvidenceDialog.close();});
    }
    intakeEvidenceReturnFocus=trigger||document.activeElement;intakeEvidenceDialog.innerHTML=intakeEvidencePanel(a);
    intakeEvidenceDialog.querySelector('[data-evidence-close]').onclick=()=>intakeEvidenceDialog.close();
    intakeEvidenceDialog.querySelectorAll('[data-evidence-family]').forEach(button=>button.onclick=()=>{intakeEvidenceReturnFocus=null;intakeEvidenceDialog.close();dialog.close();state.intakeDataset='all';state.intakeFilter='all';state.intakePage=0;route(button.dataset.evidenceProject,'intake',button.dataset.evidenceFamily);});
    if(!intakeEvidenceDialog.open)intakeEvidenceDialog.showModal();
  }

  function renderMain(){
    displayed=[];const p=C.projects.find(p=>p.id===state.project);const all=(state.view==='shot_plans'&&state.album==='all-projects'?C.assets.filter(normalVisible):projectAssets(['review_queue','archive'].includes(state.view))).filter(a=>state.view==='archive'?isArchived(a):!isArchived(a)).filter(queryMatch);const docs=all.filter(isDoc);const media=all.filter(a=>!isDoc(a));
    const castHeading=state.album&&['cast','working'].includes(state.view)?((C.castCollections||[]).find(g=>g.project===state.project&&[g.id,g.id+'-working'].includes(state.album))||(C.castCollections||[]).find(g=>g.project===state.project&&(g.sourceAlbumIDs||[]).includes(state.album)))?.title:null;
    const heading=state.view==='intake'?'Intake verification':state.view==='comfy'&&!state.album?'Comfy results & swap targets':state.view==='storyboard'&&state.album.startsWith('story:')?selectedStoryboardStory()?.title||'Storyboard':state.view==='shot_plans'?(state.album==='all-projects'?'All shot plans':'Shot plans'):state.album?(state.album==='hon:piercings'?'Piercings and jewelry':state.album===state.project+':grill-designs'||state.view==='details'&&grillSourceAlbumIDs().has(state.album)&&grillDesignGroups().length?'Grills':castHeading||C.albums.find(a=>a.id===state.album)?.title):cats[state.view]||{mission_control:'Mission Control',collaborators:'Collaborators',all:p.name+' reference library',favorites:'Your favorites',export_basket:'Export basket',review_queue:'Review queue',archive:'Archive',shot_plans:'Shot plans',documents:'Documents & notes',intake:'Intake verification'}[state.view];
    let html=`<p class="eyebrow">${state.view==='shot_plans'&&state.album==='all-projects'?'Across all projects':esc(p.subtitle)}</p><div class="library-heading"><h1>${esc(heading)}</h1>${state.view==='videos'?`<div class="video-controls"><label class="video-sort" for="video-layout"><span>Layout</span><select id="video-layout"><option value="grouped" ${state.videoLayout==='grouped'?'selected':''}>Grouped</option><option value="all" ${state.videoLayout==='all'?'selected':''}>All clips</option></select></label><label class="video-sort" for="video-sort"><span>Sort</span><select id="video-sort">${Object.entries(videoSortLabels).map(([value,label])=>`<option value="${value}" ${state.videoSort===value?'selected':''}>${label}</option>`).join('')}</select></label></div>`:''}</div><p class="intro">${state.view==='intake'?'Originals, repairs and team review evidence, grouped together.':state.view==='comfy'?'Results first, with the source likenesses and technical inputs used for swaps. Character, mouth and grill references stay in Working references.':state.view==='collaborators'?'Workflows, source references, and prepared handoffs across your projects.':state.view==='mission_control'?'Your next moves, prepared handoffs, and ideas waiting for their next pass.':state.view==='all'?'Artwork first, grouped by purpose. Open a cover to browse its references here; select an image inside to review it.':state.view==='export_basket'?'A separate selection from across all projects. Add or remove references with ⇩; your favorites stay unchanged. The export is a file list, not a media bundle.':state.view==='favorites'?'Your review shortlist. These stars do not change the character locks or original files.':state.view==='shot_plans'?'Collect shot ideas and draft prompts, then export a handoff for your chosen collaborator. These plans have not been sent or generated.':state.view==='archive'?'Earlier designs and references you have archived. Open an image to restore it. Reviews, favorites, plans and original files are retained.':state.view==='review_queue'?'Unanswered requests first. Saved fixes, removal decisions and earlier references are in the collapsed sections below.':state.view==='details'?'Standalone artwork first. Placement examples are inside each item.':state.view==='documents'?'Notes are grouped by subject. Click a file to read a preview without leaving the library.':'Choose a group or browse the previews below.'}</p>`;
    if(['mission_control','collaborators'].includes(state.view)){const back=libraryReturn();html=`<a class="library-back" href="#${[back.project,back.view,back.album].filter(Boolean).map(encodeURIComponent).join('/')}">← Back to library</a>`+html;}
    if(!storageOK)html+='<p class="notice">Browser storage is unavailable. Export your review to keep decisions, notes, and favorites.</p>';
    if(state.album&&state.view!=='shot_plans')html+=`<p><button class="subtle-button" id="back-group">← Back to ${esc(cats[state.view]||(state.view==='intake'?'Intake verification':'all files'))}</button></p>`;
    if(state.view==='mission_control')html+=missionControl()+(C.reviewIntake?'<section class="mission-intake"><h2>Received review handoff</h2><p>Compare originals, current candidates and version history from the frozen package.</p><button class="pill" data-mission-view="intake">Open Intake verification</button></section>':'')+documentGroups(docs);
    else if(state.view==='intake')html+=intakeWorkspace();
    else if(state.view==='collaborators')html+=collaboratorsWorkspace();
    else if(state.view==='export_basket'){
      const selected=basketAssets().filter(queryMatch);html+=`<div class="tools"><span>${selected.length} references shown · ${basketAssets().length} in basket</span><button class="pill" id="export-basket-list" ${basket.size?'':'disabled'}>Export selection list</button><button class="pill" id="clear-basket" ${basket.size?'':'disabled'}>Clear basket</button></div><p class="notice">Imports add matching references to this basket. Clearing it only clears this selection; it does not change stars, review notes, or files.</p>`;
      html+=mediaGroup('Selected pictures & clips','References from all projects, ready for your next package.',selected.filter(a=>!isDoc(a)));html+=documentGroups(selected.filter(isDoc));if(!selected.length)html+='<div class="empty">Your basket is empty, or no selections match the search. Use ⇩ on a preview to collect a subset.</div>';
    } else if(state.view==='favorites'){

      const fav=media.filter(a=>favorites.has(a.id));html+=fav.length?`<div class="tools"><span>${fav.length} selected</span><button class="pill" id="export-main">Export favorites</button></div><div class="gallery">${fav.map(card).join('')}</div>`:'<div class="empty">No favorites yet. Click ☆ on an image or video to add it here.</div>';
    } else if(state.view==='shot_plans'){
      const plans=all.filter(a=>reviewRecord(a.id).shotPlan&&(state.destination==='all'||reviewRecord(a.id).shotPlan.destinations.includes(state.destination)));
      html+=`<div class="tools"><label for="plan-project">Project</label><select id="plan-project"><option value="all" ${state.album==='all-projects'?'selected':''}>All projects</option><option value="project" ${state.album!=='all-projects'?'selected':''}>${esc(p.name)}</option></select><label for="plan-destination">Destination</label><select id="plan-destination">${['all',...destinations].map(d=>`<option value="${d}" ${state.destination===d?'selected':''}>${esc(d==='all'?'All collaborators':destinationLabel(d))}</option>`).join('')}</select><button class="pill" id="export-handoff-txt">Export handoff TXT</button><button class="pill" id="export-handoff-json">Export handoff JSON</button></div><p class="notice">Handoffs include exact reference IDs and filenames, plus your notes and prompt. Attach the actual images or clips yourself; media files are not bundled in the export.</p>`;
      html+=mediaGroup('Planned shots',`${plans.length} plans${state.album==='all-projects'?' across all projects':''}. Open a reference to refine its idea, prompt, or destinations.`,plans.filter(a=>!isDoc(a)));
      html+=documentGroups(plans.filter(isDoc));if(!plans.length)html+='<div class="empty">No shots planned here yet. Open a reference and choose Plan a shot.</div>';
    } else if(state.view==='archive'){
      const archivedReferences=archiveReferenceGroups(media);html+=archivedReferences.html+mediaGroup('Archived pictures & clips','',archivedReferences.remaining)+documentGroups(docs);
      if(!all.length)html+='<div class="empty">'+(state.search.trim()?'No archived references match this search.':'No archived references in this project.')+'</div>';
    } else if(state.view==='review_queue'){
      const comparisons=sourceComparisonPanels();
      const pendingComparisons=sourceComparisonPairs(state.project).filter(pair=>pair.status==='pending_comparison').length;
      if(comparisons)html+=pendingComparisons?comparisons:`<details class="detail-drawer review-history"><summary>Saved source comparisons</summary>${comparisons}</details>`;
      const queued=all.filter(inReviewQueue), awaiting=all.filter(pendingReviewDecision), promotions=queued.filter(a=>reviewRecord(a.id).workingReference?.status==='requested'), fixes=queued.filter(a=>reviewRecord(a.id).status==='needs_fixes'), removals=queued.filter(a=>isArchived(a)||reviewRecord(a.id).status==='remove');
      html+=`<div class="tools"><span>${awaiting.length} unanswered image requests${pendingComparisons?' · '+pendingComparisons+' source comparisons pending':''} · ${fixes.length} need fixes · ${removals.length} marked for removal</span><button class="pill" id="export-review-main">Export review</button></div>`;
      html+=mediaGroup('Awaiting your decision','Nova has flagged a missing Keep / Needs fixes / Remove choice. Existing ratings and design stages remain unchanged.',awaiting.filter(a=>!isDoc(a)));
      if(promotions.length)html+=`<details class="detail-drawer review-history"><summary>Earlier saved reference requests · ${promotions.length}</summary>${mediaGroup('Earlier requests','Preserved from the previous controls. Production and the reference role now describe approved use.',promotions.filter(a=>!isDoc(a)))}</details>`;
      if(fixes.length)html+=`<details class="detail-drawer review-history"><summary>Saved decisions · Needs fixes · ${fixes.length}</summary>${mediaGroup('Needs fixes','Your decision is saved. Correction work remains with the team.',fixes.filter(a=>!isDoc(a)))}</details>`;
      if(removals.length)html+=`<details class="detail-drawer review-history"><summary>Saved removal decisions and archive · ${removals.length}</summary>${mediaGroup('Marked for removal','Your decision is saved. Original files remain available.',removals.filter(a=>!isDoc(a)))}</details>`;
      html+=documentGroups(queued.filter(isDoc));if(!awaiting.length)html+='<div class="empty">No unanswered image review requests. Saved decisions remain available above.</div>';
    } else if(state.view==='working')html+=workingReferencesWorkspace();
    else if(state.view==='documents')html+=documentGroups(docs);
    else if(state.view==='details'&&state.project==='hon'&&['all','visuals'].includes(state.detailLayout))html+=honTattooReferences();
    else if(state.view==='details'&&state.detailLayout!=='all')html+=detailExplorer();
    else if(state.view==='outfits'&&!state.album)html+=outfitExplorer(media);
    else if(state.view==='comfy'&&!state.album)html+=comfyWorkspace(media);
    else if(state.view==='cast')html+=castExplorer(state.album);
    else if(state.view==='storyboard')html+=storyboardExplorer(media);
    else if(state.view==='videos'&&state.project==='hon'&&!state.album&&state.videoLayout==='grouped')html+=videoPurposeExplorer(media);
    else if(state.view==='all'&&!state.album&&C.browseLayout?.projects?.[state.project])html+=compactAllFiles(projectAssets())+(['all','documents'].includes(state.allPurpose)?documentGroups(docs):'');
    else {
      let albums=C.albums.filter(a=>a.project===state.project&&(state.view==='all'||a.category===state.view)&&(!state.album||a.id===state.album)&&!(state.view==='all'&&!state.album&&a.category==='working')&&!(state.view==='details'&&grillSourceAlbumIDs().has(a.id)));
      if(state.view==='storyboard')html+='<p class="notice">Story ideas grouped by beat. Panel numbers identify the source; song timings are still to be aligned.</p>';
      if(state.view==='details')html+=detailExplorer()+collectionCards(grillDesignGroups())+'<p class="notice">Use each reference for its selected detail. A tattoo or piercing example does not replace the whole character.</p>'+(grillSourceAlbumIDs().has(state.album)?`<p><a href="${esc(castHubHref(state.project,'working',state.album))}">Browse the full mouth reference collection in Working references</a></p>`:'');
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
             if(!outfitsShown){const groups=outfitGroups(media);shown+=groups.reduce((n,g)=>n+g.items.length,0);html+=outfitExplorer(media,true);outfitsShown=true;}
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
           if(state.view==='outfits'&&state.album&&items.some(a=>a.propState==='with_gun')){
            html+=mediaGroup('Gun variants','Received candidates. Compare side placement, clothing and character details with the source.',items.filter(a=>a.propState==='with_gun'));
            html+=mediaGroup('Other views & revisions',al.description,items.filter(a=>a.propState!=='with_gun'));
          } else if(state.view==='all'&&!state.album&&al.category==='details')html+=detailAlbumGroups(al,items);
          else if(state.view==='comfy'&&al.id==='hon:head-anchor-b-candidates')html+=collectionCards(collectionGroups([{...al,title:'Head anchors - returned drafts',role:'3 mouth/piercing variants',coverID:al.assetIDs[0],unit:'variants',description:'Same portrait, different upper grills and nose/lip hoops. This cover is a browsing preview; every version keeps its own review and is not a canonical or accepted head.',sections:[{title:'Mouth and piercing variants',assetIDs:al.assetIDs}]}],items));
          else html+=mediaGroup(al.title,state.view==='all'?'':al.description,items,al.id);
        }
      }
      if(!shown&&!html.includes('data-collection=')&&!(state.view==='details'&&grillSourceAlbumIDs().has(state.album)))html+='<div class="empty">No matching previews. Try another category or search.</div>';
      if(state.view==='all'&&!state.album)html+=documentGroups(docs);
    }
    document.querySelector('#main').innerHTML=html;
    document.querySelectorAll('[data-open]').forEach(b=>b.onclick=()=>{
      const intakeScope=b.closest?.('.intake-gallery-family')?'.intake-gallery .media-open':b.closest?.('.intake-family')?'.intake-family .media-open':null;
      intakeViewerSequence=intakeScope?[...new Set([...document.querySelectorAll(intakeScope)].filter(button=>!button.closest('details:not([open])')).map(button=>button.dataset.open))]:null;
      if(intakeViewerSequence)displayed=[...intakeViewerSequence];
      openViewer(b.dataset.open);
    });
    document.querySelectorAll('[data-favorite]').forEach(b=>b.onclick=()=>toggleFavorite(b.dataset.favorite));
    document.querySelectorAll('[data-basket]').forEach(b=>b.onclick=()=>toggleBasket(b.dataset.basket));
    document.querySelector('#export-basket-list')?.addEventListener('click',exportBasket);document.querySelector('#clear-basket')?.addEventListener('click',()=>{basket.clear();saveBasket();notice('Export basket cleared. Favorites and review notes are unchanged.');});
     document.querySelectorAll('[data-album]').forEach(b=>b.onclick=()=>{const a=C.albums.find(x=>x.id===b.dataset.album);route(state.project,a.category,a.id);});
     document.querySelectorAll('[data-outfit-category]').forEach(button=>button.onclick=()=>selectOutfitCategory(button.dataset.outfitCategory));
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
    document.querySelectorAll('[data-all-purpose]').forEach(button=>button.onclick=()=>{state.allPurpose=button.dataset.allPurpose;renderMain();document.querySelector('[data-all-purpose="'+state.allPurpose+'"]')?.focus({preventScroll:true});});
    document.querySelectorAll('[data-browse-bucket]').forEach(button=>button.onclick=()=>{
      const id=button.dataset.browseBucket,top=button.getBoundingClientRect().top;
      collapsedBrowseBuckets.has(id)?collapsedBrowseBuckets.delete(id):collapsedBrowseBuckets.add(id);renderMain();
      const replacement=[...document.querySelectorAll('[data-browse-bucket]')].find(b=>b.dataset.browseBucket===id);
      if(replacement){window.scrollBy({top:replacement.getBoundingClientRect().top-top,behavior:'instant'});replacement.focus({preventScroll:true});}
    });
    document.querySelectorAll('[data-mission-view]').forEach(button=>button.onclick=()=>{const allPlans=button.dataset.missionView==='shot_plans'&&button.dataset.missionScope==='all';if(allPlans)state.destination='all';const project=C.projects.some(p=>p.id===button.dataset.missionProject)?button.dataset.missionProject:state.project;if(button.dataset.missionProject){state.search='';state.intakeDataset='all';state.intakeFilter='all';state.intakePage=0;}route(project,button.dataset.missionView,allPlans?'all-projects':'');});
    document.querySelectorAll('[data-source-comparison]').forEach(button=>button.onclick=()=>{const pair=sourceComparisonPairs().find(item=>item.id===button.dataset.sourceComparison);if(pair)route(pair.project,'review_queue');});
    document.querySelectorAll('[data-collaborator-provider]').forEach(button=>button.onclick=()=>{state.collaborator=button.dataset.collaboratorProvider;state.collaboratorSection='work';renderMain();document.querySelector('[data-collaborator-provider="'+state.collaborator+'"]')?.focus({preventScroll:true});});
    document.querySelectorAll('[data-collaborator-section]').forEach(button=>{
      button.onclick=()=>{state.collaboratorSection=button.dataset.collaboratorSection;renderMain();document.querySelector('[data-collaborator-section="'+state.collaboratorSection+'"]')?.focus({preventScroll:true});};
      button.onkeydown=event=>{const tabs=[...document.querySelectorAll('[data-collaborator-section]')],index=tabs.indexOf(button),last=tabs.length-1,next={ArrowRight:(index+1)%tabs.length,ArrowLeft:(index+last)%tabs.length,Home:0,End:last}[event.key];if(next===undefined)return;event.preventDefault();tabs[next].click();};
    });
    document.querySelectorAll('[data-export-intent]').forEach(select=>select.onchange=()=>{state.exportIntent=select.value==='multiverse_ingredients'?'multiverse_ingredients':'prime';render();});
    document.querySelector('#prepare-review-sweep')?.addEventListener('click',prepareReviewSweep);
    document.querySelectorAll('[data-detail-layout]').forEach(button=>button.onclick=()=>{state.detailLayout=['visuals','approved','archive','all'].includes(button.dataset.detailLayout)?button.dataset.detailLayout:'approved';renderMain();});
    document.querySelectorAll('[data-cast-filter]').forEach(button=>button.onclick=()=>{state.castFilter=button.dataset.castFilter;renderMain();});
    document.querySelector('#cast-source')?.addEventListener('change',e=>{state.castSource=e.target.value;renderMain();});
    document.querySelector('[data-cast-reset]')?.addEventListener('click',()=>{state.castFilter='all';state.castSource='all';renderMain();});
    document.querySelectorAll('[data-cast-source]').forEach(button=>button.onclick=()=>{state.castFilter='all';state.castSource=button.dataset.castSource;route(state.project,'cast');});
    document.querySelectorAll('[data-detail-profile]').forEach(button=>button.onclick=()=>{state.detailProfile=button.dataset.detailProfile;renderMain();});
    document.querySelectorAll('[data-story-layout]').forEach(button=>button.onclick=()=>{state.storyLayout=button.dataset.storyLayout==='progress'?'progress':'panels';renderMain();});
    document.querySelector('#structure-filter')?.addEventListener('change',e=>{state.structureFilter=e.target.value;renderMain();});
    document.querySelector('#structure-foundation')?.addEventListener('change',e=>{state.structureFoundation=e.target.value;renderMain();});
    document.querySelector('#structure-sequence')?.addEventListener('change',e=>{state.structureSequence=e.target.value;renderMain();});
    document.querySelector('#story-select')?.addEventListener('change',e=>{const story=storyboardStories().find(s=>s.id===e.target.value);if(story)route(story.project,'storyboard','story:'+story.id);});
    document.querySelector('#story-stage')?.addEventListener('change',e=>{state.storyStage=Object.hasOwn(storyboardStages,e.target.value)?e.target.value:'all';renderMain();});
    document.querySelector('#story-theme')?.addEventListener('change',e=>{state.storyTheme=e.target.value;renderMain();});
    document.querySelector('#story-start')?.addEventListener('change',e=>{state.storyStart=Math.min(Number(e.target.value),state.storyEnd);renderMain();});
    document.querySelector('#story-end')?.addEventListener('change',e=>{state.storyEnd=Math.max(Number(e.target.value),state.storyStart);renderMain();});
    document.querySelector('#story-reset')?.addEventListener('click',()=>{state.storyStart=0;state.storyEnd=100;state.storyTheme='all';state.storyStage='all';renderMain();});
    document.querySelectorAll('[data-mission-export]').forEach(button=>button.onclick=()=>{if(button.dataset.missionExport==='PanhandlerNova'){exportReview();return;}const previous={destination:state.destination,search:state.search};state.destination=button.dataset.missionExport;state.search='';try{exportShotHandoff('txt','all');}finally{Object.assign(state,previous);}});
    document.querySelector('#video-sort')?.addEventListener('change',e=>{state.videoSort=Object.hasOwn(videoSortLabels,e.target.value)?e.target.value:'longest';renderMain();});
    document.querySelector('#video-layout')?.addEventListener('change',e=>{state.videoLayout=e.target.value==='all'?'all':'grouped';renderMain();});
    document.querySelector('#back-group')?.addEventListener('click',()=>route(state.project,state.view));
    document.querySelector('#plan-project')?.addEventListener('change',e=>route(state.project,'shot_plans',e.target.value==='all'?'all-projects':''));
    document.querySelector('#plan-destination')?.addEventListener('change',e=>{state.destination=e.target.value;renderMain();});
    document.querySelector('#export-handoff-txt')?.addEventListener('click',()=>exportShotHandoff('txt',state.album==='all-projects'?'all':state.project));
    document.querySelector('#export-handoff-json')?.addEventListener('click',()=>exportShotHandoff('json',state.album==='all-projects'?'all':state.project));
    document.querySelectorAll('[data-intake-disclosure]').forEach(drawer=>drawer.addEventListener('toggle',()=>{if(drawer.isConnected)intakeDisclosureState.set(drawer.dataset.intakeDisclosure,drawer.open);}));
    document.querySelector('#intake-layout')?.addEventListener('change',e=>{
      const next=e.target.value==='gallery'?'gallery':'evidence',previous=state.album?'evidence':state.intakeLayout==='gallery'?'gallery':'evidence';
      state.intakeLayout=next;state.intakePage=Math.floor((state.intakePage||0)*(previous==='gallery'?36:12)/(next==='gallery'?36:12));
      if(state.album){const f=intakeFamilies().find(f=>f.project===state.project&&f.id===state.album);state.intakeDataset=f?.dataset||'all';state.intakeBatch=f?intakeBatchKey(f):'all';state.intakeFilter='all';state.intakePage=0;route(state.project,'intake');}
      else{renderMain();document.querySelector('#intake-layout')?.focus({preventScroll:true});}
    });
    document.querySelector('#intake-dataset')?.addEventListener('change',e=>{state.intakeDataset=e.target.value;state.intakeBatch='all';state.intakePage=0;renderMain();});
    document.querySelector('#intake-decision-filter')?.addEventListener('change',e=>{state.intakeDecision=['pending','reviewed','all'].includes(e.target.value)?e.target.value:'pending';state.intakePage=0;renderMain();});
    document.querySelector('#intake-filter')?.addEventListener('change',e=>{state.intakeFilter=e.target.value;state.intakePage=0;renderMain();});
    document.querySelectorAll('[data-intake-batch]').forEach(button=>button.onclick=()=>{state.intakeBatch=button.dataset.intakeBatch;state.intakePage=0;renderMain();document.querySelector('#intake-results')?.scrollIntoView?.({block:'start'});});
    document.querySelectorAll('[data-intake-detail]').forEach(button=>button.onclick=()=>{state.intakePage=0;route(state.project,'intake',button.dataset.intakeDetail);});
    document.querySelectorAll('[data-intake-page]').forEach(button=>button.onclick=()=>{state.intakePage=Number(button.dataset.intakePage);renderMain();document.querySelector('#intake-results')?.scrollIntoView?.({block:'start'});});
    document.querySelectorAll('[data-intake-family]').forEach(button=>button.onclick=()=>{state.intakeDataset='all';state.intakeFilter='all';state.intakePage=0;route(button.dataset.intakeProject,'intake',button.dataset.intakeFamily);});
    bindSceneReadinessControls();
    document.querySelectorAll('[data-mouth-look]').forEach(button=>button.onclick=()=>{const id=button.dataset.mouthLook;closedMouthLooks.has(id)?closedMouthLooks.delete(id):closedMouthLooks.add(id);renderMain();});
    document.querySelector('#export-main')?.addEventListener('click',exportFavorites);document.querySelector('#export-review-main')?.addEventListener('click',exportReview);
    if(dialog.open&&intakeViewerSequence)displayed=[...intakeViewerSequence];
  }
  const dialog=document.createElement('dialog');dialog.className='viewer';dialog.setAttribute('aria-label','Media preview');document.body.append(dialog);
  function documentPreview(a){
    const text=String(a.text||'');
    if(a.inert||!/\.(?:txt|md|markdown)$/i.test(a.filename||''))return '<pre>'+esc(text)+'</pre>';
    const inline=value=>esc(value).replace(/`([^`]+)`/g,'<code>$1</code>').replace(/\*\*([^*]+)\*\*/g,'<strong>$1</strong>');
    const lines=text.replace(/\r\n?/g,'\n').split('\n'),parts=[];let paragraph=[],list=[],listType='',listStart=1,code=null;
    const flushParagraph=()=>{if(paragraph.length){parts.push('<p>'+inline(paragraph.join(' '))+'</p>');paragraph=[];}};
    const flushList=()=>{if(list.length){parts.push('<'+listType+(listType==='ol'?' start="'+listStart+'"':'')+'>'+list.map(item=>'<li>'+inline(item)+'</li>').join('')+'</'+listType+'>');list=[];listType='';}};
    for(let i=0;i<lines.length;i++){
      const line=lines[i],trimmed=line.trim();
      if(/^\s*```/.test(line)){flushParagraph();flushList();if(code===null)code=[];else{parts.push('<pre><code>'+esc(code.join('\n'))+'</code></pre>');code=null;}continue;}
      if(code!==null){code.push(line);continue;}
      if(!trimmed){flushParagraph();flushList();continue;}
      const heading=/^(#{1,6})\s+(.+?)\s*#*$/.exec(trimmed),upper=trimmed.length<110&&/[A-Z]{3}/.test(trimmed)&&trimmed===trimmed.toUpperCase()&&!/[{}<>\/\\=]/.test(trimmed);
      if(heading||upper){flushParagraph();flushList();const level=heading?Math.min(heading[1].length+1,6):2;parts.push('<h'+level+'>'+inline(heading?heading[2]:trimmed)+'</h'+level+'>');continue;}
      if(/^(?:-{3,}|\*{3,}|_{3,})$/.test(trimmed)){flushParagraph();flushList();parts.push('<hr>');continue;}
      if(trimmed.includes('|')&&/^\s*\|?\s*:?-{3,}/.test(lines[i+1]||'')){
        flushParagraph();flushList();const cells=value=>value.trim().replace(/^\||\|$/g,'').split('|').map(v=>v.trim()),heads=cells(trimmed),rows=[];i++;
        while(i+1<lines.length&&lines[i+1].includes('|')&&lines[i+1].trim())rows.push(cells(lines[++i]));
        parts.push('<div class="document-table"><table><thead><tr>'+heads.map(v=>'<th>'+inline(v)+'</th>').join('')+'</tr></thead><tbody>'+rows.map(row=>'<tr>'+row.map(v=>'<td>'+inline(v)+'</td>').join('')+'</tr>').join('')+'</tbody></table></div>');continue;
      }
      const bullet=/^(?:[-*+]\s+|([0-9]+)[.)]\s+)(.+)$/.exec(trimmed);
      if(bullet){flushParagraph();const type=bullet[1]?'ol':'ul';if(listType&&listType!==type)flushList();if(!list.length)listStart=Number(bullet[1]||1);listType=type;list.push(bullet[2]);continue;}
      if(list.length&&/^\s+/.test(line)){list[list.length-1]+=' '+trimmed;continue;}
      flushList();paragraph.push(trimmed);
    }
    flushParagraph();flushList();if(code!==null)parts.push('<pre><code>'+esc(code.join('\n'))+'</code></pre>');
    return '<article class="document-reader"><h1>'+esc(a.title)+'</h1>'+parts.join('')+'</article>';
  }
  function openViewer(id){
    const a=browseAsset(id);if(!a)return;id=a.id;currentID=id;const doc=isDoc(a),connections=doc?'':storyConnections(a),i=displayed.indexOf(id);
    const media=a.kind==='video'?`<video controls playsinline preload="metadata" poster="${esc(href(a.thumb))}" src="${esc(href(a.src))}"></video>`:a.kind==='pdf'?`<iframe title="PDF preview" src="${esc(href(a.src))}"></iframe>`:a.kind==='document'?documentPreview(a):`<img src="${esc(href(a.src))}" alt="${esc(a.title)}" id="full-image">`;
    dialog.innerHTML=`<div class="viewer-body"><div class="viewer-head"><span>${doc?'Document preview':`${Math.max(i+1,1)} / ${Math.max(displayed.length,1)} · ${a.kind==='video'?'Video':'Image'} preview`}</span><div class="view-nav">${!doc?`<button id="previous" aria-label="Previous image" ${i<=0?'disabled':''}>←</button><button id="next" aria-label="Next image" ${i<0||i>=displayed.length-1?'disabled':''}>→</button>`:''}${['image','gif'].includes(a.kind)?'<button id="zoom" aria-label="Toggle full-size zoom">Zoom</button>':''}<button id="close-viewer" aria-label="Close preview">✕</button></div></div><div class="stage">${media}</div><aside class="viewer-info"><p class="label">${esc(cats[a.category]||'Document')}</p><h2>${esc(a.title)}</h2><p class="filename">${esc(a.filename)}</p><div class="viewer-quick-actions">${!doc?`<button class="action" id="viewer-favorite">${favorites.has(id)?'★ Favorited':'☆ Add to favorites'}</button>`:''}<button class="action export-basket-action ${basket.has(id)?'on':''}" id="viewer-basket" data-basket="${esc(id)}" aria-pressed="${basket.has(id)}">${basket.has(id)?'⇩ In export basket':'⇩ Add to export basket'}</button></div>${reviewControls(a)}${a.lyric?`<p class="label">Lyric connection</p><p>${esc(a.lyric)}</p>`:''}${a.beat?`<p>${esc(a.beat)}</p>`:''}${a.motion?`<p class="label">Motion idea</p><p>${esc(a.motion)}</p>`:''}${a.inert?'<p>Preserved helper script. This viewer only displays its text.</p>':''}${writerConnections(a)}${!doc?connections+referenceControls(a)+workflowStageControls(a):''}${intakeAssetEvidence(a)}${shotPlanControls(a)}${!doc?collaboratorControls(a):''}<a class="small-link" href="${esc(href(a.src))}" target="_blank" rel="noopener" ${a.inert?'download':''}>Open original file ↗</a><details><summary>File details</summary><p>${esc(a.repoPath)}</p>${a.sha256?`<p>SHA-256<br>${esc(a.sha256)}</p>`:''}<p>${esc(typeof a.sourceStatus==='string'?a.sourceStatus:'Source record retained')}</p></details></aside></div>`;
    document.querySelector('#close-viewer').onclick=()=>dialog.close();
    document.querySelector('#previous')?.addEventListener('click',()=>openViewer(displayed[i-1]));
    document.querySelector('#next')?.addEventListener('click',()=>openViewer(displayed[i+1]));
    document.querySelector('#zoom')?.addEventListener('click',()=>document.querySelector('#full-image').classList.toggle('zoomed'));
    document.querySelector('#viewer-favorite')?.addEventListener('click',e=>{toggleFavorite(id);e.target.textContent=favorites.has(id)?'★ Favorited':'☆ Add to favorites';});
    document.querySelector('#viewer-basket').onclick=()=>toggleBasket(id);
    document.querySelector('#viewer-archive').onclick=()=>toggleArchive(id);
    document.querySelectorAll('[data-review-status]').forEach(button=>button.onclick=()=>updateReview(id,{status:button.dataset.reviewStatus||null}));
    document.querySelector('#review-note').oninput=e=>updateReview(id,{note:e.target.value});
    bindNotePresets(id);
    document.querySelector('#viewer-save-review').onclick=chooseReviewFile;document.querySelector('#viewer-export-review').onclick=exportReview;
    dialog.querySelectorAll('[data-open]').forEach(button=>button.onclick=()=>openViewer(button.dataset.open));
    dialog.querySelectorAll('[data-story-shot]').forEach(button=>button.onclick=()=>{dialog.close();const shot=storyWorkItems(button.dataset.storyProject).find(s=>s.id===button.dataset.storyShot),story=shot?.independentSequenceID&&storyboardStories(button.dataset.storyProject).find(s=>s.sequenceID===shot.independentSequenceID);route(button.dataset.storyProject,'storyboard',story?'story:'+story.id:'');if(!story){state.storyLayout='progress';renderMain();}document.getElementById(story?'story-shot-'+(shot.storyShotID||shot.id):'shot-work-'+button.dataset.storyShot)?.scrollIntoView({block:'center'});});
    dialog.querySelectorAll('[data-intake-family]').forEach(button=>button.onclick=()=>{dialog.close();state.intakeDataset='all';state.intakeFilter='all';state.intakePage=0;route(button.dataset.intakeProject,'intake',button.dataset.intakeFamily);});
    bindShotPlanControls(id);bindReferenceControls(id);bindSceneReadinessControls();bindValidationControls(a);
    document.querySelector('#reference-storyboard-stage')?.addEventListener('change',e=>{updateReview(id,{storyboardStage:Object.hasOwn(storyboardStages,e.target.value)?e.target.value:null});const label=document.querySelector('#reference-stage-status');if(label)label.textContent='Current stage: '+(storyboardStages[storyboardStage(byID.get(id))]||'not assigned')+'. This applies to this image and its role; separate character components keep their locks.';});
    document.querySelectorAll('[data-creative-review-recipient]').forEach(button=>button.onclick=()=>{
      const request=normalizedCreativeReview(reviewRecord(id).creativeReview),recipient=button.dataset.creativeReviewRecipient,targets=request?.recipients||[];
      updateReview(id,{creativeReview:normalizedCreativeReview({...request,recipients:targets.includes(recipient)?targets.filter(d=>d!==recipient):[...targets,recipient]})});
    });
    document.querySelector('#viewer-export-creative-review')?.addEventListener('click',()=>exportCreativeReviewRequests(id));
    if(!dialog.open)dialog.showModal();
  }
  dialog.addEventListener('close',()=>{intakeViewerSequence=null;dialog.querySelector('video')?.pause();dialog.innerHTML='';currentID='';renderMain();});
  dialog.addEventListener('click',e=>{const evidence=e.target.closest('[data-intake-evidence]');if(evidence){openIntakeEvidence(evidence.dataset.intakeEvidence,evidence);return;}if(e.target===dialog)dialog.close();});
  document.addEventListener('keydown',e=>{if(!dialog.open||intakeEvidenceDialog?.open||e.target.closest('input,textarea,select,[contenteditable="true"]'))return;const i=displayed.indexOf(currentID);if(e.key==='ArrowRight'&&i>=0&&i<displayed.length-1){e.preventDefault();openViewer(displayed[i+1]);}if(e.key==='ArrowLeft'&&i>0){e.preventDefault();openViewer(displayed[i-1]);}});
  function collaboratorControls(a){
    const targets=normalizedCreativeReview(reviewRecord(a.id).creativeReview)?.recipients||[],names=creativeReviewRecipients.filter(([id])=>targets.includes(id)).map(([,name])=>name);
    return `<section class="quick-collaborators creative-review" aria-label="Request creative review"><h3>Creative review</h3><p>Find a story use · music video or stories between videos</p><div class="quick-collaborator-buttons creative-review-buttons">${creativeReviewRecipients.map(([id,name])=>`<button id="creative-review-${id}" data-creative-review-recipient="${id}" aria-pressed="${targets.includes(id)}" class="${targets.includes(id)?'selected':''}">${name}</button>`).join('')}</div><p id="quick-collaborator-status" role="status">${esc(names.length?'Review queued for '+names.join(', ')+' · not sent':'Choose the person who should review this image.')}</p><button class="pill" id="viewer-export-creative-review" ${targets.length?'':'disabled'}>Export review request</button><p>Save your review file or export this request for Nova to relay. No shot is planned and no one is notified automatically.</p></section>`;
  }
  function refreshCollaboratorUI(){
    const targets=normalizedCreativeReview(reviewRecord(currentID).creativeReview)?.recipients||[],names=creativeReviewRecipients.filter(([id])=>targets.includes(id)).map(([,name])=>name);
    document.querySelectorAll('[data-creative-review-recipient]').forEach(button=>{const on=targets.includes(button.dataset.creativeReviewRecipient);button.classList.toggle('selected',on);button.setAttribute('aria-pressed',String(on));});
    const status=document.querySelector('#quick-collaborator-status');if(status)status.textContent=names.length?'Review queued for '+names.join(', ')+' · not sent':'Choose the person who should review this image.';
    const exportButton=document.querySelector('#viewer-export-creative-review');if(exportButton)exportButton.disabled=!targets.length;
  }
  function assistantLikenessProposal(a){
    const p=assistantLikenessAssessments.get(a.id);if(!p)return '';
    return `<details class="detail-drawer assistant-likeness-proposal"><summary>Nova’s proposal: ${p.likenessRating===null?'Not assessable':p.likenessRating+'/5'}</summary><p class="review-help">Proposal only. Your rating above remains the decision used for reference selection. Scope: ${esc(String(p.scope||'').replace(/_/g,' '))} · Confidence: ${esc(p.confidence)} · Assessed: ${esc(p.assessedAtUTC)}.</p><p>${esc(p.summary)}</p>${Array.isArray(p.observations)&&p.observations.length?`<ul>${p.observations.map(o=>`<li><b>${esc(o.feature)}:</b> ${esc(o.finding)} <small>(${esc(o.visibility)}; ${esc(o.severity)})</small></li>`).join('')}</ul>`:''}<p class="review-help">Compared with: ${p.referenceAssets.map(r=>esc(byID.get(r.assetID).title)).join('; ')}. Hidden or obscured features cannot be verified from this image.</p></details>`;
  }
  function workflowStageControls(a){const r=reviewRecord(a.id),stage=storyboardStage(a),rating=normalizedRating(r.likenessRating),sceneRating=normalizedRating(r.sceneQualityRating);return `<section class="workflow-stage-controls"><h3>Design stage</h3><label for="reference-storyboard-stage">Stage for this image</label><select id="reference-storyboard-stage"><option value="">Use source stage</option>${Object.entries(storyboardStages).map(([id,label])=>`<option value="${id}" ${stage===id?'selected':''}>${label}</option>`).join('')}</select><label for="reference-likeness-rating">Character / component likeness</label><select id="reference-likeness-rating"><option value="" ${rating===null?'selected':''}>Unrated</option>${[1,2,3,4,5].map(n=>`<option value="${n}" ${rating===n?'selected':''}>${n}/5 ${'★'.repeat(n)}</option>`).join('')}</select>${validationPanel(a,'character')}${assistantLikenessProposal(a)}<p class="review-help">Judge the character or scoped component against its gold standard. Keep framing, lighting and scene appeal out of this score. Hidden features remain unassessed; a rating does not change the character or approve production.</p><label for="reference-scene-quality-rating">Scene craft</label><select id="reference-scene-quality-rating"><option value="" ${sceneRating===null?'selected':''}>Unrated</option>${[1,2,3,4,5].map(n=>`<option value="${n}" ${sceneRating===n?'selected':''}>${n}/5 ${'★'.repeat(n)}</option>`).join('')}</select>${validationPanel(a,'scene')}<p class="review-help">Rate framing, lighting, staging and atmosphere. A strong scene can still need a character repair. Preserve its strengths in your note; this score does not replace the separate scene-readiness review or approve production.</p><p id="reference-stage-status" class="review-help">Current stage: ${esc(storyboardStages[stage]||'not assigned')}. Production approves this image for its role. A scene or prop can need a fix while separately locked character parts remain usable.</p></section>`;}
  function referenceControls(a){const r=reviewRecord(a.id);return `<section class="reference-controls" aria-label="Reference lane and role"><h3>Reference role</h3><label for="reference-variant">Creative lane</label><select id="reference-variant"><option value="prime" ${r.variant!=='multiverse'?'selected':''}>Prime / current direction</option><option value="multiverse" ${r.variant==='multiverse'?'selected':''}>Multiverse idea</option></select><p class="review-help">Prime can include a selected close variation. It keeps the same canonical face and mouth; Multiverse is a separate creative idea.</p><div id="multiverse-selection-control" ${r.variant==='multiverse'?'':'hidden'}><label for="reference-multiverse-selection">Multiverse selection</label><select id="reference-multiverse-selection"><option value="candidate" ${r.multiverseSelection!=='approved'?'selected':''}>Candidate</option><option value="approved" ${r.multiverseSelection==='approved'?'selected':''} ${normalizedRating(r.likenessRating)>=2?'':'disabled'}>Approved Multiverse selection</option></select><p id="multiverse-selection-help" class="review-help" role="status"></p></div><label for="working-reference-scope">Use this reference for</label><select id="working-reference-scope">${Object.entries(workingScopes).map(([id,label])=>`<option value="${id}" ${selectedWorkingScope(r)===id?'selected':''}>${label}</option>`).join('')}</select><p id="working-reference-status" class="review-help" role="status"></p></section>`;}
  function refreshReferenceUI(){
    const a=byID.get(currentID);if(!a)return;const r=reviewRecord(currentID),scope=selectedWorkingScope(r),select=document.querySelector('#working-reference-scope');if(select)select.value=scope;
    const multiverseControl=document.querySelector('#multiverse-selection-control'),multiverseSelect=document.querySelector('#reference-multiverse-selection'),multiverseHelp=document.querySelector('#multiverse-selection-help');
    if(multiverseControl)multiverseControl.hidden=r.variant!=='multiverse';if(multiverseSelect){multiverseSelect.value=r.multiverseSelection==='approved'?'approved':'candidate';const option=multiverseSelect.querySelector('option[value="approved"]');if(option)option.disabled=!(normalizedRating(r.likenessRating)>=2);}
    if(multiverseHelp)multiverseHelp.textContent=normalizedRating(r.likenessRating)>=2?'Choose explicitly whether this alternative belongs in Approved Multiverse. Ratings alone never select it; this does not approve production.':r.multiverseSelection==='approved'?'Your saved selection is retained, but it is outside Approved Multiverse until character/component likeness is at least 2/5.':'A likeness rating of at least 2/5 is required before selecting Approved Multiverse.';
    const role=effectiveReferenceRole(a).replace(/_/g,' '),selection=isWorkingScope(r.workingReferenceScope)?'Selected use: '+workingScopes[scope]+'. ':'';
    const status=document.querySelector('#working-reference-status');if(status)status.textContent=selection+(r.status==='remove'||isArchived(a)?'Marked for removal from ordinary browsing. Original and history are retained.':r.variant==='multiverse'?'Multiverse idea; separate from Prime character parts.':'Recorded role: '+role+'. Production adds approved use for this image; an existing component lock keeps its narrower scope.')+(r.workingReference?.status==='requested'?' Earlier request retained for the review history.':'');
  }
  function bindReferenceControls(id){
    document.querySelector('#reference-variant')?.addEventListener('change',e=>updateReview(id,{variant:e.target.value==='multiverse'?'multiverse':'prime',variantSource:'user',...(e.target.value==='multiverse'?{workingReference:null}:{})}));
    document.querySelector('#reference-multiverse-selection')?.addEventListener('change',e=>{const choice=e.target.value,r=reviewRecord(id);if(r.variant==='multiverse'&&(choice==='candidate'||choice==='approved'&&normalizedRating(r.likenessRating)>=2))updateReview(id,{multiverseSelection:choice});else refreshReferenceUI();});
    document.querySelector('#working-reference-scope')?.addEventListener('change',e=>{if(isWorkingScope(e.target.value))updateReview(id,{workingReferenceScope:e.target.value});});
    document.querySelector('#reference-likeness-rating')?.addEventListener('change',e=>{const raw=e.target.value,value=raw===''?null:Number(raw);if(raw===''||normalizedRating(value)!==null)updateReview(id,{likenessRating:value});});
    document.querySelector('#reference-scene-quality-rating')?.addEventListener('change',e=>{const raw=e.target.value,value=raw===''?null:Number(raw);if(raw===''||normalizedRating(value)!==null)updateReview(id,{sceneQualityRating:value});});
    refreshReferenceUI();
  }
  async function prepareReviewSweep(){
    const data=reviewPayload();downloadJSON({...data,reviewSweep:{status:'prepared; waiting for Nova',requestedAt:new Date().toISOString(),pendingWorkingReferences:data.items.filter(i=>i.workingReference?.status==='requested').map(i=>({id:i.id,sha256:i.sha256,scope:i.workingReference.scope}))}},'cfa-review-sweep.json');
    const saved=reviewFileHandle?await writeReviewFile():false;const status=document.querySelector('#review-sweep-status');if(status)status.textContent=(saved?'Chosen review file saved. ':'')+'Review sweep exported. Give it to Nova and ask her to review the queued changes. No files were deleted and no task was started.';
  }
  function shotPlanControls(a){
    const plan=reviewRecord(a.id).shotPlan, values=plan||normalizedPlan({});
    return `<section class="shot-plan-controls" aria-label="Shot planning"><label class="plan-toggle"><input type="checkbox" id="shot-plan-enabled" ${plan?'checked':''}> Plan a shot</label><p class="review-help">A creative plan is separate from your keep/fix/removal decision. Nothing is sent or generated here.</p><div id="shot-plan-fields" ${plan?'':'hidden'}><fieldset><legend>Where might this shot go?</legend>${destinations.map(d=>`<label><input type="checkbox" data-shot-destination="${d}" ${values.destinations.includes(d)?'checked':''}> ${esc(destinationLabel(d))}</label>`).join('')}</fieldset><label for="shot-scene-binding">Scene for this plan (optional)</label><select id="shot-scene-binding"><option value="">Unbound draft / planning only</option>${storyWorkItems(a.project).map(shot=>`<option value="${esc(shot.id)}" ${values.sceneIDs?.includes(shot.id)?'selected':''}>${esc(shot.title)} · ${esc(shot.sectionLabel||shot.id)}</option>`).join('')}</select><label for="shot-idea">Shot idea</label><textarea id="shot-idea" rows="3" maxlength="20000" placeholder="The moment, action, or feeling to explore…">${esc(values.idea)}</textarea><label for="shot-prompt">Draft prompt (optional)</label><textarea id="shot-prompt" rows="5" maxlength="30000" placeholder="What the collaborator should create or preserve…">${esc(values.prompt)}</textarea><p class="review-help">Status: planned. Export a provider handoff from Shot plans when you are ready.</p></div></section>`;
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
      const plan=reviewRecord(a.id).shotPlan,sceneReadiness=(plan.sceneIDs||[]).map(id=>sceneReviewRecord(a.project,id)).filter(Boolean).map(record=>({...record,...sceneHandoffGate(record),technicalValidation:validationTechnicalGate(record)}));
      return {...exportReference(a),title:a.title,reviewStatus:reviewRecord(a.id).status,note:reviewRecord(a.id).note,shotPlan:plan,sceneReadiness,handoffPurpose:sceneReadiness.length&&sceneReadiness.every(r=>r.productionEligible&&r.technicalValidation?.technicalReady)?'production_target':'planning_or_repair'};
    });
    const records=new Map([...sceneReviews.values()].filter(r=>scope==='all'||r.project===scope).map(r=>[r.project+':'+r.shotID,r]));for(const item of items)for(const r of item.sceneReadiness)records.set(r.project+':'+r.shotID,r);
    const scenes=[...records.values()].map(record=>({...record,title:(C.shotMaterials?.shots||[]).find(s=>s.project===record.project&&s.id===record.shotID)?.title||record.shotID,...sceneHandoffGate(record),technicalValidation:validationTechnicalGate(record)}));
    return {format:'cfa-shot-handoff-v1',exported:new Date().toISOString(),project:scope,destination:state.destination,exportIntent:state.exportIntent,status:'planned; not sent or generated',referencePolicy:{path:referencePolicyPath,instruction:referencePolicyText},sceneReadinessReminder:'A production target needs the human B-or-better gate and current passes for every declared, bound validation scope. Final result acceptance is separate; missing declarations, blocked and unbound plans remain planning or repair handoffs.',attachmentReminder:'Attach the actual images or clips identified below. This handoff contains references and text only; no media files are bundled.',scenes,items};
  }
  function exportShotHandoff(format,scope=state.project){
    const data=shotHandoffPayload(scope),filename='cfa-shot-handoff-'+scope+'-'+state.destination+'.'+format;
    if(format==='json')downloadJSON(data,filename);
    else {
      const text=['CFA SHOT HANDOFF',`Project: ${data.project} | Destination: ${destinationLabel(state.destination)}`,`Export intent: ${data.exportIntent==='prime'?'Prime references':'Multiverse creative ingredients'}`,data.status,data.attachmentReminder,`Reference policy: ${data.referencePolicy.path}`,data.referencePolicy.instruction,data.sceneReadinessReminder,'',...data.scenes.flatMap(r=>[`Scene: ${r.title} (${r.shotID})`,`Whole scene grade: ${r.grade||'Ungraded'} | ${r.productionEligible?'B target met':'Planning / repair'}`,`Blockers: ${r.criticalBlockers.join('; ')||'(none recorded)'}`,`Readiness: ${r.reasons.join('; ')||'Required ingredients reviewed ready'}`,`Technical validation: ${r.technicalValidation?.technicalReady?'Ready for declared use':'Unresolved'} | ${(r.technicalValidation?.reasons||[]).join('; ')||'All declared scopes currently pass'}`,`Scene note: ${r.note||'(none)'}`,`Shoot plan: ${r.shootPlan.reviewStatus} | Reviewed by: ${r.shootPlan.reviewedBy||'(none)'} | ${r.shootPlan.reviewedAt||'no verification time'}`,`Direction: ${r.shootPlan.direction||'(missing)'}`,`Camera: ${r.shootPlan.camera||'(missing)'}`,`Lighting: ${r.shootPlan.lighting||'(missing)'}`,`Shoot plan review note: ${r.shootPlan.note||'(none)'}`,...r.ingredients.map(i=>`${i.required?'Required':'Optional'}: ${i.label} | ${i.status} | ${i.assetID||'no file'} | ${i.sha256||'no hash'} | ${i.note||'no evidence note'}`),'']),...data.items.flatMap((a,i)=>[
        `${i+1}. ${a.title}`,`Reference ID: ${a.id}`,`SHA-256: ${a.sha256||'not recorded'}`,`File: ${a.filename}`,`Source path: ${a.path||'see source catalog'}`,
        `Destinations: ${a.shotPlan.destinations.map(destinationLabel).join(', ')}`,`Lane: ${a.variant}`,`Reference role: ${a.referenceRole}`,`Likeness to gold standard: ${a.likenessRating===null?'Unrated':a.likenessRating+'/5'}`,`Scene craft: ${a.sceneQualityRating===null?'Unrated':a.sceneQualityRating+'/5'} (framing, lighting and staging; separate from likeness and production readiness)`,`Character validation: ${a.validationEvidence.character.label} | Scene validation: ${a.validationEvidence.scene.label}`,`Review: ${a.reviewStatus||'unreviewed'}`,`Review note / known differences: ${a.knownDifferences||'(none)'}`,`Scene use: ${a.referenceUsePolicy.explicitSceneReference?.instruction||a.referenceUsePolicy.defaultReferenceSelection.instruction}`,
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
    if(data.format===VALIDATION_KEY){importValidation(data);return;}
    if(data.validationEvidence){if(validationStorageError)throw Error('Resolve the unread evidence backup before importing a review with validation evidence.');checkValidationEnvelope(data.validationEvidence);}
    if(data.format===EXPORT_KEY&&Array.isArray(data.items)){const result=importBasket(data.items);saveBasket();render();notice(`${result.added} matching references added to the export basket; ${result.skipped} unmatched entries skipped.`);return;}
    let records=[],starItems=[];
    if(data.format===REVIEW_KEY){records=data.items||data.reviewDecisions||data.decisions;starItems=data.favorites||[];if(!Array.isArray(records)||!Array.isArray(starItems))throw Error('The review file has invalid lists.');}
    else if(data.format==='cfa-visual-favorites-v1'&&Array.isArray(data.items))starItems=data.items;
    else throw Error('Choose an exported CFA review, favorites, or selection-list file.');
    let imported=0,stars=0,skipped=0;
    archiveLegacy(records);if(data.validationEvidence)mergeValidation(data.validationEvidence);
    for(const item of records){const record=normalizedReview(item);if(record){mergeReview(record);imported++;}else skipped++;}
    for(const item of starItems){const a=matchingAsset(typeof item==='string'?{id:item}:item,{requireHash:data.format===REVIEW_KEY,allowAliasID:true});if(a){favorites.add(a.id);stars++;}else skipped++;}
    if(data.format==='cfa-visual-favorites-v1'&&data.notes&&typeof data.notes==='object'){
      for(const [id,note] of Object.entries(data.notes)){if(typeof note!=='string')continue;const a=matchingAsset({id,sha256:data.note_refs?.[id]});if(a){const record=normalizedReview({id,sha256:data.note_refs?.[id]||a.sha256,note,updatedAt:data.exported||null});if(record){archiveLegacy([{id,sha256:data.note_refs?.[id]||a.sha256,note,updatedAt:data.exported||null}]);mergeReview(record);imported++;}}}
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
