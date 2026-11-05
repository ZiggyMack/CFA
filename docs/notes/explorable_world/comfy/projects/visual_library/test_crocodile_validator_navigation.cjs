/* Real-catalog Crocodile reachability and validator browsing actions.
   Reuses the established DOM/storage double; this is not browser visual QA. */
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const clone=value=>JSON.parse(JSON.stringify(value));
const source=fs.readFileSync(path.join(__dirname,'library.js'),'utf8');
const raw=fs.readFileSync(path.join(__dirname,'catalog.js'),'utf8');
const catalog=JSON.parse(raw.slice(raw.indexOf('=')+1).trim().replace(/;$/,''));
const byID=new Map(catalog.assets.map(a=>[a.id,a]));
const REVIEW_KEY='cfa-visual-review-v1',FAVORITES_KEY='cfa-visual-favorites-v1',EXPORT_KEY='cfa-visual-export-v1';
const existing=fs.readFileSync(path.join(__dirname,'test_collections_navigation.cjs'),'utf8');
let bootSource=existing.slice(existing.indexOf('function boot()'),existing.indexOf('const page = boot()'));
const hook='window.__collectionsTest={';
assert(bootSource.includes(hook),'Shared navigation harness is available');
bootSource=bootSource.replace(hook,hook+'clickMission(project,view){const button=[...document.querySelectorAll("[data-mission-view]")].find(b=>b.dataset.missionProject===project&&b.dataset.missionView===view);if(!button)throw Error("Missing action: "+project+"/"+view);button.click();},');
const boot=new Function('source','catalog','byID','clone','assert','vm','REVIEW_KEY','FAVORITES_KEY','EXPORT_KEY',bootSource+';return boot;')(source,catalog,byID,clone,assert,vm,REVIEW_KEY,FAVORITES_KEY,EXPORT_KEY);
const page=boot(),api=page.api;
const before={reviews:clone(api.reviewPayload().items),assets:clone(page.C.assets),albums:clone(page.C.albums),cast:clone(page.C.castCollections),storage:Object.fromEntries(page.storage)};
const cast=page.C.castCollections.find(g=>g.id==='hon:boss-round01'),anchor='HD-RETURN-8421e7cfa1a0';
assert(cast,'Existing Crocodile character is retained');
assert.equal(cast.coverID,anchor,'Selected BOSS-008 remains the cover');
assert.equal(cast.representativeID,anchor,'Character hub retains the exact selected representative');
assert.deepEqual(clone(cast.currentIDs),[anchor],'New studies do not replace the selected reference');
assert.deepEqual(clone(cast.workingReferenceIDs),[anchor],'New studies are not implicitly selected or approved');
assert.equal(cast.characterStudyIDs.length,15);
assert.equal(cast.sceneStudyIDs.length,15);
assert.equal(cast.revisionStudyIDs.length,3);
const incoming=[...cast.characterStudyIDs,...cast.sceneStudyIDs,...cast.revisionStudyIDs];
assert.equal(new Set(incoming).size,33,'Thirty-three distinct received images have one study role each');
assert.deepEqual([...cast.sceneAssetIDs].sort(),[...incoming].sort(),'All received images are connected to the existing character hub');
for(const id of incoming){
  assert(byID.has(id),'Every mapped image exists: '+id);
  assert(cast.assetIDs.includes(id),'Every received image belongs to the character: '+id);
  assert(api.normalVisible(byID.get(id)),'Received image is browseable: '+id);
}
let checks=1;
function go(hash){page.location.hash=hash;api.parseHash();api.expandedCollections.clear();api.renderMain();}
function assertMedia(ids,message){for(const id of ids)assert.equal([...page.html().matchAll(new RegExp('data-open="'+id+'"','g'))].length,1,message+': '+id);}
for(const hash of ['#hon/working','#hon/working/hon%3Aboss-round01']){
  go(hash);
  assert(page.toggles(cast.id+'-working').length,'Crocodile is reachable from Working route: '+hash);
  assert(!page.html().includes('data-open="'+incoming[0]+'"'),'Received views start collapsed');
  page.toggle(cast.id+'-working');
  assert.equal(page.location.hash,hash,'Expansion stays on its current route');
  const work=api.castWorkingGroups(cast.id)[0];
  assert.equal(work.cover.id,anchor);
  assert.equal(work.items.length,34,'Selected anchor plus 33 received studies are visible');
  assertMedia([anchor,...incoming],'Each Working image is reachable exactly once');
  for(const title of ['Boss dais · character and staging candidates','Counting room · scene candidates','Earlier repair versions'])assert(page.html().includes(title),'Study roles remain separated: '+title);
  assert(page.html().includes('#hon/cast/hon%3Aboss-round01'),'Working links to the same character hub');
  checks++;
}
for(const hash of ['#hon/cast','#hon/cast/hon%3Aboss-round01']){
  go(hash);page.toggle(cast.id);
  const hub=api.castHubGroups(cast.id)[0];
  assert.equal(hub.cover.id,anchor);
  assert.equal(hub.items.length,34,'Hub connects selected anchor and all 33 received views');
  assertMedia([anchor,...incoming],'Each hub image is reachable exactly once');
  for(const [title,count] of [['Boss dais · character and staging candidates',15],['Counting room · scene candidates',15],['Earlier repair versions',3]]){
    const section=hub.sections.find(s=>s.title===title);
    assert.equal(section?.assetIDs.length,count,'Hub preserves the distinct study group: '+title);
    assert(page.html().includes(title),'Expanded hub exposes the named study group: '+title);
  }
  assert(!hub.sections.some(s=>s.title==='Scene appearances'),'Received studies are not duplicated inside a generic scene drawer');
  assert(page.html().includes('#hon/working/hon%3Aboss-round01'),'Hub has a direct route back to these Working references');
  checks++;
}
const task=page.C.missionControl.tasks.find(t=>t.id==='reference-validation-evidence-ui-20261013');
assert.equal(task.status,'in_progress');
assert.equal(task.backgroundDetails,true);
const expected=[['hon','intake'],['lisan','intake'],['hon','working'],['lisan','working']];
assert.deepEqual(clone(task.userAction.links.map(l=>[l.project,l.view])),expected,'Four explicit user destinations are configured');
go('#hon/mission_control');
let html=page.html();
const card=html.match(new RegExp('<article[^>]*data-task-id="'+task.id+'"[\\s\\S]*?</article>'))?.[0];
assert(card,'Validator card appears in Mission Control');
assert(card.includes('For you now')&&card.includes('No new validator decision is waiting on you'),'The visible instruction distinguishes browsing from a new decision request');
const background=card.match(/<details class="mission-background"[^>]*>/)?.[0];
assert(background&&!/\sopen(?:\s|=|>)/.test(background),'Technical background begins closed');
assert(card.indexOf('mission-user-action')<card.indexOf('mission-background'),'Browsing actions precede team records');
assert(card.includes('Team progress and source records')&&card.includes('Team next step:'),'Owner work is labeled as team work');
assert.equal((card.match(/data-mission-project=/g)||[]).length,4);
for(const [project,view] of expected){
  go('#hon/mission_control');
  api.setState({search:'stale filter',intakeDataset:'not-a-current-dataset',intakeFilter:'unavailable',intakePage:99});
  api.clickMission(project,view);
  assert.equal(api.getState().project,project,'Action selects its named project');
  assert.equal(api.getState().view,view,'Action selects its named view');
  assert.equal(api.getState().album,'','Action starts at the full destination');
  assert.equal(page.location.hash.replace(/^#/,''),project+'/'+view,'The destination is shareable through the real hash route');
  assert.equal(api.getState().search,'','User action clears stale search');
  assert.equal(api.getState().intakeDataset,'all');
  assert.equal(api.getState().intakeFilter,'all');
  assert.equal(api.getState().intakePage,0);
  api.parseHash();api.renderMain();
  assert.equal(api.getState().project,project);assert.equal(api.getState().view,view);
  if(view==='intake')assert(page.html().includes('Frozen handoff r002'),'Intake route renders the existing handoff');
  else assert(page.html().includes('Character bill of materials'),'Working route renders reference collections');
  checks++;
}
assert.deepEqual(clone(api.reviewPayload().items),before.reviews,'Browsing never changes saved review decisions');
assert.deepEqual(clone(page.C.assets),before.assets,'Source asset metadata is unchanged');
assert.deepEqual(clone(page.C.albums),before.albums,'Album memberships are unchanged');
assert.deepEqual(clone(page.C.castCollections),before.cast,'Character membership and selected anchor remain unchanged');
assert.deepEqual(Object.fromEntries(page.storage),before.storage,'Reviews, favorites and export basket remain byte-equivalent');
assert.equal(page.writes.length,0,'Browsing writes no local storage');
console.log(JSON.stringify({passed:true,checks,crocodileNewImages:33,workingImages:34,hubImages:34,selectedAnchorPreserved:true,validatorActions:4,backgroundClosed:true,reviewWrites:0,browserVisualQA:false}));
