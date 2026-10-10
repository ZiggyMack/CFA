/* Real catalog and library regression checks with the existing scope-test DOM double.
   Verifies handlers, decisions and exports; this is not browser visual QA. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const clone = value => JSON.parse(JSON.stringify(value));
const REVIEW_KEY = 'cfa-visual-review-v1', FAVORITES_KEY = 'cfa-visual-favorites-v1';
const catalogJS = fs.readFileSync(path.join(__dirname, 'catalog.js'), 'utf8');
const catalog = JSON.parse(catalogJS.slice(catalogJS.indexOf('=') + 1).trim().replace(/;$/, ''));
const overlay = JSON.parse(fs.readFileSync(path.join(__dirname, '../../../../downloads/cfa-review (9).json'), 'utf8'));
const ids = {
  face:'HD-RETURN-6c8900223ee9', cheek:'HD-RETURN-9ace849985b4', chest:'HD-RETURN-7b156019ddf8',
  neck:'HD-RETURN-7fe77eadd174', wrist:'HD-DROP-b18c4a123579', chain:'HD-B-708df0bb5bff',
  iced:'HD-GRILLUP-40064d98db89', fix:'HD-RETURN-1e8c86b1c729', multiverse:'HD-RETURN-10ac9771fdeb',
  scene:'LAG-467cd70039955ce1', unknown:'HD-DROP-e57d15439d03'
};
const byID = new Map(catalog.assets.map(a => [a.id, a]));
for (const id of Object.values(ids)) assert(byID.has(id), 'Actual fixture exists: ' + id);
assert.equal(overlay.format, REVIEW_KEY);

// Reuse the actual existing DOM/storage double rather than invent a second DOM implementation.
// Only its instrumentation is replaced; the real library is freshly read at each boot.
const scopeTest = fs.readFileSync(path.join(__dirname, 'test_reference_scope.cjs'), 'utf8');
const bootSource = scopeTest.slice(scopeTest.indexOf('function boot('), scopeTest.indexOf('async function main()'));
const originalHook = 'window.__scopeTest={openViewer,reviewRecord,reviewPayload,importReview,exportReference,inReviewQueue,whenFileWritesSettle(){return fileWriteChain;}};';
const testHook = 'window.__scopeTest={C,workingBOMEntries,effectiveReferenceRole,referenceUsePolicy,exportReference,shotHandoffPayload,exportShotHandoff,projectAssets,reviewRecord,updateReview,reviews,normalizedReview,reviewPayload,importReview,openViewer,inReviewQueue,workingReferencesWorkspace,renderMain,render,viewerHTML(){return dialog.innerHTML;},setState(p){Object.assign(state,p);},whenFileWritesSettle(){return fileWriteChain;}};';
assert(bootSource.includes(originalHook), 'Existing DOM double exposes the expected hook');
const bootFunction = new Function('source','catalog','clone','assert','vm','REVIEW_KEY','FAVORITES_KEY','assets',
  bootSource.replace(originalHook, testHook) + ';return boot;');
const boot = (saved = {}, input = catalog) => bootFunction(
  fs.readFileSync(path.join(__dirname, 'library.js'), 'utf8'), catalog, clone, assert, vm, REVIEW_KEY, FAVORITES_KEY, catalog.assets
)(saved, input);

async function main() {
  let checks = 0;
  const page = boot({[REVIEW_KEY]:JSON.stringify(overlay)}), api = page.api;
  const asset = id => api.C.assets.find(a => a.id === id);
  const entry = id => api.workingBOMEntries('hon').find(e => e.asset.id === id);
  const originalAssets = clone(api.C.assets), beforeBrowse = clone(api.reviewPayload().items);
  const roles = {face:'identity', cheek:'cheek_detail', chest:'chest_placement', neck:'neck_placement', wrist:'visible_jewelry_only', chain:'mouth_detail', iced:'optional_iced_look'};
  for (const [name, role] of Object.entries(roles)) {
    assert(entry(ids[name]), 'Selected component is in BOM: ' + name);
    assert.equal(entry(ids[name]).role, role, 'Scope remains bounded: ' + name);
    assert.equal(entry(ids[name]).asset.sha256, byID.get(ids[name]).sha256, 'Exact source hash retained: ' + name);
  }
  assert.equal(entry(ids.iced).optional, true, 'Iced r4 remains optional');
  assert.equal(entry(ids.face).optional, false, 'Selected default is not optional');
  assert.equal(asset(ids.wrist).componentApprovals[0].acceptsFullLook, false);
  assert.equal(api.effectiveReferenceRole(asset(ids.wrist)), 'visible_jewelry_only', 'Broad identity dropdown cannot broaden wrist lock');
  assert.equal(api.effectiveReferenceRole(asset(ids.cheek)), 'cheek_detail', 'Old full-look request cannot broaden corrected cheek lock');
  checks++;

  assert.equal(api.reviewRecord(ids.fix).storyboardStage, 'production');
  assert.equal(api.reviewRecord(ids.fix).status, 'needs_fixes', 'Production does not erase defect');
  assert(!entry(ids.fix) || entry(ids.fix).approved === false, 'Unresolved Production image is excluded from approved BOM');
  assert.equal(api.reviewRecord(ids.multiverse).variant, 'multiverse');
  assert(!entry(ids.multiverse) || entry(ids.multiverse).approved === false, 'Mixed Multiverse sheet is not Prime master');
  checks++;

  const workspace = api.workingReferencesWorkspace();
  assert.equal(typeof workspace, 'string');
  assert(workspace.includes(ids.face), 'Actual selected cover is rendered');
  assert(/bill of materials|approved parts|working references/i.test(workspace));
  assert(/details|expand|data-.*toggle/i.test(workspace), 'Approved parts can expand');
  api.setState({view:'all'}); api.renderMain();
  api.setState({view:'working'}); api.renderMain();
  assert.deepEqual(clone(api.reviewPayload().items), beforeBrowse, 'Browsing makes no decisions');
  assert.deepEqual(clone(api.C.assets), originalAssets, 'Browsing preserves source metadata/hashes');
  checks++;

  api.updateReview(ids.unknown, {status:'keep', storyboardStage:'production', variant:'prime', likenessRating:5});
  assert.equal(entry(ids.unknown).role, 'scene', 'Unknown browser Production choice defaults to scene');
  assert.equal(api.effectiveReferenceRole(asset(ids.unknown)), 'scene');
  assert.equal(entry(ids.face).role, 'identity', 'Five stars cannot replace default identity');
  api.updateReview(ids.unknown, {storyboardStage:'preliminary', status:'needs_fixes'});
  for (const name of ['face','cheek','wrist','chain']) assert(entry(ids[name]), 'Unrelated scene downgrade leaves lock: ' + name);
  checks++;

  api.updateReview(ids.unknown, {status:'remove', note:'Retain source; hide normal preview.'});
  assert(!api.projectAssets().some(a => a.id === ids.unknown), 'Normal browse/count membership excludes removals');
  assert(api.projectAssets(true).some(a => a.id === ids.unknown), 'Review/history retains removals');
  assert.equal(api.inReviewQueue(asset(ids.unknown)), true);
  api.setState({view:'all', search:''}); api.renderMain();
  assert(!page.node('#main').innerHTML.includes('data-open="' + ids.unknown + '"'), 'Normal browse hides removed preview');
  api.setState({view:'review_queue'}); api.renderMain();
  assert(page.node('#main').innerHTML.includes('data-open="' + ids.unknown + '"'), 'Review queue opens original');
  assert(api.reviewPayload().items.some(r => r.id === ids.unknown && r.status === 'remove'));
  assert.deepEqual(clone(api.C.assets), originalAssets, 'Filtering never deletes or rewrites originals');
  checks++;

  api.updateReview(ids.face, {likenessRating:null, note:'Known difference: collar is a scene choice.'});
  const stageBeforeScore = api.reviewRecord(ids.face).storyboardStage;
  api.openViewer(ids.face);
  const rating = page.node('#reference-likeness-rating');
  assert.equal(rating.value, '', 'Unrated is explicit; missing score is not five');
  assert.deepEqual(rating.options, ['', '1', '2', '3', '4', '5']);
  assert.throws(() => page.node('#request-working-reference'), /Rendered control exists/, 'Redundant request action is absent');
  const viewer = api.viewerHTML();
  assert(viewer.includes('id="reference-storyboard-stage"'), 'Design-stage control remains available');
  assert(viewer.indexOf('id="reference-likeness-rating"') > viewer.indexOf('id="reference-storyboard-stage"'), 'Rating appears below design-stage control');
  rating.value = '4'; rating.fire('change');
  assert.equal(api.reviewRecord(ids.face).likenessRating, 4, 'Actual listener saves integer');
  assert.equal(api.reviewRecord(ids.face).storyboardStage, stageBeforeScore, 'Rating cannot promote stage');
  assert.equal(api.reviewRecord(ids.face).note, 'Known difference: collar is a scene choice.');
  assert.equal(entry(ids.face).role, 'identity');
  for (const invalid of [-1,0,6,2.5,'5',{},true]) {
    const normalized = api.normalizedReview({id:ids.face, sha256:asset(ids.face).sha256, likenessRating:invalid});
    assert(normalized, 'Bad score does not discard other fields');
    assert.equal(normalized.likenessRating, null, 'Invalid score is Unrated: ' + JSON.stringify(invalid));
  }
  assert.equal(api.normalizedReview({id:ids.face, sha256:'0'.repeat(64), likenessRating:5}), null, 'Wrong hash cannot attach rating');
  checks++;

  const reloaded = boot(page.snapshot());
  assert.equal(reloaded.api.reviewRecord(ids.face).likenessRating, 4, 'Rating survives reload');
  const portable = clone(reloaded.api.reviewPayload());
  assert.equal(portable.items.find(r => r.id === ids.face).likenessRating, 4);
  const imported = boot({}, {...catalog, reviewDecisions:[]});
  imported.api.importReview(portable);
  assert.equal(imported.api.reviewRecord(ids.face).likenessRating, 4, 'Rating survives export/import');
  const reference = clone(imported.api.exportReference(imported.api.C.assets.find(a => a.id === ids.face)));
  assert.equal(reference.likenessRating, 4, 'Reference export carries rating');
  assert(/collar/.test(reference.knownDifferences || reference.note || ''), 'Reference export carries differences');
  checks++;

  const policy = clone(api.referenceUsePolicy(asset(ids.scene)));
  assert.equal(policy.explicitSceneReference.id, ids.scene);
  assert.equal(policy.explicitSceneReference.sha256, asset(ids.scene).sha256);
  assert.equal(policy.explicitSceneReference.scope, 'this_scene_only');
  assert.equal(policy.sceneSpecific, true);
  assert.equal(policy.imageDoesNotReplaceIdentity, true);
  assert.equal(policy.ratingDoesNotApprove, true);
  const defaults = clone(api.referenceUsePolicy(asset(ids.wrist))).defaultReferenceSelection;
  assert.equal(defaults.requiredRole, 'visible_jewelry_only', 'Reference match stays in component role');
  assert.equal(defaults.sameRoleRequired, true);
  assert.equal(defaults.unratedIsNotFive, true);
  assert(/gold|canonical/i.test(defaults.instruction));
  assert(/highest|rated/i.test(defaults.instruction));
  checks++;

  api.setState({project:'hon', view:'shot_plans', destination:'all', exportIntent:'prime', search:''});
  api.updateReview(ids.face, {shotPlan:{status:'planned', destinations:['Gemini'], idea:'Close-up at cab window.', prompt:'Keep locked mouth and wrist.'}});
  const planned = clone(api.shotHandoffPayload()).items.find(a => a.id === ids.face);
  assert(planned, 'Actual handoff includes planned reference');
  assert.equal(planned.likenessRating, 4);
  assert(planned.referenceUsePolicy || planned.referencePolicy || planned.policy, 'Handoff carries reference policy');
  api.exportShotHandoff('json');
  const exportedJSON = JSON.parse(await page.downloads.at(-1).blob.text());
  assert.equal(exportedJSON.items.find(a => a.id === ids.face).likenessRating, 4);
  api.exportShotHandoff('txt');
  const text = await page.downloads.at(-1).blob.text();
  assert(/likeness|reference rating/i.test(text), 'Text handoff names rating');
  assert(/4\s*(?:\/\s*5|out of 5)|rating[^\n]*4/i.test(text), 'Text carries bounded score');
  assert(/collar/.test(text), 'Text carries known differences');
  assert(/identity|canonical|reference policy|this.scene/i.test(text), 'Text states reference boundary');
  assert.deepEqual(clone(api.C.assets), originalAssets, 'Exports preserve metadata/hashes');
  checks++;

  console.log(JSON.stringify({passed:true, scenarios:checks, catalogAssets:catalog.assets.length, browserOverlay:overlay.exported, browserVisualQA:false}));
}
main().catch(error => {console.error(error); process.exitCode = 1;});
