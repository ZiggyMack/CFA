/* Neutral coordinator requests and assistant proposals use the real library and existing DOM double.
   These tests check state/rendering boundaries, not browser visual appearance. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const crypto = require('node:crypto');
const clone = value => JSON.parse(JSON.stringify(value));
const REVIEW_KEY = 'cfa-visual-review-v1', FAVORITES_KEY = 'cfa-visual-favorites-v1';
const catalogJS = fs.readFileSync(path.join(__dirname, 'catalog.js'), 'utf8');
const catalog = JSON.parse(catalogJS.slice(catalogJS.indexOf('=') + 1).trim().replace(/;$/, ''));
const requests = JSON.parse(fs.readFileSync(path.join(__dirname, 'review_requests.json'), 'utf8')).requests;
const root = path.resolve(__dirname, '../../../../../..');
for (const r of requests) {
  const a = catalog.assets.find(a => a.id === r.id);
  assert(a && r.sha256 === a.sha256, 'Request binds a catalog asset: ' + r.id);
  const actual = crypto.createHash('sha256').update(fs.readFileSync(path.join(root, a.repoPath))).digest('hex');
  assert.equal(actual, r.sha256, 'Request binds the unchanged disk source: ' + r.id);
}
assert.equal(requests.length, 3, 'The bounded missing-mouth-decision intake contains three requests');

const scopeTest = fs.readFileSync(path.join(__dirname, 'test_reference_scope.cjs'), 'utf8');
const bootSource = scopeTest.slice(scopeTest.indexOf('function boot('), scopeTest.indexOf('async function main()'));
const originalHook = 'window.__scopeTest={openViewer,reviewRecord,reviewPayload,importReview,exportReference,inReviewQueue,whenFileWritesSettle(){return fileWriteChain;}};';
const testHook = 'window.__scopeTest={C,reviewRecord,reviewPayload,importReview,exportReference,inReviewQueue,activeReviewRequest,workingBOMEntries,updateReview,openViewer,render,renderMain,viewerHTML(){return dialog.innerHTML;},setState(p){Object.assign(state,p);},whenFileWritesSettle(){return fileWriteChain;}};';
assert(bootSource.includes(originalHook), 'Existing DOM double exposes the expected hook');
const bootFunction = new Function('source','catalog','clone','assert','vm','REVIEW_KEY','FAVORITES_KEY','assets',
  bootSource.replace(originalHook, testHook) + ';return boot;');
function boot(saved = {}, input = catalog) {
  return bootFunction(fs.readFileSync(path.join(__dirname, 'library.js'), 'utf8'), catalog, clone,
    assert, vm, REVIEW_KEY, FAVORITES_KEY, catalog.assets)(saved, input);
}

async function main() {
  let checks = 0;
  const input = clone(catalog); input.reviewRequests = requests;
  // Keep the actual assets, ratings and scopes; make missing triage explicit in this fixture.
  for (const r of requests) {
    let decision = input.reviewDecisions.find(d => d.id === r.id);
    if (!decision) input.reviewDecisions.push(decision = {id:r.id, sha256:r.sha256, origin:'user'});
    decision.status = null;
  }
  const saved = {[REVIEW_KEY]:JSON.stringify({format:REVIEW_KEY, items:input.reviewDecisions})};
  const page = boot(saved, input), api = page.api;
  const asset = id => api.C.assets.find(a => a.id === id);
  const before = clone(api.reviewPayload().items);
  for (const r of requests) {
    assert(api.activeReviewRequest(asset(r.id)), 'A missing triage status activates its explicit request');
    assert.equal(api.inReviewQueue(asset(r.id)), true);
    assert.equal(api.reviewRecord(r.id).status, null, 'Request does not invent a user choice');
  }
  assert.deepEqual(clone(api.reviewPayload().items), before, 'Queue checks do not mutate reviews');
  assert.equal(api.reviewPayload().reviewRequests, undefined, 'Catalog requests are not stored as user reviews');
  checks++;

  api.setState({view:'review_queue'}); api.render();
  const queueHTML = page.node('#main').innerHTML;
  assert(queueHTML.includes('Awaiting your decision'));
  for (const r of requests) assert(queueHTML.includes(r.id), 'Requested asset rendered in queue: ' + r.id);
  page.open(requests[0].id);
  assert(api.viewerHTML().includes(requests[0].reason), 'Viewer presents the specific neutral reason');
  assert(api.viewerHTML().includes('Nova requested your decision'));
  checks++;

  const withoutRequests = boot(saved, {...input, reviewRequests:[]});
  assert.deepEqual(clone(api.workingBOMEntries()), clone(withoutRequests.api.workingBOMEntries()),
    'A coordinator request neither blocks nor broadens existing component approvals');
  checks++;

  for (const [i, status] of ['keep','needs_fixes','remove'].entries()) {
    const id = requests[i].id; const original = clone(api.reviewRecord(id));
    api.updateReview(id, {status});
    assert.equal(api.activeReviewRequest(asset(id)), null, 'A valid human choice closes the missing-decision request');
    assert.equal(api.reviewRecord(id).likenessRating, original.likenessRating, 'Triage preserves rating');
    assert.equal(api.reviewRecord(id).storyboardStage, original.storyboardStage, 'Triage preserves design stage');
    assert.equal(api.inReviewQueue(asset(id)), status !== 'keep', 'Existing fix/remove queue logic remains available');
  }
  api.updateReview(requests[0].id, {status:null});
  assert(api.activeReviewRequest(asset(requests[0].id)), 'Clearing a triage decision reopens the request');
  const reloaded = boot(page.snapshot(), input);
  assert(reloaded.api.activeReviewRequest(reloaded.api.C.assets.find(a => a.id === requests[0].id)),
    'Browser storage without requests cannot erase a catalog request');
  checks++;

  const id = requests[0].id;
  reloaded.api.importReview({format:REVIEW_KEY, items:[{id, sha256:requests[0].sha256, status:'keep', origin:'user'}], favorites:[]});
  assert.equal(reloaded.api.activeReviewRequest(reloaded.api.C.assets.find(a => a.id === id)), null);
  reloaded.api.updateReview(id, {status:null});
  assert(reloaded.api.activeReviewRequest(reloaded.api.C.assets.find(a => a.id === id)),
    'An imported user choice does not delete the catalog request');
  const invalid = boot(saved, {...input, reviewRequests:requests.map(r => ({...r, sha256:'0'.repeat(64)}))});
  for (const r of requests) assert.equal(invalid.api.activeReviewRequest(invalid.api.C.assets.find(a => a.id === r.id)), null,
    'A stale source hash cannot queue another image');
  checks++;

  // A high assistant proposal must never become a human score, approval or selection priority.
  const subject = catalog.assets.find(a => a.id === id), gold = catalog.assets.find(a => a.id === 'HD-B-91ef00348229');
  assert(gold, 'Actual scoped dental gold reference exists');
  const proposal = {assetID:id, sha256:subject.sha256, assessedBy:'nova', assessedAtUTC:'2026-10-10T16:00:00Z',
    likenessRating:5, scope:'visible_character_features', confidence:'low', summary:'Visible features only; the face is partly obscured.',
    observations:[{feature:'Grill', finding:'Visible gold matches; hidden teeth cannot be checked.', visibility:'partial', severity:'unverified'}],
    referenceAssets:[{assetID:gold.id, sha256:gold.sha256}], status:'proposal'};
  const proposalInput = {...input, assistantLikenessAssessments:[proposal]};
  const proposalPage = boot(saved, proposalInput), proposalAPI = proposalPage.api;
  const originalRecord = clone(proposalAPI.reviewRecord(id)), originalPayload = clone(proposalAPI.reviewPayload().items);
  proposalPage.open(id);
  assert(proposalAPI.viewerHTML().includes('Nova’s proposal: 5/5'));
  assert(proposalAPI.viewerHTML().includes('Hidden or obscured features cannot be verified'));
  assert(proposalAPI.viewerHTML().indexOf('reference-likeness-rating') < proposalAPI.viewerHTML().indexOf('Nova’s proposal'),
    'Proposal appears below the user rating selector');
  assert.deepEqual(clone(proposalAPI.reviewPayload().items), originalPayload);
  assert.equal(proposalAPI.exportReference(subject).likenessRating, originalRecord.likenessRating ?? null,
    'Reference export retains the user score, not the assistant score');
  assert.equal(proposalAPI.reviewPayload().assistantLikenessAssessments, undefined);
  assert.deepEqual(clone(proposalAPI.workingBOMEntries()), clone(boot(saved,input).api.workingBOMEntries()),
    'Proposal does not alter reference selection or approved scope');
  checks++;

  const selector = proposalPage.node('#reference-likeness-rating'); selector.value = '2'; selector.fire('change');
  assert.equal(proposalAPI.reviewRecord(id).likenessRating, 2, 'The actual user rating handler remains authoritative');
  assert.equal(proposalAPI.exportReference(subject).likenessRating, 2);
  assert.equal(proposalAPI.C.assistantLikenessAssessments[0].likenessRating, 5, 'User rating does not rewrite the recorded assistant proposal');
  const staleGold = boot(saved, {...proposalInput, assistantLikenessAssessments:[{...proposal, referenceAssets:[{assetID:gold.id, sha256:'0'.repeat(64)}]}]});
  staleGold.open(id); assert(!staleGold.api.viewerHTML().includes('Nova’s proposal'), 'Proposal with stale gold reference is hidden');
  const unassessable = boot(saved, {...proposalInput, assistantLikenessAssessments:[{...proposal, likenessRating:null}]});
  unassessable.open(id); assert(unassessable.api.viewerHTML().includes('Nova’s proposal: Not assessable'));
  checks++;

  console.log(`Review requests and assistant proposals: ${checks} checks passed.`);
}
main().catch(error => {console.error(error); process.exitCode = 1;});
