/* Location Scout regression checks against the real catalog.
   The DOM double verifies markup, handlers and persistence semantics; browser layout is checked separately. */
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');
const clone=value=>JSON.parse(JSON.stringify(value));
const source=fs.readFileSync(path.join(__dirname,'library.js'),'utf8');
const catalog=JSON.parse(fs.readFileSync(path.join(__dirname,'catalog.js'),'utf8').split('=').slice(1).join('=').trim().replace(/;$/,''));
const REVIEW_KEY='cfa-visual-review-v1';

function boot(saved={},hash='#criminal_mind/locations',catalogOverride={}){
  const elements=new Set(),nodes=new Map(),storage=new Map(Object.entries(saved)),writes=[],downloads=[],blobs=new Map();
  const decode=value=>value.replace(/&quot;/g,'"').replace(/&#39;/g,"'").replace(/&amp;/g,'&').replace(/&lt;/g,'<').replace(/&gt;/g,'>');
  const dataKey=name=>name.replace(/^data-/,'').replace(/-([a-z])/g,(_,letter)=>letter.toUpperCase());
  const removeTree=element=>{for(const child of element.children||[])removeTree(child);elements.delete(element);if(element.id&&nodes.get('#'+element.id)===element)nodes.delete('#'+element.id);};
  class Element{
    constructor(tag='div'){
      this.tag=tag;this.dataset={};this.attributes={};this.children=new Set();this.listeners=new Map();this._html='';this.value='';this.open=false;
      this.textContent='';
      this.classList={toggle(){},add(){},remove(){},contains:name=>(this.attributes.class||'').split(/\s+/).includes(name)};elements.add(this);
    }
    set innerHTML(html){
      for(const child of this.children)removeTree(child);this.children.clear();this._html=html;
      for(const match of html.matchAll(/<([a-z][\w-]*)\b([^>]*)>/gi)){
        const child=new Element(match[1]);
        for(const attribute of match[2].matchAll(/([\w-]+)="([^"]*)"/g))child.setAttribute(attribute[1],decode(attribute[2]));
        for(const attribute of match[2].matchAll(/\s(data-[\w-]+)(?=\s|$)/g))if(!Object.hasOwn(child.attributes,attribute[1]))child.setAttribute(attribute[1],'');
        child.disabled=/(?:^|\s)disabled(?:\s|$)/.test(match[2]);this.children.add(child);
      }
      for(const match of html.matchAll(/<textarea\b[^>]*\bid="([^"]+)"[^>]*>([\s\S]*?)<\/textarea>/gi)){
        const textarea=nodes.get('#'+match[1]);if(textarea)textarea.value=decode(match[2]);
      }
    }
    get innerHTML(){return this._html;}
    setAttribute(name,value){this.attributes[name]=String(value);if(name.startsWith('data-'))this.dataset[dataKey(name)]=String(value);else if(name==='id'){this.id=String(value);nodes.set('#'+this.id,this);}else this[name]=value;}
    addEventListener(name,callback){if(!this.listeners.has(name))this.listeners.set(name,[]);this.listeners.get(name).push(callback);}
    fire(name){const event={target:this,preventDefault(){}};let result=this['on'+name]?.(event);for(const callback of this.listeners.get(name)||[])result=callback(event);return result;}
    click(){if(this.disabled)return;if(this.tag==='a'&&this.download)downloads.push({name:this.download,blob:blobs.get(this.href)});return this.fire('click');}
    append(child){this.children.add(child);if(child.id)nodes.set('#'+child.id,child);}
    querySelector(){return null;}querySelectorAll(){return [];}getBoundingClientRect(){return {top:100};}focus(){this.focused=true;}showModal(){this.open=true;}close(){this.open=false;}remove(){removeTree(this);}
  }
  nodes.set('#app',new Element());
  const selectAll=selector=>{const match=/^\[([\w-]+)(?:="([^"]*)")?\]$/.exec(selector);if(!match)return[];return[...elements].filter(element=>Object.hasOwn(element.attributes,match[1])&&(match[2]===undefined||element.attributes[match[1]]===match[2]));};
  const document={currentScript:{src:'file:///D:/Documents/CFA/docs/notes/explorable_world/comfy/projects/visual_library/library.js'},body:new Element('body'),createElement:tag=>new Element(tag),addEventListener(){},querySelector:selector=>nodes.get(selector)||selectAll(selector)[0]||null,querySelectorAll:selectAll};
  const location={hash},window={REVIEW_CATALOG:{...clone(catalog),...clone(catalogOverride)},REVIEW_INITIAL:{project:'criminal_mind',view:'locations'},addEventListener(){},scrollTo(){},scrollBy(){}};
  class TestURL extends URL{static createObjectURL(blob){const url='blob:location-'+blobs.size;blobs.set(url,blob);return url;}static revokeObjectURL(){}}
  const context={window,document,location,URL:TestURL,Blob,Intl,console,setTimeout(){return 1;},clearTimeout(){},localStorage:{getItem:key=>storage.get(key)??null,setItem(key,value){storage.set(key,value);writes.push([key,value]);}},sessionStorage:{getItem(){return null;},setItem(){}}};
  const hook=`window.__locationTest={C,route,renderMain,locationFamilies,locationFamilyCount,storyboardSequenceCount,supportingCastCount,outfitCollectionCount,accessoryUnitCount,workingReferenceSetCount,locationScoutSelection,locationReviewRecord,updateLocationReview,reviewRecord,reviewPayload,importReview,updateReview,selectedReviewScope,getState:()=>state,setCasaStage(value){state.casaStages=state.casaStages||{};state.casaStages[state.project]=value;},setReviewIdentity(project,actor,scope){actorSelections.set(project,actor);scopeSelections.set(project,scope);}};`;
  const instrumented=source.replace(/\}\)\(\);\s*$/,hook+'})();');assert.notEqual(instrumented,source,'Location test hook attached');vm.runInNewContext(instrumented,context);
  return{
    api:window.__locationTest,location,writes,storage,downloads,
    html:()=>nodes.get('#main').innerHTML,shell:()=>nodes.get('#app').innerHTML,
    visible:()=>nodes.get('#main').innerHTML+'\n'+[...elements].map(element=>element.textContent||'').join('\n'),
    node(selector){const control=nodes.get(selector)||selectAll(selector)[0];assert(control,'Control exists: '+selector);return control;},
    input(selector,value){const control=this.node(selector);control.value=value;return control.fire('input');},
    change(selector,value){const control=this.node(selector);control.value=value;return control.fire('change');},
    click(attribute,value){const control=selectAll('['+attribute+']').find(element=>element.attributes[attribute]===value);assert(control,'Control exists: '+attribute+'='+value);control.click();},
    snapshot:()=>Object.fromEntries(storage)
  };
}

