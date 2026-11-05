/* Direct clarification precedence using the real library and collection DOM double.
   Synthetic browser snapshots only. No host review or user grade is written. */
const assert=require('node:assert/strict'), fs=require('node:fs'), path=require('node:path'), vm=require('node:vm');
const clone=value=>JSON.parse(JSON.stringify(value));
const REVIEW_KEY='cfa-visual-review-v1', FAVORITES_KEY='cfa-visual-favorites-v1', EXPORT_KEY='cfa-visual-export-v1';
const raw=fs.readFileSync(path.join(__dirname,'catalog.js'),'utf8');
const catalog=JSON.parse(raw.slice(raw.indexOf('=')+1).trim().replace(/;$/,''));
const byID=new Map(catalog.assets.map(a=>[a.id,a]));
const assetID='HD-FALCON-381883a6beb1ed5e', frame=byID.get(assetID);
const canonical=catalog.reviewDecisions.find(r=>r.id===assetID);
assert(frame && /C04-005/.test(frame.title),'Actual C04-005 asset exists');
assert(canonical && canonical.status==='keep' && canonical.sha256===frame.sha256,'Canonical direct Keep binds the exact asset');
const confirmedAt=Date.parse(canonical.directUserClarification?.recordedAtUTC);
assert(Number.isFinite(confirmedAt),'Canonical clarification has a valid time');
const oldTime=new Date(confirmedAt-1000).toISOString(), newTime=new Date(confirmedAt+1000).toISOString();
const stale={id:assetID,sha256:frame.sha256,status:null,note:'Synthetic old-browser note retained.',
  origin:'user',updatedAt:oldTime,workingReferenceScope:'scene',storyboardStage:'detailed_design',
  likenessRating:4,sceneQualityRating:5,shotPlan:null};
const existing=fs.readFileSync(path.join(__dirname,'test_collections_navigation.cjs'),'utf8');
let bootSource=existing.slice(existing.indexOf('function boot()'),existing.indexOf('const page = boot()'));
const oldHook='window.__collectionsTest={normalVisible,collectionCards,collectionGroups,sharedCharacterReferences,castExplorer,castHubGroups,castWorkingGroups,parseHash,detailAlbumGroups,renderMain,expandedCollections,reviews,reviewRecord,reviewPayload,basketPayload,setState(p){Object.assign(state,p);},getState(){return state;}};';
const hook='window.__collectionsTest={C,reviewRecord,reviewPayload,normalizedReview,importReview,workingBOMEntries};';
assert(bootSource.includes(oldHook),'Reuse real collection DOM/storage double');
bootSource=bootSource.replace(oldHook,hook)
  .replace('function boot() {','function boot(savedInput = {}, catalogInput = catalog) {')
  .replace('const storage = new Map(Object.entries(saved));','const storage = new Map(Object.entries(savedInput));')
  .replace('REVIEW_CATALOG:clone(catalog)','REVIEW_CATALOG:clone(catalogInput)');
const bootFunction=new Function('source','catalog','byID','clone','assert','vm','REVIEW_KEY','FAVORITES_KEY','EXPORT_KEY',
  bootSource+';return boot;');
const boot=(record=stale,supplied=catalog)=>bootFunction(fs.readFileSync(path.join(__dirname,'library.js'),'utf8'),
  catalog,byID,clone,assert,vm,REVIEW_KEY,FAVORITES_KEY,EXPORT_KEY)(
    {[REVIEW_KEY]:JSON.stringify({format:REVIEW_KEY,items:[record],favorites:[]})},supplied);
const otherFields=['note','likenessRating','sceneQualityRating','storyboardStage','workingReferenceScope','shotPlan','updatedAt'];
const sameBrowserFields=(actual,expected)=>otherFields.forEach(field=>assert.deepEqual(actual[field],expected[field],'Clarification preserves browser '+field));

