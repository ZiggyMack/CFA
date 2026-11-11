/* Head variants, purpose filters, story provenance and tattoo/video presentation.
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
const assetsBefore=clone(page.C.assets),albumsBefore=clone(page.C.albums),bomBefore=clone(page.C.characterBOM||page.C.characterBOMs||null);
const stablePayload=value=>{const payload=clone(value);delete payload.exported;return payload;};
const reviewsBefore=stablePayload(api.reviewPayload()),basketBefore=stablePayload(api.basketPayload(true)),storageBefore=Object.fromEntries(page.storage);
let checks=0;
const hasLeaf=id=>page.html().includes('data-open="'+id+'"');
const groups=()=>[...page.html().matchAll(/data-collection="([^"]+)"/g)].map(m=>m[1]);
function state(p){api.expandedCollections.clear();api.setState({project:'hon',view:'all',album:'',search:'',storyStart:0,storyEnd:100,storyStage:'all',storyTheme:'all',allPurpose:'all',...p});api.renderMain();}

// Distinct mouths share one neutral preview; every original file remains inside.
const head='hon:head-anchor-b-candidates',heads=catalog.albums.find(a=>a.id===head).assetIDs;
assert.equal(heads.length,3);assert.equal(new Set(heads.map(id=>byID.get(id).sha256)).size,3);
state({view:'comfy',album:head});
assert.deepEqual(groups(),[head]);assert(page.html().includes('3 mouth/piercing variants'));
assert(!page.html().includes('not a canonical or accepted head')); // explanation stays inside drawer
assert.equal((page.html().match(/<img /g)||[]).length,1,'one collapsed cover');
for(const id of heads)assert(!hasLeaf(id),'variants start collapsed');
const route=page.location.hash;page.toggle(head);assert.equal(page.location.hash,route);
for(const id of heads)assert(hasLeaf(id),'all mouth versions remain available');
assert(page.html().includes('not a canonical or accepted head'));checks++;
state({view:'comfy',album:head,search:byID.get(heads[1]).filename});page.toggle(head);
assert(hasLeaf(heads[1]));assert(!hasLeaf(heads[0]));assert(!hasLeaf(heads[2]));checks++;

// Purpose chips hide unrelated sections and leave BOM expansion available.
state({view:'all'});assert(page.html().includes('data-purpose="all"'));
const chipNames=page.elements('[data-all-purpose]').map(e=>e.dataset.allPurpose);
for(const name of ['outfits','details','cast','storyboard','videos','comfy','inspiration','documents'])assert(chipNames.includes(name));
assert(!chipNames.includes('working'),'The detailed working BOM has its own workspace');
state({view:'working'});assert(!page.html().includes('data-outfit-collection='));
assert(page.html().includes('data-collection="hon:character-bom"'));assert(!page.html().includes('class="cast-explorer"'));
const bomGroup=groups()[0];assert(bomGroup);page.toggle(bomGroup);assert(page.html().includes('Verbose BOM'));checks++;
state({view:'all'});page.click('data-all-purpose','outfits');assert(page.html().includes('data-outfit-collection='));assert(!page.html().includes('class="working-bom"'));checks++;
page.click('data-all-purpose','details');assert(page.html().includes('Tattoo stencils'));assert(!page.html().includes('data-outfit-collection='));checks++;
page.click('data-all-purpose','documents');assert(!page.html().includes('data-collection="'));assert(page.html().includes('document'));checks++;
const css=fs.readFileSync(path.join(__dirname,'library.css'),'utf8');assert(css.includes('.all-files-workspace .working-bom>.collection-catalog{grid-template-columns:repeat(auto-fill,minmax(220px,1fr))}'));

// SB numeric order remains inside six original source collections.
state({view:'storyboard'});
const sbAlbums=catalog.albums.filter(a=>a.project==='hon'&&a.category==='storyboard'&&a.assetIDs.some(id=>byID.get(id)?.storyboardOrder));
assert.equal(sbAlbums.length,6);for(const al of sbAlbums)assert(groups().includes(al.id));
const falcon=catalog.assets.filter(a=>a.project==='hon'&&/^HON-FALCON-/.test(a.sourceIntake||''));assert(falcon.length>=50);
assert(groups().includes('hon:falcon-reference-exploration'));assert(page.html().includes('Claude directed the scene/category concepts')===false,'provenance is inside drawer');
page.toggle('hon:falcon-reference-exploration');assert(page.html().includes('Claude directed the scene/category concepts'));
assert(page.html().includes('not narrative chapters'));const categoryCount=new Set(falcon.map(a=>a.providerCategory)).size;
assert.equal(groups().filter(id=>/^hon:falcon-reference-c\d+$/.test(id)).length,categoryCount);
page.toggle('hon:falcon-reference-c01');const c01=falcon.filter(a=>a.providerCategory.startsWith('C01-')&&!a.archived&&api.reviewRecord(a.id).status!=='remove');
for(const a of c01)assert(hasLeaf(a.id));checks++;
api.setState({storyStart:25,storyEnd:50});api.renderMain();for(const a of c01)assert(hasLeaf(a.id),'source-panel range does not drop untimed candidates');checks++;
const sourceAlbum=sbAlbums[0];state({view:'storyboard',album:sourceAlbum.id});page.toggle(sourceAlbum.id);
const sourceIDs=[...page.html().matchAll(/data-open="([^"]+)"/g)].map(m=>byID.get(m[1])).filter(a=>a?.storyboardOrder).map(a=>a.storyboardOrder);
assert.deepEqual(sourceIDs,[...sourceIDs].sort((a,b)=>a-b));assert(!groups().includes('hon:falcon-reference-exploration'));checks++;
const falconAlbum=catalog.albums.find(a=>a.id==='hon:falcon-group1-c01');state({view:'storyboard',album:falconAlbum.id});page.toggle(falconAlbum.id);page.toggle('hon:falcon-reference-c01');
for(const id of falconAlbum.assetIDs.filter(id=>!byID.get(id).archived&&api.reviewRecord(id).status!=='remove'))assert(hasLeaf(id));assert(!page.html().includes('id="story-start"'));
assert(!hasLeaf(falcon.find(a=>a.providerCategory.startsWith('C02-')).id));checks++;
// The selected Grill Up reference/history remain separate from its ten panels.
const grillSequenceID='HON-QUARTERS-GRILL-CHANGE-20261009',grillStory=catalog.storyboardStories.find(s=>s.sequenceID===grillSequenceID);assert(grillStory);
state({view:'storyboard'});assert(page.html().includes('data-story-card="'+grillStory.id+'"'),'Independent Grill Up story is available from the song landing');
assert(!page.html().includes('id="shot-work-'+grillSequenceID+'"'),'Independent planning is not inserted into the song');
state({view:'storyboard',album:'story:'+grillStory.id});assert(groups().includes(grillSequenceID),'Selected Grill Up story preserves reference/history collection');
assert(page.html().includes('id="shot-work-'+grillSequenceID+'"'),'Selected Grill Up story preserves its existing planning card');
assert(page.html().includes('data-scene-id="'+grillSequenceID+'"'),'Scene readiness remains reachable');

// Tattoo All references combines artwork and body evidence without approval changes.
state({view:'details',detailLayout:'all'});
for(const key of ['ship','eye','know','blaster','leigh','scoundrel','optional-motifs'])assert(groups().includes('hon:tattoo-'+key));
assert(page.html().includes('One collection per tattoo'));assert(!page.html().includes('class="working-bom"'));
page.toggle('hon:tattoo-eye');for(const title of ['Artwork / stencil','Placement and mannequin guide','Body appearances'])assert(page.html().includes(title),'Tattoo workspace retains '+title);checks++;

// Video grouping uses real album purpose, retaining existing four design stages.
state({view:'videos',videoLayout:'grouped'});
assert(page.html().includes('Scene and performance attempts'));assert(page.html().includes('Exploratory tests and turnarounds'));
assert(groups().includes('hon:video-action'));assert(groups().includes('hon:video-turnaround'));
page.toggle('hon:video-action');for(const id of catalog.albums.find(a=>a.id==='hon:video-action').assetIDs.filter(id=>byID.get(id)?.kind==='video'&&!byID.get(id).archived&&api.reviewRecord(id).status!=='remove'))assert(hasLeaf(id));checks++;

assert.deepEqual(clone(page.C.assets),assetsBefore,'catalog assets unchanged');
assert.deepEqual(clone(page.C.albums),albumsBefore,'source albums and counts unchanged');
assert.deepEqual(clone(page.C.characterBOM||page.C.characterBOMs||null),bomBefore,'BOM unchanged');
assert.deepEqual(stablePayload(api.reviewPayload()),reviewsBefore,'no review decisions altered');
assert.deepEqual(stablePayload(api.basketPayload(true)),basketBefore,'no export selections altered');
assert.deepEqual(Object.fromEntries(page.storage),storageBefore,'browse actions do not write review storage');
assert.equal(page.writes.length,0);
console.log(JSON.stringify({passed:true,checks,headVariants:heads.length,FalconDrafts:falcon.length,sourceStoryPanels:36,reviewWrites:0,browserVisualQA:false}));
