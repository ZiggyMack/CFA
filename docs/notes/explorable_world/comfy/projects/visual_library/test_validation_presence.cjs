/* Presence is separate from visibility and outcome. Synthetic evidence only;
   real source definitions and the real renderer run against isolated storage. */
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const clone=value=>JSON.parse(JSON.stringify(value));
const source=fs.readFileSync(path.join(__dirname,'library.js'),'utf8');
const raw=fs.readFileSync(path.join(__dirname,'catalog.js'),'utf8');
const catalog=JSON.parse(raw.slice(raw.indexOf('=')+1).trim().replace(/;$/,''));
const validation=JSON.parse(fs.readFileSync(path.join(__dirname,'reference_validation.json'),'utf8'));
catalog.referenceValidation=validation;
const REVIEW_KEY='cfa-visual-review-v1',FAVORITES_KEY='cfa-visual-favorites-v1',EXPORT_KEY='cfa-visual-export-v1',VK='cfa-reference-validation-v1';
const byID=new Map(catalog.assets.map(a=>[a.id,a]));
let harness=fs.readFileSync(path.join(__dirname,'test_collections_navigation.cjs'),'utf8');
harness=harness.slice(harness.indexOf('function boot() {'),harness.indexOf('\nconst page = boot(), api = page.api;'));
harness=harness.replace('function boot() {','function boot(seed={},chosenCatalog=catalog) {')
 .replace('new Map(Object.entries(saved))','new Map(Object.entries({...saved,...seed}))')
 .replace('REVIEW_CATALOG:clone(catalog)','REVIEW_CATALOG:clone(chosenCatalog)')
 .replace('querySelectorAll() {return [];}','querySelectorAll(selector) {return selectAll(selector).filter(e=>this.children.has(e));}')
 .replace('window.__collectionsTest={','window.__collectionsTest={dialog,validationAssessment,validationPanel,validationLatest,validationHistory,validationEnvelope,checkValidationEnvelope,importValidation,importReview,openViewer,vBinding,')
 .replace('html:() => nodes.get','nodes,selectAll,context,html:() => nodes.get');
const boot=eval('('+harness.replace(/^function boot/,'function')+')');
const page=boot(),api=page.api;
const active=validation.criteriaSets.find(c=>c.id==='hon-face-piercings');
const legacy=validation.criteriaSets.find(c=>c.id==='hon-face');
assert(active&&legacy,'New and historical Hon criteria definitions coexist');
assert.equal(active.version,'2026-10-27.1');
const presenceIDs=active.criteria.filter(c=>c.presenceRequired).map(c=>c.id);
assert.deepEqual(presenceIDs,['ear-piercings','nose-piercings','lip-piercings']);
assert.deepEqual(active.criteria.map(c=>c.id),['face',...presenceIDs]);
assert(legacy.criteria.some(c=>c.id==='no-dice'),'Historical forehead criterion is retained');
assert.equal(legacy.sha256,'87425efbb49dc395c8c655ba28d4ffd79b37332d9d2b5b866f45cd80ec169b25','Historical definition binding remains unchanged');
assert(validation.inactiveCriteriaSetIDs.includes(legacy.id),'Historical criteria are retired only from new entry');
const target=byID.get('HD-FALCON-381883a6beb1ed5e');assert(target);
function fixture(id='presence-fixture',definition=active){
 return {schemaVersion:1,id,target:clone(api.vBinding(target)),axis:definition.axis,applicability:'required',status:'pass',
  scope:clone(definition.scope),criteria:{id:definition.id,version:definition.version,sha256:definition.sha256},reference:clone(definition.reference),
  reviewer:{name:'Synthetic test only',model:'human',surface:'Isolated DOM regression',reviewedAtUTC:'2026-10-27T12:00:00Z'},
  imagesSeen:[{...clone(api.vBinding(target)),accessible:true,view:'original'},{...clone(definition.reference),accessible:true,view:'original'}],
  criteriaResults:definition.criteria.map(c=>({criterionID:c.id,visibility:'visible',outcome:'pass',observation:'Synthetic presence regression evidence',...(c.presenceRequired?{presence:'present'}:{})})),
  evidence:'Synthetic comparison for regression testing only',uncertainty:'',provenance:{source:'Isolated JS test'}};
}
const envelope=assessments=>({format:VK,schemaVersion:1,assessments});
const checks=[];function check(name,fn){fn();checks.push(name);}

check('present visible passing piercings can pass the stated scope',()=>{
 const assessment=fixture();api.checkValidationEnvelope(envelope([assessment]));
 const result=api.validationAssessment(assessment);assert.equal(result.status,'pass');assert.equal(result.current,true);
 assert.equal(result.definition.wholeActorApproval,false,'The scope is not whole-actor approval');
});

