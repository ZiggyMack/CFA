/* Verify published Flow prototype contracts against the actual library renderer.
   --prebuild supplies only registered manifest additions in memory. Neither mode
   builds the site, opens a browser, writes reviews, or modifies source media. */
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const L=__dirname;
const R=path.resolve(L,'../../../../../..'),prebuild=process.argv.includes('--prebuild');
const story01SequenceID='LAG-STORY-01-THE-GLOVED-HAND';
const clone=value=>JSON.parse(JSON.stringify(value));
const REVIEW_KEY='cfa-visual-review-v1',FAVORITES_KEY='cfa-visual-favorites-v1';
const raw=fs.readFileSync(path.join(L,'catalog.js'),'utf8');
const catalog=JSON.parse(raw.slice(raw.indexOf('=')+1).trim().replace(/;$/,''));
const manifest=JSON.parse(fs.readFileSync(path.join(L,'flow_prototypes.json'),'utf8'));
assert.equal(manifest.publicationState,'registered_for_site_build');
assert.equal(manifest.media.length,3);
assert.equal(manifest.documents.length,3);
assert.equal(manifest.albums.length,2);
assert.equal(manifest.shots.length,3);
assert.deepEqual(manifest.media.map(m=>m.id),['FLOW-LAG-SW2-001','FLOW-LAG-SIGNAL-001','FLOW-LAG-SIGNAL-002']);
const supplied=clone(catalog);
if(prebuild){
  const existing=new Set(catalog.assets.map(a=>a.id));
  assert(manifest.media.concat(manifest.documents).every(a=>!existing.has(a.id)),'Use published mode after the new records are built');
  const url=p=>path.relative(L,path.join(R,p)).split(path.sep).map(encodeURIComponent).join('/');
  for(const item of manifest.media){
    const {path:p,thumbnailPath,...asset}=item;
    supplied.assets.push({...asset,src:url(p),thumb:url(thumbnailPath),repoPath:p,filename:path.basename(p)});
  }
  for(const item of manifest.documents){
    supplied.assets.push({id:item.id,project:item.project,src:url(item.path),filename:path.basename(item.path),title:item.title,repoPath:item.path,historicalRepoPath:item.path,category:'documents',album:item.album,kind:'document',text:fs.readFileSync(path.join(R,item.path),'utf8').replace(/^\uFEFF/,'').slice(0,40000),note:'',inert:false,sha256:item.sha256,bytes:item.bytes,sourceStatus:item.sourceStatus,intakeID:item.intakeID});
  }
  for(const album of manifest.albums){
    const {related,...rest}=album;
    supplied.albums.push({...rest,assetIDs:[...new Set([...manifest.media.filter(a=>a.album===album.id).map(a=>a.id),...related])]});
  }
  supplied.shotMaterials.shots.push(...clone(manifest.shots));
}
const additions={assets:supplied.assets.filter(a=>manifest.media.some(m=>m.id===a.id)),shots:manifest.shots};
assert.equal(additions.assets.length,3);
const expectedByID=new Map(supplied.assets.map(a=>[a.id,a]));
for(const item of manifest.media.concat(manifest.documents)){
  const actual=expectedByID.get(item.id);
  assert(actual,'Registered asset exists: '+item.id);
  assert.equal(actual.sha256,item.sha256);
  assert.equal(actual.bytes,item.bytes);
  assert.equal(actual.repoPath,item.path);
}
for(const album of manifest.albums){
  const actual=supplied.albums.find(a=>a.id===album.id);
  assert(actual);
  assert.deepEqual(actual.assetIDs,manifest.media.map(a=>a.id));
}
for(const shot of additions.shots){
  const derived=supplied.shotMaterials.shots.find(s=>s.id===shot.id),expected=!prebuild&&shot.id==='LAG-FLOW-SW2-001'?{...shot,independentSequenceID:story01SequenceID,storyShotID:'S01-4.1'}:shot;
  assert.deepEqual(derived,expected,'Only explicit Story01 placement metadata may augment the source Flow shot');
  if(shot.id!=='LAG-FLOW-SW2-001')assert(!derived.independentSequenceID&&!derived.storyShotID,'Signal remains a song-specific placement record');
  assert.equal(shot.timing,'unassigned');
  assert.deepEqual(shot.panelAssetIDs,[]);
  for(const material of shot.materials)assert.equal(expectedByID.get(material.assetID)?.sha256,material.sha256);
}

