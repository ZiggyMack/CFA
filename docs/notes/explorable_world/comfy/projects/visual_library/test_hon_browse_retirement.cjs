/* Hon Comfy/Inspiration cleanup: actual renderer and catalog in a Node DOM double.
   No source-file deletion, catalog mutation, or live-browser visual QA. */
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const clone=x=>JSON.parse(JSON.stringify(x)),root=__dirname;
const source=fs.readFileSync(path.join(root,'library.js'),'utf8');
const raw=fs.readFileSync(path.join(root,'catalog.js'),'utf8'),catalog=JSON.parse(raw.slice(raw.indexOf('=')+1).trim().replace(/;$/,''));
const config=JSON.parse(fs.readFileSync(path.join(root,'collections.json'),'utf8'));
const REVIEW_KEY='cfa-visual-review-v1',FAVORITES_KEY='cfa-visual-favorites-v1',EXPORT_KEY='cfa-visual-export-v1';
const harness=fs.readFileSync(path.join(root,'test_collections_navigation.cjs'),'utf8');
let body=harness.slice(harness.indexOf('function boot()'),harness.indexOf('const page = boot()'));
body=body.replace(/window\.__collectionsTest=\{[^\n]+?\};/,'window.__collectionsTest={C,render,renderMain,parseHash,route,normalVisible,isArchived,projectAssets,reviewRecord,reviewPayload,reviews,creatureBossIdeasGroup,castHubGroups,comfyMouthAlbum,normalizedBrowseRoute,sharedCharacterReferences,setState(p){Object.assign(state,p);},getState(){return state;}};');
body=body.replace('location,writes,storage,scrolls,','location,writes,storage,scrolls,appHTML:()=>nodes.get("#app").innerHTML,');
function pageFor(model=catalog){return new Function('source','catalog','byID','clone','assert','vm','REVIEW_KEY','FAVORITES_KEY','EXPORT_KEY',body+';return boot();')(source,model,new Map(model.assets.map(a=>[a.id,a])),clone,assert,vm,REVIEW_KEY,FAVORITES_KEY,EXPORT_KEY);}
const page=pageFor(),api=page.api,byID=new Map(api.C.assets.map(a=>[a.id,a]));
const reviewsBefore=clone(api.reviewPayload().items),catalogBefore=clone(api.C),storedBefore=Object.fromEntries(page.storage);
const creatureAlbum=api.C.albums.find(a=>a.id==='hon:creature-ideas');assert(creatureAlbum);
const creatureIDs=creatureAlbum.assetIDs;
let checks=0;

const sourceAlbum=config.albums.find(a=>a.id==='creature-ideas');
assert.equal(sourceAlbum.collection_id,'cast');assert.equal(new Set(sourceAlbum.asset_ids).size,12);
assert.deepEqual([...sourceAlbum.asset_ids].sort(),[...creatureIDs].sort());
for(const id of creatureIDs)assert.equal(config.assets.find(a=>a.asset_id===id).collection_id,'cast');
for(const id of ['cast','inspiration']){
  const collection=config.collections.find(c=>c.id===id);
  assert.equal(collection.display_asset_count,collection.display_asset_ids.length);
  assert.equal(new Set(collection.display_asset_ids).size,collection.display_asset_count);
  assert.equal(collection.album_ids.includes('creature-ideas'),id==='cast');
  assert.equal(creatureIDs.filter(assetID=>collection.display_asset_ids.includes(assetID)).length,id==='cast'?12:0);
}
if(process.argv.includes('--published')){
  assert.equal(creatureAlbum.category,'cast','Rebuilt album category is published');
  for(const id of creatureIDs)assert.equal(byID.get(id).category,'cast','Rebuilt asset category is published');
}
checks+=3;

api.setState({project:'hon',view:'comfy',album:'',search:''});api.render();
assert(!page.html().includes('comfy-mouth-references'),'Hon Comfy no longer repeats the mouth/head section');
assert(!page.html().includes('HD-LIKENESS-02'),'Historical group photo is absent from ordinary Comfy');
assert(api.isArchived(byID.get('HD-LIKENESS-02')),'Group source remains accessible in Archive');
const unrelated=api.C.albums.filter(a=>a.project==='hon'&&a.category==='comfy'&&!api.comfyMouthAlbum(a)).flatMap(a=>a.assetIDs).filter(id=>api.normalVisible(byID.get(id)));
assert(unrelated.length>0);for(const id of unrelated)assert(page.html().includes('data-open="'+id+'"'),'Other Comfy reference remains: '+id);
assert(!page.appHTML().includes('data-view="inspiration"'),'Hon Inspiration navigation is removed');
const displayedComfyCount=new Set(unrelated).size;
assert(page.appHTML().includes('data-view="comfy" class="active">Comfy swap targets<span class="count">'+displayedComfyCount+'</span>'),'Comfy count matches its visible groups');
checks+=4;

api.setState({view:'working'});api.renderMain();page.toggle(api.C.characterBOM.characters.find(c=>c.project==='hon').id);
assert(page.html().includes('Verbose BOM'),'The detailed working board remains available');
const mouth=byID.get('HD-B-91ef00348229');assert(mouth&&api.normalVisible(mouth),'Canonical mouth reference stays active');
checks++;

