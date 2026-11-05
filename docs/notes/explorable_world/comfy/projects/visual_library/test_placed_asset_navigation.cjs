/* Filed clips keep their review identity while old routes remain usable.
   Real renderer/handlers run against copied catalogs and isolated browser storage. */
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const clone=value=>JSON.parse(JSON.stringify(value));
const source=fs.readFileSync(path.join(__dirname,'library.js'),'utf8');
const raw=fs.readFileSync(path.join(__dirname,'catalog.js'),'utf8');
const catalog=JSON.parse(raw.slice(raw.indexOf('=')+1).trim().replace(/;$/,''));
const REVIEW_KEY='cfa-visual-review-v1',FAVORITES_KEY='cfa-visual-favorites-v1',EXPORT_KEY='cfa-visual-export-v1';
const byID=new Map(catalog.assets.map(a=>[a.id,a]));
const ids=['GEM-8B51108E','GEM-92EF6FD7'],destination='hon:video-supporting_cast',checks=[];
let harness=fs.readFileSync(path.join(__dirname,'test_collections_navigation.cjs'),'utf8');
harness=harness.slice(harness.indexOf('function boot() {'),harness.indexOf('\nconst page = boot(), api = page.api;'));
harness=harness.replace('function boot() {','function boot(seed={},chosenCatalog=catalog) {')
 .replace('new Map(Object.entries(saved))','new Map(Object.entries({...saved,...seed}))')
 .replace('REVIEW_CATALOG:clone(catalog)','REVIEW_CATALOG:clone(chosenCatalog)')
 .replace('querySelectorAll() {return [];}','querySelectorAll(selector) {return selectAll(selector).filter(e=>this.children.has(e));}')
 .replace('window.__collectionsTest={','window.__collectionsTest={render,route,normalizedBrowseRoute,')
 .replace('html:() => nodes.get','nodes,selectAll,html:() => nodes.get');
const boot=eval('('+harness.replace(/^function boot/,'function')+')');
const same=(actual,expected,message)=>assert.deepEqual(clone(actual),clone(expected),message);
const routeState=p=>{const s=p.api.getState();return {project:s.project,view:s.view,album:s.album};};
function hash(p,value){p.location.hash=value;p.api.parseHash();p.api.renderMain();}
function check(name,fn){fn();checks.push(name);}

