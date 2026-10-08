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
  let state = {...initial, view:location.hash?initial.view:'mission_control', album:'', search:'', destination:'all', videoSort:'longest', videoLayout:'grouped', collaborator:'ComfyUI',exportIntent:'prime',detailLayout:'profiles',detailProfile:'',storyTheme:'all',storyStage:'all',storyStart:0,storyEnd:100}, currentID = '', displayed = [], toastTimer;
  const REVIEW_KEY = 'cfa-visual-review-v1', EXPORT_KEY = 'cfa-visual-export-v1';
  const statusLabels = {keep:'Keep', needs_fixes:'Needs fixes', remove:'Marked for removal'};
  const workingScopes={complete_look:'Complete look',identity:'Identity',outfit:'Outfit',scene:'Scene',detail:'Detail only'};
  const storyboardStages={preliminary:'Preliminary',detailed_design:'Detailed design',verification:'Verification',production:'Production'};
  let favorites = new Set(), basket = new Set(), storageOK = true, reviews = new Map();
  let reviewFileHandle = null, fileSaveTimer, fileWriteChain = Promise.resolve();
  let reviewRevision = 0, fileSavedRevision = 0, fileWriting = false;
  let fileMessage = 'Browser backup only · export or choose a review file to share.';
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
    return {status:'planned',destinations:targets,idea:typeof plan.idea==='string'?plan.idea.slice(0,20000):'',prompt:typeof plan.prompt==='string'?plan.prompt.slice(0,30000):''};
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
    if(Object.hasOwn(item,'storyboardStage'))record.storyboardStage=Object.hasOwn(storyboardStages,item.storyboardStage)?item.storyboardStage:null;
    return record;
  }
  function normalizedWorkingReference(value){return value&&['requested','approved'].includes(value.status)&&Object.hasOwn(workingScopes,value.scope)?{status:value.status,scope:value.scope}:null;}
  function mergeReview(record){const merged={status:null,note:'',shotPlan:null,...reviews.get(record.id),...record};if(merged.variant==='multiverse')merged.workingReference=null;reviews.set(record.id,merged);}
  for (const item of C.reviewDecisions || []) {
    const record = normalizedReview(item,'catalog'); if(record)mergeReview(record);
  }
  try {
    const saved = JSON.parse(localStorage.getItem(REVIEW_KEY) || 'null');
    if(saved?.format===REVIEW_KEY && Array.isArray(saved.items)) {
      for(const item of saved.items){const record=normalizedReview(item,'browser');if(record)mergeReview(record);}
    }
  } catch {storageOK=false;}

  try { const saved=JSON.parse(localStorage.getItem('cfa-visual-favorites-v1') || '[]'); if(Array.isArray(saved))favorites=new Set(saved.filter(id=>byID.has(id))); } catch {storageOK=false;}
  try{const saved=JSON.parse(localStorage.getItem(EXPORT_KEY)||'null');if(saved?.format===EXPORT_KEY&&Array.isArray(saved.items)){for(const item of saved.items){const a=matchingAsset(item);if(a&&(!a.sha256||item.sha256===a.sha256))basket.add(a.id);}}}catch{storageOK=false;}
  const iconStar = id => favorites.has(id) ? '★' : '☆';
  function notice(message) {let t=document.querySelector('.toast');if(!t){t=document.createElement('div');t.className='toast';t.setAttribute('role','status');document.body.append(t);}t.textContent=message;clearTimeout(toastTimer);toastTimer=setTimeout(()=>t.remove(),3500);}
  function assetReference(a){return {id:a.id,project:a.project,filename:a.filename,path:a.repoPath,sha256:a.sha256||null,role:a.category};}
  function exportAllowed(a){const r=reviewRecord(a.id);return !a.archived&&r.status!=='remove'&&(state.exportIntent==='multiverse_ingredients'||r.variant!=='multiverse');}
  function exportReference(a){const r=reviewRecord(a.id);return {...assetReference(a),variant:r.variant||'prime',workingReference:r.workingReference||null,storyboardStage:storyboardStage(a)};}
  function exportIntentControls(){return `<label class="export-intent">Export intent<select data-export-intent><option value="prime" ${state.exportIntent==='prime'?'selected':''}>Prime references</option><option value="multiverse_ingredients" ${state.exportIntent==='multiverse_ingredients'?'selected':''}>Multiverse creative ingredients</option></select></label><p class="export-intent-help">${state.exportIntent==='prime'?'Multiverse ideas and removal requests stay out of exports.':'Multiverse ideas may be included as creative ingredients; removal requests still stay out.'} Review backups keep everything.</p>`;}
  function reviewPayload(){return {format:REVIEW_KEY,exported:new Date().toISOString(),
    status:'review decisions and notes; removal is a queue, not a file deletion',
    items:[...reviews.values()].map(record=>({...assetReference(byID.get(record.id)),...record})),
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
      fileStatus('This browser needs Export review. Choose docs/notes/cfa-review.json when saving the download.');
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
    reviewRevision++;saveBrowserReview();refreshReviewUI();scheduleFileSave();
  }
  function reviewControls(a){const record=reviewRecord(a.id);return `<section class="review-controls" aria-label="Review this reference"><h3>Your review</h3><p id="review-current-status" class="review-current">${esc(statusLabels[record.status]||'No triage decision')}</p><div class="review-actions">${[['keep','Keep'],['needs_fixes','Needs fixes'],['remove','Mark for removal'],['','Clear decision']].map(([value,label])=>`<button data-review-status="${value}" class="${record.status===(value||null)?'selected':''}" aria-pressed="${record.status===(value||null)}">${label}</button>`).join('')}</div><label for="review-note">Your note</label><textarea id="review-note" rows="4" maxlength="20000" placeholder="What should stay, change, or be removed from the working collection?">${esc(record.note)}</textarea><p class="review-help">Marking for removal queues a sorting request. It never deletes the source file. Clear removes the decision and keeps your note.</p><p class="review-file-status" data-review-file-status role="status">${esc(fileMessage)}</p><button class="small-link" id="viewer-save-review">Save review file</button><button class="small-link" id="viewer-export-review">Export review</button></section>`;}

  function toggleFavorite(id){favorites.has(id)?favorites.delete(id):favorites.add(id);saveFavorites();document.querySelectorAll('[data-favorite]').forEach(b=>{const on=favorites.has(b.dataset.favorite);b.classList.toggle('on',on);b.textContent=iconStar(b.dataset.favorite);b.setAttribute('aria-pressed',String(on));b.setAttribute('aria-label',(on?'Remove favorite: ':'Favorite: ')+byID.get(b.dataset.favorite).title);});const count=document.querySelector('[data-view="favorites"] .count');if(count)count.textContent=projectAssets().filter(a=>favorites.has(a.id)).length;if(state.view==='favorites'&&!currentID)renderMain();}
  function basketPayload(backup=false){const selected=[...basket].map(id=>byID.get(id)).filter(Boolean),items=backup?selected:selected.filter(exportAllowed);return {format:EXPORT_KEY,exported:new Date().toISOString(),status:backup?'browser selection backup; not an export handoff':'selected references; no approval implied',exportIntent:backup?'review_backup':state.exportIntent,excludedCount:selected.length-items.length,referenceReminder:'This is a selection list. The actual images, clips, and documents are not bundled.',items:items.map(exportReference)};}
  function saveBasket(){reviewRevision++;saveBrowserReview();scheduleFileSave();document.querySelectorAll('[data-view="export_basket"] .count').forEach(e=>e.textContent=basketAssets().length);document.querySelectorAll('[data-basket]').forEach(button=>{const on=basket.has(button.dataset.basket);button.classList.toggle('on',on);button.textContent=button.id==='viewer-basket'?(on?'⇩ In export basket':'⇩ Add to export basket'):(on?'✓':'⇩');button.setAttribute('aria-pressed',String(on));button.setAttribute('aria-label',(on?'Remove from export basket: ':'Add to export basket: ')+byID.get(button.dataset.basket).title);});if(state.view==='export_basket'&&!currentID)renderMain();}
  function toggleBasket(id){if(!byID.has(id))return;basket.has(id)?basket.delete(id):basket.add(id);saveBasket();}
  function exportBasket(){const data=basketPayload();downloadJSON(data,'cfa-export-selection.json');notice(data.items.length+' references exported; '+data.excludedCount+' excluded by export intent. Media files are not bundled.');}
  function importBasket(items){let added=0,skipped=0;for(const item of items){const a=matchingAsset(item);if(a&&(!a.sha256||item.sha256===a.sha256)){basket.add(a.id);added++;}else skipped++;}return {added,skipped};}
  function queryMatch(a){const text=[a.title,a.filename,a.album,isDoc(a)?a.text:'',a.note,a.beat,a.lyric,reviewRecord(a.id).note,...(a.tags||[])].join(' ').toLowerCase();return text.includes(state.search.toLowerCase().trim());}
  function projectAssets(includeArchived=false){return C.assets.filter(a=>a.project===state.project&&(includeArchived||!a.archived));}
  const basketAssets=()=>C.assets.filter(a=>basket.has(a.id)&&!a.archived);
  function libraryLocation(){return ['mission_control','collaborators'].includes(state.view)?null:{project:state.project,view:state.view,album:state.album};}
  function rememberLibrary(){const previous=libraryLocation();if(previous){state.lastLibrary=previous;try{sessionStorage.setItem('cfa-last-library',JSON.stringify(previous));}catch{}}}
  function libraryReturn(){let saved=state.lastLibrary;try{saved=saved||JSON.parse(sessionStorage.getItem('cfa-last-library')||'null');}catch{}return saved&&C.projects.some(p=>p.id===saved.project)&&!['mission_control','collaborators'].includes(saved.view)?saved:{project:'hon',view:'all',album:''};}
  function route(project,view='all',album=''){rememberLibrary();state={...state,project,view,album,search:''};location.hash=[project,view,album].filter(Boolean).map(encodeURIComponent).join('/');render();window.scrollTo({top:0,behavior:'instant'});}
  function parseHash(){const [p,v,a]=location.hash.slice(1).split('/').map(decodeURIComponent);if(C.projects.some(x=>x.id===p)){state.project=p;state.view=['mission_control','collaborators','all','favorites','export_basket','review_queue','shot_plans','documents',...Object.keys(cats)].includes(v)?v:'all';state.album=a||'';}}
  function render(){
    const p=C.projects.find(p=>p.id===state.project);const all=projectAssets();
    document.title=p.name+' · Visual library';
    document.querySelector('#app').innerHTML=`<div class="shell"><aside class="sidebar"><p class="brand">CFA / VISUAL LIBRARY</p><div class="project-picker">${C.projects.map(x=>`<button data-project="${x.id}" class="${state.project===x.id?'active':''}">${esc(x.name)}<small>${esc(x.subtitle)}</small></button>`).join('')}</div><nav class="nav" aria-label="Studio navigation"><button data-view="mission_control" class="${state.view==='mission_control'?'active':''}">Ziggy’s Corner</button><button data-view="collaborators" class="${state.view==='collaborators'?'active':''}">Collaborators</button><button data-view="all" class="${state.view==='all'?'active':''}">All files <span class="count">${all.filter(a=>!isDoc(a)).length} visuals</span></button>${C.categories.map(([id,name])=>{const albums=C.albums.filter(x=>x.project===state.project&&x.category===id);const count=new Set(albums.flatMap(x=>x.assetIDs).filter(id=>byID.has(id)&&!byID.get(id).archived)).size;return count?`<button data-view="${id}" class="${state.view===id?'active':''}">${esc(name)}<span class="count">${count}</span></button>`:'';}).join('')}<button data-view="favorites" class="${state.view==='favorites'?'active':''}">☆ Favorites <span class="count">${all.filter(a=>favorites.has(a.id)).length}</span></button><button data-view="export_basket" class="${state.view==='export_basket'?'active':''}">⇩ Export basket <span class="count">${basketAssets().length}</span></button><button data-view="review_queue" class="${state.view==='review_queue'?'active':''}">Review queue <span class="count">${projectAssets(true).filter(inReviewQueue).length}</span></button><button data-view="shot_plans" class="${state.view==='shot_plans'?'active':''}">Shot plans <span class="count">${all.filter(a=>reviewRecord(a.id).shotPlan).length}</span></button><button data-view="documents" class="${state.view==='documents'?'active':''}">Documents <span class="count">${all.filter(isDoc).length}</span></button></nav><div class="sidebar-foot">${exportIntentControls()}<button id="save-review">Save review file</button><button id="export-review">↓ Export review & notes</button><button id="import">↑ Import review or selections</button><button id="export">↓ Export favorites only</button><p class="review-storage-hint">Choose the repo’s docs/notes/cfa-review.json to share decisions with Nova. Browser backup is local to this browser; other devices do not sync automatically.</p><p class="review-file-status" data-review-file-status role="status">${esc(fileMessage)}</p><p class="build-stamp">Build ${esc(window.REVIEW_BUILD||'local preview')}</p></div></aside><div class="workspace"><div class="topbar"><span class="breadcrumb">${esc(p.name)} / ${esc(cats[state.view]||({'mission_control':'Mission Control','collaborators':'Collaborators','all':'All files','favorites':'Favorites','export_basket':'Export basket','review_queue':'Review queue','shot_plans':'Shot plans','documents':'Documents'}[state.view]))}</span><input class="search" id="search" type="search" placeholder="Search looks, scenes, details…" aria-label="Search library" value="${esc(state.search)}"></div><main class="main" id="main"></main></div></div>`;
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
  function card(a){if(!displayed.includes(a.id))displayed.push(a.id);return `<article class="media-card" data-review-card="${esc(a.id)}">${reviewRecord(a.id).status?`<span class="review-chip ${reviewRecord(a.id).status}">${esc(statusLabels[reviewRecord(a.id).status])}</span>`:''}<button class="favorite ${favorites.has(a.id)?'on':''}" data-favorite="${esc(a.id)}" aria-label="${favorites.has(a.id)?'Remove favorite: ':'Favorite: '}${esc(a.title)}" aria-pressed="${favorites.has(a.id)}">${iconStar(a.id)}</button><button class="basket-toggle ${basket.has(a.id)?'on':''}" data-basket="${esc(a.id)}" title="Export basket" aria-label="${basket.has(a.id)?'Remove from export basket: ':'Add to export basket: '}${esc(a.title)}" aria-pressed="${basket.has(a.id)}">${basket.has(a.id)?'✓':'⇩'}</button><button class="media-open" data-open="${esc(a.id)}"><div class="media-thumb"><img loading="lazy" src="${esc(href(a.thumb))}" alt="${esc(a.title)}">${a.kind==='video'||a.kind==='gif'?`<span class="play">${a.kind==='video'?'▶':'GIF'} ${clipDuration(a)===null?'Duration unknown':Math.round(clipDuration(a)*10)/10+'s'}</span>`:''}</div><div class="media-copy"><b>${esc(a.title)}</b><small>${esc(a.sceneID?a.lyric||'Storyboard idea':C.albums.find(x=>x.id===a.album)?.title||a.filename)}</small></div></button></article>`;}
  function mediaGroup(title,description,items,albumID=''){
    if(!items.length)return '';
    return `<section class="story-section"><div class="section-head"><h2>${esc(title)}</h2>${albumID?`<button class="subtle-button" data-album="${esc(albumID)}">Open group · ${items.length}</button>`:`<span class="muted">${items.length}</span>`}</div>${description?`<p>${esc(description)}</p>`:''}<div class="gallery">${items.map(card).join('')}</div></section>`;
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
    let html=`<div class="tools"><label for="detail-layout">Browse</label><select id="detail-layout"><option value="profiles" ${state.detailLayout==='profiles'?'selected':''}>Character profiles</option><option value="all" ${state.detailLayout==='all'?'selected':''}>All references</option></select></div>`;
    if(state.detailLayout==='all')return html;
    if(!profiles.length)return html+'<p class="notice">Character profiles are being organized. Choose All references to browse the available material.</p>';
    html+=`<div class="tools detail-profile-tabs" aria-label="Character profile">${profiles.map(p=>`<button class="pill ${state.detailProfile===p.id?'active':''}" data-detail-profile="${esc(p.id)}">${esc(p.character||p.title)}</button>`).join('')}</div>`;
    const profile=profiles.find(p=>p.id===state.detailProfile),objects=(profile.objects||[]).filter(o=>!query||[o.title,o.kind,o.location,o.status,o.summary].join(' ').toLowerCase().includes(query)||[...(o.assetIDs||[]),...(o.stencilAssetIDs||[]),...(o.exampleAssetIDs||[])].some(id=>byID.has(id)&&queryMatch(byID.get(id))));
    html+=`<h2>${esc(profile.title||profile.character)}</h2><p class="intro">Choose a tattoo or piercing to see its references, stencil candidates, and placement evidence. Each item keeps its own review status.</p><div class="detail-object-grid">`;
    for(const o of objects){const ids=[...(o.stencilAssetIDs||[]),...(o.assetIDs||[]),...(o.exampleAssetIDs||[])],cover=ids.map(id=>byID.get(id)).find(a=>a&&!a.archived&&!isDoc(a));html+=`<article class="detail-object">${cover?`<button class="detail-object-cover" data-open="${esc(cover.id)}"><img loading="lazy" src="${esc(href(cover.thumb))}" alt="${esc(o.title)}"></button>`:''}<div class="detail-object-copy"><p class="eyebrow">${esc([o.kind,o.location].filter(Boolean).join(' · '))}</p><h3>${esc(o.title)}</h3>${o.status?`<p class="detail-object-status">${esc(String(o.status).replace(/_/g,' '))}</p>`:''}<p>${esc(o.summary||'')}</p><details class="detail-evidence"><summary>References & placement</summary>${workflowReferences('Stencil references',o.stencilAssetIDs)}${workflowReferences('Reference images',o.assetIDs)}${workflowReferences('Placement examples',o.exampleAssetIDs)}</details></div></article>`;}
    return html+'</div>'+(!objects.length?'<p class="empty">No matching details in this character profile.</p>':'');
  }
  function storyThemes(a){
    const themes=C.albums.filter(al=>al.project===state.project&&al.category==='storyboard'&&al.assetIDs.includes(a.id)).map(al=>({id:al.id,title:al.title}));
    for(const tag of a.storyboardThemes||a.themes||a.tags||[])if(typeof tag==='string'&&!/^(storyboard|series\s*\d+)$/i.test(tag))themes.push({id:'tag:'+tag,title:tag});return themes;
  }
  function storyboardStage(a){return reviewRecord(a.id).storyboardStage||a.storyboardStage||(a.category==='storyboard'?'preliminary':null);}
  function storyboardExplorer(media){
    const albums=C.albums.filter(al=>al.project===state.project&&al.category==='storyboard'&&(!state.album||al.id===state.album)),ids=new Set(albums.flatMap(al=>al.assetIDs)),all=media.filter(a=>ids.has(a.id));
    const position=a=>typeof a.storyboardPosition==='number'&&Number.isFinite(a.storyboardPosition)?a.storyboardPosition:null;
    const ranged=all.filter(a=>(!state.storyStage||state.storyStage==='all'||storyboardStage(a)===state.storyStage)&&(position(a)===null?state.storyStart===0&&state.storyEnd===100:position(a)>=state.storyStart&&position(a)<=state.storyEnd));
    const themes=new Map(ranged.flatMap(storyThemes).map(t=>[t.id,t.title]));if(state.storyTheme!=='all'&&!themes.has(state.storyTheme))state.storyTheme='all';
    const cards=ranged.filter(a=>state.storyTheme==='all'||storyThemes(a).some(t=>t.id===state.storyTheme)).sort((a,b)=>(a.storyboardOrder??Infinity)-(b.storyboardOrder??Infinity)||clipTitleOrder.compare(a.title,b.title));
    const meta=Array.isArray(C.storyboardMetadata)?C.storyboardMetadata.find(m=>m.project===state.project):C.storyboardMetadata?.[state.project];
    let html=`<section class="story-controls"><div class="story-stage"><label for="story-stage">Stage</label><select id="story-stage"><option value="all">All stages</option>${Object.entries(storyboardStages).map(([id,label])=>`<option value="${id}" ${state.storyStage===id?'selected':''}>${label}</option>`).join('')}</select></div><div class="story-theme"><label for="story-theme">Theme</label><select id="story-theme"><option value="all">All themes in this range</option>${[...themes].map(([id,title])=>`<option value="${esc(id)}" ${state.storyTheme===id?'selected':''}>${esc(title)}</option>`).join('')}</select></div><div class="story-range"><label for="story-start">From <output>${state.storyStart}%</output><input id="story-start" type="range" min="0" max="100" step="5" value="${state.storyStart}" aria-label="Start of source panel range"></label><label for="story-end">To <output>${state.storyEnd}%</output><input id="story-end" type="range" min="0" max="100" step="5" value="${state.storyEnd}" aria-label="End of source panel range"></label><button class="pill" id="story-reset">Full storyboard</button></div><p class="review-help">Source panel order, not song seconds. ${esc(meta?.timingStatus||'Song timing has not been aligned.')} Themes update with the selected range.</p></section><p class="video-sort-note">${cards.length} matching panels · ${themes.size} available themes in this range</p>`;
    html+=mediaGroup('Story panels','In source panel order.',cards);if(!cards.length)html+='<p class="empty">No panels match this range and theme.</p>';return html;
  }
  const missionProviders=[['Grok','Grok'],['Gemini','Gemini'],['Flow','Flow'],['PanhandlerNova','Panhandler Nova']];
  const missionProject=t=>C.projects.find(p=>p.id===t.project)?.name||'Across projects';
  const missionStatuses={ready:'Ready to send',needs_input:'Needs your input',planned:'Planned',in_progress:'In progress',done:'Done'};
  function providerKey(value){const key=String(value||'').toLowerCase().replace(/[^a-z]/g,'');return missionProviders.find(([id])=>id.toLowerCase()===key)?.[0]||'';}
  function safeMissionHref(value){
    if(typeof value!=='string'||!value.trim())return '';let decoded;
    try{decoded=decodeURIComponent(value.trim());}catch{return '';}
    if(/[\x00-\x1f\x7f\\]/.test(decoded)||/^(?:[a-z][a-z0-9+.-]*:|\/)/i.test(decoded))return '';
    try{const target=new URL(value,base);return target.protocol===base.protocol&&target.origin===base.origin?target.href:'';}catch{return '';}
  }
  function missionTaskLinks(task){return (Array.isArray(task.links)?task.links:[]).map(link=>{
    if(byID.has(link.assetID))return `<button class="pill" data-open="${esc(link.assetID)}">${esc(link.label||'Open reference')}</button>`;
    const url=safeMissionHref(link.href);return url?`<a class="pill" href="${esc(url)}" ${/\.zip(?:[?#]|$)/i.test(url)?'download':''} target="_blank" rel="noopener">${esc(link.label||'Open prepared file')} ↗</a>`:'';
  }).join('');}
  function missionTaskCard(t){return `<details class="mission-task" ${['ready','needs_input'].includes(t.status)?'open':''}><summary><span class="mission-status ${esc(t.status)}">${esc(missionStatuses[t.status]||'Planned')}</span><b>${esc(t.title)}</b><small class="mission-project">${esc(missionProject(t))}</small></summary><p>${esc(t.summary||'')}</p>${t.nextAction?`<p class="mission-next-action"><strong>Next:</strong> ${esc(t.nextAction)}</p>`:''}${Array.isArray(t.missing)&&t.missing.length?`<div class="mission-missing"><strong>Still needed</strong><ul>${t.missing.map(item=>`<li>${esc(item)}</li>`).join('')}</ul></div>`:''}<div class="tools">${missionTaskLinks(t)}</div></details>`;}
  function workflowReferences(title,ids){
    const references=(Array.isArray(ids)?ids:[]).map(id=>byID.get(id)).filter(a=>a&&!a.archived&&(title!=='Source references'||exportAllowed(a)));if(!references.length)return '';
    return `<section class="workflow-references"><h3>${esc(title)}</h3><div class="workflow-reference-grid">${references.map(a=>{if(!isDoc(a)&&!displayed.includes(a.id))displayed.push(a.id);return `<button data-open="${esc(a.id)}" class="workflow-reference">${!isDoc(a)?`<img loading="lazy" src="${esc(href(a.thumb))}" alt="">`:''}<span>${esc(a.title)}</span></button>`;}).join('')}</div></section>`;
  }
  function safeComfyURL(value){try{const url=new URL(value);return url.protocol==='https:'&&url.hostname==='cloud.comfy.org'&&!url.username&&!url.password&&!url.port?url.href:'';}catch{return '';}}
  function collaboratorsWorkspace(){
    const providers=[['ComfyUI','ComfyUI'],['Flow','Flow'],['Gemini','Gemini'],['Grok','Grok'],['PanhandlerNova','Panhandler Nova']];
    const selected=state.collaborator,providerName=providers.find(([id])=>id===selected)?.[1]||'ComfyUI',query=state.search.toLowerCase().trim();
    let html=`<div class="tools collaborator-tabs" role="group" aria-label="Choose collaborator">${providers.map(([id,label])=>`<button class="pill ${selected===id?'active':''}" aria-pressed="${selected===id}" data-collaborator-provider="${id}">${label}</button>`).join('')}</div>`;
    if(selected==='ComfyUI'){
      const workflows=(Array.isArray(C.productionWorkflows)?C.productionWorkflows:[]).filter(w=>w.provider==='ComfyUI'&&[w.title,w.summary,w.nextAction,missionProject(w)].join(' ').toLowerCase().includes(query));
      html+=`<div class="workflow-list">${workflows.map(w=>{const cloud=safeComfyURL(w.cloudURL);return `<article class="production-workflow"><p class="eyebrow">${esc(missionProject(w))}</p><h2>${esc(w.title)}</h2><p class="workflow-status">${esc(w.statusLabel||String(w.status||'Planned').replace(/_/g,' '))}</p><p class="intro">${esc(w.summary||'')}</p>${w.nextAction?`<p class="mission-next-action"><strong>Next:</strong> ${esc(w.nextAction)}</p>`:''}${workflowReferences('Source references',w.sourceAssetIDs)}${workflowReferences('Outputs',w.outputAssetIDs)}${workflowReferences('Workflow & notes',w.documentAssetIDs)}${cloud?`<a class="pill cloud-workflow-link" href="${esc(cloud)}" target="_blank" rel="noopener">Open saved Comfy workflow ↗</a>`:''}</article>`;}).join('')}</div>`;
      if(!workflows.length)html+='<div class="empty">No matching ComfyUI workflow is listed yet.</div>';
    } else {
      const tasks=(C.missionControl?.tasks||[]).filter(t=>providerKey(t.provider)===selected&&[t.title,t.summary,t.nextAction,missionProject(t)].join(' ').toLowerCase().includes(query));
      html+=`<section class="collaborator-work"><h2>${esc(providerName)}</h2>${tasks.map(missionTaskCard).join('')}</section>`;
      const plans=C.assets.filter(a=>!a.archived&&reviewRecord(a.id).shotPlan?.destinations.includes(selected)&&queryMatch(a));
      if(plans.length){html+=mediaGroup('Draft shot queue','Planned here; attach the actual files when you send your handoff.',plans.filter(a=>!isDoc(a)));html+=`<div class="tools"><button class="pill" data-mission-export="${selected}">Export ${esc(providerName)} shot handoff</button></div>`;}
      if(selected==='PanhandlerNova')html+='<div class="tools"><button class="pill" data-mission-export="PanhandlerNova">Export review for Nova</button></div>';
      if(!tasks.length){const briefs=C.assets.filter(a=>isDoc(a)&&/collaborator/i.test(a.album||'')&&(a.album+' '+a.title).toLowerCase().includes(providerName.toLowerCase())&&queryMatch(a));html+=documentGroups(briefs);if(!briefs.length&&!plans.length)html+='<p class="notice">No prepared handoff for this collaborator yet. Queue a reference from its preview to start a draft.</p>';}
    }
    return html;
  }
  function missionControl(){
    const board=C.missionControl||{}, rank={ready:0,needs_input:1,in_progress:2,planned:3,done:4};
    const tasks=(Array.isArray(board.tasks)?board.tasks:[]).map(t=>({...t,status:Object.hasOwn(missionStatuses,t.status)?t.status:'planned'})).sort((a,b)=>rank[a.status]-rank[b.status]);
    const query=state.search.toLowerCase().trim(),visible=tasks.filter(t=>[t.provider,t.title,t.summary,t.nextAction,...(Array.isArray(t.missing)?t.missing:[])].join(' ').toLowerCase().includes(query));
    const assets=C.assets,queued=assets.filter(inReviewQueue),plans=assets.filter(a=>!a.archived&&reviewRecord(a.id).shotPlan),count=status=>tasks.filter(t=>t.status===status).length;
    let html=`<div class="mission-counts">${[['Ready to send',count('ready')],['Needs your input',count('needs_input')],['In progress',count('in_progress')],['Shot plans',plans.length]].map(([label,n])=>`<div><strong>${n}</strong><span>${label}</span></div>`).join('')}</div><p class="mission-note">Tasks cover all projects and come from the prepared board. Review choices and shot plans reflect this browser; they have not been sent to a collaborator.</p><section class="mission-next"><h2>Current work</h2><button class="pill review-sweep" id="prepare-review-sweep">Prepare review sweep</button><p class="mission-note">Save your review, favorites, and working-reference requests, then ask Nova to run the sweep. This button does not start Codex or delete files.</p><p id="review-sweep-status" role="status"></p>${visible.filter(t=>t.status!=='done').slice(0,3).map(t=>`<div class="mission-next-row"><span class="mission-status ${t.status}">${esc(missionStatuses[t.status])}</span><div><b>${esc(t.title)}</b><small class="mission-project">${esc(missionProject(t))}</small><p>${esc(t.nextAction||t.summary||'Open the handoff below for the next step.')}</p></div></div>`).join('')||'<p>Choose a reference and plan a shot, or add a review note to shape the next pass.</p>'}<div class="tools"><button class="pill" data-mission-view="review_queue">Review ${esc(C.projects.find(p=>p.id===state.project)?.name)} · ${projectAssets(true).filter(inReviewQueue).length}</button><button class="pill" data-mission-view="shot_plans">This project’s shot plans · ${projectAssets().filter(a=>reviewRecord(a.id).shotPlan).length}</button><button class="pill" data-mission-view="all">Browse the library</button></div></section><div class="section-head"><h2>Collaborator handoffs</h2></div><div class="mission-providers">`;
    for(const [id,name] of missionProviders){
      const work=visible.filter(t=>providerKey(t.provider)===id), planned=plans.filter(a=>reviewRecord(a.id).shotPlan.destinations.includes(id));
      html+=`<article class="mission-provider"><h3>${name}</h3><p class="mission-provider-count">${work.length} prepared ${work.length===1?'task':'tasks'}${id==='PanhandlerNova'?` · ${queued.length} review items`:` · ${planned.length} planned shots`}</p>${work.map(missionTaskCard).join('')||'<p class="mission-note">No prepared handoff listed yet.</p>'}${id==='PanhandlerNova'?`<button class="pill" data-mission-export="${id}">Export review for Nova</button>`:planned.length?`<button class="pill" data-mission-export="${id}">Export ${name} shot handoff</button>`:''}</article>`;
    }
    html+='</div>';const undecided=plans.filter(a=>reviewRecord(a.id).shotPlan.destinations.includes('undecided')).length;
    if(undecided)html+=`<p class="notice">${undecided} shot ${undecided===1?'idea still needs':'ideas still need'} a destination. You can keep exploring before choosing a collaborator.</p>`;
    if(board.updated)html+=`<p class="mission-note">Prepared board updated ${esc(board.updated)}. A prepared handoff is ready for you to send; this library does not send it automatically.</p>`;
    return html;
  }
  function renderMain(){
    displayed=[];const p=C.projects.find(p=>p.id===state.project);const all=projectAssets(state.view==='review_queue').filter(queryMatch);const docs=all.filter(isDoc);const media=all.filter(a=>!isDoc(a));
    const heading=state.album?C.albums.find(a=>a.id===state.album)?.title:cats[state.view]||{mission_control:'Mission Control',collaborators:'Collaborators',all:p.name+' reference library',favorites:'Your favorites',export_basket:'Export basket',review_queue:'Review queue',shot_plans:'Shot plans',documents:'Documents & notes'}[state.view];
    let html=`<p class="eyebrow">${esc(p.subtitle)}</p><div class="library-heading"><h1>${esc(heading)}</h1>${state.view==='videos'?`<div class="video-controls"><label class="video-sort" for="video-layout"><span>Layout</span><select id="video-layout"><option value="grouped" ${state.videoLayout==='grouped'?'selected':''}>Grouped</option><option value="all" ${state.videoLayout==='all'?'selected':''}>All clips</option></select></label><label class="video-sort" for="video-sort"><span>Sort</span><select id="video-sort">${Object.entries(videoSortLabels).map(([value,label])=>`<option value="${value}" ${state.videoSort===value?'selected':''}>${label}</option>`).join('')}</select></label></div>`:''}</div><p class="intro">${state.view==='collaborators'?'Workflows, source references, and prepared handoffs across your projects.':state.view==='mission_control'?'Your next moves, prepared handoffs, and ideas waiting for their next pass.':state.view==='all'?'Artwork first, grouped by purpose. Click a preview to enlarge it; star anything you want to revisit.':state.view==='export_basket'?'A separate selection from across all projects. Add or remove references with ⇩; your favorites stay unchanged. The export is a file list, not a media bundle.':state.view==='favorites'?'Your review shortlist. These stars do not change the character locks or original files.':state.view==='shot_plans'?'Collect shot ideas and draft prompts, then export a handoff for your chosen collaborator. These plans have not been sent or generated.':state.view==='review_queue'?'Needs-fix notes and removal requests gathered for the next sorting pass. Source files remain in place.':state.view==='documents'?'Notes are grouped by subject. Click a file to read a preview without leaving the library.':'Choose a group or browse the previews below.'}</p>`;
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
      html+=mediaGroup('Working-reference requests','Queued for review; the source and character standards have not changed.',promotions.filter(a=>!isDoc(a)));
      html+=mediaGroup('Needs fixes','Open a reference to read or update the correction note.',fixes.filter(a=>!isDoc(a)));
      html+=mediaGroup('Marked for removal','Queued for a later sorting pass. Nothing has been deleted.',removals.filter(a=>!isDoc(a)));
      html+=documentGroups(queued.filter(isDoc));if(!queued.length)html+='<div class="empty">Your review queue is clear. Open a reference and choose Needs fixes or Mark for removal to add it.</div>';
    } else if(state.view==='documents')html+=documentGroups(docs);
    else if(state.view==='details'&&state.detailLayout==='profiles')html+=detailExplorer();
    else if(state.view==='storyboard')html+=storyboardExplorer(media);
    else {
      let albums=C.albums.filter(a=>a.project===state.project&&(state.view==='all'||a.category===state.view)&&(!state.album||a.id===state.album));
      if(state.view==='storyboard')html+='<p class="notice">Story ideas grouped by beat. Panel numbers identify the source; song timings are still to be aligned.</p>';
      if(state.view==='details')html+=detailExplorer()+'<p class="notice">Use each reference for its selected detail. A tattoo or piercing example does not replace the whole character.</p>';
      if(state.view!=='all'&&!state.album&&albums.length>1)html+=`<div class="video-filter">${albums.map(a=>`<button class="pill" data-album="${esc(a.id)}">${esc(a.title)}</button>`).join('')}</div>`;
      const categoryOrder=Object.keys(cats);
      albums.sort((a,b)=>categoryOrder.indexOf(a.category)-categoryOrder.indexOf(b.category));
      let shown=0;
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
          const items=state.view==='videos'?sortClips(al.assetIDs.map(id=>byID.get(id)).filter(a=>a&&isClip(a)&&visibleIDs.has(a.id))):media.filter(a=>state.view==='all'?a.album===al.id:al.assetIDs.includes(a.id));
          if(!items.length)continue;
          shown+=items.length;html+=mediaGroup(al.title,state.view==='all'?'':al.description,items,al.id);
        }
      }
      if(!shown)html+='<div class="empty">No matching previews. Try another category or search.</div>';
      if(state.view==='all'&&!state.album)html+=documentGroups(docs);
    }
    document.querySelector('#main').innerHTML=html;
    document.querySelectorAll('[data-open]').forEach(b=>b.onclick=()=>openViewer(b.dataset.open));
    document.querySelectorAll('[data-favorite]').forEach(b=>b.onclick=()=>toggleFavorite(b.dataset.favorite));
    document.querySelectorAll('[data-basket]').forEach(b=>b.onclick=()=>toggleBasket(b.dataset.basket));
    document.querySelector('#export-basket-list')?.addEventListener('click',exportBasket);document.querySelector('#clear-basket')?.addEventListener('click',()=>{basket.clear();saveBasket();notice('Export basket cleared. Favorites and review notes are unchanged.');});
    document.querySelectorAll('[data-album]').forEach(b=>b.onclick=()=>{const a=C.albums.find(x=>x.id===b.dataset.album);route(state.project,a.category,a.id);});
    document.querySelectorAll('[data-mission-view]').forEach(button=>button.onclick=()=>route(state.project,button.dataset.missionView));
    document.querySelectorAll('[data-collaborator-provider]').forEach(button=>button.onclick=()=>{state.collaborator=button.dataset.collaboratorProvider;renderMain();});
    document.querySelectorAll('[data-export-intent]').forEach(select=>select.onchange=()=>{state.exportIntent=select.value==='multiverse_ingredients'?'multiverse_ingredients':'prime';render();});
    document.querySelector('#prepare-review-sweep')?.addEventListener('click',prepareReviewSweep);
    document.querySelector('#detail-layout')?.addEventListener('change',e=>{state.detailLayout=e.target.value==='all'?'all':'profiles';renderMain();});
    document.querySelectorAll('[data-detail-profile]').forEach(button=>button.onclick=()=>{state.detailProfile=button.dataset.detailProfile;renderMain();});
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
    document.querySelector('#export-main')?.addEventListener('click',exportFavorites);document.querySelector('#export-review-main')?.addEventListener('click',exportReview);
  }
  const dialog=document.createElement('dialog');dialog.className='viewer';dialog.setAttribute('aria-label','Media preview');document.body.append(dialog);
  function openViewer(id){
    const a=byID.get(id);if(!a)return;currentID=id;const i=displayed.indexOf(id),doc=isDoc(a);
    const media=a.kind==='video'?`<video controls playsinline preload="metadata" poster="${esc(href(a.thumb))}" src="${esc(href(a.src))}"></video>`:a.kind==='pdf'?`<iframe title="PDF preview" src="${esc(href(a.src))}"></iframe>`:a.kind==='document'?`<pre>${esc(a.text)}</pre>`:`<img src="${esc(href(a.src))}" alt="${esc(a.title)}" id="full-image">`;
    dialog.innerHTML=`<div class="viewer-body"><div class="viewer-head"><span>${doc?'Document preview':`${Math.max(i+1,1)} / ${Math.max(displayed.length,1)} · ${a.kind==='video'?'Video':'Image'} preview`}</span><div class="view-nav">${!doc?`<button id="previous" aria-label="Previous image" ${i<=0?'disabled':''}>←</button><button id="next" aria-label="Next image" ${i<0||i>=displayed.length-1?'disabled':''}>→</button>`:''}${['image','gif'].includes(a.kind)?'<button id="zoom" aria-label="Toggle full-size zoom">Zoom</button>':''}<button id="close-viewer" aria-label="Close preview">✕</button></div></div><div class="stage">${media}</div><aside class="viewer-info"><p class="label">${esc(cats[a.category]||'Document')}</p><h2>${esc(a.title)}</h2><p class="filename">${esc(a.filename)}</p><div class="viewer-quick-actions">${!doc?`<button class="action" id="viewer-favorite">${favorites.has(id)?'★ Favorited':'☆ Add to favorites'}</button>`:''}<button class="action export-basket-action ${basket.has(id)?'on':''}" id="viewer-basket" data-basket="${esc(id)}" aria-pressed="${basket.has(id)}">${basket.has(id)?'⇩ In export basket':'⇩ Add to export basket'}</button></div>${!doc?collaboratorControls(a):''}${a.lyric?`<p class="label">Lyric connection</p><p>${esc(a.lyric)}</p>`:''}${a.beat?`<p>${esc(a.beat)}</p>`:''}${a.motion?`<p class="label">Motion idea</p><p>${esc(a.motion)}</p>`:''}${a.note?`<p class="label">Review note</p><p>${esc(a.note)}</p>`:''}${a.inert?'<p>Preserved helper script. This viewer only displays its text.</p>':''}${!doc?referenceControls(a)+workflowStageControls(a):''}${reviewControls(a)}${shotPlanControls(a)}<a class="small-link" href="${esc(href(a.src))}" target="_blank" rel="noopener" ${a.inert?'download':''}>Open original file ↗</a><details><summary>File details</summary><p>${esc(a.repoPath)}</p>${a.sha256?`<p>SHA-256<br>${esc(a.sha256)}</p>`:''}<p>${esc(typeof a.sourceStatus==='string'?a.sourceStatus:'Source record retained')}</p></details></aside></div>`;
    document.querySelector('#close-viewer').onclick=()=>dialog.close();
    document.querySelector('#previous')?.addEventListener('click',()=>openViewer(displayed[i-1]));
    document.querySelector('#next')?.addEventListener('click',()=>openViewer(displayed[i+1]));
    document.querySelector('#zoom')?.addEventListener('click',()=>document.querySelector('#full-image').classList.toggle('zoomed'));
    document.querySelector('#viewer-favorite')?.addEventListener('click',e=>{toggleFavorite(id);e.target.textContent=favorites.has(id)?'★ Favorited':'☆ Add to favorites';});
    document.querySelector('#viewer-basket').onclick=()=>toggleBasket(id);
    document.querySelectorAll('[data-review-status]').forEach(button=>button.onclick=()=>updateReview(id,{status:button.dataset.reviewStatus||null}));
    document.querySelector('#review-note').oninput=e=>updateReview(id,{note:e.target.value});
    document.querySelector('#viewer-save-review').onclick=chooseReviewFile;document.querySelector('#viewer-export-review').onclick=exportReview;
    bindShotPlanControls(id);bindReferenceControls(id);
    document.querySelector('#reference-storyboard-stage')?.addEventListener('change',e=>{updateReview(id,{storyboardStage:Object.hasOwn(storyboardStages,e.target.value)?e.target.value:null});const label=document.querySelector('#reference-stage-status');if(label)label.textContent='Current stage: '+(storyboardStages[storyboardStage(byID.get(id))]||'not assigned')+'. This is separate from reference approval.';});
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
  dialog.addEventListener('close',()=>{dialog.querySelector('video')?.pause();dialog.innerHTML='';currentID='';if(['mission_control','collaborators','favorites','export_basket','review_queue','shot_plans'].includes(state.view))renderMain();});
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
  function workflowStageControls(a){const stage=storyboardStage(a);return `<details class="workflow-stage-controls"><summary>Workflow stage · ${esc(storyboardStages[stage]||'not assigned')}</summary><label for="reference-storyboard-stage">Storyboard stage</label><select id="reference-storyboard-stage"><option value="">Use source stage</option>${Object.entries(storyboardStages).map(([id,label])=>`<option value="${id}" ${stage===id?'selected':''}>${label}</option>`).join('')}</select><p id="reference-stage-status" class="review-help">Current stage: ${esc(storyboardStages[stage]||'not assigned')}. This is separate from reference approval.</p></details>`;}
  function referenceControls(a){const r=reviewRecord(a.id);return `<section class="reference-controls" aria-label="Reference lane and working-reference request"><h3>Reference role</h3><label for="reference-variant">Creative lane</label><select id="reference-variant"><option value="prime" ${r.variant!=='multiverse'?'selected':''}>Prime / current direction</option><option value="multiverse" ${r.variant==='multiverse'?'selected':''}>Multiverse idea</option></select><p class="review-help">Multiverse ideas stay available for exploration and are excluded from Prime handoffs.</p><label for="working-reference-scope">Working reference for</label><select id="working-reference-scope">${Object.entries(workingScopes).map(([id,label])=>`<option value="${id}" ${r.workingReference?.scope===id?'selected':''}>${label}</option>`).join('')}</select><div class="reference-request-actions"><button id="request-working-reference">Request working reference</button><button id="clear-working-reference" ${r.workingReference?.status==='requested'?'':'hidden'}>Cancel request</button></div><p id="working-reference-status" class="review-help" role="status"></p></section>`;}
  function refreshReferenceUI(){
    const a=byID.get(currentID);if(!a)return;const r=reviewRecord(currentID),blocked=a.archived||r.status==='remove'||r.variant==='multiverse',button=document.querySelector('#request-working-reference');
    if(button){button.disabled=blocked;button.textContent=r.workingReference?.status==='requested'?'Update request':'Request working reference';}
    const clear=document.querySelector('#clear-working-reference');if(clear)clear.hidden=r.workingReference?.status!=='requested';
    const status=document.querySelector('#working-reference-status');if(status)status.textContent=blocked?'Prime working references cannot be requested from Multiverse ideas, archived files, or removal requests.':r.workingReference?.status==='requested'?'Request queued for '+workingScopes[r.workingReference.scope]+'. Ask Nova to review it; nothing has been promoted.':r.workingReference?.status==='approved'?'Reviewed working reference: '+workingScopes[r.workingReference.scope]+'.':'Choose a scope and request a review. This does not change the character standard.';
  }
  function bindReferenceControls(id){
    document.querySelector('#reference-variant')?.addEventListener('change',e=>updateReview(id,{variant:e.target.value==='multiverse'?'multiverse':'prime',variantSource:'user',...(e.target.value==='multiverse'?{workingReference:null}:{})}));
    document.querySelector('#request-working-reference')?.addEventListener('click',()=>{const r=reviewRecord(id);if(byID.get(id).archived||r.variant==='multiverse'||r.status==='remove')return;updateReview(id,{workingReference:{status:'requested',scope:document.querySelector('#working-reference-scope').value}});});
    document.querySelector('#clear-working-reference')?.addEventListener('click',()=>updateReview(id,{workingReference:null}));refreshReferenceUI();
  }
  async function prepareReviewSweep(){
    const data=reviewPayload();downloadJSON({...data,reviewSweep:{status:'prepared; waiting for Nova',requestedAt:new Date().toISOString(),pendingWorkingReferences:data.items.filter(i=>i.workingReference?.status==='requested').map(i=>({id:i.id,sha256:i.sha256,scope:i.workingReference.scope}))}},'cfa-review-sweep.json');
    const saved=reviewFileHandle?await writeReviewFile():false;const status=document.querySelector('#review-sweep-status');if(status)status.textContent=(saved?'Chosen review file saved. ':'')+'Review sweep exported. Give it to Nova and ask her to review the queued changes. No files were deleted and no task was started.';
  }
  function shotPlanControls(a){
    const plan=reviewRecord(a.id).shotPlan, values=plan||normalizedPlan({});
    return `<section class="shot-plan-controls" aria-label="Shot planning"><label class="plan-toggle"><input type="checkbox" id="shot-plan-enabled" ${plan?'checked':''}> Plan a shot</label><p class="review-help">A creative plan is separate from your keep/fix/removal decision. Nothing is sent or generated here.</p><div id="shot-plan-fields" ${plan?'':'hidden'}><fieldset><legend>Where might this shot go?</legend>${destinations.map(d=>`<label><input type="checkbox" data-shot-destination="${d}" ${values.destinations.includes(d)?'checked':''}> ${d==='undecided'?'Undecided':d}</label>`).join('')}</fieldset><label for="shot-idea">Shot idea</label><textarea id="shot-idea" rows="3" maxlength="20000" placeholder="The moment, action, or feeling to explore…">${esc(values.idea)}</textarea><label for="shot-prompt">Draft prompt (optional)</label><textarea id="shot-prompt" rows="5" maxlength="30000" placeholder="What the collaborator should create or preserve…">${esc(values.prompt)}</textarea><p class="review-help">Status: planned. Export a provider handoff from Shot plans when you are ready.</p></div></section>`;
  }
  function bindShotPlanControls(id){
    document.querySelector('#shot-plan-enabled').onchange=e=>{
      updateReview(id,{shotPlan:e.target.checked?normalizedPlan({}):null});
      document.querySelector('#shot-plan-fields').hidden=!e.target.checked;
      if(e.target.checked){document.querySelector('#shot-idea').value='';document.querySelector('#shot-prompt').value='';document.querySelectorAll('[data-shot-destination]').forEach(input=>input.checked=input.dataset.shotDestination==='undecided');}
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
    return {format:'cfa-shot-handoff-v1',exported:new Date().toISOString(),project:scope,destination:state.destination,
      exportIntent:state.exportIntent,
      status:'planned; not sent or generated',
      attachmentReminder:'Attach the actual images or clips identified below. This handoff contains references and text only; no media files are bundled.',
      items:(scope==='all'?C.assets:projectAssets()).filter(exportAllowed).filter(queryMatch).filter(a=>reviewRecord(a.id).shotPlan&&(state.destination==='all'||reviewRecord(a.id).shotPlan.destinations.includes(state.destination)))
        .map(a=>({...exportReference(a),title:a.title,reviewStatus:reviewRecord(a.id).status,note:reviewRecord(a.id).note,shotPlan:reviewRecord(a.id).shotPlan}))};
  }
  function exportShotHandoff(format,scope=state.project){
    const data=shotHandoffPayload(scope),filename='cfa-shot-handoff-'+scope+'-'+state.destination+'.'+format;
    if(format==='json')downloadJSON(data,filename);
    else {
      const text=['CFA SHOT HANDOFF',`Project: ${data.project} | Destination: ${state.destination}`,`Export intent: ${data.exportIntent==='prime'?'Prime references':'Multiverse creative ingredients'}`,data.status,data.attachmentReminder,'',...data.items.flatMap((a,i)=>[
        `${i+1}. ${a.title}`,`Reference ID: ${a.id}`,`SHA-256: ${a.sha256||'not recorded'}`,`File: ${a.filename}`,`Source path: ${a.path||'see source catalog'}`,
        `Destinations: ${a.shotPlan.destinations.join(', ')}`,`Lane: ${a.variant}`,`Review: ${a.reviewStatus||'unreviewed'}`,`Review note: ${a.note||'(none)'}`,
        `Shot idea: ${a.shotPlan.idea||'(to be written)'}`,`Draft prompt: ${a.shotPlan.prompt||'(not drafted)'}`,''])].join('\n');
      const url=URL.createObjectURL(new Blob([text],{type:'text/plain;charset=utf-8'})),link=document.createElement('a');link.href=url;link.download=filename;link.click();setTimeout(()=>URL.revokeObjectURL(url),3000);
    }
    notice(data.items.length+' planned shots exported. Attach the actual reference files when handing them over.');
  }
  function exportFavorites(){const selected=[...favorites].map(id=>byID.get(id)).filter(Boolean),items=selected.filter(exportAllowed).map(exportReference);downloadJSON({format:'cfa-visual-favorites-v1',exported:new Date().toISOString(),exportIntent:state.exportIntent,status:'user review shortlist; not automatic final approval',items},'CFA-favorites-'+new Date().toISOString().slice(0,10)+'.json');notice(items.length+' favorites exported; '+(selected.length-items.length)+' excluded by export intent. Full review backups retain every star.');}
  function downloadJSON(data,filename){const blob=new Blob([JSON.stringify(data,null,2)],{type:'application/json'}),url=URL.createObjectURL(blob),link=document.createElement('a');link.href=url;link.download=filename;link.click();setTimeout(()=>URL.revokeObjectURL(url),3000);}
  function exportReview(){downloadJSON(reviewPayload(),'cfa-review.json');notice('Review exported with decisions, notes, and favorites. Save it as docs/notes/cfa-review.json to share it.');}
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
    if(data.format===REVIEW_KEY&&Array.isArray(data.exportBasket)){const result=importBasket(data.exportBasket);skipped+=result.skipped;}
    reviewRevision++;saveBrowserReview();scheduleFileSave();render();notice(`${imported} review records and ${stars} favorites imported; ${skipped} unmatched entries skipped.`);
  }
  const input=document.createElement('input');input.type='file';input.accept='.json,application/json';input.id='import-file';input.hidden=true;document.body.append(input);
  input.onchange=async()=>{try{const file=input.files?.[0];if(!file)return;if(file.size>5*1024*1024)throw Error('Choose a review file smaller than 5 MB.');importReview(JSON.parse(await file.text()));}catch(error){notice(error instanceof SyntaxError?'That file is not valid JSON.':error.message||'Could not import that review file.');}finally{input.value='';}};
  window.addEventListener('beforeunload',e=>{if(reviewFileHandle&&(fileSaveTimer||fileWriting||reviewRevision!==fileSavedRevision)){e.preventDefault();e.returnValue='';}});
  window.addEventListener('hashchange',()=>{rememberLibrary();parseHash();render();});parseHash();render();
})();
