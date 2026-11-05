/* Real-library scene-craft contracts. Scores are synthetic; project review files are untouched. */
const assert = require('node:assert/strict');
const fs = require('node:fs'), path = require('node:path'), vm = require('node:vm');
const clone = value => JSON.parse(JSON.stringify(value));
const REVIEW_KEY = 'cfa-visual-review-v1', FAVORITES_KEY = 'cfa-visual-favorites-v1';
const raw = fs.readFileSync(path.join(__dirname, 'catalog.js'), 'utf8');
const catalog = JSON.parse(raw.slice(raw.indexOf('=') + 1).trim().replace(/;$/, ''));
const assetID = 'HD-FALCON-194702e9e041362d';
const frame = catalog.assets.find(a => a.id === assetID);
const shot = catalog.shotMaterials.shots.find(s => s.project === 'hon' && s.id === 'S01B');
assert(frame && frame.project === 'hon' && /C01-002/.test(frame.title), 'Actual C01-002 fixture exists');
assert(shot, 'Existing scene ID supplies an independent readiness fixture');
const plan = {status:'planned', destinations:['Flow'], idea:'Synthetic scene craft test.', prompt:'Preserve scene.', sceneIDs:[shot.id]};
const seed = {id:assetID, sha256:frame.sha256, status:'keep', note:'Synthetic fixture; preserve scene and correct identity separately.',
  origin:'user', variant:'prime', workingReferenceScope:'scene', storyboardStage:'detailed_design', likenessRating:2, shotPlan:plan};
const scene = {project:'hon', shotID:shot.id, grade:'C', note:'Synthetic blocked scene, not a project judgment.',
  criticalBlockers:['Identity still needs review.'], ingredients:[{id:'missing-character', label:'Missing required character reference',
    role:'identity', kind:'reference', required:true, status:'missing', assetID:null, sha256:null, note:'No reviewed identity binding.'}],
  shootPlan:{direction:'Test direction', camera:'Test framing', lighting:'Test lighting', reviewStatus:'unreviewed', reviewedBy:'', reviewedAt:null, note:''}};
const input = {...catalog, reviewDecisions:[seed], sceneReviews:[scene]};
const existing = fs.readFileSync(path.join(__dirname, 'test_reference_scope.cjs'), 'utf8');
const bootSource = existing.slice(existing.indexOf('function boot('), existing.indexOf('async function main()'));
const oldHook = 'window.__scopeTest={openViewer,reviewRecord,reviewPayload,importReview,exportReference,inReviewQueue,whenFileWritesSettle(){return fileWriteChain;}};';
const hook = 'window.__scopeTest={C,openViewer,reviewRecord,reviewPayload,normalizedReview,importReview,exportReference,exportReview,exportFavorites,toggleFavorite,toggleBasket,basketPayload,workingBOMEntries,effectiveReferenceRole,sceneReviewRecord,sceneHandoffGate,shotHandoffPayload,exportShotHandoff,updateReview,viewerHTML(){return dialog.innerHTML;},setState(p){Object.assign(state,p);},whenFileWritesSettle(){return fileWriteChain;}};';
assert(bootSource.includes(oldHook), 'Reuse existing DOM/storage double');
const bootFunction = new Function('source','catalog','clone','assert','vm','REVIEW_KEY','FAVORITES_KEY','assets',
  bootSource.replace(oldHook, hook) + ';return boot;');
const boot = (saved={}, supplied=input, options={}) => bootFunction(
  fs.readFileSync(path.join(__dirname, 'library.js'), 'utf8'), supplied, clone, assert, vm, REVIEW_KEY, FAVORITES_KEY, supplied.assets
)(saved, supplied, options);
const scores = item => ({likenessRating:item.likenessRating, sceneQualityRating:item.sceneQualityRating});

