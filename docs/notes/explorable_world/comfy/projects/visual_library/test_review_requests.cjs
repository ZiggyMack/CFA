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
const sourceRequests = JSON.parse(fs.readFileSync(path.join(__dirname, 'review_requests.json'), 'utf8')).requests;
const mouthRequestIDs = ['HD-B-d98197d470ce', 'HD-VIS-5b76b446306e', 'HD-VIS-bb94cfd4b528'];
const requests = mouthRequestIDs.map(id => sourceRequests.find(request => request.id === id));
const root = path.resolve(__dirname, '../../../../../..');
for (const r of sourceRequests) {
  const a = catalog.assets.find(a => a.id === r.id);
  assert(a && r.sha256 === a.sha256, 'Request binds a catalog asset: ' + r.id);
  const actual = crypto.createHash('sha256').update(fs.readFileSync(path.join(root, a.repoPath))).digest('hex');
  assert.equal(actual, r.sha256, 'Request binds the unchanged disk source: ' + r.id);
}
assert(requests.every(Boolean), 'The three original mouth requests remain recorded');
assert.equal(new Set(sourceRequests.map(request => request.id)).size, sourceRequests.length, 'Source requests are unique by asset');
for (const id of ['HD-FALCON-ee485849b0e6528a', 'HD-FALCON-af69f68b13ef0012']) {
  const repair = sourceRequests.find(request => request.id === id);
  assert(repair && repair.requestedAt === '2026-10-14' && repair.type === 'missing_decision',
    'Later C04-002 repair request remains separate from the bounded mouth fixture: ' + id);
}

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

