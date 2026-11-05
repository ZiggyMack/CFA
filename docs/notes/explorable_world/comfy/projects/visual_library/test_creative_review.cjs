/* Real-library creative-review queue checks with the existing collection DOM double.
   Synthetic in-memory reviews only; no provider dispatch or project ratings are written. */
const assert=require('node:assert/strict'), fs=require('node:fs'), path=require('node:path'), vm=require('node:vm');
const clone=value => JSON.parse(JSON.stringify(value));
const REVIEW_KEY='cfa-visual-review-v1', FAVORITES_KEY='cfa-visual-favorites-v1', EXPORT_KEY='cfa-visual-export-v1';
const raw=fs.readFileSync(path.join(__dirname,'catalog.js'),'utf8');
const catalog=JSON.parse(raw.slice(raw.indexOf('=')+1).trim().replace(/;$/,''));
const byID=new Map(catalog.assets.map(a => [a.id,a]));
const assetID='HD-FALCON-194702e9e041362d', frame=byID.get(assetID);
assert(frame && /C01-002/.test(frame.title),'Use actual C01-002 fixture');
const recipients=['claude','grok_chief','gemini_chat','flow'];
const seed={id:assetID,sha256:frame.sha256,status:'keep',note:'Synthetic creative-review note.',
  variant:'prime',workingReferenceScope:'scene',storyboardStage:'detailed_design',likenessRating:3,sceneQualityRating:4};
const input={...catalog,reviewDecisions:[seed],sceneReviews:[]};
const original=fs.readFileSync(path.join(__dirname,'test_collections_navigation.cjs'),'utf8');
let bootSource=original.slice(original.indexOf('function boot()'),original.indexOf('const page = boot()'));
const hookStart=bootSource.indexOf('window.__collectionsTest={');
const hookEnd=bootSource.indexOf(';})();',hookStart);
assert(hookStart>=0&&hookEnd>hookStart,'Bounded collection test hook');
const oldHook=bootSource.slice(hookStart,hookEnd+1);
const hook='window.__collectionsTest={C,reviews,openViewer,reviewRecord,reviewPayload,importReview,exportReference,normalizedCreativeReview,creativeReviewHandoffPayload,exportCreativeReviewRequests,updateReview,workingBOMEntries,sceneReviewRecord,sceneHandoffGate,viewerHTML(){return dialog.innerHTML;},getCurrentID(){return currentID;},clickRecipient(id){const b=document.querySelector("#creative-review-"+id);if(!b)throw Error("Recipient button exists: "+id);b.click();},node(selector){const n=document.querySelector(selector);if(!n)throw Error("Node exists: "+selector);return n;},setState(p){Object.assign(state,p);}};';
assert(bootSource.includes(oldHook),'Reuse collection DOM and real bound button handlers');
bootSource=bootSource.replace(oldHook,hook)
  .replace('function boot() {','function boot(savedInput = {}, catalogInput = catalog) {')
  .replace('const storage = new Map(Object.entries(saved));','const storage = new Map(Object.entries(savedInput));')
  .replace('REVIEW_CATALOG:clone(catalog)','REVIEW_CATALOG:clone(catalogInput)')
  .replace('const elements = new Set(), nodes = new Map(), writes = [], scrolls = [];',
    'const elements = new Set(), nodes = new Map(), writes = [], scrolls = [], downloads = [], blobs = new Map(); class TestURL extends URL {static createObjectURL(blob){const url="blob:test-"+blobs.size;blobs.set(url,blob);return url;}static revokeObjectURL(){}}')
  .replace('click() {if (this.disabled) return;', 'click() {if (this.disabled) return; if(this.tag === "a")downloads.push({name:this.download,blob:blobs.get(this.href)});')
  .replace('location,URL,Intl,console,','location,URL:TestURL,Blob,Intl,console,')
  .replace('location,writes,storage,scrolls,','location,writes,storage,scrolls,downloads,');
const bootFunction=new Function('source','catalog','byID','clone','assert','vm','REVIEW_KEY','FAVORITES_KEY','EXPORT_KEY','Blob',
  bootSource+';return boot;');
const boot=(saved={}, supplied=input) => bootFunction(fs.readFileSync(path.join(__dirname,'library.js'),'utf8'),
  catalog,byID,clone,assert,vm,REVIEW_KEY,FAVORITES_KEY,EXPORT_KEY,Blob)(saved,supplied);