async function main() {
  let checks=0;
  const page=boot(), api=page.api;
  const asset=() => api.C.assets.find(a => a.id === assetID);
  const originals=clone({assets:api.C.assets, characterBOM:api.C.characterBOM, shots:api.C.shotMaterials.shots});
  const bomBefore=clone(api.workingBOMEntries('hon'));
  const sceneBefore=clone(api.sceneReviewRecord('hon', shot.id));
  const gateBefore=clone(api.sceneHandoffGate(sceneBefore));
  assert.equal(gateBefore.productionEligible, false);
  page.open(assetID);
  const quality=page.node('#reference-scene-quality-rating');
  assert.equal(quality.value, '', 'Legacy review is Unrated rather than inferred five');
  assert.deepEqual(quality.options, ['', '1', '2', '3', '4', '5']);
  assert(api.viewerHTML().includes('Scene craft'), 'New rating has an explicit label');
  const before=clone(api.reviewRecord(assetID));
  quality.value='5'; quality.fire('change');
  const rated=clone(api.reviewRecord(assetID));
  assert.deepEqual(scores(rated), {likenessRating:2, sceneQualityRating:5}, 'Low likeness and high craft coexist without averaging');
  for(const field of ['status','note','variant','workingReferenceScope','storyboardStage','shotPlan','workingReference'])
    assert.deepEqual(rated[field], before[field], 'Craft does not change '+field);
  assert.equal(api.effectiveReferenceRole(asset()), 'scene');
  assert.deepEqual(clone(api.workingBOMEntries('hon')), bomBefore, 'Craft does not approve or replace a BOM component');
  assert.deepEqual(clone(api.sceneReviewRecord('hon', shot.id)), sceneBefore, 'Scene review and shoot verification remain unchanged');
  assert.deepEqual(clone(api.sceneHandoffGate(api.sceneReviewRecord('hon', shot.id))), gateBefore, 'High craft cannot make a blocked scene ready');
  checks++;

  page.open(assetID);
  assert.equal(page.node('#reference-scene-quality-rating').value, '5', 'Recreated viewer restores craft');
  const reloaded=boot(page.snapshot()); reloaded.open(assetID);
  assert.equal(reloaded.node('#reference-scene-quality-rating').value, '5', 'Browser backup restores craft');
  assert.deepEqual(scores(reloaded.record(assetID)), {likenessRating:2, sceneQualityRating:5});
  reloaded.node('#viewer-export-review').click();
  const portable=JSON.parse(await reloaded.downloads.at(-1).blob.text());
  assert.deepEqual(scores(portable.items.find(r => r.id === assetID)), {likenessRating:2, sceneQualityRating:5});
  const imported=boot({}, {...catalog, reviewDecisions:[], sceneReviews:[]});
  imported.api.importReview(portable); imported.open(assetID);
  assert.equal(imported.node('#reference-scene-quality-rating').value, '5', 'Portable import preserves craft');
  assert.deepEqual(scores(imported.record(assetID)), {likenessRating:2, sceneQualityRating:5});
  assert.deepEqual(clone(imported.api.sceneReviewRecord('hon', shot.id)), sceneBefore);
  checks++;

  for(const valid of [1,2,3,4,5,null]) {
    const normalized=api.normalizedReview({...seed, sceneQualityRating:valid});
    assert.equal(normalized.sceneQualityRating, valid);
    assert.equal(normalized.likenessRating, 2);
  }
  for(const invalid of [-1,0,6,2.5,'5',{},[],true]) {
    const invalidPage=boot({}, {...catalog, reviewDecisions:[], sceneReviews:[]});
    invalidPage.api.importReview({format:REVIEW_KEY, items:[{...seed, sceneQualityRating:invalid}], favorites:[]});
    assert.equal(invalidPage.record(assetID).sceneQualityRating, null, 'Invalid score becomes Unrated: '+JSON.stringify(invalid));
    assert.equal(invalidPage.record(assetID).likenessRating, 2, 'Invalid craft retains valid likeness');
    assert.equal(invalidPage.record(assetID).status, 'keep');
  }
  const mismatch=boot({}, {...catalog, reviewDecisions:[], sceneReviews:[]});
  mismatch.api.importReview({format:REVIEW_KEY, items:[{...seed, sha256:'0'.repeat(64), sceneQualityRating:5}], favorites:[]});
  assert.equal(mismatch.record(assetID).sceneQualityRating, undefined, 'Wrong hash cannot attach a score');
  assert.equal(mismatch.record(assetID).likenessRating, undefined);
  assert.equal(Object.hasOwn(api.normalizedReview(seed), 'sceneQualityRating'), false, 'Legacy import does not invent craft');
  imported.api.importReview({format:REVIEW_KEY, items:[seed], favorites:[]});
  assert.equal(imported.record(assetID).sceneQualityRating, 5, 'Old partial import does not erase craft');
  imported.api.importReview({format:REVIEW_KEY, items:[{...seed, sceneQualityRating:null}], favorites:[]});
  imported.open(assetID);
  assert.equal(imported.node('#reference-scene-quality-rating').value, '', 'Explicit Unrated clears craft');
  assert.equal(imported.record(assetID).likenessRating, 2);
  checks++;

  api.setState({project:'hon', view:'shot_plans', destination:'all', exportIntent:'prime', search:''});
  assert.deepEqual(scores(clone(api.exportReference(asset()))), {likenessRating:2, sceneQualityRating:5});
  api.toggleBasket(assetID);
  assert.deepEqual(scores(clone(api.basketPayload()).items.find(a => a.id === assetID)), {likenessRating:2, sceneQualityRating:5});
  api.toggleFavorite(assetID); api.exportFavorites();
  const favorite=JSON.parse(await page.downloads.at(-1).blob.text());
  assert.deepEqual(scores(favorite.items.find(a => a.id === assetID)), {likenessRating:2, sceneQualityRating:5});
  const handoff=clone(api.shotHandoffPayload()).items.find(a => a.id === assetID);
  assert.deepEqual(scores(handoff), {likenessRating:2, sceneQualityRating:5});
  assert.equal(handoff.handoffPurpose, 'planning_or_repair', 'High craft keeps a blocked scene in repair');
  assert.equal(handoff.sceneReadiness[0].productionEligible, false);
  api.exportShotHandoff('json');
  const json=JSON.parse(await page.downloads.at(-1).blob.text());
  assert.deepEqual(scores(json.items.find(a => a.id === assetID)), {likenessRating:2, sceneQualityRating:5});
  api.exportShotHandoff('txt');
  const text=await page.downloads.at(-1).blob.text();
  assert(/Likeness[^\n]*2\s*\/\s*5/i.test(text), 'Text carries separate likeness score');
  assert(/Scene craft:\s*5\s*\/\s*5/i.test(text), 'Text carries explicitly named craft score');
  assert.deepEqual(clone(api.C.characterBOM), originals.characterBOM);
  checks++;

  const autosave=boot({}, input, {fileAutosave:true});
  autosave.open(assetID); await autosave.node('#viewer-save-review').click();
  autosave.node('#reference-scene-quality-rating').value='4';
  autosave.node('#reference-scene-quality-rating').fire('change');
  await autosave.flushTimers();
  let file=JSON.parse(autosave.fileWrites.at(-1));
  assert.deepEqual(scores(file.items.find(r => r.id === assetID)), {likenessRating:2, sceneQualityRating:4}, 'Review-file autosave preserves both scores');
  autosave.open(assetID);
  autosave.node('#reference-scene-quality-rating').value='';
  autosave.node('#reference-scene-quality-rating').fire('change');
  await autosave.flushTimers();
  file=JSON.parse(autosave.fileWrites.at(-1));
  assert.deepEqual(scores(file.items.find(r => r.id === assetID)), {likenessRating:2, sceneQualityRating:null}, 'Clearing craft saves Unrated without clearing likeness');
  assert.deepEqual(file.sceneReviews[0], sceneBefore);
  assert.deepEqual(clone({assets:api.C.assets, characterBOM:api.C.characterBOM, shots:api.C.shotMaterials.shots}), originals, 'Scores and exports preserve sources, canonical BOM and acceptance records');
  checks++;
  console.log(JSON.stringify({passed:true, scenarios:checks, fixture:assetID, separateScores:true, projectGradesAssigned:false, browserVisualQA:false}));
}
main().catch(error => {console.error(error); process.exitCode=1;});