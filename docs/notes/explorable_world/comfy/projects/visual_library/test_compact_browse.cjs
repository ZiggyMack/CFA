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

function boot() {
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
  const location = {hash:'#hon/all'};
  const window = {REVIEW_CATALOG:clone(catalog), REVIEW_INITIAL:{project:'hon',view:'all'}, addEventListener(){},scrollTo(){},scrollBy(value){scrolls.push(value);}};
  const context = {window,document,location,URL,Intl,console,
    setTimeout(){return 1;},clearTimeout(){},
    localStorage:{getItem:key => storage.get(key) ?? null,setItem(key,value){storage.set(key,value);writes.push([key,value]);}},
    sessionStorage:{getItem(){return null;},setItem(){}}
  };
  const instrumented = source.replace(/\}\)\(\);\s*$/, 'window.__collectionsTest={renderMain,expandedCollections,collapsedBrowseBuckets,reviews,reviewRecord,reviewPayload,basketPayload,setState(p){Object.assign(state,p);},getState(){return state;}};})();');
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

const page = boot(), api = page.api;
let checks = 0;
const initialReview = clone(api.reviewPayload()), initialBasket = clone(api.basketPayload(true));
const initialStorage = Object.fromEntries(page.storage);
const albumByID = new Map(catalog.albums.map(a => [a.id,a]));
const originalAssets = clone(catalog.assets);
const thumbURL = id => new URL(byID.get(id).thumb, 'file:///D:/Documents/CFA/docs/notes/explorable_world/comfy/projects/visual_library/').href;
const hasLeaf = id => page.html().includes('data-open="' + id + '"');
const active = a => a && !a.archived && api.reviewRecord(a.id).status !== 'remove';
const members = id => albumByID.get(id).assetIDs.map(id => byID.get(id)).filter(active);
function summary(id) {
  const start = page.html().indexOf('data-collection="' + id + '"');
  assert(start >= 0, 'Collection is rendered: ' + id);
  const panel = 'id="collection-' + id.replace(/[^a-z0-9_-]/gi, '-') + '"';
  const end = page.html().indexOf(panel, start);
  assert(end > start, 'Collection has its own inline panel: ' + id);
  return page.html().slice(start, end);
}
function expectCover(collectionID, assetID) {
  assert(summary(collectionID).includes(thumbURL(assetID)), 'Exact requested cover is used: ' + collectionID + ' / ' + assetID);
}
function toggleWithoutNavigation(id) {
  const before = page.location.hash;
  page.toggle(id);
  assert.equal(page.location.hash,before,'Expanding/collapsing stays on the current route: ' + id);
}
function reset() {
  api.setState({project:'hon',view:'all',album:'',search:''});
  api.expandedCollections.clear();api.collapsedBrowseBuckets.clear();api.renderMain();
}

// Cross-referenced tattoo albums must not reintroduce story shots as extra detail covers.
for(const id of ['hon:face-neck-ink','hon:ship-tattoo','hon:grillz']) {
  assert.equal(page.toggles(id).length,0,'Cross-referenced detail album does not duplicate already grouped subjects: '+id);
}
const openingGrin=catalog.assets.find(a=>a.project==='hon' && a.storyboardOrder===1);
assert.equal(page.html().split(thumbURL(openingGrin.id)).length-1,1,'SB-01 has one exact thumbnail on the initial page, as its storyboard section cover');
const icedGrill='HD-DROP-defe480b085f';
assert(catalog.sharedReferenceCollections.some(g=>(g.assetIDs||[]).includes(icedGrill)),'The dedicated grill detail remains in its shared reference group');
checks++;

// Six story sections become covers. Ordered shot cards remain one click away.
const storyAlbums = catalog.albums.filter(a => a.project === 'hon' && a.category === 'storyboard' && a.id !== 'hon:story-quarters-grill-change');
assert.equal(storyAlbums.length,6,'Six original story sections remain');
const storyCovers = {'hon:story-ship':16,'hon:story-turn':23,'hon:story-love':30,'hon:story-outro':36};
for (const [id,number] of Object.entries(storyCovers)) expectCover(id,catalog.assets.find(a => a.project === 'hon' && a.storyboardOrder === number).id);
for (const al of storyAlbums) {
  const assets = members(al.id).filter(a => a.storyboardOrder);
  assert(page.toggles(al.id).length,'Each story section has an inline control: ' + al.id);
  for (const a of assets) assert(!hasLeaf(a.id),'Story shots do not flood the initial page: ' + a.title);
  toggleWithoutNavigation(al.id);
  const actual = [...page.html().matchAll(/data-open="([^"]+)"/g)].map(m=>byID.get(m[1])).filter(a=>a && a.album===al.id).map(a=>a.storyboardOrder);
  assert.deepEqual(actual,assets.map(a=>a.storyboardOrder).sort((a,b)=>a-b),'Expanded shots use numeric SB order: ' + al.id);
  toggleWithoutNavigation(al.id);
  for (const a of assets) assert(!hasLeaf(a.id),'Collapsed story hides its children again: ' + a.title);
}
checks++;