api.setState({view:'cast',album:'',search:''});api.renderMain();
const visibleCreatureIDs=creatureIDs.filter(id=>api.normalVisible(byID.get(id)));
assert.equal(visibleCreatureIDs.length,12,'All twelve current creature examples remain visible');
assert(page.html().includes('class="collapsible-section creature-boss-ideas"'));
for(const id of visibleCreatureIDs)assert.equal(page.html().split('data-open="'+id+'"').length-1,1,'Each creature appears once: '+id);
assert(!api.castHubGroups().some(g=>g.id==='hon:creature-ideas'),'No duplicate generic creature character hub');
assert(api.castHubGroups().some(g=>g.id==='hon:boss-round01'),'Existing selected crocodile hub remains');
assert(!api.castHubGroups().flatMap(g=>g.items.map(a=>a.id)).some(id=>creatureIDs.includes(id)),'Creature ideas do not duplicate existing cast');
checks+=3;

api.setState({view:'all',album:'',search:'',allPurpose:'all'});api.renderMain();
for(const id of visibleCreatureIDs)assert.equal(page.html().split('data-open="'+id+'"').length-1,1,'All files shows creature image once: '+id);
api.setState({view:'cast',search:'a query matching no creature reference'});api.renderMain();assert(!api.creatureBossIdeasGroup());
checks+=2;

page.location.hash='#hon/inspiration';api.parseHash();api.render();
assert.equal(api.getState().view,'archive');assert.equal(api.getState().album,'');assert.equal(page.location.hash,'hon/archive');
page.location.hash='#hon/inspiration/hon%3Acreature-ideas';api.parseHash();api.setState({search:''});api.renderMain();
assert.equal(api.getState().view,'cast');assert.equal(api.getState().album,'hon:creature-ideas');
assert(page.html().includes('Creature boss ideas'));assert(!page.html().includes('data-collection="hon:boss-round01"'));
assert.deepEqual(clone(api.normalizedBrowseRoute('lisan','inspiration','test')), {view:'inspiration',album:'test'});
checks+=3;

api.setState({view:'archive',album:'',search:''});api.renderMain();
assert(page.html().includes('data-open="HD-LIKENESS-02"'),'Archived source photo can still be reviewed');
const retiredIDs=api.C.albums.filter(a=>['hon:scene-ideas','hon:outfit-ideas'].includes(a.id)).flatMap(a=>a.assetIDs);
assert.equal(retiredIDs.length,22);
const archivedIdeas=retiredIDs.filter(id=>api.isArchived(byID.get(id)));assert(archivedIdeas.length);
for(const id of archivedIdeas)assert(page.html().includes('data-open="'+id+'"'),'Archived inspiration remains reachable: '+id);
assert(creatureIDs.every(id=>!api.isArchived(byID.get(id))));
checks+=2;

// Explicit restores and accepted current use take precedence over the default retirement.
const target=archivedIdeas[0],saved=clone(api.reviewRecord(target));
api.reviews.set(target,{...saved,collectionState:'working'});assert(!api.isArchived(byID.get(target)));
api.reviews.set(target,{...saved,collectionState:null,status:'keep',storyboardStage:'production'});assert(!api.isArchived(byID.get(target)));
api.reviews.set(target,{...saved,collectionState:null,workingReference:{status:'approved',scope:'outfit'}});assert(!api.isArchived(byID.get(target)));
api.reviews.set(target,{...saved,collectionState:'archived',status:'keep',storyboardStage:'production'});assert(api.isArchived(byID.get(target)));
if(reviewsBefore.some(r=>r.id===target))api.reviews.set(target,saved);else api.reviews.delete(target);
checks+=2;

const lisanModel=clone(catalog),sample=clone(lisanModel.assets.find(a=>a.project==='lisan'&&a.kind==='image'));
Object.assign(sample,{id:'TEST-LISAN-INSPIRATION',album:'lisan:test-inspiration',category:'inspiration',archived:false});
lisanModel.assets.push(sample);lisanModel.albums.push({id:sample.album,project:'lisan',category:'inspiration',title:'Lisan inspiration remains',assetIDs:[sample.id]});
const lisan=pageFor(lisanModel);lisan.api.setState({project:'lisan',view:'inspiration',album:'',search:''});lisan.api.render();
assert(lisan.appHTML().includes('data-view="inspiration"'));assert(lisan.html().includes('data-open="TEST-LISAN-INSPIRATION"'));
lisan.api.setState({view:'comfy'});lisan.api.renderMain();assert(lisan.html().includes('comfy-mouth-references'),'Lisan Comfy mouth collections are unchanged');
checks+=2;

assert.deepEqual(clone(api.C),catalogBefore,'Presentation does not alter catalog data');
assert.deepEqual(clone(api.reviewPayload().items),reviewsBefore,'Browsing and default Archive policy preserve saved decisions');
assert.deepEqual(Object.fromEntries(page.storage),storedBefore);assert.equal(page.writes.length,0);
checks++;
console.log(JSON.stringify({passed:true,checks,creatureImages:12,archivedInspiration:archivedIdeas.length,comfyVisible:displayedComfyCount,publishedCategories:process.argv.includes('--published'),sourceFilesDeleted:0,reviewWrites:0,browserVisualQA:false}));
