/* Actionable winners use the normal exact-image reviewer; source metadata never
   grants a site decision. This reuses the real DOM/storage double without a browser. */
const assert=require('node:assert/strict'), fs=require('node:fs'), path=require('node:path'), vm=require('node:vm');
const clone=value=>JSON.parse(JSON.stringify(value));
const REVIEW_KEY='cfa-visual-review-v1', FAVORITES_KEY='cfa-visual-favorites-v1', EXPORT_KEY='cfa-visual-export-v1';
const source=fs.readFileSync(path.join(__dirname,'library.js'),'utf8');
const raw=fs.readFileSync(path.join(__dirname,'catalog.js'),'utf8');
const catalog=JSON.parse(raw.slice(raw.indexOf('=')+1).trim().replace(/;$/,''));
const byID=new Map(catalog.assets.map(a=>[a.id,a]));
const harness=fs.readFileSync(path.join(__dirname,'test_review_intake.cjs'),'utf8');
let bootSource=harness.slice(harness.indexOf('function boot()'),harness.indexOf('const page=boot()'));
const originalHook='window.__collectionsTest={renderMain,intakeFamily,intakeAssetEvidence,supplementPanel,supplementCard,expandedCollections,collapsedBrowseBuckets,reviews,reviewRecord,reviewPayload,basketPayload,setState(p){Object.assign(state,p);},getState(){return state;}};';
const testHook='window.__collectionsTest={renderMain,supplementLinks,supplementPanel,supplementCard,reviews,reviewRecord,reviewPayload,basketPayload,viewerHTML(){return dialog.innerHTML;},viewerOpen(){return dialog.open;},viewerAssetID(){return currentID;},setState(p){Object.assign(state,p);},getState(){return state;}};';
assert(bootSource.includes(originalHook),'Reuse the established intake DOM/storage harness');
bootSource=bootSource.replace(originalHook,testHook);
const boot=new Function('source','catalog','byID','clone','assert','vm','REVIEW_KEY','FAVORITES_KEY','EXPORT_KEY',bootSource+';return boot;')(
 source,catalog,byID,clone,assert,vm,REVIEW_KEY,FAVORITES_KEY,EXPORT_KEY);
function stable(payload){const copy=clone(payload);delete copy.exported;return copy;}
const page=boot(),api=page.api;
const initialReviews=stable(api.reviewPayload()),initialBasket=stable(api.basketPayload(true)),initialStorage=Object.fromEntries(page.storage);
const frozenIntake=JSON.stringify(page.C.reviewIntake);
let checks=0;

// Technical receipts remain available but never masquerade as the next review step.
const specimen={id:'winners-fixture',title:'Winners supplement',indexURL:'../fixture/WINNERS_index.html',
 csvURL:'../fixture/WINNERS.csv',receiptURL:'../fixture/RECEIPT.txt',mediaDelivery:{fullImages:50},items:[]};
const links=api.supplementLinks(specimen);
const drawer=links.match(/<details\b([^>]*)class="supplement-source-details"([^>]*)>([\s\S]*?)<\/details>/);
assert(drawer,'Technical source links have a dedicated drawer');
assert(!/\bopen\b/.test(drawer[1]+drawer[2]),'Source details start closed');
assert(drawer[3].includes('Source details')&&drawer[3].includes('50 full images received'),'Drawer has a readable delivery summary');
assert(drawer[3].includes('not a review checklist'),'Source documents are identified as delivery records');
assert(/<a\b[^>]*download=[^>]*>Download source manifest/.test(drawer[3]),'Raw CSV is an explicit download');
assert(drawer[3].includes('RECEIPT.txt'),'Original receipt remains inside optional details');
const withoutDrawer=links.replace(drawer[0],'');
assert(withoutDrawer.includes('Supplied winners index'),'Human-readable index remains outside the drawer');
assert(!withoutDrawer.includes('WINNERS.csv')&&!withoutDrawer.includes('RECEIPT.txt'),'No technical link competes with the index');
checks++;

// A verified exact-byte match opens the same viewer and controls as other images.
const exactAsset=catalog.assets.find(a=>a.project==='hon'&&a.kind==='image'&&a.sha256&&!api.reviewRecord(a.id).status);
assert(exactAsset,'Fixture uses an unreviewed real image');
const exact={id:'exact-action-fixture',project:'hon',title:'Exact image review fixture',version:'v002',group:'validated',
 label:'V-validated (scoped), awaiting Ziggy',sha256:exactAsset.sha256,thumbURL:exactAsset.thumb,fullImageURL:exactAsset.src,
 availability:'local_original_verified',exactAssetID:exactAsset.id,familyIDs:[],vVerdict:'PASS-ADVISORY',
 reviewScope:'Chest only',advisories:'An advisory remains attached',sourceEvidence:'Fixture evidence'};