// Cover choices are clip-specific, independent of longest/shortest sort preferences.
const videoCovers = {
  'hon:video-action':'GEM-92C65823',
  'hon:video-performance':'GEM-2E6EF86C',
  'hon:video-dinner':'GEM-58328BF1',
  'hon:video-cockpit':'GEM-80AAE2E2'
};
for (const [id,cover] of Object.entries(videoCovers)) {
  expectCover(id,cover);
  for (const a of members(id)) assert(!hasLeaf(a.id),'Video children begin collapsed: ' + a.title);
  toggleWithoutNavigation(id);
  for (const a of members(id)) assert(hasLeaf(a.id),'Every original clip remains accessible inline: ' + a.title);
  toggleWithoutNavigation(id);
}
api.setState({videoSort:'shortest'});api.renderMain();
for (const [id,cover] of Object.entries(videoCovers)) expectCover(id,cover);
api.setState({videoSort:'longest'});api.renderMain();
checks++;

// Experiments, turnarounds and source likenesses sit under one Comfy parent.
expectCover('hon:comfy-workspace','HD-COMFY-MOTION-V001');
const comfyChildren = ['hon:video-comfy_experiments','hon:video-turnaround','hon:comfy-likeness-HON-DOLO','hon:source-group-photo'];
for (const id of comfyChildren) {
  assert.equal(page.toggles(id).length,0,'No separate top-level Comfy album: ' + id);
  for (const a of members(id)) assert(!hasLeaf(a.id),'Comfy leaf remains inside its parent: ' + a.title);
}
toggleWithoutNavigation('hon:comfy-workspace');
for (const id of comfyChildren) {
  assert(page.toggles(id).length,'Nested Comfy album is present: ' + id);
  for (const a of members(id)) assert(!hasLeaf(a.id),'Opening parent only reveals child covers: ' + a.title);
  toggleWithoutNavigation(id);
  for (const a of members(id)) assert(hasLeaf(a.id),'Comfy child preserves all references: ' + a.title);
  toggleWithoutNavigation(id);
}
toggleWithoutNavigation('hon:comfy-workspace');
checks++;

// A scoped removal must not be undone by a cover choice; fall back without losing notes.
const selected = 'GEM-92C65823', hadReview = api.reviews.has(selected), savedReview = api.reviews.get(selected), effectiveReview = clone(api.reviewRecord(selected));
api.reviews.set(selected,{...effectiveReview,status:'remove',note:'Keep this note while hiding the cover.'});api.renderMain();
assert(!summary('hon:video-action').includes(thumbURL(selected)),'Removed requested cover falls back to an available clip');
toggleWithoutNavigation('hon:video-action');assert(!hasLeaf(selected),'Removed clip stays absent from expanded collection');
assert.equal(api.reviewRecord(selected).note,'Keep this note while hiding the cover.');
if(hadReview)api.reviews.set(selected,savedReview);else api.reviews.delete(selected);reset();
checks++;

// A matched scene is reachable in its parent, with original route and no globally false empty state.
api.setState({search:'Beat the Maw'});api.renderMain();
assert(page.toggles('hon:story-ship').length,'Search finds the containing story section');
assert(!page.html().includes('No matching previews.'),'Matched section does not produce a contradictory empty message');
toggleWithoutNavigation('hon:story-ship');
const maw = catalog.assets.find(a=>a.title==='SB-16 · Beat the Maw');assert(hasLeaf(maw.id),'Matching scene is reachable inline');
reset();checks++;