const request=ids => ({status:'queued',recipients:ids,purpose:'find_story_use',scope:'music_video_and_interstitials',note:''});
const clean=()=>({...catalog,reviewDecisions:[],sceneReviews:[]});

async function main() {
  let checks=0;
  const page=boot(), api=page.api;
  const sources=clone({assets:api.C.assets,BOM:api.C.characterBOM,shots:api.C.shotMaterials});
  const bomBefore=clone(api.workingBOMEntries('hon'));
  const scenesBefore=clone(api.reviewPayload().sceneReviews);
  const before=clone(api.reviewRecord(assetID));
  api.openViewer(assetID);
  assert(api.viewerHTML().includes('Creative review'),'Creative-review purpose is clearly named');
  assert(!api.viewerHTML().includes('data-quick-collaborator='),'Old top execution-destination shortcuts are absent');
  for(const id of recipients)assert(api.viewerHTML().includes('data-creative-review-recipient="'+id+'"'),'Canonical named recipient: '+id);
  assert.equal(api.node('#viewer-export-creative-review').disabled,true,'No request cannot be exported as a dispatch');
  api.clickRecipient('claude');
  let record=clone(api.reviewRecord(assetID));
  assert.deepEqual(record.creativeReview,request(['claude']),'Claude click selects only Claude, without broadcast');
  assert.equal(api.getCurrentID(),assetID,'Queue action stays in the selected image viewer');
  for(const field of ['shotPlan','status','variant','workingReferenceScope','workingReference','storyboardStage','likenessRating','sceneQualityRating','note'])
    assert.deepEqual(record[field],before[field],'Creative request does not mutate '+field);
  assert.deepEqual(clone(api.workingBOMEntries('hon')),bomBefore,'Queue does not approve any component');
  assert.deepEqual(clone(api.reviewPayload().sceneReviews),scenesBefore,'Queue leaves readiness and shoot-plan evidence unchanged');
  assert.equal(api.node('#viewer-export-creative-review').disabled,false,'Explicit selection enables portable request');
  checks++;

  api.clickRecipient('claude');
  assert.equal(api.reviewRecord(assetID).creativeReview,null,'Last recipient toggle clears request');
  for(const id of recipients) {
    api.clickRecipient(id);
    assert.deepEqual(clone(api.reviewRecord(assetID).creativeReview.recipients),[id],'Only the clicked recipient is queued: '+id);
    api.clickRecipient(id);
    assert.equal(api.reviewRecord(assetID).creativeReview,null);
  }
  api.clickRecipient('claude'); api.clickRecipient('grok_chief');
  assert.deepEqual(clone(api.reviewRecord(assetID).creativeReview.recipients),['claude','grok_chief'],'A second recipient requires a second explicit click');
  assert(!api.reviewRecord(assetID).creativeReview.recipients.includes('flow'));
  api.clickRecipient('grok_chief');
  checks++;

  const saved=Object.fromEntries(page.storage), reloaded=boot(saved);
  assert.deepEqual(clone(reloaded.api.reviewRecord(assetID).creativeReview),request(['claude']),'Queue survives browser backup/reload');
  const portable=clone(api.reviewPayload());
  const imported=boot({},clean()); imported.api.importReview(portable);
  assert.deepEqual(clone(imported.api.reviewRecord(assetID).creativeReview),request(['claude']),'Queue survives normalized portable import');
  assert.equal(imported.api.reviewRecord(assetID).shotPlan,null,'Import does not create a production plan');
  const normalized=clone(api.normalizedCreativeReview({status:'sent',recipients:['claude','bogus','claude'],purpose:'generate_video',scope:'unlimited',note:'Specific creative question.'}));
  assert.deepEqual(normalized,{...request(['claude']),note:'Specific creative question.'},'Normalizer filters/deduplicates canonical recipients and prevents imported sent/generation claims');
  for(const invalid of [null,{},[],{recipients:'claude'},{recipients:['Claude','unknown']}])
    assert.equal(api.normalizedCreativeReview(invalid),null,'No valid recipients means no request');
  imported.api.importReview({format:REVIEW_KEY,items:[seed],favorites:[]});
  assert.deepEqual(clone(imported.api.reviewRecord(assetID).creativeReview),request(['claude']),'Older partial import does not erase separately saved request');
  imported.api.importReview({format:REVIEW_KEY,items:[{...seed,creativeReview:null}],favorites:[]});
  assert.equal(imported.api.reviewRecord(assetID).creativeReview,null,'Explicit null clears queue');
  const wrongHash=boot({},clean());
  wrongHash.api.importReview({format:REVIEW_KEY,items:[{...seed,sha256:'0'.repeat(64),creativeReview:request(['claude'])}],favorites:[]});
  assert.equal(wrongHash.api.reviewRecord(assetID).creativeReview,undefined,'Mismatched source cannot acquire a creative request');
  checks++;

  const exported=clone(api.exportReference(api.C.assets.find(a=>a.id===assetID)));
  assert.deepEqual(exported.creativeReview,request(['claude']));
  assert.equal(exported.sha256,frame.sha256);
  assert.equal(exported.likenessRating,3); assert.equal(exported.sceneQualityRating,4);
  const handoff=clone(api.creativeReviewHandoffPayload(assetID));
  assert.equal(handoff.format,'cfa-creative-review-handoff-v1');
  assert.equal(handoff.status,'queued; not sent or generated');
  assert.equal(handoff.items.length,1);
  const item=handoff.items[0];
  assert.equal(item.id,assetID); assert.equal(item.sha256,frame.sha256); assert.equal(item.path,frame.repoPath);
  assert.deepEqual(item.creativeReview,request(['claude']));
  assert.equal(item.likenessRating,3); assert.equal(item.sceneQualityRating,4);
  assert.equal(item.note,seed.note,'Human creative/review note is retained');
  assert.equal(item.providerNote,frame.note,'Reported provider QA and its caveat remain available');
  assert(/music video|between videos|interstitial/i.test(item.instruction),'Creative request covers music video and interstitial stories');
  assert.deepEqual(JSON.parse(JSON.stringify(handoff)),handoff,'Payload is portable JSON');
  api.node('#viewer-export-creative-review').click();
  const downloaded=JSON.parse(await page.downloads.at(-1).blob.text());
  assert.equal(downloaded.format,handoff.format);
  assert.deepEqual(downloaded.items,handoff.items,'Actual viewer export writes the selected request only');
  assert.equal(api.creativeReviewHandoffPayload('UNKNOWN-ASSET').items.length,0,'Unknown current ID cannot widen export to all queued images');
  checks++;

  const legacyPlan={status:'planned',destinations:['Flow','Grok'],idea:'Existing execution draft.',prompt:'Existing exact prompt.'};
  const legacy=boot({}, {...catalog,reviewDecisions:[{...seed,shotPlan:legacyPlan}],sceneReviews:[]});
  legacy.api.openViewer(assetID);
  legacy.api.clickRecipient('claude');
  assert.deepEqual(clone(legacy.api.reviewRecord(assetID).shotPlan),legacyPlan,'Creative-review selection preserves previous generation destinations');
  assert.deepEqual(clone(legacy.api.reviewRecord(assetID).creativeReview),request(['claude']));
  const legacyPortable=clone(legacy.api.reviewPayload()), legacyImported=boot({},clean());
  legacyImported.api.importReview(legacyPortable);
  assert.deepEqual(clone(legacyImported.api.reviewRecord(assetID).shotPlan),legacyPlan);
  assert.deepEqual(clone(legacyImported.api.reviewRecord(assetID).creativeReview),request(['claude']));
  assert.deepEqual(clone({assets:api.C.assets,BOM:api.C.characterBOM,shots:api.C.shotMaterials}),sources,'Queue and exports preserve sources, canonical components and acceptance records');
  assert.deepEqual(clone(api.workingBOMEntries('hon')),bomBefore);
  assert.deepEqual(clone(api.reviewPayload().sceneReviews),scenesBefore);
  checks++;
  console.log(JSON.stringify({passed:true,scenarios:checks,fixture:assetID,namedRecipients:true,productionPlanIndependent:true,providerMessagesSent:0,projectGradesAssigned:false,browserVisualQA:false}));
}
main().catch(error=>{console.error(error);process.exitCode=1;});