// Reuse the data-attribute DOM double for actual sidebar, Mission and triage handlers.
function bootPending(savedInput, input) {
  const text=fs.readFileSync(path.join(__dirname,'test_collections_navigation.cjs'),'utf8').replace(/\r\n/g,'\n');
  let body=text.slice(text.indexOf('function boot() {'),text.indexOf('\nconst page = boot(), api = page.api;'));
  assert(body.includes('reviewPayload,basketPayload,'));
  body=body.replace('function boot() {','function boot(savedInput) {')
    .replace('const storage = new Map(Object.entries(saved));','const storage = new Map(Object.entries({...saved,...savedInput}));')
    .replace('reviewPayload,basketPayload,','reviewPayload,basketPayload,pendingReviewDecision,inReviewQueue,activeReviewRequest,updateReview,importReview,openViewer,render,')
    .replace("html:() => nodes.get('#main').innerHTML,","html:() => nodes.get('#main').innerHTML,\n    selectAll,node:selector=>nodes.get(selector),");
  const countAnchor="this.children.add(child);\n      }\n    }\n    get innerHTML()";
  assert(body.includes(countAnchor));
  const countCode='      const queueCount=html.match(/data-view="review_queue"[^>]*>[\\s\\S]*?<span class="count">(\\d+)<\\/span>/);\n'+
    '      if(queueCount){const count=new Element("span");count.textContent=queueCount[1];nodes.set(\'[data-view="review_queue"] .count\',count);this.children.add(count);}\n';
  body=body.replace(countAnchor,'this.children.add(child);\n      }\n'+countCode+'    }\n    get innerHTML()');
  const execute=new Function('source','catalog','byID','clone','assert','vm','URL','Intl','console','REVIEW_KEY','FAVORITES_KEY','EXPORT_KEY',body+'\nreturn boot;');
  return execute(fs.readFileSync(path.join(__dirname,'library.js'),'utf8'),input,new Map(input.assets.map(a=>[a.id,a])),clone,assert,vm,URL,Intl,console,REVIEW_KEY,FAVORITES_KEY,'cfa-visual-export-v1')(savedInput);
}
function pendingDecisionCoverage(input,saved) {
  const p=bootPending(saved,input),initialCatalog=clone(p.C),initialFavorites=p.storage.get(FAVORITES_KEY),initialBasket=clone(p.api.basketPayload(true).items);
  const target=id=>p.C.assets.find(a=>a.id===id);
  const click=(page,attribute,value)=>{const b=page.selectAll('['+attribute+'="'+value+'"]')[0];assert(b,'Actual bound button: '+attribute+'='+value);assert.equal(typeof b.onclick,'function');b.click();};
  const pending=(page,project='hon')=>page.C.assets.filter(a=>a.project===project&&page.api.pendingReviewDecision(a)).map(a=>a.id);
  const sidebar=page=>Number(page.node('[data-view="review_queue"] .count').textContent);
  const comparable=value=>value===undefined?undefined:clone(value);
  function outsideClosedDetails(html){
    let result='',last=0;const stack=[];
    for(const match of html.matchAll(/<\/?details\b[^>]*>/g)){
      if(!stack.includes(true))result+=html.slice(last,match.index);
      if(/^<\//.test(match[0]))stack.pop();else stack.push(!/\sopen(?:\s|=|>)/.test(match[0]));
      last=match.index+match[0].length;
    }
    if(!stack.includes(true))result+=html.slice(last);return result;
  }
  function countersAndRoutes(page,expected,project='hon'){
    const before=clone(page.api.reviewPayload().items),writes=page.writes.length;
    page.api.setState({project,view:'mission_control',album:'',search:''});page.api.render();
    assert.equal(pending(page,project).length,expected);assert.equal(sidebar(page),expected,'Sidebar counts unanswered visible requests only');
    const mission=page.html().match(/data-mission-view="review_queue"[^>]*>[^<]*?(\d+)<\/button>/);
    if(expected){
      assert(mission,'Mission contains project review navigation');assert.equal(Number(mission[1]),expected,'Mission and sidebar agree');
      click(page,'data-mission-view','review_queue');
      assert.equal(page.location.hash.replace(/^#/,''),project+'/review_queue');assert.equal(page.api.getState().view,'review_queue');assert.equal(page.api.getState().project,project);
      assert(page.html().includes(expected+' unanswered image requests'),'Button opens the queue whose pending count was shown');
    }else{
      assert(!mission,'No empty Image review action is presented');assert(page.html().includes('No images awaiting your review'));
    }
    page.api.setState({view:'all'});page.api.render();click(page,'data-view','review_queue');
    assert.equal(page.location.hash.replace(/^#/,''),project+'/review_queue');assert(page.html().includes(expected+' unanswered image requests'));
    assert.deepEqual(clone(page.api.reviewPayload().items),before,'Count rendering and both routes are read-only');assert.equal(page.writes.length,writes);
  }
  function decide(page,id,status){
    page.api.openViewer(id);click(page,'data-review-status',status||'');
    assert.equal(page.api.reviewRecord(id).status,status);
  }
  countersAndRoutes(p,3);countersAndRoutes(p,0,'lisan');countersAndRoutes(p,3);
  assert.deepEqual(pending(p).sort(),requests.map(r=>r.id).sort());
  for(const [index,status] of ['keep','needs_fixes','remove'].entries()){
    const id=requests[index].id,before=clone(p.api.reviewRecord(id));
    decide(p,id,status);
    assert.equal(sidebar(p),2-index,'Triage immediately decrements the live sidebar, including Fix and Remove');
    assert.equal(p.api.pendingReviewDecision(target(id)),false);
    assert.equal(p.api.inReviewQueue(target(id)),status!=='keep','Fix/removal history remains in the broad queue');
    for(const field of ['likenessRating','sceneQualityRating','storyboardStage','workingReference','workingReferenceScope','shotPlan','note'])
      assert.deepEqual(comparable(p.api.reviewRecord(id)[field]),comparable(before[field]),'Triage preserves '+field);
    countersAndRoutes(p,2-index);
  }
  const zero=p.html(),visible=outsideClosedDetails(zero);
  assert(visible.includes('No unanswered image review requests. Saved decisions remain available above.'));
  assert(!visible.includes('data-open="'+requests[1].id+'"')&&!visible.includes('data-open="'+requests[2].id+'"'),'Answered fixes/removals do not flood the default queue');
  for(const title of ['Saved decisions · Needs fixes']){
    const drawer=zero.match(new RegExp('<details\\b([^>]*)><summary>'+title+'[^<]*<\\/summary>'));
    assert(drawer,'Saved history remains available: '+title);assert(drawer[1].includes('review-history'));assert(!/\sopen(?:\s|=|$)/.test(drawer[1]),'Saved history starts closed');
  }
  assert(zero.includes('data-open="'+requests[1].id+'"'));click(p,'data-open',requests[1].id);
  assert(!zero.includes('data-open="'+requests[2].id+'"'),'Removed reference no longer appears in Review queue');
  p.api.setState({view:'archive',album:'',search:''});p.api.render();
  const archive=p.html(),removalDrawer=archive.match(/<details\b([^>]*)><summary>Saved removal decisions and archive[^<]*<\/summary>/);
  assert(removalDrawer&&!/\sopen(?:\s|=|$)/.test(removalDrawer[1]),'Removal history is available in a closed Archive drawer');
  assert(archive.includes('data-open="'+requests[2].id+'"'));click(p,'data-open',requests[2].id);
  const reloaded=bootPending(Object.fromEntries(p.storage),input);countersAndRoutes(reloaded,0);
  for(const [index,status] of ['keep','needs_fixes','remove'].entries())assert.equal(reloaded.api.reviewRecord(requests[index].id).status,status,'Saved decisions survive reload');
  const id=requests[0].id;decide(reloaded,id,null);assert.equal(sidebar(reloaded),1);countersAndRoutes(reloaded,1);
  const cleared=bootPending(Object.fromEntries(reloaded.storage),input);countersAndRoutes(cleared,1);
  const favorites=JSON.parse(cleared.storage.get(FAVORITES_KEY)||'[]');
  cleared.api.importReview({format:REVIEW_KEY,items:[{id,sha256:'0'.repeat(64),status:'keep'}],favorites});
  assert.equal(cleared.api.reviewRecord(id).status,null,'Wrong review hash cannot close the request');countersAndRoutes(cleared,1);
  cleared.api.importReview({format:REVIEW_KEY,items:[{id,sha256:requests[0].sha256,status:'keep'}],favorites});
  countersAndRoutes(cleared,0);decide(cleared,id,null);countersAndRoutes(cleared,1);
  const invalid=bootPending(saved,{...input,reviewRequests:requests.map(r=>({...r,sha256:'0'.repeat(64)}))});
  countersAndRoutes(invalid,0);
  for(const r of requests)assert.equal(invalid.api.activeReviewRequest(invalid.C.assets.find(a=>a.id===r.id)),null,'Stale request hash never queues an image');
  const archivedInput=clone(input),archivedSaved=clone(saved),archivedReview=JSON.parse(archivedSaved[REVIEW_KEY]);
  archivedReview.items.find(record=>record.id===id).collectionState='archived';
  archivedSaved[REVIEW_KEY]=JSON.stringify(archivedReview);
  const archived=bootPending(archivedSaved,archivedInput);countersAndRoutes(archived,2);
  assert.equal(archived.api.pendingReviewDecision(archived.C.assets.find(a=>a.id===id)),false,'Archived request is not pending');
  assert.equal(archived.api.inReviewQueue(archived.C.assets.find(a=>a.id===id)),true,'Archived history remains available');
  assert.deepEqual(clone(p.C),initialCatalog,'Triage never modifies source catalog, requests, approvals or timing');
  assert.equal(p.storage.get(FAVORITES_KEY),initialFavorites);assert.deepEqual(clone(p.api.basketPayload(true).items),initialBasket);
  assert.equal(fs.readFileSync(path.join(__dirname,'catalog.js'),'utf8'),catalogJS,'No production catalog mutation');
  return 7;
}

async function main() {
  let checks = 0;
  const input = clone(catalog); input.reviewRequests = requests;
  // Keep the actual assets, ratings and scopes. Older mouth sources are now historical;
  // explicitly restore only this isolated fixture so it can exercise three pending choices.
  for (const r of requests) {
    let decision = input.reviewDecisions.find(d => d.id === r.id);
    if (!decision) input.reviewDecisions.push(decision = {id:r.id, sha256:r.sha256, origin:'user'});
    decision.status = null;
    decision.collectionState = 'working';
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

  checks += pendingDecisionCoverage(input,saved);
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