let checks=0;
const page=boot(), loaded=clone(page.api.reviewRecord(assetID));
assert.equal(loaded.status,'keep','Stale browser null cannot erase direct human Keep');
sameBrowserFields(loaded,stale);
assert.equal(page.writes.length,0,'Boot normalizes in memory without writing browser storage');
const saved=JSON.parse(page.storage.get(REVIEW_KEY)).items[0];
assert.equal(saved.status,null,'Original browser snapshot remains unchanged at boot');
assert.deepEqual(clone(page.api.C),catalog,'Precedence leaves catalog metadata and canonical clarification untouched');
checks++;

const equal=boot({...stale,updatedAt:new Date(confirmedAt).toISOString()});
assert.equal(equal.api.reviewRecord(assetID).status,'keep','Clarification wins when timestamps are equal');
assert.equal(equal.writes.length,0);
for(const status of ['needs_fixes','remove',null]) {
  const next={...stale,status,updatedAt:newTime,note:'Synthetic newer decision: '+status};
  const newer=boot(next);
  assert.equal(newer.api.reviewRecord(assetID).status,status,'Newer browser intent wins: '+status);
  sameBrowserFields(clone(newer.api.reviewRecord(assetID)),next);
  assert.equal(newer.writes.length,0,'Loading newer intent still does not write');
}
checks++;

const wrongBrowser=boot({...stale,sha256:'0'.repeat(64),status:'remove'});
assert.equal(wrongBrowser.api.reviewRecord(assetID).status,'keep','Mismatched browser hash cannot override canonical Keep');
assert.equal(wrongBrowser.api.reviewRecord(assetID).note,canonical.note,'Mismatched record cannot attach its unrelated note');
assert.equal(wrongBrowser.writes.length,0);
const badCanonical={...catalog,reviewDecisions:catalog.reviewDecisions.map(r=>r.id===assetID?{...r,sha256:'0'.repeat(64)}:r)};
const unbound=boot(stale,badCanonical);
assert.equal(unbound.api.reviewRecord(assetID).status,null,'Wrong canonical hash cannot create a clarification override');
sameBrowserFields(clone(unbound.api.reviewRecord(assetID)),stale);
const noClarification={...catalog,reviewDecisions:catalog.reviewDecisions.map(r=>{
  if(r.id!==assetID)return r;const result={...r};delete result.directUserClarification;return result;
})};
assert.equal(boot(stale,noClarification).api.reviewRecord(assetID).status,null,'Ordinary catalog Keep does not get this special precedence');
checks++;

const imported=clone(page.api.normalizedReview(stale,'import'));
assert.equal(imported.status,null,'The narrow browser rule does not rewrite an explicitly imported review');
sameBrowserFields(imported,stale);
const invalidTime={...catalog,reviewDecisions:catalog.reviewDecisions.map(r=>r.id===assetID?
  {...r,directUserClarification:{...r.directUserClarification,recordedAtUTC:'not-a-date'}}:r)};
assert.equal(boot(stale,invalidTime).api.reviewRecord(assetID).status,null,'Invalid clarification time cannot claim precedence');
assert.deepEqual(clone(page.api.reviewPayload().items.find(r=>r.id===assetID)).shotPlan,null,'Resolving Keep creates no production plan');
assert.deepEqual(clone(page.api.C.characterBOM),catalog.characterBOM,'Clarification does not rewrite approved character parts');
assert.deepEqual(clone(page.api.reviewPayload().sceneReviews),clone(catalog.sceneReviews||[]),'Clarification leaves whole-scene readiness and shoot review unchanged');
checks++;

