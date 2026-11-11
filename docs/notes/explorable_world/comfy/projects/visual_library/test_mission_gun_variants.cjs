/* Actual-library regression check using the existing DOM/storage double.
   Review changes below are isolated fixtures, never saved user decisions.
   Verifies rendered markup, bound image actions and hash routing, not layout. */
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),crypto=require('node:crypto');
const clone=value=>JSON.parse(JSON.stringify(value));
const root=__dirname,source=fs.readFileSync(path.join(root,'library.js'),'utf8');
const raw=fs.readFileSync(path.join(root,'catalog.js'),'utf8');
const catalog=JSON.parse(raw.slice(raw.indexOf('=')+1).trim().replace(/;$/,''));
const byID=new Map(catalog.assets.map(a=>[a.id,a]));
const REVIEW_KEY='cfa-visual-review-v1',FAVORITES_KEY='cfa-visual-favorites-v1',EXPORT_KEY='cfa-visual-export-v1';
const existing=fs.readFileSync(path.join(root,'test_collections_navigation.cjs'),'utf8');
let bootSource=existing.slice(existing.indexOf('function boot()'),existing.indexOf('const page = boot()'));
const oldHook='window.__collectionsTest={normalVisible,collectionCards,collectionGroups,sharedCharacterReferences,castExplorer,castHubGroups,castWorkingGroups,parseHash,detailAlbumGroups,renderMain,expandedCollections,reviews,reviewRecord,reviewPayload,basketPayload,setState(p){Object.assign(state,p);},getState(){return state;}};';
const hook='window.__collectionsTest={C,reviews,reviewRecord,reviewPayload,normalVisible,missionTaskPresentation,missionTaskCard,outfitGunReviewAssets,outfitGunReviewLinks,renderMain,parseHash,setState(p){Object.assign(state,p);},getState(){return state;},getCurrentID(){return currentID;},gunButtons(id){return [...document.querySelectorAll("[data-open]")].filter(b=>b.dataset.open===id);},albumLinks(href){return [...document.querySelectorAll("[href]")].filter(a=>a.tag==="a"&&a.href===href);},closeViewer(){document.querySelector("#close-viewer")?.click();},viewerHTML(){return dialog.innerHTML;}};';
assert(bootSource.includes(oldHook),'The shared DOM double exposes the expected instrumentation point');
bootSource=bootSource.replace(oldHook,hook).replace('function boot() {','function boot(browserRecords=[]) {').replace('items:[storedReview]','items:[storedReview,...browserRecords]');
assert(bootSource.includes('items:[storedReview,...browserRecords]'),'Browser overlays load through the real review importer');
const boot=new Function('source','catalog','byID','clone','assert','vm','REVIEW_KEY','FAVORITES_KEY','EXPORT_KEY',bootSource+';return boot;')(source,catalog,byID,clone,assert,vm,REVIEW_KEY,FAVORITES_KEY,EXPORT_KEY);
const expectedIDs=[
  'HD-RETURN-2f30bc9f7c38','HD-RETURN-a460b7c979de','HD-RETURN-8b34de066ace',
  'HD-RETURN-957897bd45c4','HD-RETURN-766f51a7e850','HD-RETURN-6aec219ca1aa',
  'HD-RETURN-4c2ad7996c90','HD-RETURN-ec68c973d240','HD-RETURN-c35561756692',
  'HD-RETURN-a0217b496d6c','HD-RETURN-8b4faedeee99','HD-RETURN-7d5aa7ef2c92',
  'HD-RETURN-26a91590b6c0','HD-RETURN-3b8efde8889d','HD-RETURN-efc1886a0d62',
  'HD-RETURN-53315f76a5d4','HD-RETURN-86cb39e4d5b6'
];
const yellowID='HD-RETURN-86cb39e4d5b6',burgundyID='HD-RETURN-efc1886a0d62';
const page=boot(),api=page.api,task=page.C.missionControl.tasks.find(t=>t.id==='favorites-prop-sweep');
assert(task,'The gun-variant handoff exists');
const originalCatalog=clone(catalog),originalPageCatalog=clone(page.C),originalTask=clone(task);
const originalReviews=clone(api.reviewPayload().items),originalStorage=Object.fromEntries(page.storage);
const received=api.outfitGunReviewAssets();
assert.deepEqual([...received.map(a=>a.id)].sort(),[...expectedIDs].sort(),'Exactly the 17 canonical received variants are selected');
assert.equal(new Set(received.map(a=>a.sha256)).size,17,'The duplicate Saloon filename is one canonical image');
assert.equal(new Set(received.map(a=>a.outfitAlbumID)).size,17,'Every variant belongs to a different outfit');
for(const a of received){
  assert.equal(a.sourceIntake,'HON-GROK-RETURN-20261009');assert.equal(a.propState,'with_gun');
  assert.equal(a.project,'hon');assert.equal(a.kind,'image');
  assert(page.C.albums.find(al=>al.id===a.outfitAlbumID)?.assetIDs.includes(a.id),'Variant is a real member of its linked outfit: '+a.id);
}
const initialRecords=new Map(received.map(a=>[a.id,clone(api.reviewRecord(a.id))]));
function expectedCounts(p){
  const assets=new Map(p.C.assets.map(a=>[a.id,a]));
  const visible=received.filter(a=>p.api.normalVisible(assets.get(a.id)));
  const records=received.map(a=>p.api.reviewRecord(a.id));
  const pending=visible.filter(a=>!['keep','needs_fixes','remove'].includes(p.api.reviewRecord(a.id).status)).length;
  const keep=records.filter(r=>r.status==='keep').length,fixes=records.filter(r=>r.status==='needs_fixes').length,removed=records.filter(r=>r.status==='remove').length;
  return {visible:visible.length,hidden:received.length-visible.length,pending,keep,fixes,removed,answered:keep+fixes+removed,unavailable:received.length-pending-keep-fixes-removed};
}
for(const id of [yellowID,burgundyID]){
  const canonical=catalog.reviewDecisions.find(r=>r.id===id),record=api.reviewRecord(id);
  assert(canonical&&/gun/i.test(canonical.note)&&/approved/i.test(canonical.note),'Scoped gun approval is retained in the user note');
  // Burgundy can change from Keep to Needs fixes without invalidating its gun approval.
  for(const key of ['status','note','likenessRating','sceneQualityRating','variant','storyboardStage'])
    assert.deepEqual(record[key],canonical[key],'Canonical whole-image review is respected independently of gun approval: '+id+' '+key);
}
const yellowAlbum=page.C.albums.find(al=>al.id==='hon:outfit-yellow');
assert.equal(yellowAlbum.assetIDs.length,8);assert(yellowAlbum.assetIDs.includes(yellowID));
assert.equal(new Set([...expectedIDs,...yellowAlbum.assetIDs]).size,24,'The eight yellow views contribute seven additional originals, not eight new gun variants');

