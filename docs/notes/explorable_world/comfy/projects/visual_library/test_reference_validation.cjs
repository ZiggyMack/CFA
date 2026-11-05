
/* Real renderer/storage code with DOM doubles. No production evidence written. */
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const clone=v=>JSON.parse(JSON.stringify(v));
const source=fs.readFileSync(path.join(__dirname,'library.js'),'utf8');
const catalog=JSON.parse(fs.readFileSync(path.join(__dirname,'catalog.js'),'utf8').split('=').slice(1).join('=').trim().replace(/;$/,''));
const validation=JSON.parse(fs.readFileSync(path.join(__dirname,'reference_validation.json'),'utf8'));
const mouth=JSON.parse(fs.readFileSync(path.join(__dirname,'mouth_coverage.json'),'utf8'));
catalog.referenceValidation=validation;catalog.mouthCoverage=mouth;
for(const a of mouth.media)if(!catalog.assets.some(x=>x.id===a.id))catalog.assets.push({...a,src:a.repoPath,thumb:a.repoPath,album:'lisan:'+a.group});
const REVIEW_KEY='cfa-visual-review-v1',FAVORITES_KEY='cfa-visual-favorites-v1',EXPORT_KEY='cfa-visual-export-v1',VK='cfa-reference-validation-v1';
const byID=new Map(catalog.assets.map(a=>[a.id,a]));
let harness=fs.readFileSync(path.join(__dirname,'test_collections_navigation.cjs'),'utf8');
harness=harness.slice(harness.indexOf('function boot() {'),harness.indexOf('\nconst page = boot(), api = page.api;'));
harness=harness.replace('function boot() {','function boot(seed={},chosenCatalog=catalog,chosenSource=source) {')
.replace('new Map(Object.entries(saved))','new Map(Object.entries({...saved,...seed}))')
.replace('REVIEW_CATALOG:clone(catalog)','REVIEW_CATALOG:clone(chosenCatalog)')
.replace('const instrumented = source.replace','const instrumented = chosenSource.replace')
.replace("assert.notEqual(instrumented, source","assert.notEqual(instrumented, chosenSource")
.replace('querySelectorAll() {return [];}','querySelectorAll(selector) {return selectAll(selector).filter(e=>this.children.has(e));}')
.replace('window.__collectionsTest={','window.__collectionsTest={validationAssessment,validationSummary,validationLatest,validationHistory,validationEnvelope,checkValidationEnvelope,importValidation,importReview,saveBrowserReview,updateReview,sceneReviewRecord,sceneHandoffGate,validationTechnicalGate,validationSceneBinding,shotHandoffPayload,mouthCoverageStats,mouthCoverageBoard,workflowStageControls,openViewer,dialog,writeReviewFile,setFileHandle(h){reviewFileHandle=h;},')
.replace('html:() => nodes.get','nodes,selectAll,context,html:() => nodes.get');
const boot=eval('('+harness.replace(/^function boot/,'function')+')');
const checks=[];function check(name,fn){fn();checks.push(name);}
function evidencePreserved(actual,expected){
 const rows=v=>v.map(x=>JSON.stringify(x)).sort();
 assert.deepEqual(rows(actual.assessments),rows(expected.assessments),'All immutable assessments survive');
 for(const key of ['legacyReviewArchive','unreadBackups']){const got=new Set(rows(actual[key]||[]));for(const row of rows(expected[key]||[]))assert(got.has(row),'Exact archived record survives: '+key);}
}
const page=boot(),api=page.api;
const before=clone(api.reviewPayload());
const originalSource=fs.readFileSync(path.join(__dirname,'../collaborators/site_publication_20261013/reference_validation_20261013/source_before/library.js'),'utf8');
// Baseline source gets its original test hook rather than new-function references.
let oldHarness=harness.replace('chosenSource.replace','chosenSource.replace');
const hookStart=oldHarness.indexOf('window.__collectionsTest={'), hookEnd=oldHarness.indexOf('collectionCards,',hookStart);
oldHarness=oldHarness.slice(0,hookStart)+'window.__collectionsTest={'+oldHarness.slice(hookEnd);
const oldBoot=eval('('+oldHarness.replace(/^function boot/,'function')+')'),old=oldBoot({},catalog,originalSource);
check('Canonical reviews and runtime legacy behavior preserved',()=>{
 const canonical=JSON.parse(fs.readFileSync(path.join(__dirname,'../hon_dolo_strictly_business/feedback/review_decisions.json'),'utf8')).items;
 assert.deepEqual(catalog.reviewDecisions,canonical);
 // Archive choices were dropped by the 20261013 runtime; the new UI preserves that existing field.
 const oldPayload=clone(old.api.reviewPayload());
 // This explicit visual-duplicate family now shares the newest review; its raw records remain below.
 const alias=catalog.assetAliases.find(a=>a.id==='HD-MOUTH-UPDATE-20261009-01'&&a.canonicalID==='HD-B-91ef00348229');
 assert(alias&&alias.kind==='visual_duplicate_reencoding','Only the declared visual duplicate explains the baseline change');
 const canonicalReview=canonical.find(r=>r.id===alias.canonicalID),duplicateReview=canonical.find(r=>r.id===alias.id);
 assert.equal(canonicalReview.sha256,alias.canonicalSHA256);assert.equal(duplicateReview.sha256,alias.sha256);
 assert.equal(byID.get(alias.canonicalID).sha256,alias.canonicalSHA256);assert(!byID.has(alias.id));
 const reviewFields=({id,filename,path,sha256,updatedAt,...fields})=>fields;
 assert.deepEqual(reviewFields(duplicateReview),reviewFields(canonicalReview),'The two actual saved reviews differ only in asset identity and timestamp');
 assert(Date.parse(duplicateReview.updatedAt)>Date.parse(canonicalReview.updatedAt),'The duplicate carries the newer saved decision');
 const expectedItems=clone(oldPayload.items),expectedCanonical=expectedItems.find(r=>r.id===alias.canonicalID);
 assert.equal(expectedCanonical.updatedAt,canonicalReview.updatedAt);
 expectedCanonical.updatedAt=duplicateReview.updatedAt;
 assert.deepEqual(clone(before.items).map(({collectionState,...record})=>record),expectedItems,'Every pre-Archive review field is unchanged except this verified newer alias-family timestamp');
 const oldHashProbe=clone(validation.assessments[0]);oldHashProbe.target={...oldHashProbe.target,assetID:alias.id,sha256:alias.sha256};
 const oldHashResult=api.validationAssessment(oldHashProbe);
 assert(oldHashResult.reasons.includes('Target image is missing.'),'Visual aliases never redirect hash-bound validation evidence');
 assert.notEqual(oldHashResult.status,'pass');
 for(const record of canonical.filter(r=>['archived','working'].includes(r.collectionState)))assert.equal(before.items.find(r=>r.id===record.id)?.collectionState,record.collectionState,'Canonical archive choice is retained: '+record.id);
 for(const field of ['sceneReviews','favorites','exportBasket'])assert.deepEqual(clone(before[field]),oldPayload[field]);
 const archive=api.validationEnvelope().legacyReviewArchive;
 for(const record of catalog.reviewDecisions)assert(archive.some(r=>JSON.stringify(r)===JSON.stringify(record)));
 assert.equal(catalog.reviewDecisions.filter(r=>r.storyboardStage==='verification').length,18);
 for(const r of catalog.reviewDecisions.filter(r=>r.storyboardStage==='verification'))assert.equal(api.validationSummary(byID.get(r.id),'character').status,'not_checked');
 assert.equal(page.writes.length,0);
});
const dental=validation.criteriaSets.find(c=>c.id==='hon-dental'),first=validation.assessments.find(a=>a.target.assetID==='HD-B-ef471a1f5e46'&&a.axis==='character');
function fixture(id='synthetic-pass'){const a=clone(first);a.id=id;a.criteria={id:dental.id,version:dental.version,sha256:dental.sha256};a.scope=clone(dental.scope);a.status='pass';a.criteriaResults=a.criteriaResults.filter(c=>c.criterionID!=='articulation');a.reviewer.reviewedAtUTC='2026-10-14T01:00:00Z';return a;}
const envelope=assessments=>({format:VK,schemaVersion:1,assessments});
check('independent axes, N/A and scoped pass',()=>{
 const a=fixture();assert.equal(api.validationAssessment(a).status,'pass');assert.equal(api.validationAssessment(a).current,true);
 assert.equal(api.validationSummary(byID.get(a.target.assetID),'scene').applicability,'not_applicable');
 const na=clone(a);na.axis='scene';na.applicability='not_applicable';assert.notEqual(api.validationAssessment(na).status,'pass');
 assert.equal(api.validationSummary(byID.get('HD-B-125e06fc0938'),'character').status,'fail');
});
check('missing target/reference pixels and required occlusion cannot pass',()=>{
 for(const change of [a=>a.imagesSeen=[],a=>a.imagesSeen[0].accessible=false,a=>a.imagesSeen[1].view='contact_sheet',a=>a.reference=null,a=>a.criteriaResults[0].visibility='occluded',a=>a.criteriaResults.pop(),a=>a.evidence='']){
  const a=fixture();change(a);assert.notEqual(api.validationAssessment(a).status,'pass');
 }
});
check('required jewelry versus allowed natural variation',()=>{
 const a=fixture();a.criteriaResults.find(r=>r.criterionID==='lip-rings').outcome='fail';assert.equal(api.validationAssessment(a).status,'fail');
 a.criteriaResults.find(r=>r.criterionID==='lip-rings').outcome='pass';a.criteriaResults.find(r=>r.criterionID==='lip-rings').observation='Two plain hoops with slightly asymmetric placement, permitted by scope.';assert.equal(api.validationAssessment(a).status,'pass');
});
check('target, reference, nomination, scope, version and criteria invalidation',()=>{
 const a=fixture(),c=page.C.referenceValidation.criteriaSets.find(c=>c.id===dental.id),n=page.C.referenceValidation.inventory.find(n=>n.id===c.nominationID),target=page.C.assets.find(x=>x.id===a.target.assetID),ref=page.C.assets.find(x=>x.id===a.reference.assetID);
 for(const [obj,key,value] of [[target,'sha256','0'.repeat(64)],[ref,'referenceVersion','new-revision'],[n,'reference',{...n.reference,sha256:'1'.repeat(64)}],[n,'scope','whole_actor'],[c,'version','next'],[c,'allowedVariation','Changed without advertised digest']]){
  const prior=clone(obj[key]??null),had=Object.hasOwn(obj,key);obj[key]=value;const result=api.validationAssessment(a);assert.notEqual(result.status,'pass');if(had)obj[key]=prior;else delete obj[key];
 }
});
check('atomic nested validation and immutable collisions',()=>{
 const count=api.validationHistory.size;
 for(const change of [a=>a.imagesSeen=[null],a=>a.criteriaResults=[null],a=>a.criteriaResults[0].outcome='invented',a=>a.reviewer.name='']){
  const a=fixture();change(a);assert.throws(()=>api.importValidation(envelope([a])));assert.equal(api.validationHistory.size,count);
 }
 api.importValidation(envelope([fixture()]));const after=api.validationHistory.size;
 api.importValidation(envelope([fixture()]));assert.equal(api.validationHistory.size,after);
 const collision=fixture();collision.evidence='Different';assert.throws(()=>api.importValidation(envelope([fixture('another'),collision])));assert.equal(api.validationHistory.size,after);
});
check('history and old backup imports never clear evidence',()=>{
 const oldCount=api.validationHistory.size;
 api.importReview({format:REVIEW_KEY,items:clone(before.items),favorites:clone(before.favorites),exportBasket:clone(before.exportBasket)});
 assert.equal(api.validationHistory.size,oldCount);
 const earlier=fixture('earlier-uncertain');earlier.status='uncertain';earlier.reviewer.reviewedAtUTC='2026-10-12T00:00:00Z';api.importValidation(envelope([earlier]));
 assert.equal(api.validationLatest(first.target.assetID,'character',dental.id)[0].id,'synthetic-pass');
 for(const field of ['items','sceneReviews','favorites','exportBasket'])assert.deepEqual(clone(api.reviewPayload()[field]),before[field]);
});
check('sidecar restart and full-review round trip retain raw archive and history',()=>{
 const restored=boot(Object.fromEntries(page.storage));evidencePreserved(clone(restored.api.validationEnvelope()),clone(api.validationEnvelope()));
 const fresh=boot();fresh.api.importReview(clone(api.reviewPayload()));evidencePreserved(clone(fresh.api.validationEnvelope()),clone(api.validationEnvelope()));
});
check('evidence-only storage failure does not interrupt legacy saves',()=>{
 const p=boot(),set=p.context.localStorage.setItem;p.context.localStorage.setItem=(key,value)=>{if(key===VK)throw Error('quota');set(key,value);};
 p.api.updateReview('HD-B-31e4e53fdc8a',{note:'Synthetic persistence check'});
 const saved=JSON.parse(p.storage.get(REVIEW_KEY));assert.equal(saved.items.find(a=>a.id==='HD-B-31e4e53fdc8a').note,'Synthetic persistence check');assert(p.writes.some(([key])=>key===FAVORITES_KEY));assert(p.writes.some(([key])=>key===EXPORT_KEY));
});
check('corrupt/future evidence storage remains exportable and unmodified',()=>{
 for(const raw of ['{broken',JSON.stringify({format:VK,schemaVersion:99,assessments:[]})]){
  const p=boot({[VK]:raw});p.api.saveBrowserReview();assert.equal(p.storage.get(VK),raw);assert.throws(()=>p.api.importValidation(envelope([fixture()])));
  const backed=p.api.reviewPayload().validationEvidence;assert(backed.unreadBackups.some(b=>b.sourceKey===VK&&b.raw===raw));assert.equal(backed.assessments.length,validation.assessments.length);
 }
});
check('failed evidence save keeps the visible export warning',()=>{
 const p=boot(),set=p.context.localStorage.setItem;p.context.localStorage.setItem=(key,value)=>{if(key===VK)throw Error('quota');set(key,value);};
 p.api.importValidation(envelope([fixture('quota-test')]));
 const messages=[...p.context.document.body.children].map(n=>n.textContent).filter(Boolean);
 assert(messages.at(-1).includes('browser evidence backup failed'));assert(p.api.validationEnvelope().assessments.some(a=>a.id==='quota-test'));
});
check('unread stores retain raw metadata and valid histories independently',()=>{
 const future={format:VK,schemaVersion:99,assessments:[{id:'future-record',custom:'retain me'}]};
 const custom={...before.items[0],customProvenance:{source:'Original full metadata'}};
 const legacyRaw=JSON.stringify({format:REVIEW_KEY,items:[custom],validationEvidence:future});
 const valid=envelope([fixture('valid-sidecar')]);
 const p=boot({[REVIEW_KEY]:legacyRaw,[VK]:JSON.stringify(valid)});p.api.saveBrowserReview();
 let result=p.api.reviewPayload().validationEvidence;
 assert(result.assessments.some(a=>a.id==='valid-sidecar'));assert(result.unreadBackups.some(b=>b.sourceKey===REVIEW_KEY&&b.raw===legacyRaw));
 assert(result.legacyReviewArchive.some(r=>r.customProvenance?.source==='Original full metadata'));
 const q=boot({[REVIEW_KEY]:JSON.stringify({format:REVIEW_KEY,items:[custom],validationEvidence:valid}),[VK]:'{broken'});
 result=q.api.reviewPayload().validationEvidence;assert(result.assessments.some(a=>a.id==='valid-sidecar'));assert(result.unreadBackups.some(b=>b.raw==='{broken'));assert(result.legacyReviewArchive.some(r=>r.customProvenance));
 q.api.saveBrowserReview();const restarted=boot(Object.fromEntries(q.storage));evidencePreserved(clone(restarted.api.validationEnvelope()),clone(q.api.validationEnvelope()));
 const restored=boot();restored.api.importReview(clone(q.api.reviewPayload()));evidencePreserved(clone(restored.api.validationEnvelope()),clone(q.api.validationEnvelope()));
 const oldItems=clone(q.api.reviewPayload().items),oldEvidence=clone(q.api.validationEnvelope());
 assert.throws(()=>q.api.importReview({format:REVIEW_KEY,items:[{...custom,note:'Do not apply'}],validationEvidence:envelope([fixture('blocked-full')])}));
 assert.deepEqual(clone(q.api.reviewPayload().items),oldItems);assert.deepEqual(clone(q.api.validationEnvelope()),oldEvidence);
});
check('newer unrelated N/A cannot hide a current applicable pass',()=>{
 const c=clone(catalog);c.referenceValidation.assessments=c.referenceValidation.assessments.filter(a=>a.target.assetID!==first.target.assetID);
 const p=boot({},c),a=fixture('only-pass'),na=clone(a);na.id='later-na';na.criteria=null;na.reference=null;na.scope={id:'unrelated-na',kind:'none',label:'Unrelated scope'};na.applicability='not_applicable';na.status='not_checked';na.criteriaResults=[];na.reviewer.reviewedAtUTC='2026-10-15T01:00:00Z';
 p.api.importValidation(envelope([a,na]));const summary=p.api.validationSummary(p.C.assets.find(x=>x.id===a.target.assetID),'character');assert.equal(summary.status,'pass');assert.equal(summary.applicability,'required');assert.equal(summary.scopeResults.length,2);
});
function withSceneCriteria(){
 const c=clone(catalog),d=clone(dental),n=clone(c.referenceValidation.inventory.find(n=>n.id===d.nominationID));
 d.id='synthetic-scene';d.axis='scene';d.title='Synthetic scene criterion';d.scope={id:d.id,kind:'scene',label:d.title};d.nominationID='synthetic-scene-nomination';d.nominationScope='scene';n.id=d.nominationID;n.scope='scene';
 c.referenceValidation.criteriaSets.push(d);c.referenceValidation.inventory.push(n);return c;
}
check('character and scene form criteria with identical IDs remain independent',()=>{
 for(const axis of ['character','scene']){
  const c=withSceneCriteria(),p=boot({},c),id=first.target.assetID;p.api.openViewer(id);const original=clone(p.api.reviewPayload().items);
  const field=(a,key)=>p.selectAll('[data-v-field]').find(n=>n.dataset.vAxis===a&&n.dataset.vField===key);
  for(const a of ['character','scene']){
   const choice=field(a,'criteria');choice.value=a==='character'?'hon-dental':'synthetic-scene';for(const f of choice.listeners.get('change')||[])f({target:choice});
   field(a,'reviewer').value='Synthetic '+a;field(a,'model').value='human';field(a,'status').value=a==='character'?'fail':'pass';field(a,'applicability').value='required';field(a,'evidence').value='Synthetic '+a+' observation';field(a,'uncertainty').value='Test only';field(a,'seen').checked=true;
  }
  p.selectAll('[data-v-visibility]').forEach(n=>n.value='visible');p.selectAll('[data-v-outcome]').forEach(n=>n.value=n.dataset.vAxis==='character'?'fail':'pass');p.selectAll('[data-v-observation]').forEach(n=>n.value='Observed '+n.dataset.vAxis);
  p.selectAll('[data-v-save]').find(n=>n.dataset.vSave===axis).click();
  const record=p.api.validationLatest(id,axis,axis==='character'?'hon-dental':'synthetic-scene').find(a=>a.reviewer.name==='Synthetic '+axis);
  assert(record);assert(record.criteriaResults.every(r=>r.observation==='Observed '+axis));assert.equal(p.api.validationAssessment(record).status,axis==='character'?'fail':'pass');assert.deepEqual(clone(p.api.reviewPayload().items),original);
 }
});
check('all scopes stay visible; narrower pass cannot hide unresolved work',()=>{
 const p=boot();p.api.importValidation(envelope([fixture()]));const summary=p.api.validationSummary(p.C.assets.find(a=>a.id===first.target.assetID),'character');
 assert(summary.scopeResults.length>=2);assert.notEqual(summary.status,'pass');assert(p.api.validationPanel?true:summary.label.includes('scopes'));
});
check('technical readiness requires declarations bound to ingredients and shoot plan',()=>{
 const p=boot(),shot=p.C.shotMaterials.shots.find(s=>s.project==='hon'),r=p.api.sceneReviewRecord('hon',shot.id),a=fixture();
 r.grade='B';r.criticalBlockers=[];r.ingredients=[{id:'required-mouth',kind:'reference',role:'detail',label:'Mouth',assetID:a.target.assetID,sha256:a.target.sha256,required:true,status:'ready',note:'Synthetic'}];
 r.shootPlan={direction:'Synthetic action',camera:'Synthetic camera',lighting:'Synthetic light',reviewStatus:'verified',reviewedBy:'Fixture',reviewedAt:'2026-10-14T01:00:00Z',note:''};
 assert.equal(p.api.sceneHandoffGate(r).productionEligible,true);assert.equal(p.api.validationTechnicalGate(r).technicalReady,false);
 p.api.importValidation(envelope([a]));
 const plan={project:r.project,shotID:r.shotID,version:'test1',provenance:{source:'Synthetic fixture'},binding:p.api.validationSceneBinding(r),requiredChecks:[{ingredientID:'required-mouth',assetID:a.target.assetID,axis:'character',criteriaID:dental.id,scopeID:dental.scope.id,label:'Mouth scope'}]};
 p.C.referenceValidation.sceneUses.push(plan);assert.equal(p.api.validationTechnicalGate(r).technicalReady,true);
 r.ingredients[0].assetID='HD-B-31e4e53fdc8a';assert.equal(p.api.validationTechnicalGate(r).technicalReady,false);r.ingredients[0].assetID=a.target.assetID;
 r.shootPlan.direction='Changed action';assert.equal(p.api.validationTechnicalGate(r).technicalReady,false);
});
check('mouth board counts and actual toggle/asset handlers',()=>{
 const p=boot();p.api.setState({project:'hon',view:'working',album:''});p.api.renderMain();
 const character=p.selectAll('[data-collection-toggle]').find(n=>n.dataset.collectionToggle==='hon:character-bom');assert(character);character.click();
 const stats=p.api.mouthCoverageStats(p.C.mouthCoverage.looks.find(l=>l.id==='hon-external-off'));assert.equal(stats.files,50);assert.equal(stats.labels,50);assert.equal(stats.validatedLabels,0);assert.equal(stats.distinctUsable,null);
 const toggle=p.selectAll('[data-mouth-look]').find(n=>n.dataset.mouthLook==='hon-external-off');assert(toggle);
 assert(p.html().includes('data-mouth-look="hon-external-off" aria-expanded="true"'));assert(p.html().includes('09/10: different bytes'));
 assert(!p.html().includes('class="mouth-metrics"'));assert(p.html().includes('<details><summary>Core articulation labels'));
 toggle.click();assert(!p.html().includes('09/10: different bytes'));
 p.selectAll('[data-mouth-look]').find(n=>n.dataset.mouthLook==='hon-external-off').click();assert(p.html().includes('09/10: different bytes'));
 const open=p.selectAll('[data-open]').find(n=>n.dataset.open==='HD-B-31e4e53fdc8a');assert(open);open.click();assert(p.api.dialog.innerHTML.includes('data-validation-axis="character"'));assert(p.api.dialog.innerHTML.includes('data-validation-axis="scene"'));
 const lag=p.C.mouthCoverage.looks.find(l=>l.id==='lisan-natural'),ls=p.api.mouthCoverageStats(lag);assert.equal(ls.files,89);assert.equal(ls.labels,49);assert.equal(ls.acceptedFiles,7);assert.equal(ls.acceptedLabels,5);
 assert.equal(p.C.mouthCoverage.recipe.requiredStillAtlasSlots,0);
});
check('actual evidence form saves a scoped record without changing stars',()=>{
 const p=boot(),id='HD-B-31e4e53fdc8a';p.api.openViewer(id);const original=clone(p.api.reviewPayload().items);
 const field=key=>p.selectAll('[data-v-field]').find(n=>n.dataset.vAxis==='character'&&n.dataset.vField===key);
 field('criteria').value='hon-dental';for(const f of field('criteria').listeners.get('change')||[])f({target:field('criteria')});
 field('reviewer').value='Synthetic human';field('model').value='human';field('status').value='pass';field('applicability').value='required';field('evidence').value='Synthetic form handler check';field('uncertainty').value='Test only';field('seen').checked=true;
 p.selectAll('[data-v-visibility]').forEach(n=>n.value='visible');p.selectAll('[data-v-outcome]').forEach(n=>n.value='pass');p.selectAll('[data-v-observation]').forEach(n=>n.value='Synthetic observed requirement');
 const save=p.selectAll('[data-v-save]').find(n=>n.dataset.vSave==='character');save.click();
 assert(p.api.validationLatest(id,'character','hon-dental').some(a=>a.reviewer.name==='Synthetic human'));assert.deepEqual(clone(p.api.reviewPayload().items),original);assert(p.storage.has(VK));
});
(async()=>{
 const p=boot();let contents='';p.api.setFileHandle({name:'synthetic-review.json',async createWritable(){return {async write(v){contents=v;},async close(){},async abort(){}};}});
 await p.api.writeReviewFile();const data=JSON.parse(contents);assert.equal(data.validationEvidence.format,VK);assert.deepEqual(data.items,clone(p.api.reviewPayload().items));checks.push('real serialized review-file writer includes evidence and preserved legacy archive');
 console.log(JSON.stringify({passed:true,scenarios:checks.length,checks,browserVisualQA:false,productionWrites:0,syntheticAssessmentsPersistedToSource:0},null,2));
})().catch(e=>{console.error(e);process.exitCode=1;});