check('empty Unassigned roots and original album routes resolve to their current destinations',()=>{
 const p=boot();assert(!p.C.assets.some(a=>a.project==='unassigned'),'Fixture catalog contains the applied placement');
 same(p.api.normalizedBrowseRoute('unassigned','all',''),{project:'hon',view:'intake',album:''});
 same(p.api.normalizedBrowseRoute('unassigned','videos','unassigned:video-needs_review'),{project:'hon',view:'videos',album:destination});
 p.api.route('unassigned','all');same(routeState(p),{project:'hon',view:'intake',album:''});assert.equal(p.location.hash.replace(/^#/,''),'hon/intake');
 hash(p,'#unassigned/all');same(routeState(p),{project:'hon',view:'intake',album:''});assert(p.html().includes('Intake verification'));
 hash(p,'#unassigned/videos/unassigned%3Avideo-needs_review');same(routeState(p),{project:'hon',view:'videos',album:destination});
 for(const id of ids)assert(p.html().includes('data-open="'+id+'"'),'The filed video stays reachable: '+id);
});

check('old exact-asset links follow the same ID to Hon and retain the requested image or video',()=>{
 const p=boot();
 for(const id of ids){
  hash(p,'#unassigned/asset/'+id);same(routeState(p),{project:'hon',view:'videos',album:destination});
  assert.equal(p.api.getState().openAsset,id,'Exact old asset link still identifies the original clip');
  assert(p.html().includes('data-open="'+id+'"'));
 }
});

check('navigation offers Intake once above Corner and hides only the empty Unassigned project',()=>{
 const p=boot();p.api.render();const html=p.nodes.get('#app').innerHTML;
 assert(!html.includes('data-project="unassigned"'),'No empty project button');assert(html.includes('data-project="hon"')&&html.includes('data-project="lisan"'));
 assert.equal((html.match(/data-view="intake"/g)||[]).length,1,'Intake is not duplicated by category navigation');
 assert(html.indexOf('data-view="intake"')<html.indexOf('data-view="mission_control"'),'Intake appears above Ziggy’s Corner');
 const intake=p.selectAll('[data-view]').find(n=>n.dataset.view==='intake');assert(intake);intake.click();same(routeState(p),{project:'hon',view:'intake',album:''});
});

check('new genuinely unassigned media keeps its project and ordinary routes available',()=>{
 const c=clone(catalog),newAsset={...clone(c.assets.find(a=>a.id===ids[0])),id:'TEST-FUTURE-UNASSIGNED',project:'unassigned',album:'unassigned:video-needs_review',title:'Future unassigned clip',sha256:'f'.repeat(64)};
 delete newAsset.placement;delete newAsset.characterCollectionID;c.assets.push(newAsset);
 c.albums.push({id:newAsset.album,project:'unassigned',category:'videos',title:'Future clips',description:'',assetIDs:[newAsset.id]});
 const p=boot({},c);same(p.api.normalizedBrowseRoute('unassigned','all',''),{project:'unassigned',view:'all',album:''});
 p.api.render();assert(p.nodes.get('#app').innerHTML.includes('data-project="unassigned"'));
 p.api.route('unassigned','all');same(routeState(p),{project:'unassigned',view:'all',album:''});assert(p.html().includes('data-open="TEST-FUTURE-UNASSIGNED"'));
 hash(p,'#unassigned/videos/unassigned%3Avideo-needs_review');same(routeState(p),{project:'unassigned',view:'videos',album:newAsset.album});assert(p.html().includes('data-open="TEST-FUTURE-UNASSIGNED"'),'A reused source album remains accessible for its new contents');
 // Earlier links to the two already-filed clips still go to their own Hon album.
 hash(p,'#unassigned/asset/'+ids[1]);assert.equal(p.api.getState().project,'hon');assert.equal(p.api.getState().openAsset,ids[1]);
});

check('old ID and SHA reviews keep notes variants favorites basket and the correction plan under Hon',()=>{
 const oldReviews=catalog.reviewDecisions.filter(r=>ids.includes(r.id)).map(r=>({...clone(r),project:'unassigned'}));
 assert.equal(oldReviews.length,2);const expected=new Map(oldReviews.map(r=>[r.id,r]));
 const p=boot({[REVIEW_KEY]:JSON.stringify({format:REVIEW_KEY,items:oldReviews}),[FAVORITES_KEY]:JSON.stringify(ids),[EXPORT_KEY]:JSON.stringify({format:EXPORT_KEY,items:oldReviews.map(r=>({id:r.id,sha256:r.sha256,project:'unassigned'}))})});
 const sourceBefore=JSON.stringify(p.C),storageBefore=Object.fromEntries(p.storage),reviewsBefore=clone(p.api.reviewPayload().items);
 for(const id of ids){
  const r=p.api.reviewRecord(id),old=expected.get(id);assert.equal(r.status,old.status);assert.equal(r.note,old.note);assert.equal(r.variant,old.variant);same(r.shotPlan??null,old.shotPlan??null);
 }
 const payload=p.api.reviewPayload();for(const list of [payload.items.filter(r=>ids.includes(r.id)),payload.favorites,payload.exportBasket]){
  assert.equal(list.length,2);for(const item of list){assert.equal(item.project,'hon');assert.equal(item.sha256,expected.get(item.id).sha256);assert.equal(item.path,byID.get(item.id).repoPath);}
 }
 p.api.route('hon','shot_plans');assert(p.html().includes('GEM-92EF6FD7'),'Saved correction plan appears under Hon');
 p.api.route('unassigned','all');p.api.route('hon','cast','hon:cast-hooded');p.toggle('hon:cast-hooded');
 for(const id of ids)assert(p.html().includes('data-open="'+id+'"'),'Hooded traveler hub includes the same filed video');
 same(p.api.reviewPayload().items,reviewsBefore,'Browsing does not rewrite user choices');assert.equal(JSON.stringify(p.C),sourceBefore,'Browsing does not mutate source metadata');
 assert.deepEqual(Object.fromEntries(p.storage),storageBefore);assert.equal(p.writes.length,0,'Navigation writes no review data');
});

for(const name of checks)console.log('PASS '+name);
console.log('Placed asset navigation checks passed: '+checks.length);
