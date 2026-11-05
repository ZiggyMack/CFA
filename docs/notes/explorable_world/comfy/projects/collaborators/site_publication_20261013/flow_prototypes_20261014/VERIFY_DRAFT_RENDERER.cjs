/* Draft catalog additions only; actual library.js in the established DOM/storage
   double. No site build, browser access, local review writes or media mutation. */
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const L=path.resolve(__dirname,'../../../visual_library');
const clone=value=>JSON.parse(JSON.stringify(value));
const REVIEW_KEY='cfa-visual-review-v1',FAVORITES_KEY='cfa-visual-favorites-v1';
const raw=fs.readFileSync(path.join(L,'catalog.js'),'utf8');
const catalog=JSON.parse(raw.slice(raw.indexOf('=')+1).trim().replace(/;$/,''));
const additions=JSON.parse(fs.readFileSync(path.join(__dirname,'DRAFT_ADDITIONS_FIXTURE.json'),'utf8'));
const supplied=clone(catalog);
supplied.assets.push(...additions.assets);
supplied.albums.push(...additions.albums);
supplied.shotMaterials.shots.push(...additions.shots);
const scopeTest=fs.readFileSync(path.join(L,'test_reference_scope.cjs'),'utf8');
const bootSource=scopeTest.slice(scopeTest.indexOf('function boot('),scopeTest.indexOf('async function main()'));
const oldHook='window.__scopeTest={openViewer,reviewRecord,reviewPayload,importReview,exportReference,inReviewQueue,whenFileWritesSettle(){return fileWriteChain;}};';
const newHook='window.__scopeTest={openViewer,C,dialog,reviewRecord,sceneReviewRecord,sceneHandoffGate,storyConnections,storyboardStage,renderMain,setState(p){Object.assign(state,p);},whenFileWritesSettle(){return fileWriteChain;}};';
assert(bootSource.includes(oldHook));
const createBoot=new Function('source','catalog','clone','assert','vm','REVIEW_KEY','FAVORITES_KEY','assets',bootSource.replace(oldHook,newHook)+';return boot;');
const page=createBoot(fs.readFileSync(path.join(L,'library.js'),'utf8'),supplied,clone,assert,vm,REVIEW_KEY,FAVORITES_KEY,supplied.assets)({},supplied);
const api=page.api,originalAssets=JSON.stringify(catalog.assets),originalShots=JSON.stringify(catalog.shotMaterials.shots);
const byID=new Map(api.C.assets.map(a=>[a.id,a]));
let checks=0;

for(const shot of additions.shots){
  const [source,clip,intake]=shot.materials.map(m=>byID.get(m.assetID));
  assert(source&&clip&&intake);
  for(const [origin,targets] of [[clip,[source,intake]],[source,[clip,intake]]]){
    const html=api.storyConnections(origin);
    for(const target of targets)assert(html.includes('data-open="'+target.id+'"'),'Exact source/result/intake viewer link '+target.id);
  }
  api.openViewer(clip.id);
  assert(api.dialog.innerHTML.includes('<video controls playsinline preload="metadata"'),'Native video player');
  assert(api.dialog.innerHTML.includes('data-open="'+source.id+'"'));
  assert(api.dialog.innerHTML.includes('data-open="'+intake.id+'"'));
  if(clip.id==='FLOW-LAG-SIGNAL-002'){
    assert(api.dialog.innerHTML.includes('data-open="FLOW-LAG-SIGNAL-001"'),'Take-two viewer retains take-one baseline');
    assert(api.storyConnections(byID.get('FLOW-LAG-SIGNAL-001')).includes('data-open="FLOW-LAG-SIGNAL-002"'),'Take-one viewer links its later comparison');
    assert.equal(clip.parentAssetID,'LAG500-L19-S3','Both takes share the actual starting still');
  }
  assert.equal(api.storyboardStage(clip),'preliminary');
  const review=api.reviewRecord(clip.id);
  assert(!review.status&&!review.workingReference&&!review.likenessRating&&!review.sceneQualityRating,'No inferred review');
  const scene=api.sceneReviewRecord('lisan',shot.id);
  assert.equal(scene.grade,null);
  assert(scene.ingredients.every(i=>i.status==='unreviewed'&&!i.required));
  assert.equal(api.sceneHandoffGate(scene).productionEligible,false);
  api.openViewer(intake.id);
  assert(api.dialog.innerHTML.includes('Document preview'));
  assert(api.dialog.innerHTML.includes(intake.sha256));
  checks++;
}
for(const [view,album] of [['videos','lisan:video-flow-prototypes'],['storyboard','lisan:story-flow-prototypes']]){
  api.setState({project:'lisan',view,album,search:'',storyStage:'all',storyStart:0,storyEnd:100,storyTheme:'all',storyLayout:'panels'});
  api.renderMain();
  const html=page.node('#main').innerHTML;
  for(const clip of additions.assets.filter(a=>a.kind==='video'))assert(html.includes('data-open="'+clip.id+'"'),view+' includes same exact clip ID');
  checks++;
}
api.setState({project:'lisan',view:'storyboard',album:'',storyLayout:'progress'});
api.renderMain();
for(const shot of additions.shots)assert(page.node('#main').innerHTML.includes('id="shot-work-'+shot.id+'"'));
assert(page.node('#main').innerHTML.includes('Placement still needed'));
assert.equal(JSON.stringify(api.C.assets.slice(0,catalog.assets.length)),originalAssets);
assert.equal(JSON.stringify(api.C.shotMaterials.shots.slice(0,catalog.shotMaterials.shots.length)),originalShots);
assert.equal(page.writes.length,0,'Reading and rendering creates no review storage writes');
assert.equal(page.fileWrites.length,0,'No review file writes');
checks++;
console.log(JSON.stringify({checks,videoSourceAndIntakeLinks:true,sourceResultLinks:true,videoAndStoryboardMembership:true,unplacedShotProgress:true,preliminaryWithoutReviewSeeds:true,existingAssetsAndShotsPreserved:true,storageWrites:page.writes.length,reviewFileWrites:page.fileWrites.length,browserQA:false,siteBuilt:false},null,2));
