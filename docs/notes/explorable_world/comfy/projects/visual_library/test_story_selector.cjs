/* Story routing and shot rendering against the actual local library script.
   Uses the pinned map as a prebuild fixture when the catalog is not rebuilt yet.
   --published requires the real catalog contract. No source or review writes. */
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const L=__dirname,clone=value=>JSON.parse(JSON.stringify(value));
const REVIEW_KEY='cfa-visual-review-v1',FAVORITES_KEY='cfa-visual-favorites-v1';
const raw=fs.readFileSync(path.join(L,'catalog.js'),'utf8');
const catalog=JSON.parse(raw.slice(raw.indexOf('=')+1).trim().replace(/;$/,''));
const supplied=clone(catalog),sequenceID='LAG-STORY-01-THE-GLOVED-HAND';
const sourceMap=JSON.parse(fs.readFileSync(path.join(L,'../lisan_al_gaib/story/writer_pass_20261012/STORY_01_PANEL_MAP_20261014.json'),'utf8'));
const published=(supplied.storyboardStories||[]).some(s=>s.sequenceID===sequenceID);
if(process.argv.includes('--published'))assert(published,'Story catalog must be published before this check');
if(!published){
  const byPath=new Map(supplied.assets.map(a=>[a.repoPath,a]));
  const byHash=new Map(supplied.assets.filter(a=>a.sha256).map(a=>[a.sha256,a]));
  const seq=clone(sourceMap),ids=new Set();
  const kinds={'the Keepers':'character','Angels':'character','the oldest Keeper':'character','Jet in the scene (LAG-JET-01)':'character','Jet in the scene':'character','the child with the lamp':'character','Sassy':'character','James (lettered)':'character','the thumper rack (a new request)':'object_design','the lattice (its form a proposal; colour unrecorded)':'object_design','the lattice':'object_design'};
  for(const shot of seq.shots){
    shot.pendingReferenceDetails=shot.pendingReferences.map(label=>({label,kind:kinds[label]}));
    for(const material of shot.materials){
      let asset=byPath.get(material.repoPath)||byHash.get(material.sha256);
      if(!asset){asset={id:'story01-test:'+material.sha256.slice(0,16),project:'lisan',category:'storyboard',album:'lisan:story01-frames',kind:'image',title:path.posix.basename(material.repoPath),filename:path.posix.basename(material.repoPath),repoPath:material.repoPath,src:'test.jpg',thumb:'test.jpg',sha256:material.sha256,bytes:material.bytes};supplied.assets.push(asset);byPath.set(asset.repoPath,asset);byHash.set(asset.sha256,asset);}
      material.assetID=asset.id;ids.add(asset.id);
    }
  }
  seq.assetIDs=[...ids];seq.sourceAlbumIDs=['lisan:story01-frames'];seq.coverID=seq.shots[0].materials[0].assetID;
  supplied.storyboardSequences=[...(supplied.storyboardSequences||[]).filter(s=>s.id!==seq.id),seq];
  const docs={};
  for(const [id,project,title] of [['test:meta-writing','lisan','Meta Mirror cue map'],['test:story01-writing','lisan','Story 01 skeleton'],['test:prose-writing','lisan','Series seed'],['test:hon-writing','hon','Hon scene cards']]){
    supplied.assets.push({id,project,title,category:'documents',kind:'document',album:project+':test-documents',filename:id+'.txt',repoPath:id+'.txt',src:'test.txt',sha256:id.padEnd(64,'0'),text:title,note:''});docs[id]=id;
  }
  supplied.storyboardStories=[
    {id:'lisan:meta-mirror',project:'lisan',title:'Meta Mirror',kind:'song',documentIDs:['test:meta-writing']},
    {id:'lisan:story-01',project:'lisan',title:seq.title,kind:'sequence',sequenceID,coverID:seq.coverID,documentIDs:['test:story01-writing']},
    {id:'lisan:series-seeds',project:'lisan',title:'Series and seeds',kind:'prose',documentIDs:['test:prose-writing']},
    {id:'hon:strictly-business',project:'hon',title:'Strictly Business',kind:'song',documentIDs:['test:hon-writing']},
    ...(supplied.storyboardSequences||[]).filter(s=>s.project==='hon').map(s=>({id:s.id,project:'hon',title:s.title,kind:'sequence',sequenceID:s.id,documentIDs:[]}))
  ];
  const sw2=(supplied.shotMaterials?.shots||[]).find(s=>s.id==='LAG-FLOW-SW2-001');
  assert(sw2,'Existing exact Flow record is available');sw2.independentSequenceID=sequenceID;sw2.storyShotID='S01-4.1';
}
const scopeTest=fs.readFileSync(path.join(L,'test_reference_scope.cjs'),'utf8');
const bootSource=scopeTest.slice(scopeTest.indexOf('function boot('),scopeTest.indexOf('async function main()'));
const oldHook='window.__scopeTest={openViewer,reviewRecord,reviewPayload,importReview,exportReference,inReviewQueue,whenFileWritesSettle(){return fileWriteChain;}};';
const newHook='window.__scopeTest={C,dialog,openViewer,reviewRecord,reviewPayload,renderMain,route,selectedStoryboardStory,storyboardStories,storySequenceCoverage,storyConnections,writerDevelopment,resetStoryFilters,songSourcePanels,getState(){return {...state};},setState(p){Object.assign(state,p);},expandCollection(id){expandedCollections.add(id);renderMain();},navigate(hash){location.hash=hash;parseHash();render();},whenFileWritesSettle(){return fileWriteChain;}};';
assert(bootSource.includes(oldHook));
const makeBoot=new Function('source','catalog','clone','assert','vm','REVIEW_KEY','FAVORITES_KEY','assets',bootSource.replace(oldHook,newHook)+';return boot;');
const page=makeBoot(fs.readFileSync(path.join(L,'library.js'),'utf8'),supplied,clone,assert,vm,REVIEW_KEY,FAVORITES_KEY,supplied.assets)({},supplied);
const api=page.api,originalCatalog=JSON.stringify(api.C);
const reviewSnapshot=()=>JSON.stringify(Object.fromEntries(['items','sceneReviews','favorites','exportBasket'].map(key=>[key,api.reviewPayload()[key]])));
const reviews=reviewSnapshot();
const html=()=>page.node('#main').innerHTML;
const story01=api.storyboardStories('lisan').find(s=>s.sequenceID===sequenceID),seq=api.C.storyboardSequences.find(s=>s.id===sequenceID);
const choose=id=>{const select=page.node('#story-select');select.value=id;select.fire('change');};
const toStory=story=>api.navigate('#'+[story.project,'storyboard','story:'+story.id].map(encodeURIComponent).join('/'));
let checks=0;