// Synthetic confirmations work before publication and bind both exact portrait sources.
// The human decision precedes its later import; that delay cannot erase newer browser intent.
const portraitSources=[
 ['LAG-602a9fd4021dc356','602a9fd4021dc356086728a781aee985741811b3b401a52d9e85869652bb944f'],
 ['LAG-63126392af1ccf8b','63126392af1ccf8b6cd667998e169aeb2cd8fdf7ebaa79976b39730255677026']
];
const decisionAtUTC='2026-10-14T01:48:00Z',recordedAtUTC='2026-10-14T02:47:00Z';
const nonRatingFields=['status','note','sceneQualityRating','storyboardStage','workingReferenceScope','workingReference','shotPlan','updatedAt','origin'];
let portraitRatingCases=0;
function expectPortraitRating(record,supplied,expected,label){
 const p=boot(record,supplied),actual=clone(p.api.reviewRecord(record.id));
 assert.equal(actual.likenessRating,expected,label);
 for(const field of nonRatingFields)assert.deepEqual(actual[field],record[field],label+' preserves '+field);
 assert.equal(p.writes.length,0,label+' writes no browser storage');
 assert.deepEqual(JSON.parse(p.storage.get(REVIEW_KEY)).items,[record],label+' preserves the saved browser record');
 assert.deepEqual(clone(p.api.C),supplied,label+' preserves catalog sources, reviews and scopes');
 assert.equal(p.api.normalizedReview(record,'import').likenessRating,record.likenessRating,'Explicit import remains a user action');
 portraitRatingCases++;
}
for(const [portraitID,sha256] of portraitSources){
 assert.equal(byID.get(portraitID)?.sha256,sha256,'Exact portrait source is present: '+portraitID);
 const ratingRecord={id:portraitID,sha256,likenessRating:5,humanRatingConfirmation:{field:'likenessRating',value:5,decisionAtUTC,recordedAtUTC}};
 const ratedCatalog=clone(catalog);ratedCatalog.reviewDecisions=ratedCatalog.reviewDecisions.filter(r=>r.id!==portraitID).concat(ratingRecord);
 for(const value of [null,2]){
  const old={id:portraitID,sha256,likenessRating:value,sceneQualityRating:3,status:'needs_fixes',note:'Retain this note',
   origin:'user',workingReferenceScope:'detail',workingReference:{status:'approved',scope:'detail'},storyboardStage:'detailed_design',shotPlan:null,updatedAt:'2026-10-14T01:47:00Z'};
  for(const [updatedAt,expected,label] of [
   [old.updatedAt,5,'Before human decision'],
   [decisionAtUTC,5,'Equal human decision time'],
   ['2026-10-14T01:49:00Z',value,'Between human decision and later import'],
   ['2026-10-14T02:48:00Z',value,'After later import']
  ])expectPortraitRating({...old,updatedAt},ratedCatalog,expected,label);
  const legacy=clone(ratedCatalog);delete legacy.reviewDecisions.at(-1).humanRatingConfirmation.decisionAtUTC;
  expectPortraitRating({...old,updatedAt:'2026-10-14T01:49:00Z'},legacy,5,'Legacy confirmation falls back to recording time');
  const invalidLegacy=clone(legacy);invalidLegacy.reviewDecisions.at(-1).humanRatingConfirmation.recordedAtUTC='invalid';
  expectPortraitRating(old,invalidLegacy,value,'Invalid legacy recording time has no precedence');
  for(const [change,expected,label] of [
   [{decisionAtUTC:'invalid'},value,'Malformed decision time cannot fall through to later recording time'],
   [{recordedAtUTC:'invalid'},5,'Valid decision time governs independently of recording time'],
   [{field:'sceneQualityRating'},value,'Confirmation for another field has no likeness precedence'],
   [{value:4},value,'Mismatched confirmation value has no precedence']
  ]){
   const changed=clone(ratedCatalog);Object.assign(changed.reviewDecisions.at(-1).humanRatingConfirmation,change);
   expectPortraitRating(old,changed,expected,label);
  }
  const wrongHash=clone(ratedCatalog);wrongHash.reviewDecisions.at(-1).sha256='0'.repeat(64);
  expectPortraitRating(old,wrongHash,value,'Confirmation for another source hash has no precedence');
  const ordinary=clone(ratedCatalog);delete ordinary.reviewDecisions.at(-1).humanRatingConfirmation;
  expectPortraitRating(old,ordinary,value,'Ordinary catalog rating has no special precedence');
 }
 checks++;
}

console.log(JSON.stringify({passed:true,scenarios:checks,portraitRatingCases,portraitFixtures:portraitSources.map(([id])=>id),fixture:assetID,staleStatusResolved:true,newerIntentPreserved:true,
  bootReviewWrites:page.writes.length,projectGradesAssigned:false,browserVisualQA:false}));