function render(p=page){p.api.setState({project:'hon',view:'mission_control',album:'',search:'gun variants'});p.api.renderMain();return p.html();}
function group(html){const m=html.match(/<section class="mission-resource-group" data-resource-group="gun-variants">([\s\S]*?)<\/section>/);assert(m,'The complete gun-variant group is rendered');return m[1];}
function assertPresentation(p,expected){
  const t=p.C.missionControl.tasks.find(t=>t.id===task.id),shown=p.api.missionTaskPresentation(t),html=render(p),markup=group(html);
  assert.equal(shown.reviewProgress.requested,17);assert.equal(shown.reviewProgress.answered,expected.answered);
  assert.equal(shown.reviewProgress.pendingIDs.length,expected.pending);assert.equal(shown.reviewProgress.unavailableIDs.length,expected.unavailable);
  assert(shown.summary.includes(expected.keep+' Keep, '+expected.fixes+' Needs fixes, '+expected.removed+' marked for removal'));
  assert.equal(shown.status,expected.pending?'needs_input':'in_progress');
  assert.equal((markup.match(/data-gun-variant=/g)||[]).length,expected.pending+expected.answered);
  assert.equal((markup.match(/data-open=/g)||[]).length,expected.pending+expected.answered,'One action per pending or answered variant, including removed history');
  const card=p.api.missionTaskCard(shown);
  for(const id of [...shown.previewAssetIDs,...shown.reviewedPreviewAssetIDs])assert.equal((card.match(new RegExp('data-open="'+id+'"','g'))||[]).length,1,'Dedicated outfit comparisons do not duplicate the generic history: '+id);
  assert.equal(new Set([...markup.matchAll(/data-gun-variant="([^"]+)"/g)].map(m=>m[1])).size,expected.pending+expected.answered);
  assert.equal(shown.missing.length,expected.pending||expected.unavailable?1:0);
  if(expected.pending)assert.equal(shown.title,task.reviewGate.label+' · '+expected.pending+' awaiting review');
  else if(expected.unavailable)assert.equal(shown.statusLabel,'Reference check needed');
  else assert.equal(shown.title,task.reviewGate.completed.title);
  assert(html.includes(shown.title),'Mission Control uses the derived title, not the stale source title');
  return {shown,markup,html};
}
const base=expectedCounts(page),initialVisible=received.filter(a=>!a.archived&&initialRecords.get(a.id).status!=='remove');
let displayed=assertPresentation(page,base);
assert(displayed.markup.includes('<details><summary>Already reviewed · '+base.answered+'</summary>'),'All answered variants remain available in a closed drawer');
assert(!displayed.markup.includes('<details open'),'Existing reviews do not flood the pending list');
const pendingMarkup=displayed.markup.split('<details>')[0],reviewedMarkup=displayed.markup.split('<details>')[1];
assert.equal((pendingMarkup.match(/data-gun-variant=/g)||[]).length,base.pending);
assert.equal((reviewedMarkup.match(/data-gun-variant=/g)||[]).length,base.answered);
assert(displayed.shown.summary.includes('Gun-placement approval remains scoped'));
assert.equal(displayed.shown.nextAction,task.reviewGate.completed.nextAction);
assert.deepEqual(clone(displayed.shown.links),clone(task.links),'Source links remain unchanged; rendering deduplicates target actions');
for(const link of task.links.filter(link=>!link.assetID&&!/outfit-yellow/.test(link.href||'')))assert(displayed.shown.links.some(l=>l.href===link.href),'Prepared reading links are preserved');
assert.deepEqual(clone(task),originalTask,'Presentation leaves the canonical handoff untouched');

for(const a of received){
  render();
  const button=api.gunButtons(a.id);assert(button.length>=1,'Real bound image button: '+a.id);
  assert.equal((group(page.html()).match(new RegExp('data-open="'+a.id+'"','g'))||[]).length,1,'One action in the gun-variant handoff; separate character adoption may link the same source');
  assert.equal(typeof button[0].onclick,'function');button[0].click();
  assert.equal(api.getCurrentID(),a.id,'The actual click handler opens the requested image');
  if([yellowID,burgundyID].includes(a.id))assert(api.viewerHTML().includes(initialRecords.get(a.id).note),'Viewer retains the scoped approval note');
  api.closeViewer();
  const album=page.C.albums.find(al=>al.id===a.outfitAlbumID),href='#hon/outfits/'+encodeURIComponent(album.id);
  const links=api.albumLinks(href);assert.equal(links.length,1,'The real rendered outfit anchor is present: '+album.id);
  assert.equal(links[0].href,href);
  const row=group(page.html()).match(new RegExp('<div class="mission-variant-tile" data-gun-variant="'+a.id+'">([\\s\\S]*?)</div>'))[1];
  const visibleCount=album.assetIDs.filter(id=>{const asset=page.C.assets.find(a=>a.id===id);return asset&&!asset.archived&&api.reviewRecord(id).status!=='remove';}).length;
  assert(row.includes('Compare full outfit · '+visibleCount+' images'),'Comparison count includes visible originals and the gun variant: '+album.id);
  // A browser follows this native anchor; simulate its URL, then use the real router.
  page.location.hash=links[0].href;api.parseHash();api.renderMain();
  assert.equal(api.getState().project,'hon');assert.equal(api.getState().view,'outfits');assert.equal(api.getState().album,album.id);
  assert(page.html().includes('<h1>'+album.title+'</h1>'),'The outfit link resolves to the requested collection');
}
assert.deepEqual(clone(api.reviewPayload().items),originalReviews,'Opening all variants and outfits never creates a review');

// Load an explicit, isolated browser overlay through the actual storage importer.
const candidate=received.find(a=>!initialRecords.get(a.id).status)||initialVisible.find(a=>![yellowID,burgundyID].includes(a.id));
assert(candidate,'A visible variant is available for isolated review transitions');
const overlayRecord={...initialRecords.get(candidate.id),id:candidate.id,sha256:candidate.sha256,origin:'browser',status:'needs_fixes',note:'TEST FIXTURE ONLY: preserve the gun; fix character likeness.',updatedAt:'2099-01-01T00:00:00.000Z'};
const overlayPage=boot([overlayRecord]),overlayBefore=clone(overlayPage.api.reviewPayload().items),overlayCatalog=clone(overlayPage.C),overlayStorage=Object.fromEntries(overlayPage.storage);
assert.equal(overlayPage.api.reviewRecord(candidate.id).origin,'browser');
assert.equal(overlayPage.api.reviewRecord(candidate.id).status,'needs_fixes');
assertPresentation(overlayPage,expectedCounts(overlayPage));
assert.deepEqual(clone(overlayPage.api.reviewPayload().items),overlayBefore,'Browser-overlay rendering only reads the imported decisions');
assert.deepEqual(clone(overlayPage.C),overlayCatalog);assert.deepEqual(Object.fromEntries(overlayPage.storage),overlayStorage);assert.equal(overlayPage.writes.length,0);

// Simulate a live review refresh in memory; no updateReview/save helper is called.
function fixture(id,patch){api.reviews.set(id,{...api.reviewRecord(id),...patch});}
function restoreReviews(){api.reviews.clear();for(const r of originalReviews)api.reviews.set(r.id,clone(r));}
fixture(burgundyID,{status:'needs_fixes',sceneQualityRating:5,likenessRating:2});
assertPresentation(page,expectedCounts(page));
assert.equal(api.reviewRecord(burgundyID).note,initialRecords.get(burgundyID).note,'Changing whole-image status preserves the approved gun note');
restoreReviews();
fixture(candidate.id,{status:null});assertPresentation(page,expectedCounts(page));
fixture(candidate.id,{status:'keep'});assertPresentation(page,expectedCounts(page));
fixture(candidate.id,{status:'needs_fixes'});assertPresentation(page,expectedCounts(page));
fixture(candidate.id,{status:null});assertPresentation(page,expectedCounts(page));
restoreReviews();
fixture(yellowID,{status:'remove'});
displayed=assertPresentation(page,expectedCounts(page));
assert(displayed.markup.includes('data-gun-variant="'+yellowID+'"'),'Removal stays in answered history');assert.equal(api.reviewRecord(yellowID).note,initialRecords.get(yellowID).note);
restoreReviews();
const archiveCandidate=page.C.assets.find(a=>a.id===candidate.id),wasArchived=archiveCandidate.archived;
archiveCandidate.archived=true;
displayed=assertPresentation(page,expectedCounts(page));assert(displayed.markup.includes('data-gun-variant="'+candidate.id+'"'),'Archived decisions remain reachable in history');
if(wasArchived===undefined)delete archiveCandidate.archived;else archiveCandidate.archived=wasArchived;
const yellowOriginal=yellowAlbum.assetIDs.find(id=>id!==yellowID),originalRecord=api.reviews.get(yellowOriginal);
fixture(yellowOriginal,{status:'remove'});displayed=assertPresentation(page,base);
assert(displayed.markup.match(new RegExp('data-gun-variant="'+yellowID+'">([\\s\\S]*?)</div>'))[1].includes('Compare full outfit · 7 images'),'Removing an original updates only its full-outfit count');
if(originalRecord===undefined)api.reviews.delete(yellowOriginal);else api.reviews.set(yellowOriginal,originalRecord);

for(const a of received)if(!api.reviewRecord(a.id).status)fixture(a.id,{status:'keep'});
const noPendingBefore=clone(api.reviewPayload().items);
displayed=assertPresentation(page,expectedCounts(page));
assert.equal(displayed.shown.status,'in_progress','Review completion remains separate from repair and dispatch completion');
assert.deepEqual(clone(api.reviewPayload().items),noPendingBefore,'Completion calculation never fabricates image approvals');
for(const a of received)fixture(a.id,{status:'keep'});
const allKeptBefore=clone(api.reviewPayload().items);
assert.equal(assertPresentation(page,expectedCounts(page)).shown.status,'in_progress','Keep decisions do not invent completed follow-up');
assert.deepEqual(clone(api.reviewPayload().items),allKeptBefore);
for(const a of received)fixture(a.id,{status:'remove'});
const allRemovedBefore=clone(api.reviewPayload().items);
displayed=assertPresentation(page,expectedCounts(page));
assert(displayed.markup.includes('Already reviewed · 17'),'All removed versions remain inspectable as answered history');
assert.deepEqual(clone(api.reviewPayload().items),allRemovedBefore,'An empty visible set does not turn removed images into accepted ones');
restoreReviews();assertPresentation(page,base);
assert.deepEqual(clone(api.reviewPayload().items),originalReviews);
assert.deepEqual(clone(page.C),originalPageCatalog,'Every catalog and handoff field is preserved');
assert.deepEqual(clone(catalog),originalCatalog,'The source catalog object is unchanged');
assert.deepEqual(Object.fromEntries(page.storage),originalStorage,'Reading and navigation leave browser review/favorites/basket storage untouched');
assert.equal(page.writes.length,0,'No localStorage writes occurred');
assert.equal(fs.readFileSync(path.join(root,'library.js'),'utf8'),source,'The test does not edit the renderer');
assert.equal(fs.readFileSync(path.join(root,'catalog.js'),'utf8'),raw,'The test does not edit the catalog');
const sha=text=>crypto.createHash('sha256').update(text).digest('hex');
console.log(JSON.stringify({passed:true,uniqueVariants:17,uniqueOutfits:17,initialUnreviewed:base.pending,initialReviewed:base.answered,initialHidden:base.hidden,initialKeep:base.keep,initialNeedsFixes:base.fixes,initialRemoved:base.removed,yellowFullOutfit:8,yellowVariantIncluded:true,boundImageButtonsVerified:received.length,outfitAnchorRoutesVerified:received.length,browserOverlayImport:true,liveReviewRefresh:true,archiveAndRemovalFiltering:true,removedHistoryReachable:true,noDuplicateReviewActions:true,fullOutfitCountsRespectRemoval:true,scopedGunNotesPreserved:true,allReviewedStatusDerived:true,fabricatedApprovals:0,localStorageWrites:page.writes.length+overlayPage.writes.length,catalogMutations:0,canonicalTaskMutations:0,browserVisualQA:false,sourcePins:{libraryJS:sha(source),catalogJS:sha(raw)},reviewedAssets:[yellowID,burgundyID].map(id=>({id,status:initialRecords.get(id).status,note:initialRecords.get(id).note}))}));