api.route('lisan','storyboard');
assert.equal(api.selectedStoryboardStory().id,'lisan:meta-mirror');
assert.equal(page.node('#story-select').value,'lisan:meta-mirror');
assert(html().indexOf('id="story-select"')<html().indexOf('id="story-stage"'),'Story is before secondary Stage');
assert(html().includes('50 matching panels'),'Meta Mirror preserves 50 ordered song panels');
assert.equal(api.songSourcePanels('lisan').length,50);
assert(html().includes('id="story-theme"')&&html().includes('id="story-start"')&&html().includes('id="story-end"'));
for(const story of api.storyboardStories('lisan'))assert(html().includes('data-story-card="'+story.id+'"'),'One landing card per story '+story.id);
const landing=html().split('data-story-card="'+story01.id+'"')[1].split('</a>')[0];
assert(landing.includes('Preliminary')&&landing.includes('38 shots')&&landing.includes('9 scenes'));
assert(landing.includes('33 with frames')&&landing.includes('1 with results')&&landing.includes('21 with pending references')&&landing.includes('20 need characters'),'Landing card exposes frame/result/pending scope');
const songDocs=api.selectedStoryboardStory().documentIDs;
for(const id of songDocs)assert(html().includes('data-open="'+id+'"'));
for(const id of story01.documentIDs.filter(id=>!songDocs.includes(id)))assert(!html().includes('data-open="'+id+'"'),'Sequence writings stay out of song '+id);
checks+=10;

