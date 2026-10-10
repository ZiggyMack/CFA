/* Real scene readiness contracts using the existing real-library VM/DOM double.
   Fixture grades are synthetic; no project scene is graded or approved here. */
const assert = require('node:assert/strict');
const fs = require('node:fs'), path = require('node:path'), vm = require('node:vm');
const clone = value => JSON.parse(JSON.stringify(value));
const REVIEW_KEY = 'cfa-visual-review-v1', FAVORITES_KEY = 'cfa-visual-favorites-v1';
const catalogJS = fs.readFileSync(path.join(__dirname,'catalog.js'),'utf8');
const catalog = JSON.parse(catalogJS.slice(catalogJS.indexOf('=')+1).trim().replace(/;$/,''));
const inputCatalog = {...catalog,reviewDecisions:[]};
const shot = catalog.shotMaterials.shots.find(s => s.project==='hon' && s.id==='S01B');
const otherShot = catalog.shotMaterials.shots.find(s => s.project==='hon' && s.id==='S02A');
assert(shot && otherShot,'Use actual stable scene IDs');
const byID = new Map(catalog.assets.map(a => [a.id,a]));
const frame = byID.get(shot.panelAssetIDs[0]), otherFrame = byID.get(otherShot.panelAssetIDs[0]);
assert(frame && otherFrame && frame.id!==otherFrame.id,'Actual scene references exist');
const legacyPlan = {status:'planned',destinations:['Flow'],idea:'Legacy planned shot.',prompt:'Keep the existing source.'};
const scopeTest = fs.readFileSync(path.join(__dirname,'test_reference_scope.cjs'),'utf8');
const bootSource = scopeTest.slice(scopeTest.indexOf('function boot('),scopeTest.indexOf('async function main()'));
const originalHook = 'window.__scopeTest={openViewer,reviewRecord,reviewPayload,importReview,exportReference,inReviewQueue,whenFileWritesSettle(){return fileWriteChain;}};';
const testHook = 'window.__scopeTest={openViewer,C,sceneReviews,toggleFavorite,normalizedSceneReview,sceneReviewRecord,sceneHandoffGate,updateSceneReview,reviewRecord,updateReview,reviewPayload,importReview,normalizedPlan,shotHandoffPayload,exportShotHandoff,exportReference,storyWorkCard,renderMain,setState(p){Object.assign(state,p);},whenFileWritesSettle(){return fileWriteChain;}};';
assert(bootSource.includes(originalHook),'Reuse existing DOM/storage double');
const bootFunction = new Function('source','catalog','clone','assert','vm','REVIEW_KEY','FAVORITES_KEY','assets',bootSource.replace(originalHook,testHook)+';return boot;');
const boot = (saved={},supplied=inputCatalog,options={}) => bootFunction(fs.readFileSync(path.join(__dirname,'library.js'),'utf8'),supplied,clone,assert,vm,REVIEW_KEY,FAVORITES_KEY,supplied.assets)(saved,supplied,options);

function reference(overrides={}) {
  return {id:'selected-frame',label:'Selected scene frame',role:'scene',kind:'reference',required:true,status:'ready',
    assetID:frame.id,sha256:frame.sha256,note:'Reviewed exact frame for this test fixture.',...overrides};
}
function criterion(overrides={}) {
  return {id:'action-continuity',label:'Action and continuity',role:'action',kind:'criterion',required:true,status:'ready',
    assetID:null,sha256:null,note:'Reviewed screen direction and complete visible hands.',...overrides};
}
function verifiedShootPlan(overrides={}) {
  return {direction:'Reviewed blocking, eyelines, and performance beat.',camera:'Reviewed framing and camera movement.',
    lighting:'Reviewed motivated key and exposure continuity.',reviewStatus:'verified',reviewedBy:'Synthetic test reviewer',
    reviewedAt:'2026-10-10T04:59:00Z',note:'Synthetic verification fixture, not a project approval.',...overrides};
}
function scene(grade='B',ingredients=[reference(),criterion()],overrides={}) {
  return {project:shot.project,shotID:shot.id,grade,note:'Synthetic readiness fixture only.',criticalBlockers:[],
    ingredients,shootPlan:verifiedShootPlan(),updatedAt:'2026-10-10T05:00:00Z',...overrides};
}
function importScene(api,value) {
  api.importReview({format:REVIEW_KEY,items:[],favorites:[],sceneReviews:[value]});
  return api.sceneReviewRecord(value.project,value.shotID);
}
function eligibility(api,value) {
  const gate=clone(api.sceneHandoffGate(importScene(api,value)));
  assert.equal(typeof gate.productionEligible,'boolean','Gate is explicit');
  assert(Array.isArray(gate.reasons),'Gate keeps actionable reasons');
  return gate;
}