check('absent unknown or unstated presence cannot pass',()=>{
 for(const criterionID of presenceIDs){
  for(const value of ['absent','unknown',undefined]){
   const assessment=fixture(),row=assessment.criteriaResults.find(r=>r.criterionID===criterionID);
   if(value===undefined)delete row.presence;else row.presence=value;
   // Presence is optional for importing old evidence, but not sufficient for a new scoped pass.
   api.checkValidationEnvelope(envelope([assessment]));
   const result=api.validationAssessment(assessment);
   assert.equal(result.status,'uncertain',criterionID+' / '+value+' cannot pass');
   assert.equal(result.current,false);
   assert(result.reasons.some(reason=>/presence|absent|present|unknown/i.test(reason)), 'The reason explains presence');
  }
 }
});

check('presence cannot override hidden or unavailable target evidence',()=>{
 for(const visibility of ['occluded','unknown','missing']){
  const assessment=fixture();assessment.criteriaResults.find(r=>r.criterionID==='ear-piercings').visibility=visibility;
  assert.equal(api.validationAssessment(assessment).status,'uncertain',visibility+' cannot pass despite present');
 }
 const missing=fixture();missing.imagesSeen[0].accessible=false;
 assert.equal(api.validationAssessment(missing).status,'uncertain','Unavailable image is not an absent piercing');
 const absent=fixture();absent.criteriaResults.find(r=>r.criterionID==='nose-piercings').presence='absent';
 assert.equal(absent.criteriaResults.find(r=>r.criterionID==='nose-piercings').visibility,'visible','Absent feature can be observed in a visible image');
});

check('presence enum validates atomically while legacy results without it remain valid',()=>{
 const legacyRecord=fixture('legacy-valid',legacy);
 assert(legacyRecord.criteriaResults.every(r=>!Object.hasOwn(r,'presence')));
 api.checkValidationEnvelope(envelope([legacyRecord]));assert.equal(api.validationAssessment(legacyRecord).status,'pass');
 for(const value of ['missing','visible','',null,true,1]){
  const bad=fixture('invalid-presence');bad.criteriaResults[1].presence=value;
  const before=api.validationHistory.size;
  assert.throws(()=>api.importValidation(envelope([fixture('would-be-added'),bad])),undefined,'Invalid presence: '+String(value));
  assert.equal(api.validationHistory.size,before,'Invalid nested value cannot partially import');
 }
});

check('new entry picker hides old forehead scope while history still opens',()=>{
 const p=boot();p.api.importValidation(envelope([fixture('old-forehead-history',legacy)]));
 const panel=p.api.validationPanel(target,'character');
 const picker=panel.match(/<select data-v-field="criteria" data-v-axis="character">([\s\S]*?)<\/select>/);
 assert(picker,'Criteria selector exists');
 assert(picker[1].includes('value="hon-face-piercings"'),'Current scope can be selected');
 assert(!picker[1].includes('value="hon-face"'),'Retired forehead scope cannot start a new entry');
 assert(panel.includes('old-forehead-history')||panel.includes('Criteria hon-face'),'Historical assessment remains visible');
 assert(panel.includes('no-dice'),'Old recorded forehead row stays in history');
 const archived=p.api.validationEnvelope().assessments.find(a=>a.id==='old-forehead-history');
 assert.deepEqual(clone(archived),fixture('old-forehead-history',legacy),'Historical evidence is retained exactly');
 assert.equal(p.api.validationAssessment(archived).status,'pass','Picker retirement does not invalidate an unchanged historical comparison');
});

check('only piercing rows render a separate presence selector and save it',()=>{
 const p=boot();p.api.openViewer(target.id);
 const field=key=>p.selectAll('[data-v-field]').find(n=>n.dataset.vAxis==='character'&&n.dataset.vField===key);
 const choose=field('criteria');choose.value=active.id;for(const listener of choose.listeners.get('change')||[])listener({target:choose});
 const presence=p.selectAll('[data-v-presence]').filter(n=>n.dataset.vAxis==='character');
 assert.deepEqual(presence.map(n=>n.dataset.vPresence),presenceIDs,'No presence dropdown is invented for the face row');
 const criteriaBox=p.selectAll('[data-v-criteria]').find(n=>n.dataset.vCriteria==='character');
 assert(criteriaBox.innerHTML.includes('Image unavailable'),'Visibility retains its distinct missing-image option');
 assert(criteriaBox.innerHTML.includes('value="absent"'),'Presence exposes an absent feature');
 for(const key of ['reviewer','model','evidence'])field(key).value='Synthetic form evidence';
 field('status').value='pass';field('applicability').value='required';field('seen').checked=true;
 p.selectAll('[data-v-visibility]').filter(n=>n.dataset.vAxis==='character').forEach(n=>n.value='visible');
 p.selectAll('[data-v-outcome]').filter(n=>n.dataset.vAxis==='character').forEach(n=>n.value='pass');
 p.selectAll('[data-v-observation]').filter(n=>n.dataset.vAxis==='character').forEach(n=>n.value='Synthetic observed feature');
 presence.forEach(n=>n.value=n.dataset.vPresence==='ear-piercings'?'absent':'present');
 const before=clone(p.api.reviewPayload().items);
 p.selectAll('[data-v-save]').find(n=>n.dataset.vSave==='character').click();
 const saved=p.api.validationLatest(target.id,'character',active.id).find(a=>a.reviewer.name==='Synthetic form evidence');
 assert(saved,'Form saves independent scoped evidence');
 assert.equal(saved.criteriaResults.find(r=>r.criterionID==='ear-piercings').presence,'absent');
 assert.equal(saved.criteriaResults.find(r=>r.criterionID==='nose-piercings').presence,'present');
 assert(!Object.hasOwn(saved.criteriaResults.find(r=>r.criterionID==='face'),'presence'));
 assert.equal(p.api.validationAssessment(saved).status,'uncertain','The contradictory saved pass remains uncertain');
 assert.deepEqual(clone(p.api.reviewPayload().items),before,'Evidence entry leaves user ratings and triage decisions unchanged');
});