api.setState({storyTheme:'invalid',storyStage:'production',storyStart:40,storyEnd:60,storyLayout:'progress',search:'stale filter'});
choose(story01.id);
assert.equal(api.selectedStoryboardStory().id,story01.id);
assert.equal(api.getState().search,'');
assert.deepEqual(clone(Object.fromEntries(['storyTheme','storyStage','storyStart','storyEnd','storyLayout'].map(k=>[k,api.getState()[k]]))),{storyTheme:'all',storyStage:'all',storyStart:0,storyEnd:100,storyLayout:'panels'});
assert(!html().includes('id="story-theme"')&&!html().includes('id="story-start"')&&!html().includes('id="story-end"'),'Song filters are absent from sequence');
assert(html().includes('id="story-stage"'));
assert.deepEqual(clone(api.storySequenceCoverage(seq)),{shots:38,scenes:9,frames:33,results:1,pending:21,characters:20,objects:5});
assert.equal((html().match(/data-story-shot-id=/g)||[]).length,38);
assert.equal((html().match(/data-story-scene=/g)||[]).length,9);
assert.deepEqual([...html().matchAll(/data-story-shot-id="([^"]+)"/g)].map(m=>m[1]),sourceMap.sections.flatMap(s=>s.shotIDs),'Source scene/shot order remains exact');
for(const role of ['Setting stand-in','Exact source frame','Character reference','Storyboard concept','Result on disk'])assert(html().includes(role),'Material role label '+role);
assert(html().includes('Available material is not shot readiness'));
const shot41=html().split('data-story-shot-id="S01-4.1"')[1].split('</article>')[0];
assert(shot41.includes('data-open="FLOW-LAG-SW2-001"'),'Exact Flow result belongs to S01-4.1');
assert(!html().includes('data-open="FLOW-LAG-SIGNAL-001"')&&!html().includes('data-open="FLOW-LAG-SIGNAL-002"'));
const shot53=html().split('data-story-shot-id="S01-5.3"')[1].split('</article>')[0];
assert(shot53.includes('Object / design')&&shot53.includes('the lattice'));
assert(!shot53.includes('<span>Character</span>'),'Lattice-only shot is not a missing-character shot');
for(const shot of seq.shots)for(const pending of shot.pendingReferences)assert(html().includes(pending.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;')),'Original pending label '+pending);
for(const id of story01.documentIDs)assert(html().includes('data-open="'+id+'"'));
checks+=16;

// Rendering the map must never manufacture accepted references, source scores,
// ratings, or review decisions. It also keeps material visible when its normal
// browsing category is unrelated to the sequence.
assert.equal(JSON.stringify(api.C),originalCatalog);
assert.equal(reviewSnapshot(),reviews);
assert.equal(page.writes.length,0);
page.node('#story-stage').value='production';page.node('#story-stage').fire('change');
assert(html().includes('No shots match this stage.'));
assert(!html().includes('data-story-shot-id='));
page.node('#story-stage').value='all';page.node('#story-stage').fire('change');
api.setState({search:'S01-5.3'});api.renderMain();
assert.deepEqual([...html().matchAll(/data-story-shot-id="([^"]+)"/g)].map(m=>m[1]),['S01-5.3']);
checks+=6;

const prose=api.storyboardStories('lisan').find(s=>s.kind==='prose');assert(prose,'Prose remains separately selectable');
choose(prose.id);
assert(html().includes('No panels yet.'));
assert(!html().includes('data-story-shot-id=')&&!html().includes('id="story-stage"')&&!html().includes('id="story-theme"'));
for(const id of prose.documentIDs)assert(html().includes('data-open="'+id+'"'));
const document=api.C.assets.find(a=>a.id===prose.documentIDs[0]);
if(document){page.open(document.id);assert(api.dialog.open&&api.dialog.innerHTML.includes('Document preview')&&api.dialog.innerHTML.includes(document.title),'Existing document reader opens the selected writing');api.dialog.close();}
checks+=3;

api.setState({storyTheme:'invalid',storyStage:'verification',storyStart:20,storyEnd:30,search:'stale'});
api.route('hon','storyboard');
assert.equal(api.selectedStoryboardStory().id,'hon:strictly-business');
assert(html().includes('36 matching panels'));
assert.equal(api.songSourcePanels('hon').length,36);
assert.equal(api.getState().storyStart,0);assert.equal(api.getState().storyEnd,100);assert.equal(api.getState().storyStage,'all');assert.equal(api.getState().search,'');
const legacy=api.storyboardStories('hon').find(s=>s.kind==='sequence'),honSeq=api.C.storyboardSequences.find(s=>s.id===legacy.sequenceID);
choose(legacy.id);
api.expandCollection(honSeq.id);
for(const id of honSeq.sections.flatMap(s=>s.assetIDs||[]))assert(html().includes('data-open="'+id+'"')||api.reviewRecord(id).status==='remove','Legacy section asset retained '+id);
assert(!html().includes('id="story-theme"')&&!html().includes('id="story-start"'));
api.route('hon','storyboard',honSeq.sourceAlbumIDs[0]);
assert.equal(api.selectedStoryboardStory().sequenceID,honSeq.id,'Old sequence album deep link remains usable');
checks+=7;

api.navigate('#'+['lisan','storyboard','story:'+story01.id].map(encodeURIComponent).join('/'));
assert.equal(api.selectedStoryboardStory().sequenceID,sequenceID);
assert.equal((html().match(/data-story-shot-id=/g)||[]).length,38);
api.setState({storyStart:20,storyStage:'production',search:'stale'});
api.navigate('#lisan/storyboard/story%3Alisan%3Ameta-mirror');
assert.equal(api.selectedStoryboardStory().id,'lisan:meta-mirror');
assert.equal(api.getState().storyStart,0);assert.equal(api.getState().storyStage,'all');assert.equal(api.getState().search,'');
api.setState({storyLayout:'progress'});api.renderMain();
assert(html().includes('shot-work-LAG-FLOW-SIGNAL-001')&&html().includes('shot-work-LAG-FLOW-SIGNAL-002'),'Signal clips stay with Meta Mirror');
assert(!html().includes('shot-work-LAG-FLOW-SW2-001'),'Story01 Flow is not an unplaced song clip');
assert(!html().includes('data-open="FLOW-LAG-SW2-001"'));
assert(api.writerDevelopment('lisan',true).includes('writer-development'),'Full writer development remains available to collaborators');
assert.equal(JSON.stringify(api.C),originalCatalog);
assert.equal(reviewSnapshot(),reviews);
assert.equal(page.writes.length,0);
checks+=10;
console.log(JSON.stringify({checks,mode:published?'published':'pinned-map prebuild fixture',songs:{lisan:50,hon:36},story01:clone(api.storySequenceCoverage(seq)),reviewWrites:page.writes.length}));