async function main() {
  let checks=0;
  const page=boot(), api=page.api;
  api.setState({project:'hon',view:'shot_plans',destination:'all',exportIntent:'prime',search:''});
  const originals=clone({assets:api.C.assets,characterBOM:api.C.characterBOM||null,shots:api.C.shotMaterials.shots});
  const ungraded=api.sceneReviewRecord(shot.project,shot.id);
  assert.equal(ungraded.grade,null,'Availability does not invent a grade');
  assert(ungraded.ingredients.every(i=>i.status==='unreviewed' && i.required===false),'Available materials are not automatically reviewed or required');
  assert.equal(api.sceneHandoffGate(ungraded).productionEligible,false);
  assert.equal(api.normalizedSceneReview(scene('B',[],{shotID:'NONEXISTENT-SCENE'})),null,'Unknown scene ID is rejected');
  assert.equal(api.normalizedSceneReview(scene('B',[],{project:'lisan'})),null,'Project and scene must agree');
  checks++;

  assert.equal(eligibility(api,scene('A',[reference(),criterion(),reference({id:'hands',label:'Missing fingers',assetID:null,sha256:null,status:'missing'})])).productionEligible,false,'A cannot average away required missing fingers');
  assert.equal(eligibility(api,scene('B')).productionEligible,true,'B with required Ready ingredients and verified shoot plan can hand off');
  assert.equal(eligibility(api,scene('C')).productionEligible,false,'C stays planning or repair');
  assert.equal(eligibility(api,scene(null)).productionEligible,false,'Ungraded is not B');
  assert.equal(eligibility(api,scene('B',[])).productionEligible,false,'Grade alone does not replace ingredient review');
  checks++;

  assert.equal(eligibility(api,scene('B',[reference({status:'unreviewed'}),criterion()])).productionEligible,false,'Required unreviewed material blocks');
  assert.equal(eligibility(api,scene('B',[reference({status:'needs_fixes'}),criterion()])).productionEligible,false,'Required fix blocks');
  assert.equal(eligibility(api,scene('B',[reference(),criterion(),reference({id:'optional-cigar',label:'Optional cigar',required:false,status:'missing',assetID:null,sha256:null})])).productionEligible,true,'Optional missing prop does not hold back this scene');
  assert.equal(eligibility(api,scene('A',undefined,{criticalBlockers:['Missing fingers in selected frame.']})).productionEligible,false,'Critical blocker overrides a high grade');
  checks++;

  assert.equal(eligibility(api,scene('B',[reference(),criterion({note:''})])).productionEligible,false,'Ready criterion needs reviewed evidence note');
  assert.equal(eligibility(api,scene('B',[reference(),criterion({note:'Inspected exact action and checked screen direction.',assetID:null,sha256:null})])).productionEligible,true,'Non-media criterion can be Ready without a file');
  assert.equal(eligibility(api,scene('B',[reference({assetID:null,sha256:null}),criterion()])).productionEligible,false,'Required reference cannot claim Ready while absent');
  checks++;

  const missing=scene('B',[reference({id:'crime-boss',label:'Crime boss still needed',status:'missing',assetID:null,sha256:null}),criterion()]);
  importScene(api,missing);
  let stored=clone(api.sceneReviewRecord(shot.project,shot.id));
  assert.equal(stored.ingredients.find(i=>i.id==='crime-boss').assetID,null,'Explicit absence survives import');
  assert.equal(stored.ingredients.find(i=>i.id==='crime-boss').status,'missing');
  assert.equal(eligibility(api,scene('B',[reference({sha256:'f'.repeat(64)}),criterion()])).productionEligible,false,'Imported Ready with wrong bound hash is rejected by gate');
  assert.equal(eligibility(api,scene('B',[reference({assetID:'UNKNOWN-ASSET',sha256:'e'.repeat(64)}),criterion()])).productionEligible,false,'Unknown asset cannot become Ready');
  importScene(api,missing);
  assert.equal(api.sceneReviewRecord(shot.project,shot.id).ingredients.find(i=>i.id==='crime-boss').status,'missing','Validation does not silently erase absent ingredient evidence');
  checks++;

  assert.equal(eligibility(api,scene('B',undefined,{shootPlan:verifiedShootPlan({reviewStatus:'unreviewed',reviewedBy:'',reviewedAt:null})})).productionEligible,false,'Ready ingredients cannot replace shoot-plan review');
  assert.equal(eligibility(api,scene('B',undefined,{shootPlan:verifiedShootPlan()})).productionEligible,true,'Explicit documented verified shoot plan permits otherwise-ready B handoff');
  for(const field of ['direction','camera','lighting','reviewedBy','reviewedAt']) {
    assert.equal(eligibility(api,scene('B',undefined,{shootPlan:verifiedShootPlan({[field]:''})})).productionEligible,false,'Missing shoot-plan '+field+' blocks');
  }
  const pendingShoot=scene('B',undefined,{shootPlan:verifiedShootPlan({reviewStatus:'unreviewed',reviewedBy:'',reviewedAt:null})});
  importScene(api,pendingShoot);
  api.updateSceneReview(shot.project,shot.id,{grade:'A'});
  api.updateReview(frame.id,{storyboardStage:'production'});
  const pending=api.sceneReviewRecord(shot.project,shot.id);
  assert.equal(pending.shootPlan.reviewStatus,'unreviewed','High grade or image Production does not auto-verify shoot plan');
  assert(!pending.shootPlan.reviewedAt,'Stage/grade changes do not invent verification time');
  assert.equal(api.sceneHandoffGate(pending).productionEligible,false);
  checks++;

  // A coherent shoot-plan review cannot survive changes to the plan or required cast.
  importScene(api,scene('B'));
  const verifiedBefore=clone(api.sceneReviewRecord(shot.project,shot.id).shootPlan);
  api.updateSceneReview(shot.project,shot.id,{grade:'A'});
  api.updateReview(frame.id,{likenessRating:4});
  api.toggleFavorite(frame.id);
  assert.deepEqual(clone(api.sceneReviewRecord(shot.project,shot.id).shootPlan),verifiedBefore,'Grade, likeness and favorite choices preserve independent shoot-plan evidence');
  api.updateSceneReview(shot.project,shot.id,{shootPlan:{camera:'New framing after verification.'}});
  let changed=clone(api.sceneReviewRecord(shot.project,shot.id));
  assert.equal(changed.shootPlan.direction,verifiedBefore.direction,'Partial camera edit merges prior director plan');
  assert.equal(changed.shootPlan.lighting,verifiedBefore.lighting,'Partial camera edit merges prior lighting plan');
  assert.equal(changed.shootPlan.reviewStatus,'unreviewed','Camera edit invalidates prior review centrally');
  assert.equal(changed.shootPlan.reviewedAt,null,'Camera edit clears old verification time');
  assert.equal(api.sceneHandoffGate(changed).productionEligible,false);
  api.updateSceneReview(shot.project,shot.id,{shootPlan:{reviewStatus:'verified',reviewedAt:'2026-10-10T05:01:00Z'}});
  assert.equal(api.sceneHandoffGate(api.sceneReviewRecord(shot.project,shot.id)).productionEligible,true,'Explicit renewed review with supplied new time can restore eligibility');
  const requiredChanged=clone(api.sceneReviewRecord(shot.project,shot.id).ingredients);
  requiredChanged.push(criterion({id:'new-required-check',label:'New required continuity check'}));
  api.updateSceneReview(shot.project,shot.id,{ingredients:requiredChanged});
  changed=clone(api.sceneReviewRecord(shot.project,shot.id));
  assert.equal(changed.shootPlan.reviewStatus,'unreviewed','Changed required recipe invalidates coherent plan review');
  assert.equal(changed.shootPlan.reviewedAt,null);
  api.updateSceneReview(shot.project,shot.id,{shootPlan:{reviewStatus:'verified',reviewedAt:'2026-10-10T05:02:00Z'}});
  const rebound=clone(api.sceneReviewRecord(shot.project,shot.id).ingredients);
  rebound.find(i=>i.id==='selected-frame').assetID=otherFrame.id;
  rebound.find(i=>i.id==='selected-frame').sha256=otherFrame.sha256;
  api.updateSceneReview(shot.project,shot.id,{ingredients:rebound});
  changed=clone(api.sceneReviewRecord(shot.project,shot.id));
  assert.equal(changed.shootPlan.reviewStatus,'unreviewed','Different required source binding invalidates prior shoot-plan review');
  assert.equal(changed.shootPlan.reviewedAt,null);
  importScene(api,scene('B'));
  api.updateSceneReview(shot.project,shot.id,{shootPlan:{camera:'Changed framing with stale review time.',reviewStatus:'verified',reviewedAt:verifiedBefore.reviewedAt}});
  assert.equal(api.sceneReviewRecord(shot.project,shot.id).shootPlan.reviewStatus,'unreviewed','Reusing old timestamp cannot approve changed plan');
  api.updateSceneReview(shot.project,shot.id,{shootPlan:{camera:'Final reviewed framing.',reviewStatus:'verified',reviewedAt:'2026-10-10T05:03:00Z'}});
  assert.equal(api.sceneHandoffGate(api.sceneReviewRecord(shot.project,shot.id)).productionEligible,true,'Changed plan may be explicitly reverified with a new supplied timestamp');
  checks++;

  api.updateReview(frame.id,{likenessRating:3,storyboardStage:'preliminary',status:'keep',note:'Keep known difference for this one scene.'});
  importScene(api,scene('B'));
  assert.equal(api.sceneHandoffGate(api.sceneReviewRecord(shot.project,shot.id)).productionEligible,true);
  assert.equal(api.reviewRecord(frame.id).likenessRating,3,'Readiness does not rewrite likeness stars');
  assert.equal(api.reviewRecord(frame.id).storyboardStage,'preliminary','Scene grade does not promote image stage');
  importScene(api,scene('F'));
  assert.equal(api.reviewRecord(frame.id).likenessRating,3);
  assert.equal(api.reviewRecord(frame.id).status,'keep','Scene failure does not demote a component approval');
  assert.deepEqual(clone({assets:api.C.assets,characterBOM:api.C.characterBOM||null,shots:api.C.shotMaterials.shots}),originals,'Grades do not change metadata, canonical BOM, or scene acceptance');
  checks++;

  api.updateReview(frame.id,{shotPlan:api.normalizedPlan({...legacyPlan,sceneIDs:[shot.id]})});
  api.updateReview(otherFrame.id,{shotPlan:api.normalizedPlan(legacyPlan)});
  assert.deepEqual(clone(api.reviewRecord(otherFrame.id).shotPlan),legacyPlan,'Legacy plan is unchanged and not automatically bound');
  importScene(api,scene('B'));
  const other=scene('C',[reference({assetID:otherFrame.id,sha256:otherFrame.sha256}),criterion()],{shotID:otherShot.id,project:otherShot.project});
  importScene(api,other);
  const portable=clone(api.reviewPayload());
  assert.equal(portable.sceneReviews.length,2,'Independent scenes persist separately');
  const reloaded=boot(page.snapshot());
  assert.deepEqual(clone(reloaded.api.reviewPayload().sceneReviews),portable.sceneReviews,'Scene reviews survive reload');
  assert.deepEqual(clone(reloaded.api.reviewRecord(otherFrame.id).shotPlan),legacyPlan);
  const imported=boot(); imported.api.importReview(portable);
  assert.deepEqual(clone(imported.api.reviewPayload().sceneReviews),portable.sceneReviews,'Scene records and ingredient evidence roundtrip');
  assert.deepEqual(clone(imported.api.reviewRecord(otherFrame.id).shotPlan),legacyPlan);
  assert.equal(imported.api.reviewRecord(frame.id).likenessRating,3);
  assert.equal(imported.api.sceneHandoffGate(imported.api.sceneReviewRecord(shot.project,shot.id)).productionEligible,true);
  assert.equal(imported.api.sceneHandoffGate(imported.api.sceneReviewRecord(otherShot.project,otherShot.id)).productionEligible,false);
  checks++;

  const handoff=clone(api.shotHandoffPayload()), bound=handoff.items.find(i=>i.id===frame.id), legacy=handoff.items.find(i=>i.id===otherFrame.id);
  assert(bound && legacy,'Both plans remain exportable');
  assert.equal(bound.handoffPurpose,'production_target','Explicit suitable scene binding can target production');
  assert.equal(legacy.handoffPurpose,'planning_or_repair','Unbound legacy plan remains planning-only');
  assert(Array.isArray(bound.sceneReadiness) && bound.sceneReadiness.length===1,'Only explicitly bound scene controls reference handoff');
  assert(Array.isArray(handoff.scenes) && handoff.scenes.some(s=>s.shotID===shot.id),'Handoff carries stable scene records and gates');
  importScene(api,missing);
  const blocked=clone(api.shotHandoffPayload()).items.find(i=>i.id===frame.id);
  assert.equal(blocked.handoffPurpose,'planning_or_repair','Blocked scene remains exportable for repair');
  api.exportShotHandoff('json');
  const output=JSON.parse(await page.downloads.at(-1).blob.text());
  assert.equal(output.items.find(i=>i.id===frame.id).handoffPurpose,'planning_or_repair');
  assert(JSON.stringify(output).includes('Crime boss still needed'),'JSON retains missing constituent');
  api.exportShotHandoff('txt');
  const text=await page.downloads.at(-1).blob.text();
  assert(/readiness|production|planning|repair/i.test(text),'TXT names readiness purpose');
  assert(/Crime boss still needed/.test(text),'TXT names missing constituent');
  checks++;

  const autosave=boot({},inputCatalog,{fileAutosave:true}); autosave.open(frame.id);
  await autosave.node('#viewer-save-review').click();
  importScene(autosave.api,missing); await autosave.flushTimers();
  const savedFile=JSON.parse(autosave.fileWrites.at(-1));
  assert(savedFile.sceneReviews.some(s=>s.shotID===shot.id && s.ingredients.some(i=>i.id==='crime-boss' && i.status==='missing')),'Review-file autosave preserves ingredient defects');
  checks++;
  console.log(JSON.stringify({passed:true,scenarios:checks,sceneIDs:[shot.id,otherShot.id],catalogAssets:catalog.assets.length,browserVisualQA:false,projectGradesAssigned:false}));
}
main().catch(error=>{console.error(error);process.exitCode=1;});