// Tattoo collections and process/history checks follow once the corresponding data is built.
const tattooGroups = catalog.detailDisplayGroups.filter(g=>g.project==='hon' && ['stencils','skin'].includes(g.bucket));
assert(tattooGroups.some(g=>g.bucket==='stencils') && tattooGroups.some(g=>g.bucket==='skin'),'Both visual tattoo groupings are built');
expectCover('hon:detail-blaster-art','HD-RETURN-c91af37e775d');
for(const group of tattooGroups) {
  expectCover(group.id,group.coverAssetID);
  const items=group.assetIDs.map(id=>byID.get(id)).filter(active);
  for(const a of items) assert(!hasLeaf(a.id),'Tattoo component files do not repeat as top-level previews: '+a.title);
  toggleWithoutNavigation(group.id);
  for(const a of items) assert(hasLeaf(a.id),'Artwork/placement alternatives stay available inside their design: '+a.title);
  toggleWithoutNavigation(group.id);
}
for(const bucket of ['stencils','skin']) {
  const groups=tattooGroups.filter(g=>g.bucket===bucket),other=tattooGroups.filter(g=>g.bucket!==bucket),hash=page.location.hash;
  page.click('data-browse-bucket','hon:tattoo-'+bucket);
  for(const g of groups) assert.equal(page.toggles(g.id).length,0,'Hiding tattoo bucket removes its covers: '+g.id);
  for(const g of other) assert(page.toggles(g.id).length,'Independent tattoo bucket remains available: '+g.id);
  assert.equal(page.location.hash,hash,'Tattoo bucket toggles stay inline');
  page.click('data-browse-bucket','hon:tattoo-'+bucket);
  for(const g of groups) assert(page.toggles(g.id).length,'Showing tattoo bucket restores its covers: '+g.id);
}
checks++;

// Rejections remain discoverable at the lowest level, without pushing failed images onto covers.
const archiveAlbums=['hon:mouth-b-archive','hon:return-rejected-attempts','hon:image-benchmark-review','hon:return-recovery-review'];
const rejectedIDs=catalog.assets.filter(a=>a.project==='hon' && /reject/i.test(a.filename||'')).map(a=>a.id);
for(const id of rejectedIDs) assert(!hasLeaf(id),'No rejected leaf on the initial page: '+id);
for(const id of archiveAlbums) assert.equal(page.toggles(id).length,0,'Batch/history album is not a top-level collection: '+id);
assert(page.toggles('hon:process-history').length,'One process/history entrance exists');
toggleWithoutNavigation('hon:process-history');
for(const parent of ['hon:rejects','hon:source-history']) {
  assert(page.toggles(parent).length,'History has clear nested branches: '+parent);
  assert(!summary(parent).includes('<img'),'History parent is a text bucket rather than a rejected-image cover');
}
for(const id of rejectedIDs) assert(!hasLeaf(id),'Opening process bucket does not immediately expose rejected images: '+id);
toggleWithoutNavigation('hon:rejects');
for(const id of ['hon:mouth-b-archive','hon:return-rejected-attempts']) {
  assert(page.toggles(id).length,'Each rejected batch remains reachable: '+id);
  assert(!summary(id).includes('<img'),'Rejected batch is still a text cover: '+id);
  toggleWithoutNavigation(id);
  for(const assetID of albumByID.get(id).assetIDs) assert(hasLeaf(assetID),'Rejected and archived originals remain inspectable: '+assetID);
  toggleWithoutNavigation(id);
}
toggleWithoutNavigation('hon:rejects');
toggleWithoutNavigation('hon:source-history');
for(const id of ['hon:image-benchmark-review','hon:return-recovery-review']) {
  assert(page.toggles(id).length,'Recovery/benchmark provenance remains accessible: '+id);
  assert(!summary(id).includes('<img'),'Recovery batch no longer duplicates subject previews on its cover');
  toggleWithoutNavigation(id);
  for(const assetID of albumByID.get(id).assetIDs) assert(hasLeaf(assetID),'Source history keeps originals and review identity: '+assetID);
  toggleWithoutNavigation(id);
}
reset();checks++;

// Browsing must never rewrite image identities or the user’s review/selection state.
const finalReview=clone(api.reviewPayload()), finalBasket=clone(api.basketPayload(true));
delete initialReview.exported;delete finalReview.exported;delete initialBasket.exported;delete finalBasket.exported;
assert.deepEqual(finalReview,initialReview,'Browsing preserves review decisions, notes, scopes, favorites and export selections');
assert.deepEqual(finalBasket,initialBasket,'Browsing preserves the exact export selection');
assert.deepEqual(Object.fromEntries(page.storage),initialStorage,'No local saved record was overwritten');
assert.equal(page.writes.length,0,'Pure browsing performs no storage writes');
assert.deepEqual(clone(page.C.assets),originalAssets,'Display regrouping leaves original asset metadata and hashes untouched');
checks++;
console.log(JSON.stringify({passed:true,checks,storySections:storyAlbums.length,requestedStoryCovers:Object.keys(storyCovers).length,videoCovers:Object.keys(videoCovers).length+1,tattooGroups:tattooGroups.length,archiveAlbums:archiveAlbums.length,browserVisualQA:false}));