const card=api.supplementCard(exact);
assert(card.includes('<button class="supplement-preview" data-open="'+exactAsset.id+'"'),'Image opens the exact existing reviewer');
assert(card.includes('data-open="'+exactAsset.id+'">Review image</button>'),'Card has a clear review action');
assert(card.includes('Your decision:</strong> Not reviewed'),'Provider pass does not fabricate a user Keep');
assert(card.includes('PASS-ADVISORY')&&card.includes('Chest only')&&card.includes('An advisory remains attached'),'Scope and caveat survive promotion to an actionable card');
page.C.reviewSupplements=[{...specimen,items:[exact]}];
api.setState({project:'hon',view:'intake',album:'',search:'',intakeDataset:'all'});api.renderMain();
const previewButton=page.elements('[data-open]').find(e=>e.dataset.open===exactAsset.id&&e.attributes.class==='supplement-preview');
assert(previewButton,'Rendered supplement image is wired');previewButton.click();
assert(api.viewerOpen(),'Click opens the normal viewer');
assert.equal(api.viewerAssetID(),exactAsset.id,'Viewer is bound to the full-image asset ID');
assert(api.viewerHTML().includes('Review this reference')&&api.viewerHTML().includes('data-review-status="needs_fixes"'),'Normal review controls are present');
assert(api.viewerHTML().includes(exactAsset.sha256),'Viewer shows the exact version hash');
assert.equal(api.reviewRecord(exactAsset.id).status,null,'Opening does not make a decision');
checks++;

// Preview-only, missing catalog assets and conflicting hashes cannot acquire review actions.
for(const [label,item] of [
 ['preview only',{...exact,availability:'preview_only',fullImageURL:null}],
 ['missing asset',{...exact,exactAssetID:'missing-source-id'}],
 ['wrong hash',{...exact,sha256:'0'.repeat(64)}],
 ['unsafe full-image URL',{...exact,fullImageURL:'javascript:unsafe()'}]
]){
 const html=api.supplementCard(item);
 assert(!html.includes('data-open='),label+' has no review button');
 assert(!html.includes('>Review image</button>'),label+' has no review CTA');
 assert(!html.includes('javascript:'),label+' cannot emit an unsafe URL');
}
const preview=api.supplementCard({...exact,availability:'preview_only',fullImageURL:null,exactAssetID:null});
assert(preview.includes('Preview only'),'Unavailable full images explain why they cannot be reviewed');
checks++;

// Neither opening the card nor opening its viewer writes reviews, favorites or baskets.
assert.deepEqual(stable(api.reviewPayload()),initialReviews,'All recorded user choices survive browsing');
assert.deepEqual(stable(api.basketPayload(true)),initialBasket,'Export selection survives browsing');
assert.deepEqual(Object.fromEntries(page.storage),initialStorage,'Saved browser records stay byte-for-byte unchanged');
assert.equal(page.writes.length,0,'No browser storage writes occur while inspecting the handoff');
assert.equal(JSON.stringify(page.C.reviewIntake),frozenIntake,'Frozen r002 remains unchanged');
checks++;