async function main(){
const page=boot(),api=page.api;
const families=clone(api.locationFamilies('criminal_mind',false));
assert.equal(families.length,24,'Forty-four albums consolidate into 24 explicit location families');
assert.equal(families.reduce((count,family)=>count+family.items.length,0),956,'All 956 logical assets remain in the scout inventory');
assert.equal(new Set(families.flatMap(family=>family.items.map(asset=>asset.id))).size,956,'Only asset IDs are deduplicated');
assert.equal(new Set(families.flatMap(family=>family.items.map(asset=>asset.sha256))).size,954,'Same-hash logical records remain separate');
assert.equal(api.storyboardSequenceCount('criminal_mind'),41,'Storyboard navigation counts authored sequences, not 165 planned shots');
assert.equal(api.locationFamilyCount('criminal_mind'),24,'Locations navigation counts unique recorded places, not 956 references');
assert.equal(api.supportingCastCount('criminal_mind'),33,'Supporting cast navigation counts unique characters, not their artifacts');
assert.deepEqual(['hon','lisan','criminal_mind'].map(project=>[project,api.outfitCollectionCount(project),api.accessoryUnitCount(project),api.workingReferenceSetCount(project)]),[
  ['hon',22,18,11],['lisan',51,11,2],['criminal_mind',0,0,0]
],'Outfits, Accessories and Working references count their browse units across projects');
assert.match(page.shell(),/data-view="locations"[^>]*>Locations <span class="count">24<\/span>/);
assert.match(page.shell(),/data-view="storyboard"[^>]*>Storyboard<span class="count">41<\/span>/);
assert.match(page.shell(),/data-view="cast"[^>]*>Supporting cast<span class="count">33<\/span>/);
const honNav=boot({},'#hon/all'),lisanNav=boot({},'#lisan/all');
for(const [shell,counts] of [[honNav.shell(),{working:11,outfits:22,details:18}],[lisanNav.shell(),{working:2,outfits:51,details:11}]])for(const [view,count] of Object.entries(counts))assert.match(shell,new RegExp('data-view="'+view+'"[^>]*>[^<]+<span class="count">'+count+'<\\/span>'));
const emptyWorking=boot({},'#criminal_mind/working');assert(!emptyWorking.html().includes('criminal_mind:character-bom'),'Unrelated Criminal Mind media cannot fabricate a Working-reference character card');
assert.equal(families.find(family=>family.id==='TCM-SET-HENDERSON-EXTERIOR').albums.length,2,'Base-look and camera albums share their recorded family');
assert.equal(families.find(family=>family.id==='TCM-SET-HENDERSON-EXTERIOR').lanes.look.length,10);
assert(families.find(family=>family.id==='TCM-SET-HENDERSON-EXTERIOR').lanes.coverage.length>10);
assert.match(page.html(),/24 recorded places/);assert.match(page.html(),/Story &amp; coverage brief|Story & coverage brief/);
assert.equal([...page.html().matchAll(/data-location-asset=/g)].length<=11,true,'Initial filmstrip is bounded');
assert.equal([...page.html().matchAll(/class="location-hero"/g)].length,1,'Only one hero reference is mounted');
assert(!page.html().includes('class="media-card"'),'The location room no longer mounts the generic 956-card gallery');

const before=clone(api.reviewPayload()),catalogBefore=JSON.stringify(api.C);delete before.exported;
page.click('data-location-family','TCM-SET-IMPALA');page.click('data-location-lane','coverage');
let selection=api.locationScoutSelection();assert.equal(selection.family.id,'TCM-SET-IMPALA');assert.equal(selection.lane,'coverage');assert(selection.positions.length>1,'Recorded camera positions become a camera map');
const nextPosition=selection.positions.find(value=>value!==selection.position);page.click('data-location-position',nextPosition);selection=api.locationScoutSelection();assert.equal(selection.position,nextPosition);
if(selection.items.length>1){const first=selection.asset.id;page.click('data-location-step','1');assert.notEqual(api.locationScoutSelection().asset.id,first,'Reference stepping changes only UI focus');}
const after=clone(api.reviewPayload());delete after.exported;assert.deepEqual(after,before,'Family, lane, camera-position and reference navigation do not mutate reviews');
assert.equal(JSON.stringify(api.C),catalogBefore,'Display regrouping never mutates catalog metadata');assert.equal(page.writes.length,0,'Pure scout navigation performs no storage writes');

// Family direction is its own portable record. A note may be drafted before the
// reviewer is declared, but it must not masquerade as an image choice or approval.
const impalaFamilyID='TCM-SET-IMPALA',impalaFamily=families.find(family=>family.id===impalaFamilyID);
assert(impalaFamily&&impalaFamily.items.length,'The real Impala location family is available');
const assetReviewsBeforeDraft=Object.fromEntries(impalaFamily.items.map(asset=>[asset.id,clone(api.reviewRecord(asset.id))]));
const draftNote='Needs to be changed to a Ford Interceptor. The Impala is out of date; what came up was the bar.';
api.route('criminal_mind','locations');page.click('data-location-family',impalaFamilyID);
page.input('[data-location-note]',draftNote);
let familyReview=clone(api.locationReviewRecord('criminal_mind',impalaFamilyID));
assert.equal(familyReview.note,draftNote,'Unattributed location direction is retained as a family draft');
assert(!familyReview.reviewerControllerID,'A draft does not invent a reviewer');
assert.equal(page.storage.has(REVIEW_KEY),true,'Typing location direction writes the browser review backup');
assert.equal(page.writes.some(([key])=>key===REVIEW_KEY),true,'The family draft uses the normal local review persistence');
assert.deepEqual(Object.fromEntries(impalaFamily.items.map(asset=>[asset.id,clone(api.reviewRecord(asset.id))])),assetReviewsBeforeDraft,'A family note creates no image decision or approval');
let familyPayload=clone(api.reviewPayload());
assert(Array.isArray(familyPayload.locationReviews),'Portable reviews expose family-scoped location direction');
assert.equal(familyPayload.locationReviews.find(row=>row.project==='criminal_mind'&&row.locationFamilyID===impalaFamilyID)?.note,draftNote);
api.renderMain();
assert.match(page.visible(),/saved in this browser/i,'The room clearly confirms the local backup');
assert.match(page.visible(),/not (?:sent|shared)|nothing (?:has been sent|uploads automatically)|cannot see[^.]*until[^.]*sent|export[^.]*team|do not notify/i,'The room distinguishes local saving from delivery to the team');

const draftReloaded=boot(page.snapshot(),'#criminal_mind/locations');
familyReview=clone(draftReloaded.api.locationReviewRecord('criminal_mind',impalaFamilyID));
assert.equal(familyReview.note,draftNote,'An unattributed family draft survives a fresh JS context and localStorage reload');
assert(!familyReview.reviewerControllerID,'Reload does not turn a draft into an attributed decision');
assert.deepEqual(Object.fromEntries(impalaFamily.items.map(asset=>[asset.id,clone(draftReloaded.api.reviewRecord(asset.id))])),assetReviewsBeforeDraft,'Reloaded family feedback still creates no asset decision');
draftReloaded.api.route('criminal_mind','locations');draftReloaded.click('data-location-family',impalaFamilyID);
assert.equal(draftReloaded.node('[data-location-note]').value,draftNote,'The restored draft is visible in the actual textarea');
assert.match(draftReloaded.visible(),/saved in this browser/i);
assert.match(draftReloaded.visible(),/not (?:sent|shared)|nothing (?:has been sent|uploads automatically)|cannot see[^.]*until[^.]*sent|export[^.]*team|do not notify/i);

// Exercise the actual room CTA and its generated Blob, not reviewPayload alone.
draftReloaded.click('data-location-export','');
assert.equal(draftReloaded.downloads.length,1,'Location Export review creates one download');
assert.equal(draftReloaded.downloads[0].name,'cfa-criminal_mind-location-review.json');
const portableDraft=JSON.parse(await draftReloaded.downloads[0].blob.text());
assert.equal(portableDraft.handoff?.kind,'location_review');
assert.equal(portableDraft.handoff?.project,'criminal_mind');
const exportedDraft=portableDraft.locationReviews.find(row=>row.project==='criminal_mind'&&row.locationFamilyID===impalaFamilyID);
assert.equal(exportedDraft.note,draftNote,'The downloaded handoff contains the current family draft');
assert(!exportedDraft.reviewerControllerID,'Export does not invent attribution for a draft');
assert.match(draftReloaded.visible(),/exported|download/i,'The export action gives visible confirmation');
const importedDraft=boot({},'#criminal_mind/locations');importedDraft.api.importReview(portableDraft);
assert.equal(importedDraft.api.locationReviewRecord('criminal_mind',impalaFamilyID).note,draftNote,'Downloaded family feedback imports into a clean session');
assert.deepEqual(Object.fromEntries(impalaFamily.items.map(asset=>[asset.id,clone(importedDraft.api.reviewRecord(asset.id))])),assetReviewsBeforeDraft,'Importing family feedback does not approve an asset');

// Declaring the actual reviewer confirms provenance while retaining the same
// location-only scope. It still does not select a set, frame, or asset.
const confirmedPage=boot(draftReloaded.snapshot(),'#criminal_mind/locations');
const assetReviewsBeforeConfirm=Object.fromEntries(impalaFamily.items.map(asset=>[asset.id,clone(confirmedPage.api.reviewRecord(asset.id))]));
confirmedPage.api.route('criminal_mind','locations');confirmedPage.click('data-location-family',impalaFamilyID);
confirmedPage.change('[data-location-reviewer]','baldadoon');
const confirmedReview=clone(confirmedPage.api.locationReviewRecord('criminal_mind',impalaFamilyID));
assert.equal(confirmedReview.note,draftNote);
assert.equal(confirmedReview.reviewerControllerID,'baldadoon','Confirmation records the actual director');
assert.equal(confirmedReview.decisionScope,'location','Family direction remains explicitly location-scoped');
assert.equal(confirmedReview.humanReview?.locationFamilyID,impalaFamilyID,'Attribution identifies the reviewed family, not an arbitrary image');
assert.deepEqual(Object.fromEntries(impalaFamily.items.map(asset=>[asset.id,clone(confirmedPage.api.reviewRecord(asset.id))])),assetReviewsBeforeConfirm,'Attributed family direction still creates no image decision or approval');
familyPayload=clone(confirmedPage.api.reviewPayload());
const portableConfirmed=familyPayload.locationReviews.find(row=>row.project==='criminal_mind'&&row.locationFamilyID===impalaFamilyID);
assert.equal(portableConfirmed.reviewerControllerID,'baldadoon');
assert.equal(portableConfirmed.decisionScope,'location');
assert(!portableConfirmed.status&&!portableConfirmed.workingReference&&!portableConfirmed.castUse&&!portableConfirmed.shotPlan,'A location note carries no asset approval fields');

// A publication seed restores family direction in a clean browser. Older local
// backups and imported JSON cannot roll it back; conflicts remain exportable.
const currentNote={...clone(portableConfirmed),updatedAt:'2026-11-06T12:00:00Z'};
const oldNote={...clone(currentNote),note:'Earlier draft',updatedAt:'2026-11-05T12:00:00Z'};
const noteEnvelope=record=>({format:REVIEW_KEY,items:[],favorites:[],locationReviews:[record]});
const seeded=boot({},'#criminal_mind/locations',{locationReviews:[currentNote]});
assert.equal(seeded.api.locationReviewRecord('criminal_mind',impalaFamilyID).note,currentNote.note,'Published family note seeds a clean browser');
const archivedReceipt={id:'archive-only-receipt',sha256:'a'.repeat(64),note:'Original reviewer receipt',humanReview:{reviewerControllerID:'baldadoon',fields:['note']}};
const publishedEvidence=boot({},'#criminal_mind/locations',{validationEvidence:{format:'cfa-reference-validation-v1',schemaVersion:1,assessments:[],legacyReviewArchive:[archivedReceipt]}});
assert(publishedEvidence.api.reviewPayload().validationEvidence.legacyReviewArchive.some(row=>row.id===archivedReceipt.id&&row.humanReview?.reviewerControllerID==='baldadoon'),'Catalog publication archive survives a clean browser export without becoming an active decision');
assert(!publishedEvidence.api.reviewPayload().items.some(row=>row.id===archivedReceipt.id),'Archived attribution never activates an image decision');
const provenanceExtra={...clone(currentNote),humanReview:{...clone(currentNote.humanReview),sourceReceipt:'director-original-export'},reviewer:'Director-provided label'};
const provenancePage=boot({},'#criminal_mind/locations',{locationReviews:[provenanceExtra]});
assert(provenancePage.api.reviewPayload().locationReviewBackups.some(item=>item.data.humanReview?.sourceReceipt==='director-original-export'&&item.data.reviewer==='Director-provided label'),'Supplied nested provenance and reviewer labels remain recoverable when normalization rewrites them');
const draftProvenance={...clone(currentNote),reviewerControllerID:'unrecognized-reviewer',humanReview:{sourceReceipt:'unconfirmed-original'}};
provenancePage.api.importReview(noteEnvelope(draftProvenance));
assert(provenancePage.api.reviewPayload().locationReviewBackups.some(item=>item.data.humanReview?.sourceReceipt==='unconfirmed-original'),'Unconfirmed supplied provenance is backed up without inventing confirmation');
const staleBrowser=boot({[REVIEW_KEY]:JSON.stringify(noteEnvelope(oldNote))},'#criminal_mind/locations',{locationReviews:[currentNote]});
assert.equal(staleBrowser.api.locationReviewRecord('criminal_mind',impalaFamilyID).note,currentNote.note,'Stale localStorage cannot replace newer published direction');
seeded.api.importReview(noteEnvelope(oldNote));
assert.equal(seeded.api.locationReviewRecord('criminal_mind',impalaFamilyID).note,currentNote.note,'Stale JSON cannot replace newer direction');
const conflict={...clone(currentNote),note:'Conflicting same-time suggestion'};
seeded.api.importReview(noteEnvelope(conflict));
seeded.api.importReview(noteEnvelope({...clone(oldNote),updatedAt:null}));
assert.equal(seeded.api.locationReviewRecord('criminal_mind',impalaFamilyID).note,currentNote.note,'Equal-time and undated notes cannot erase current work');
assert(seeded.api.reviewPayload().locationReviewBackups.some(item=>item.data.note===oldNote.note),'Old note is retained in the complete review backup');
assert(seeded.api.reviewPayload().locationReviewBackups.some(item=>item.data.note===conflict.note),'Conflicting note is retained for reconciliation');
const clear={...clone(currentNote),note:'',updatedAt:'2026-11-07T12:00:00Z'};
seeded.api.importReview(noteEnvelope(clear));
assert.equal(seeded.api.locationReviewRecord('criminal_mind',impalaFamilyID).note,'','A newer dated explicit clear is respected');
assert(seeded.api.reviewPayload().locationReviewBackups.some(item=>item.data.note===currentNote.note),'Cleared text remains recoverable in backup');
seeded.api.importReview(noteEnvelope({...clone(oldNote),locationFamilyID:'unknown-future-family'}));
assert(seeded.api.reviewPayload().locationReviewBackups.some(item=>item.data.locationFamilyID==='unknown-future-family'),'Unknown family feedback is preserved without rebinding');
const seededAgain=boot(seeded.snapshot(),'#criminal_mind/locations',{locationReviews:[currentNote]});
assert.equal(seededAgain.api.locationReviewRecord('criminal_mind',impalaFamilyID).note,'','Explicit clear survives fresh context plus older catalog seed');
assert.deepEqual(clone(seededAgain.api.reviewPayload().items),clone(seeded.api.reviewPayload().items),'Family-note reconciliation never changes asset reviews');

api.setCasaStage('locations');api.route('criminal_mind','casa_baldadoon');assert.match(page.html(),/Director’s chair · Location scout/);assert.match(page.html(),/Open shared Locations library/);assert.equal(api.locationScoutSelection().family.id,'TCM-SET-IMPALA','Casa reuses the shared scout selection and inventory');
for(const project of ['hon','lisan']){api.route(project,'locations');assert.equal(api.getState().view,'locations');assert.match(page.html(),/No location families have been recorded for this project yet/);}

api.route('criminal_mind','locations');
const henderson='TCM-SET-HENDERSON-EXTERIOR-L03',sibling='TCM-SET-HENDERSON-EXTERIOR-L02',sourceAsset=api.C.assets.find(asset=>asset.id===henderson);
assert(sourceAsset.relayedAuthorChoiceSignal,'The narrowly scoped relayed author signal remains catalog evidence');
assert.equal(sourceAsset.relayedAuthorChoiceSignal.reviewEvidenceStatus,'recovered_favorite_or_basket_only_no_attributed_saved_review');
assert.equal(api.reviewRecord(henderson).note,'','No missing Henderson note is invented or misattributed');
page.click('data-location-family','TCM-SET-HENDERSON-EXTERIOR');page.click('data-location-lane','look');page.click('data-location-asset',henderson);page.click('data-location-review',henderson);
assert.equal(api.selectedReviewScope('criminal_mind'),'location','The scout review entry point preselects an exact location decision scope');assert.equal(api.reviewRecord(henderson).note,'');
api.setReviewIdentity('criminal_mind','baldadoon','location');
assert.equal(api.updateReview(henderson,{note:'Synthetic location-only direction for round-trip testing.'}),true);
let record=clone(api.reviewRecord(henderson));assert.equal(record.decisionScope,'location');assert.equal(record.reviewerControllerID,'baldadoon');assert.equal(record.humanReview.assetID,henderson);assert.equal(record.humanReview.sha256,sourceAsset.sha256);assert.equal(record.status,null,'A note does not choose a review outcome');assert.equal(api.reviewRecord(sibling).note,'','Sibling options remain untouched');
api.route('criminal_mind','all');api.route('criminal_mind','locations');assert.equal(api.reviewRecord(henderson).note,record.note,'Location-only note survives navigation');
const exported=clone(api.reviewPayload()),restored=boot({},'#criminal_mind/locations');restored.api.importReview(exported);record=clone(restored.api.reviewRecord(henderson));assert.equal(record.note,'Synthetic location-only direction for round-trip testing.');assert.equal(record.decisionScope,'location');assert.equal(record.humanReview.assetID,henderson);assert.equal(record.humanReview.sha256,sourceAsset.sha256);assert.equal(restored.api.reviewRecord(sibling).note,'');

console.log(JSON.stringify({passed:true,families:families.length,assets:956,uniqueHashes:954,boundedFilmstrip:11,sharedProjects:3,locationDraftReload:true,locationExportRoundTrip:true,locationNoteRoundTrip:true,browserVisualQA:false}));
}

main().catch(error=>{console.error(error);process.exitCode=1;});