const scopeTest=fs.readFileSync(path.join(L,'test_reference_scope.cjs'),'utf8');
const bootSource=scopeTest.slice(scopeTest.indexOf('function boot('),scopeTest.indexOf('async function main()'));
const oldHook='window.__scopeTest={openViewer,reviewRecord,reviewPayload,importReview,exportReference,inReviewQueue,whenFileWritesSettle(){return fileWriteChain;}};';
const newHook='window.__scopeTest={openViewer,C,dialog,reviewRecord,reviewPayload,sceneReviewRecord,sceneHandoffGate,storyConnections,storyboardStage,renderMain,setState(p){Object.assign(state,p);},whenFileWritesSettle(){return fileWriteChain;}};';
assert(bootSource.includes(oldHook));
const createBoot=new Function('source','catalog','clone','assert','vm','REVIEW_KEY','FAVORITES_KEY','assets',bootSource.replace(oldHook,newHook)+';return boot;');
const page=createBoot(fs.readFileSync(path.join(L,'library.js'),'utf8'),supplied,clone,assert,vm,REVIEW_KEY,FAVORITES_KEY,supplied.assets)({},supplied);
const api=page.api,originalAssets=JSON.stringify(supplied.assets),originalShots=JSON.stringify(supplied.shotMaterials.shots);
const reviewSnapshot=()=>JSON.stringify(Object.fromEntries(['items','sceneReviews','favorites','exportBasket'].map(key=>[key,api.reviewPayload()[key]]))),originalReviews=reviewSnapshot();
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
    assert.equal(clip.predecessorAssetID,'FLOW-LAG-SIGNAL-001');
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
const songShots=additions.shots.filter(s=>prebuild||s.id!=='LAG-FLOW-SW2-001');
for(const shot of songShots)assert(page.node('#main').innerHTML.includes('id="shot-work-'+shot.id+'"'));
assert(page.node('#main').innerHTML.includes('Placement still needed'));
if(!prebuild){
  const songHTML=page.node('#main').innerHTML;
  assert(!songHTML.includes('id="shot-work-LAG-FLOW-SW2-001"'),'SW2 is no longer an unplaced song task');
  assert(!songHTML.includes('data-open="FLOW-LAG-SW2-001"'),'SW2 clip is not exposed as unrelated Meta Mirror material');
  const story=supplied.storyboardStories.find(s=>s.project==='lisan'&&s.sequenceID===story01SequenceID);assert(story,'Explicit Story01 destination exists');
  const sequence=supplied.storyboardSequences.find(s=>s.id===story01SequenceID);assert(sequence);
  const shot=sequence.shots.find(s=>s.shotID==='S01-4.1');assert(shot);
  assert(shot.materials.some(m=>m.assetID==='FLOW-LAG-SW2-001'&&m.role==='result_on_disk'),'Pinned Story01 map associates exact Flow return with S01-4.1');
  assert(!sequence.shots.some(s=>s.materials.some(m=>/^FLOW-LAG-SIGNAL-/.test(m.assetID))),'Signal results are absent from independent sequence map');
  api.setState({project:'lisan',view:'storyboard',album:'story:'+story.id,search:'',storyStage:'all',storyStart:0,storyEnd:100,storyTheme:'all',storyLayout:'panels'});api.renderMain();
  const sequenceHTML=page.node('#main').innerHTML,article=sequenceHTML.split('data-story-shot-id="S01-4.1"')[1]?.split('</article>')[0];
  assert(article&&article.includes('data-open="FLOW-LAG-SW2-001"'),'Exact SW2 return renders under its Story01 shot');
  assert(article.includes('Result on disk')&&article.includes('Exact source frame'));
  assert(!sequenceHTML.includes('data-open="FLOW-LAG-SIGNAL-001"')&&!sequenceHTML.includes('data-open="FLOW-LAG-SIGNAL-002"'));
  checks++;
}
assert.equal(JSON.stringify(api.C.assets),originalAssets);
assert.equal(JSON.stringify(api.C.shotMaterials.shots),originalShots);
assert.equal(reviewSnapshot(),originalReviews,'Existing reviews, scene reviews, favorites and basket remain unchanged');
assert.equal(page.writes.length,0,'Reading and rendering creates no review storage writes');
assert.equal(page.fileWrites.length,0,'No review file writes');
checks++;
console.log(JSON.stringify({checks,videoAssets:3,intakeDocuments:3,sharedAlbums:2,unplacedSongShots:songShots.length,story01SW2Placement:prebuild?'not yet registered':'S01-4.1',videoSourceAndIntakeLinks:true,sourceResultLinks:true,signalTakeOneAndTwoLinks:true,videoAndStoryboardMembership:true,preliminaryWithoutReviewSeeds:true,existingAssetsAndShotsPreserved:true,storageWrites:page.writes.length,reviewFileWrites:page.fileWrites.length,browserQA:false,catalogMode:prebuild?'prebuild fixture':'published'},null,2));