check('presence round-trips through sidecar full review and browser restart',()=>{
 const p=boot(),records=['present','absent','unknown'].map((value,index)=>{
  const r=fixture('round-trip-'+value);r.status=value==='present'?'pass':'uncertain';r.reviewer.reviewedAtUTC='2026-10-27T12:00:0'+index+'Z';r.criteriaResults[1].presence=value;return r;
 });
 records.push(fixture('legacy-round-trip',legacy));p.api.importValidation(envelope(records));
 const exported=clone(p.api.validationEnvelope());
 const restart=boot(Object.fromEntries(p.storage));
 const imported=boot();imported.api.importReview(clone(p.api.reviewPayload()));
 for(const viewer of [restart,imported])for(const original of records){
  assert.deepEqual(clone(viewer.api.validationEnvelope().assessments.find(a=>a.id===original.id)),original,'Exact evidence survives: '+original.id);
 }
 const sidecar=boot();sidecar.api.importValidation(exported);
 assert.equal(sidecar.api.validationEnvelope().assessments.find(a=>a.id==='round-trip-absent').criteriaResults[1].presence,'absent');
});

check('quick review leads the viewer with image description below Your note and archive after save',()=>{
 const fixtureCatalog=clone(catalog),asset=fixtureCatalog.assets.find(a=>a.id===target.id);
 asset.note='Synthetic review context';delete asset.lyric;delete asset.beat;delete asset.motion;
 const p=boot({},fixtureCatalog),before=clone(p.api.reviewPayload().items);p.api.openViewer(asset.id);
 const html=p.api.dialog.innerHTML;
 assert(/<div class="viewer-quick-actions">[\s\S]*?<\/div><section class="review-controls"/.test(html),'Your review follows favorite and basket buttons directly');
 const review=html.match(/<section class="review-controls"[^>]*>([\s\S]*?)<\/section>/)?.[1];assert(review,'Quick review section is rendered');
 const ordered=['<h3>Your review</h3>','id="review-current-status"','class="review-actions"','<label for="review-note">Your note</label>','id="review-note"','Image description','Synthetic review context','id="viewer-save-review"','id="viewer-export-review"','id="viewer-archive"'];
 let previous=-1;for(const marker of ordered){const position=review.indexOf(marker);assert(position>previous,'Quick review order: '+marker);previous=position;}
 for(const status of ['keep','needs_fixes','remove',''])assert(review.includes('data-review-status="'+status+'"'),'Quick triage action remains available: '+(status||'clear'));
 assert(/<\/textarea><p class="label">Image description<\/p><p>Synthetic review context<\/p>/.test(review),'Source image description follows Your note textarea directly');
 assert.equal((html.match(/<section class="review-controls"/g)||[]).length,1,'Quick review is not repeated farther down the viewer');
 const shot=html.indexOf('class="shot-plan-controls"'),creative=html.indexOf('class="quick-collaborators creative-review"');
 assert(shot>=0&&creative>shot,'Creative-review collaborators follow shot planning');
 assert(html.indexOf('Synthetic review context')<shot,'Existing source review context stays near the image');
 assert.deepEqual(clone(p.api.reviewPayload().items),before,'Opening reordered controls does not change review decisions');
 asset.lyric='Synthetic lyric';asset.beat='Synthetic beat';asset.motion='Synthetic motion';
 const story=boot({},fixtureCatalog);story.api.openViewer(asset.id);
 const storyHTML=story.api.dialog.innerHTML;
 assert(storyHTML.indexOf('id="viewer-archive"')<storyHTML.indexOf('Synthetic lyric'),'Lyric context follows the complete quick review section');
 assert(storyHTML.indexOf('Synthetic lyric')<storyHTML.indexOf('Synthetic beat'));
 assert(storyHTML.indexOf('Synthetic beat')<storyHTML.indexOf('Synthetic motion'),'Existing lyric, beat and motion context retains its order');
});

console.log(JSON.stringify({passed:true,checks:checks.length,names:checks,productionEvidenceWritten:false}));
