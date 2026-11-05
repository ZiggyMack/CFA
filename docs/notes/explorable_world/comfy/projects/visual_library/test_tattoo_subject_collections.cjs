/* Compact All files regression checks against the real catalog and library.
   Small DOM double tests markup/handlers and storage safety, not browser layout. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const clone = value => JSON.parse(JSON.stringify(value));
const source = fs.readFileSync(path.join(__dirname, 'library.js'), 'utf8');
const catalog = JSON.parse(fs.readFileSync(path.join(__dirname, 'catalog.js'), 'utf8').split('=').slice(1).join('=').trim().replace(/;$/, ''));
const REVIEW_KEY = 'cfa-visual-review-v1';
const FAVORITES_KEY = 'cfa-visual-favorites-v1';
const EXPORT_KEY = 'cfa-visual-export-v1';
const byID = new Map(catalog.assets.map(a => [a.id, a]));

function boot(initialHash='#hon/all') {
  const elements = new Set(), nodes = new Map(), writes = [], scrolls = [];
  const marked = byID.get('HD-DROP-0d83180f0903');
  const storedReview = {id:marked.id, sha256:marked.sha256, status:'keep', note:'Keep the source look and my detail note.', workingReferenceScope:'detail'};
  const saved = {
    [REVIEW_KEY]:JSON.stringify({format:REVIEW_KEY, items:[storedReview]}),
    [FAVORITES_KEY]:JSON.stringify([marked.id]),
    [EXPORT_KEY]:JSON.stringify({format:EXPORT_KEY, items:[{id:marked.id,sha256:marked.sha256}]})
  };
  const storage = new Map(Object.entries(saved));
  const decode = value => value.replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>');
  const dataKey = name => name.replace(/^data-/, '').replace(/-([a-z])/g, (_, c) => c.toUpperCase());
  class Element {
    constructor(tag = 'div') {
      this.tag = tag; this.dataset = {}; this.attributes = {}; this.children = new Set();
      this.listeners = new Map(); this.classList = {toggle(){},add(){},remove(){},contains:name => (this.attributes.class || '').split(/\s+/).includes(name)};
      this.value = ''; this._html = ''; this.open = false; elements.add(this);
    }
    set innerHTML(html) {
      for (const child of this.children) {elements.delete(child); if (child.id) nodes.delete('#' + child.id);}
      this.children.clear(); this._html = html;
      for (const match of html.matchAll(/<([a-z][\w-]*)\b([^>]*)>/gi)) {
        const child = new Element(match[1]);
        for (const attribute of match[2].matchAll(/([\w-]+)="([^"]*)"/g)) child.setAttribute(attribute[1], decode(attribute[2]));
        child.disabled = /(?:^|\s)disabled(?:\s|$)/.test(match[2]);
        this.children.add(child);
      }
    }
    get innerHTML() {return this._html;}
    setAttribute(name, value) {
      this.attributes[name] = String(value);
      if (name.startsWith('data-')) this.dataset[dataKey(name)] = String(value);
      else if (name === 'id') {this.id = value; nodes.set('#' + value, this);}
      else this[name] = value;
    }
    addEventListener(name, callback) {if (!this.listeners.has(name)) this.listeners.set(name, []); this.listeners.get(name).push(callback);}
    click() {if (this.disabled) return; this.onclick?.({target:this}); for (const callback of this.listeners.get('click') || []) callback({target:this});}
    append(child) {this.children.add(child); if (child.id) nodes.set('#' + child.id, child);}
    querySelector() {return null;}
    querySelectorAll() {return [];}
    getBoundingClientRect() {return {top:100};}
    focus() {this.focused = true;}
    showModal() {this.open = true;}
    close() {this.open = false;}
    remove() {elements.delete(this);}
  }
  nodes.set('#app', new Element());
  const selectAll = selector => {
    const match = /^\[([\w-]+)(?:="([^"]*)")?\]$/.exec(selector);
    if (!match) return [];
    return [...elements].filter(e => Object.hasOwn(e.attributes, match[1]) && (match[2] === undefined || e.attributes[match[1]] === match[2]));
  };
  const document = {
    currentScript:{src:'file:///D:/Documents/CFA/docs/notes/explorable_world/comfy/projects/visual_library/library.js'},
    body:new Element('body'), createElement:tag => new Element(tag), addEventListener(){},
    querySelector(selector) {return nodes.get(selector) || selectAll(selector)[0] || null;}, querySelectorAll:selectAll
  };
  const location = {hash:initialHash};
  const window = {REVIEW_CATALOG:clone(catalog), REVIEW_INITIAL:{project:'hon',view:'all'}, addEventListener(){},scrollTo(){},scrollBy(value){scrolls.push(value);}};
  const context = {window,document,location,URL,Intl,console,
    setTimeout(){return 1;},clearTimeout(){},
    localStorage:{getItem:key => storage.get(key) ?? null,setItem(key,value){storage.set(key,value);writes.push([key,value]);}},
    sessionStorage:{getItem(){return null;},setItem(){}}
  };
  const instrumented = source.replace(/\}\)\(\);\s*$/, 'window.__collectionsTest={honTattooDefinitions,normalVisible,isArchived,getCurrentID(){return currentID;},exportReference,effectiveReferenceRole,referenceUsePolicy,route,renderMain,expandedCollections,collapsedBrowseBuckets,reviews,reviewRecord,reviewPayload,basketPayload,setState(p){Object.assign(state,p);},getState(){return state;}};})();');
  assert.notEqual(instrumented, source, 'Collection test hook attached');
  vm.runInNewContext(instrumented, context);
  return {
    api:window.__collectionsTest, C:window.REVIEW_CATALOG, location,writes,storage,scrolls,
    html:() => nodes.get('#main').innerHTML,
    toggle(id) {const target = selectAll('[data-collection-toggle]').find(e => e.dataset.collectionToggle === id);assert(target,'Inline toggle exists: '+id);target.click();},
    toggles:id => selectAll('[data-collection-toggle]').filter(e => e.dataset.collectionToggle === id),
    elements:selectAll,
    click(attribute,id) {const target=selectAll('['+attribute+']').find(e => e.attributes[attribute]===id); assert(target,'Toggle exists: '+attribute+'='+id); target.click();}
  };
}

const page=boot('#hon/details'),api=page.api;
const stable=value=>{const p=clone(value);delete p.exported;return p;};
const before={assets:clone(page.C.assets),albums:clone(page.C.albums),reviews:stable(api.reviewPayload()),basket:stable(api.basketPayload(true)),storage:Object.fromEntries(page.storage)};
const leaf=id=>page.html().includes('data-open="'+id+'"');
const groups=()=>[...page.html().matchAll(/data-collection="([^"]+)"/g)].map(m=>m[1]);
const visible=id=>api.normalVisible(page.C.assets.find(a=>a.id===id));
let checks=0;
assert.equal(api.getState().detailLayout,'all','fresh Hon details hash defaults to All references');
assert(page.html().includes('data-detail-layout="all" aria-pressed="true"'));
const keys=['ship','eye','know','blaster','leigh','scoundrel','optional-motifs'];
for(const key of keys)assert.equal(groups().filter(id=>id==='hon:tattoo-'+key).length,1,'one cover per tattoo: '+key);
assert(!page.html().includes('data-open="HD-DROP-a428b6f6fa65"'),'references begin collapsed');checks++;

const definitions=api.honTattooDefinitions();
for(const g of definitions){
 const hashes=g.assetIDs.map(id=>byID.get(id).sha256||id);assert.equal(new Set(hashes).size,hashes.length,'unique bytes per subject: '+g.id);
 assert(!g.assetIDs.some(id=>!visible(id)),'removed/archived files not resurfaced');
 assert.equal(g.sections[0].title,'Artwork / stencil');
 assert(g.sections.findIndex(s=>s.title==='Placement and mannequin guide')<g.sections.findIndex(s=>s.title==='Body appearances'));
 assert.deepEqual([...new Set(g.sections.flatMap(section=>section.assetIDs))].sort(),[...g.assetIDs].sort(),'every reference assigned once');
 assert.equal(g.sections.flatMap(section=>section.assetIDs).length,g.assetIDs.length,'no reference repeated between sections');
}
checks++;
page.toggle('hon:tattoo-ship');
const ship=definitions.find(g=>g.tattooKey==='ship');
for(const id of ship.assetIDs)assert(leaf(id),'all ship references remain accessible: '+id);
for(const id of ['HD-DROP-a428b6f6fa65','HD-DROP-ef58d546cccd','HD-RETURN-891a3ee224eb','HD-RETURN-d430b5f72e9b'])if(visible(id))assert(leaf(id),'previously missing ship resources are reachable');
assert(!leaf('HD-RETURN-9f62f9733312'),'user-archived duplicate stays archived');
const start=page.html().indexOf('<div class="tattoo-reference-overview">'),art=page.html().indexOf('<h3>Artwork / stencil</h3>'),guide=page.html().indexOf('<h3>Placement and mannequin guide</h3>'),legacy=page.html().indexOf('<h3>Legacy placement proof · revision needed</h3>'),body=page.html().indexOf('<h3>Body appearances</h3>');
assert(start>=0&&start<art&&art<guide&&guide<legacy&&legacy<body,'artwork, map and revision proof form the first row before body appearances');
const panel='id="collection-hon-tattoo-ship" class="collection-inline-views" >';
assert(page.html().includes(panel+'<div class="tattoo-reference-overview">'),'expanded tattoo begins with the image comparison row');
const provenance=page.html().indexOf('<summary>Reference notes and provenance</summary>');
assert(provenance>body,'provenance is deferred below the references');
assert(page.html().includes('grouping grants no approval'),'original provenance retained at the bottom');
const css=fs.readFileSync(path.join(__dirname,'library.css'),'utf8');
assert(css.includes('.tattoo-subject-collections .inline-collection.is-expanded>.collection-summary{max-width:none;display:grid;grid-template-columns:minmax(0,1fr) auto'));
assert(css.includes('.tattoo-subject-collections .inline-collection.is-expanded>.collection-summary .media-thumb{width:84px;height:76px'));
assert(css.includes('.tattoo-reference-overview{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,200px),1fr))'),'responsive side-by-side overview');

const guideIDs=ship.sections.find(s=>s.title==='Placement and mannequin guide').assetIDs;
if(guideIDs.length){for(const id of guideIDs)assert(leaf(id),'actual mapped guide browsable');}else assert(page.html().includes('Pending: no dedicated placement/mannequin guide'));
checks++;

// Existing subject bookmarks pull linked resources from their registered collections.
api.expandedCollections.clear();api.route('hon','details','hon:ship-tattoo');
assert.deepEqual(groups(),['hon:tattoo-ship']);page.toggle('hon:tattoo-ship');
for(const id of ship.assetIDs)assert(leaf(id),'Ship bookmark includes its cross-album reference: '+id);
assert.equal(page.location.hash,'hon/details/hon%3Aship-tattoo');checks++;

// Piercing references stay complete; grill bookmarks now expose just one image per design.
api.expandedCollections.clear();api.route('hon','details','hon:piercings');page.toggle('hon:piercings');
for(const id of catalog.albums.find(a=>a.id==='hon:piercings').assetIDs.filter(visible))assert(leaf(id),'retained piercing reference: '+id);
for(const [project,expected,bookmarks] of [
 ['hon',['HD-B-91ef00348229','HD-GRILLUP-40064d98db89'],['hon:grillz','hon:mouth-detail-updates','hon:grill-designs']],
 ['lisan',['LAG-cb183973ed1fc70e'],['lisan:optional-grill','lisan:mouth-grill-later-repairs','lisan:grill-designs']]
]){
 for(const albumID of bookmarks){
  api.expandedCollections.clear();api.route(project,'details',albumID);
  assert.deepEqual(groups(),[project+':grill-designs']);page.toggle(project+':grill-designs');
  const opened=[...page.html().matchAll(/data-open="([^"]+)"/g)].map(m=>m[1]);
  assert.deepEqual(opened,expected,'Only the selected design references are shown: '+albumID);
  assert.equal((page.html().match(/<img /g)||[]).length,expected.length,'Each design image appears once, including its cover');
  assert(!page.html().includes('No matching previews.'));
 }
 api.expandedCollections.clear();api.route(project,'working');
 const sourceAlbums=catalog.albums.filter(a=>a.project===project&&a.category==='details'&&(project==='hon'?['hon:grillz','hon:mouth-detail-updates'].includes(a.id):/mouth|grill/i.test(a.id)));
 for(const album of sourceAlbums){
  api.expandedCollections.clear();api.route(project,'working',album.id);
  if(!album.assetIDs.some(visible)){assert(!groups().includes(album.id),'Archive-only source album stays out of Working');continue;}
  assert(groups().includes(album.id),'Original mouth/grill bookmark remains reachable in Working: '+album.id);
  page.toggle(album.id);
  for(const id of album.assetIDs.filter(visible))assert(leaf(id),'Working retains candidate: '+id);
  page.toggle(album.id);
 }
}
api.expandedCollections.clear();api.route('lisan','details','lisan:mouth-natural-r2');
assert(!groups().includes('lisan:grill-designs'),'A natural-mouth bookmark must not show an iced grill');
assert(page.html().includes('href="#lisan/working/lisan%3Amouth-natural-r2"'),'Moved mouth bookmark links to its full Working collection');
api.route('lisan','working','lisan:mouth-natural-r2');
assert.deepEqual(groups(),['lisan:mouth-natural-r2']);page.toggle('lisan:mouth-natural-r2');
for(const id of catalog.albums.find(a=>a.id==='lisan:mouth-natural-r2').assetIDs.filter(visible))assert(leaf(id));
api.expandedCollections.clear();api.route('hon','details');
assert(page.html().includes('aria-label="Tattoos"')&&!page.html().includes('Hon Dolo tattoos')&&!page.html().includes('Supporting-cast tattoo options'),'One top-level tattoo section');
assert(!page.html().includes('Mixed placement proofs and source evidence')&&!page.html().includes('accessory-explorer'),'No detached source or duplicate character jewelry section');
const proofs={eye:['HD-RETURN-3fa3290e85db','HD-TATGUIDE-b6eb3258a6ae'],know:['HD-RETURN-3fa3290e85db','HD-TATGUIDE-b6eb3258a6ae'],scoundrel:['HD-TATGUIDE-1fd07b088244','HD-TATGUIDE-b6eb3258a6ae'],leigh:['HD-RETURN-831f6171619f','HD-RETURN-b8c9247bfe47']};
for(const [key,ids] of Object.entries(proofs)){
 const subject=api.honTattooDefinitions().find(g=>g.tattooKey===key);
 for(const id of ids.filter(visible))assert(subject.sections.find(s=>s.title===(id==='HD-TATGUIDE-b6eb3258a6ae'?'Legacy placement proof · revision needed':'Source sheets and artwork comparison evidence')).assetIDs.includes(id),key+'/'+id);
 page.toggle(subject.id);for(const id of ids.filter(visible))assert(leaf(id));page.toggle(subject.id);
}
// Eye's exact requested trio is first, clickable, and never repeated among later references.
page.toggle('hon:tattoo-eye');
const eye=api.honTattooDefinitions().find(g=>g.tattooKey==='eye'),eyeFirst=eye.sections.filter(s=>s.overview).flatMap(s=>s.assetIDs);
assert.deepEqual([...eyeFirst],['HD-TATGUIDE-91d44599bd8c','HD-LOCATION-EYE-20261012','HD-TATGUIDE-b6eb3258a6ae']);
for(const id of eyeFirst){
 assert.equal((page.html().match(new RegExp('data-open="'+id+'"','g'))||[]).length,1,'one visible item per top-row reference');
 page.click('data-open',id);assert.equal(api.getCurrentID(),id,'image button opens the exact reference');
}
assert(page.html().includes('Placement-only proof with recorded defects. Revision needed; not accepted'));
page.toggle('hon:tattoo-eye');
// The first row obeys current browser decisions without writing or changing source records.
const hiddenMap='HD-LOCATION-EYE-20261012',removedProof='HD-TATGUIDE-b6eb3258a6ae';
const priorOverrides=new Map([hiddenMap,removedProof].map(id=>[id,api.reviews.get(id)]));
api.reviews.set(hiddenMap,{...api.reviewRecord(hiddenMap),id:hiddenMap,sha256:byID.get(hiddenMap).sha256,collectionState:'archived'});
api.reviews.set(removedProof,{...api.reviewRecord(removedProof),id:removedProof,sha256:byID.get(removedProof).sha256,status:'remove'});
api.renderMain();page.toggle('hon:tattoo-eye');
assert(!leaf(hiddenMap)&&!leaf(removedProof),'archived map and removed proof leave the overview immediately');
assert(leaf('HD-TATGUIDE-91d44599bd8c'),'remaining artwork stays available');
for(const [id,prior] of priorOverrides)if(prior===undefined)api.reviews.delete(id);else api.reviews.set(id,prior);
api.expandedCollections.clear();api.renderMain();checks++;
assert(!groups().includes('hon:tattoo-source-history'),'earlier alternatives are absent from Details');
const oldIDs=['HD-RETURN-d55b97a3b322','HD-RETURN-78ad6c79615a','HD-RETURN-f88ff5ae511e','HD-TATGUIDE-b80e4d006917','HD-RETURN-d91685dd99cd','HD-TATGUIDE-d152270ab369','HD-TATGUIDE-ad54ba356e7c','HD-TATGUIDE-3046dd64faa8','HD-TATGUIDE-440a8cf5e911'];
for(const id of oldIDs)assert(!visible(id),'earlier option defaults to Archive: '+id);
api.route('hon','archive');page.toggle('hon:tattoo-source-history');
for(const id of oldIDs)assert(leaf(id),'earlier source remains reachable in Archive');
assert(!api.isArchived(page.C.assets.find(a=>a.id==='HD-TATGUIDE-b6eb3258a6ae')),'requested placement proof remains active');
api.expandedCollections.clear();api.route('hon','details');page.toggle('hon:piercings');
assert(page.html().includes('Piercings and jewelry')&&page.html().includes('Jewelry on display'));
for(const group of catalog.accessoryCollections.filter(g=>g.project==='hon'))for(const id of group.assetIDs.filter(visible))assert(leaf(id),'Jewelry examples moved inside the category');
page.toggle('hon:piercings');page.toggle('hon:return-detail-art');
assert(page.html().includes('>Guns</b>')&&leaf('HD-RETURN-41b93f64e7ea'),'Gun example retained under Guns');page.toggle('hon:return-detail-art');
for(const id of ['hon:face-neck-ink','hon:optional-finish'])assert(!groups().includes(id),'Redundant collection removed: '+id);
for(const album of catalog.albums.filter(a=>a.id.startsWith('hon:chewy-')&&a.id.endsWith('-setup'))){
 assert(!groups().includes(album.id),'Chewy setup is not a tattoo/piercing collection');
 for(const id of album.assetIDs)assert(!leaf(id),'Chewy setup does not leak into Details');
}
checks++;

// File search and tattoo subject search keep the correct cover/reference path.
api.route('hon','details');api.setState({search:byID.get('HD-DROP-a428b6f6fa65').filename});api.renderMain();
assert(groups().includes('hon:tattoo-ship'));page.toggle('hon:tattoo-ship');assert(leaf('HD-DROP-a428b6f6fa65'));assert(!leaf('HD-DROP-ef58d546cccd'));
api.expandedCollections.clear();api.setState({search:'Ship tattoo'});api.renderMain();assert(groups().includes('hon:tattoo-ship'));checks++;

// Approved/Archive retain the explicit standalone-artwork policy, never inferred from body approval.
api.setState({search:''});api.renderMain();page.click('data-detail-layout','approved');
assert.equal(api.getState().detailLayout,'approved');assert(!page.html().includes('data-collection="hon:tattoo-ship"'));
const approved=new Set(catalog.detailProfiles.filter(p=>p.project==='hon').flatMap(p=>(p.objects||[]).flatMap(o=>o.approvedArtworkAssetIDs||[])));
for(const m of page.html().matchAll(/data-artwork-id="([^"]+)"/g))assert(approved.has(m[1]),'only explicit approved drawing in Approved');
page.click('data-detail-layout','archive');assert.equal(api.getState().detailLayout,'archive');
for(const m of page.html().matchAll(/data-artwork-id="([^"]+)"/g))assert(!approved.has(m[1]),'Archive does not claim approved drawing');
page.click('data-detail-layout','all');assert(groups().includes('hon:tattoo-ship'));checks++;

// A location guide is a Detail reference even if an incompatible old dropdown choice exists.
const location=page.C.assets.find(a=>a.referenceRole==='Location guide only');assert(location,'real mapped placement guide exists');
const priorDefault=location.defaultReferenceScope,hadDefault=Object.hasOwn(location,'defaultReferenceScope');
// Exercise source metadata fallback without writing a catalog or review file.
location.defaultReferenceScope='detail';assert.equal(api.reviewRecord(location.id).workingReferenceScope,'detail');
let exported=api.exportReference(location);assert.equal(exported.referenceRole,'detail');assert.equal(exported.workingReferenceScope,'detail');
assert.equal(exported.referenceUsePolicy.defaultReferenceSelection.requiredRole,'detail');assert.equal(exported.referenceUsePolicy.imageDoesNotReplaceIdentity,true);
assert.equal(exported.referenceUsePolicy.explicitSceneReference,null);
const priorReview=api.reviews.get(location.id),hadReview=api.reviews.has(location.id);
api.reviews.set(location.id,{id:location.id,sha256:location.sha256,workingReferenceScope:'identity',workingReference:{status:'approved',scope:'identity'},note:'Preserve this explicit old review while keeping the source guide role narrow.'});
assert.equal(api.reviewRecord(location.id).workingReferenceScope,'identity','explicit review data retained');
assert.equal(api.exportReference(location).referenceRole,'detail','location diagram cannot become an actor identity reference');
if(hadReview)api.reviews.set(location.id,priorReview);else api.reviews.delete(location.id);
location.defaultReferenceScope='unrecognized';assert.equal(api.reviewRecord(location.id).workingReferenceScope,undefined,'invalid source default ignored');
if(hadDefault)location.defaultReferenceScope=priorDefault;else delete location.defaultReferenceScope;
checks++;

// Preferences are local session state; a fresh page returns to All, not the prior Approved screen.
const fresh=boot('#hon/details');assert.equal(fresh.api.getState().detailLayout,'all');checks++;
assert.deepEqual(clone(page.C.assets),before.assets);assert.deepEqual(clone(page.C.albums),before.albums);
assert.deepEqual(stable(api.reviewPayload()),before.reviews);assert.deepEqual(stable(api.basketPayload(true)),before.basket);
assert.deepEqual(Object.fromEntries(page.storage),before.storage);assert.equal(page.writes.length,0);
console.log(JSON.stringify({passed:true,checks,tattooCollections:definitions.length,shipReferences:ship.assetIDs.length,shipGuideAssets:guideIDs.length,reviewWrites:0,browserVisualQA:false}));