if(!process.argv.includes('--fixtures-only')){
 const live=boot(),real=live.C.reviewSupplements.find(s=>s.mediaDelivery);
 assert(real,'Refreshed catalog contains the delivered media supplement');
 const realItems=real.items||[];
 const reviewable=realItems.filter(item=>item.availability==='local_original_verified'&&byID.get(item.exactAssetID)?.sha256===item.sha256);
 assert.equal(realItems.filter(item=>item.availability==='local_original_verified').length,50,'50 original images are verified locally');
 assert.equal(reviewable.length,45,'45 verified originals have exact catalog IDs and normal review controls');
 for(const item of reviewable){
  const html=live.api.supplementCard(item);
  assert(html.includes('data-open="'+item.exactAssetID+'"'),'Real supplied version opens its exact asset: '+item.title);
 }
 for(const item of realItems.filter(item=>item.availability==='preview_only')){
  assert(!live.api.supplementCard(item).includes('class="pill supplement-review"'),'Remaining previews cannot become reviewable accidentally');
 }
 checks++;

 // Ziggy's later choices are exact-image decisions, independent of provider grades.
 const directed=realItems.filter(item=>['validated','preliminary'].includes(item.group));
 assert.equal(directed.filter(item=>item.group==='validated').length,28,'All 28 chest corrections are represented');
 assert.equal(directed.filter(item=>item.group==='preliminary').length,13,'All 13 mouth picks remain represented');
 const directedDecisions=directed.map(item=>{
  const record=catalog.reviewDecisions.find(r=>r.id===item.exactAssetID&&r.sha256===item.sha256);
  assert(record,'A direct choice binds the supplied version: '+item.title);
  assert.equal(record.origin,'user');
  assert.equal(record.acceptedScope?.sha256,item.sha256,'Scoped acceptance binds exact bytes');
  assert.equal(record.acceptedScope.kind,item.group==='validated'?'chest_correction':'mouth_candidate','Scope follows the actual user decision');
  assert.equal(record.acceptedScope.source,'Ziggy direct voice review','Scope keeps human attribution');
  assert.equal(record.acceptedScope.accepted,record.status==='keep','Acceptance agrees with the explicit choice');
  assert.deepEqual(item.humanAcceptance,record.acceptedScope,'Supplement displays the same exact scoped decision');
  assert(record.likenessRating==null&&record.sceneQualityRating==null,'No numerical rating is invented from acceptance');
  assert.notEqual(record.storyboardStage,'production','Scoped acceptance does not promote an image to Production');
  if(item.group==='preliminary')assert.equal(item.vVerdict||'','','Mouth picks do not become V-Team validated through user acceptance');
  return record;
 });
 assert.equal(directedDecisions.filter(record=>record.status==='keep').length,39,'28 chest corrections and 11 mouth picks are kept');
 assert.equal(directedDecisions.filter(record=>record.status==='remove').length,2,'Only the two named mouth picks are removed');
 checks++;

 live.api.setState({project:'hon',view:'intake',album:'',search:'',intakeDataset:'all'});live.api.renderMain();
 const liveBefore=stable(live.api.reviewPayload());
 for(const item of [directed.find(item=>item.group==='validated'),directed.find(item=>item.sha256.startsWith('f133a3be'))]){
  const button=live.elements('[data-open]').find(e=>e.dataset.open===item.exactAssetID&&e.attributes.class==='supplement-preview');
  assert(button,'Real supplied image has a wired review preview');button.click();
  assert.equal(live.api.viewerAssetID(),item.exactAssetID,'Real preview opens its exact version');
  const expected=live.api.reviewRecord(item.exactAssetID).status;
  assert(live.api.viewerHTML().includes('data-review-status="'+expected+'" class="selected" aria-pressed="true"'),'Normal viewer shows the saved '+expected+' choice');
  assert(live.api.viewerHTML().includes(item.sha256),'Real viewer retains full hash evidence');
 }
 assert.deepEqual(stable(live.api.reviewPayload()),liveBefore,'Inspecting saved approval/removal does not revise it');
 checks++;

 const rejectedHashes=[
  'f133a3bef56b13d61c11d0a7db598e460ea193417a2566a50d9783be20c613f5',
  '3c477fb469b899f7c229ae68fe894e199370cc587573d6d18cedc54c674af5ca'
 ];
 for(const sha of rejectedHashes){
  const item=realItems.find(i=>i.sha256===sha);assert(item,'Explicitly rejected mouth version remains traceable');
  const asset=byID.get(item.exactAssetID);assert.equal(asset?.sha256,sha,'Rejection binds the full image hash');
  const record=catalog.reviewDecisions.find(r=>r.id===asset.id&&r.sha256===sha);
  assert.equal(record?.status,'remove','User rejection is a removal choice');
  assert.equal(record.origin,'user','Removal keeps human attribution');
  assert(record.directUserClarification?.text,'Exact user decision has an evidence receipt');
  assert.equal(live.api.reviewRecord(asset.id).status,'remove','Normal review controls receive the explicit rejection');
  assert.equal(item.group,'preliminary','Rejection does not rewrite source grouping');
  assert(!/FAIL/i.test(item.vVerdict||''),'Human rejection is never manufactured into a V-Team FAIL');
  const html=live.api.supplementCard(item);
  assert(html.includes('Your decision:</strong> Marked for removal'),'Supplied pick visibly reflects the user decision');
  assert(html.includes('Review saved decision'),'Rejected source remains inspectable');
 }
 assert.equal(live.writes.length,0,'Loading explicit decisions does not persist new browser state');
 checks++;
}
console.log(JSON.stringify({passed:true,checks,fixturesOnly:process.argv.includes('--fixtures-only'),browserWrites:page.writes.length,scope:'Winners source disclosure, exact-image reviewer and explicit decisions'}));
