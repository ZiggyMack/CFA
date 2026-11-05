/* Real-library collection navigation regression check with a small DOM double.
   This verifies rendered markup and the bound handlers, not browser layout. */
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
  const instrumented = source.replace(/\}\)\(\);\s*$/, 'window.__collectionsTest={normalVisible,collectionCards,collectionGroups,sharedCharacterReferences,castExplorer,castHubGroups,castWorkingGroups,parseHash,detailAlbumGroups,renderMain,expandedCollections,reviews,reviewRecord,reviewPayload,basketPayload,setState(p){Object.assign(state,p);},getState(){return state;}};})();');
  assert.notEqual(instrumented, source, 'Collection test hook attached');
  vm.runInNewContext(instrumented, context);
  return {
    api:window.__collectionsTest, C:window.REVIEW_CATALOG, location,writes,storage,scrolls,
    html:() => nodes.get('#main').innerHTML,
    toggle(id) {const target = selectAll('[data-collection-toggle]').find(e => e.dataset.collectionToggle === id);assert(target,'Inline toggle exists: '+id);target.click();},
    toggles:id => selectAll('[data-collection-toggle]').filter(e => e.dataset.collectionToggle === id)
  };
}

const page = boot(), api = page.api;
function expectCollapsed(id) {
  const panel='collection-'+id.replace(/[^a-z0-9_-]/gi,'-');
  assert(page.html().includes('<div id="'+panel+'" class="collection-inline-views" hidden></div>'),'Collapsed panel is hidden and empty: '+id);
  const toggles=page.toggles(id);assert(toggles.length,'Collapsed collection has controls: '+id);
  for(const toggle of toggles)assert.equal(toggle.attributes['aria-expanded'],'false','Controls report collapsed: '+id);
}
let checks = 0;
page.location.hash='#hon/working';api.parseHash();api.renderMain();
expectCollapsed('hon:character-bom');
const workingHash=page.location.hash;page.toggle('hon:character-bom');
assert.equal(page.location.hash,workingHash,'Dolo cover expands inline without changing the route');
assert(page.html().includes('<h3>Body art</h3>')&&page.html().includes('<h3>Bling bling</h3>')&&page.html().includes('aria-label="Verbose BOM"'),'Dolo cover handler opens its nested BOM');
page.toggle('hon:character-bom');expectCollapsed('hon:character-bom');
page.location.hash='#hon/all';api.parseHash();api.renderMain();
checks++;

const initialReview = clone(api.reviewPayload().items), initialStorage = Object.fromEntries(page.storage);
const expectedCovers = {
  'hon:cast-enforcer':'HD-DROP-0d83180f0903',
  'hon:cast-ivory':'HD-DROP-5171bb20c773',
  'hon:cast-dj':'HD-DROP-ca406436d384',
  'hon:cast-hooded':'HD-DROP-be1c0a142301',
  'hon:cast-hippo':'HD-DROP-e8d54a7bd4cf',
  'hon:cast-gecko':'HD-DROP-b4a5874b195e'
};
assert(Array.isArray(catalog.castCollections) && catalog.castCollections.length, 'Built cast grouping data is present');
assert(Array.isArray(catalog.detailDisplayGroups) && catalog.detailDisplayGroups.length >= 3, 'Built motif grouping data is present');
assert(Array.isArray(catalog.sharedReferenceCollections) && catalog.sharedReferenceCollections.length, 'Built shared-reference grouping data is present');
const media = () => page.C.assets.filter(a => a.project === 'hon' && a.kind === 'image' && !a.archived);
const renderCollection = definition => api.collectionCards(api.collectionGroups([definition], media()));

for (const [id, cover] of Object.entries(expectedCovers)) {
  const definition = catalog.castCollections.find(g => g.id === id);
  assert(definition, 'Requested cast collection exists: ' + id);
  assert.equal(definition.coverID || definition.coverAssetID, cover, 'User-selected cover remains exact: ' + id);
  const html = renderCollection(definition);
  const expectedURL = new URL(byID.get(cover).thumb, 'file:///D:/Documents/CFA/docs/notes/explorable_world/comfy/projects/visual_library/').href;
  assert(html.includes(expectedURL), 'The selected image is rendered on the collapsed cover: ' + id);
  assert(page.toggles(id).length >= 1, 'Cast collection is reachable from All files: ' + id);
}
checks++;

for (const [id, historicalID] of [['hon:cast-ivory','LEIA-STYLE-01'],['hon:cast-enforcer','VADER-ARMOR-01'],['hon:cast-dj','CHEW-STYLE-01']]) {
  const definition = catalog.castCollections.find(g => g.id === id);
  assert(definition.historyIDs.includes(historicalID), 'Earlier study retains its character membership');
  assert(!page.html().includes('data-open="' + historicalID + '"'), 'Design history stays outside the ordinary All files gallery');
  const hash = page.location.hash;
  page.toggle(id);
  assert.equal(page.location.hash, hash, 'Clicking the character cover keeps the current page/hash');
  assert(!page.html().includes('data-open="' + historicalID + '"'), 'Supporting hub does not expose design setup/history as scene appearances');
  assert(page.html().includes('#hon/working/' + encodeURIComponent(id)), 'Character hub links to its Working reference collection');
  page.toggle(id);
  page.location.hash = '#hon/working/' + encodeURIComponent(id);
  api.parseHash();api.renderMain();
  const working = api.castWorkingGroups(id)[0];
  assert(!working.items.some(a => a.id === historicalID), 'Explicitly historical study is no longer in Working references');
  page.toggle(id + '-working');
  assert(!page.html().includes('data-open="' + historicalID + '"'), 'Working expansion does not resurface archived history');
  page.toggle(id + '-working');
  page.location.hash = '#hon/archive';api.parseHash();api.renderMain();
  assert(page.html().includes('data-open="' + historicalID + '"'), 'Archive preserves the exact historical image');
  page.location.hash = '#hon/all';api.parseHash();api.renderMain();
}
for (const id of ['hon:cast-existing-LEIA','hon:cast-existing-VADER-GENERAL','hon:cast-existing-CHEWBACCA']) {
  assert.equal(page.toggles(id).length, 0, 'No second character card for earlier studies: ' + id);
  assert(!page.html().includes('data-album="' + id + '"'), 'No leftover standalone earlier-studies album link');
}
checks++;

const chain = byID.get('HD-B-708df0bb5bff');
assert(chain && /VIS-HD-47_CHAIN-BITE/.test(chain.filename), 'The real received chain-bite macro is retained');
const mouth = catalog.sharedReferenceCollections.find(g => (g.assetIDs || []).includes(chain.id));
assert(mouth, 'Chain bite belongs to a shared mouth collection');
expectCollapsed(mouth.id);
assert(!page.html().includes('class="media-open" data-open="' + chain.id + '"'), 'Individual mouth views start collapsed');
let hash = page.location.hash;
page.toggle(mouth.id);
assert.equal(page.location.hash, hash, 'Opening shared mouths is an inline action');
assert(page.html().includes('class="media-open" data-open="' + chain.id + '"'), 'Chain-bite macro is visible inside the expanded mouth collection');
for (const id of mouth.assetIDs.filter(id => api.normalVisible(byID.get(id)))) {
  assert(page.html().includes('class="media-open" data-open="' + id + '"'), 'Every received mouth member remains reachable: ' + id);
}
page.toggle(mouth.id);
expectCollapsed(mouth.id);
checks++;

const detailMembers = new Set();
const originalMotifIDs = new Set(['hon:detail-hourglass-coins','hon:detail-crowned-scales','hon:detail-serpent-coin']);
for (const group of catalog.detailDisplayGroups.filter(g => originalMotifIDs.has(g.id))) {
  assert(group.assetIDs.includes(group.coverAssetID), 'Motif cover is a real group member');
  assert.equal(group.assetIDs.length, 3, 'Motif retains RGB, transparent format and option sheet');
  group.assetIDs.forEach(id => {assert(!detailMembers.has(id), 'Motif groups have disjoint members');detailMembers.add(id);});
  assert(page.toggles(group.id).length >= 1, 'One expandable motif entry replaces its flat files');
  for (const id of group.assetIDs) assert(!page.html().includes('data-open="' + id + '"'), 'Artwork files are initially nested, not duplicate standalone cards');
  page.toggle(group.id);
  for (const id of group.assetIDs) assert(page.html().includes('data-open="' + id + '"'), 'Format and true design alternatives remain reachable: ' + id);
  page.toggle(group.id);
}
assert.equal(detailMembers.size, 9);
checks++;

const armor = catalog.castCollections.find(g => g.id === 'hon:cast-enforcer'), coverID = armor.coverID;
const oldReview = api.reviews.get(coverID);
api.reviews.set(coverID, {...api.reviewRecord(coverID), status:'remove'});
api.expandedCollections.add(armor.id);
const availableReplacementID = armor.currentIDs.find(id => id !== coverID && byID.has(id) && !byID.get(id).archived && api.reviewRecord(id).status !== 'remove');
assert(availableReplacementID, 'A surviving current design view is available for the one-cover fallback');
const filteredArmorHub = api.castHubGroups(armor.id)[0];
assert(filteredArmorHub, 'Removing the representative does not remove the entire character hub');
assert.equal(filteredArmorHub.cover.id, availableReplacementID, 'Actual cast hub uses one surviving current design cover');
let html = api.collectionCards([filteredArmorHub]);
assert(html.includes('data-collection="' + armor.id + '"'), 'Actual Supporting cast collection remains reachable');
assert(!html.includes('data-open="' + coverID + '"'), 'Marked-for-removal representative is omitted from actual hub views');
assert(!html.includes(new URL(byID.get(coverID).thumb, 'file:///D:/Documents/CFA/docs/notes/explorable_world/comfy/projects/visual_library/').href), 'Removed image is not used as the fallback cover');
assert.equal(api.reviewRecord(coverID).note, oldReview.note, 'Filtering preserves review notes');
api.reviews.set(coverID, oldReview);
api.expandedCollections.delete(armor.id);
const archivalCandidate = page.C.assets.find(a => a.id === armor.assetIDs.find(id => id !== coverID));
const wasArchived = archivalCandidate.archived;
archivalCandidate.archived = true;
api.expandedCollections.add(armor.id);
assert(!api.castWorkingGroups(armor.id)[0].items.some(a => a.id === archivalCandidate.id), 'Archived design/setup media does not reappear inside Working');
if (wasArchived === undefined) delete archivalCandidate.archived; else archivalCandidate.archived = wasArchived;
api.expandedCollections.delete(armor.id);
checks++;

api.setState({search:'chain bite'});api.renderMain();
if (!page.html().includes('class="media-open" data-open="' + chain.id + '"')) page.toggle(mouth.id);
assert(page.html().includes('class="media-open" data-open="' + chain.id + '"'), 'Search exposes the matching mouth view without changing routes');
assert.equal(page.location.hash, '#hon/all');
api.setState({search:''});api.expandedCollections.clear();api.renderMain();
checks++;

api.setState({search:'Chewy'});api.renderMain();
assert(page.toggles('hon:cast-dj').length >= 1, 'A new character alias finds the collection despite older filenames');
assert(!page.html().includes('No matching previews.'), 'Matching alias collection does not show a contradictory global empty state');
page.toggle('hon:cast-dj');
assert(page.html().includes('data-open="HD-DROP-ca406436d384"'), 'Alias search expands to the user-selected DJ portrait');
api.setState({search:''});api.expandedCollections.clear();api.renderMain();
const jewelry = page.C.assets.find(a => a.id === 'HD-DROP-b18c4a123579');
assert(jewelry?.componentApprovals?.length, 'Permanent jewelry retains its recorded scoped approval');
assert.equal(jewelry.componentApprovals[0].scope, 'visible_jewelry_only');
assert.equal(jewelry.componentApprovals[0].acceptsFullLook, false, 'Jewelry selection does not approve the whole look');
checks++;

const sequence = catalog.storyboardSequences.find(s => s.id === 'HON-QUARTERS-GRILL-CHANGE-20261009');
assert(sequence, 'Received Grill Up draft has one standalone sequence');
assert.equal(sequence.sections[0].assetIDs.length, 10, 'Ten selected panels retain their source order');
assert.equal(sequence.sections.find(s => s.history).assetIDs.length, 8, 'Eight alternatives remain nested history');
assert.equal(sequence.assetIDs.length, 19, 'The r4 look anchor stays with the same scene');
assert(page.toggles(sequence.id).length >= 1, 'All files exposes one expandable scene collection');
page.toggle(sequence.id);
for (const id of sequence.assetIDs) assert(page.html().includes('data-open="' + id + '"'), 'Every scene original is reachable inline: ' + id);
assert(page.html().includes('Earlier alternatives · history'), 'Alternatives are explicitly history');
page.toggle(sequence.id);
checks++;

const mainPanels = catalog.assets.filter(a => a.project === 'hon' && a.category === 'storyboard' && Number.isInteger(a.storyboardOrder) && a.storyboardOrder > 0 && !a.storySequenceID).sort((a,b) => a.storyboardOrder - b.storyboardOrder);
assert.equal(mainPanels.length, 36, 'Original storyboard retains 36 source panels');
assert.equal(catalog.storyboardMetadata.hon.panelCount, 36, 'Hon source panel metadata excludes untimed provider drafts');
assert.equal(catalog.storyboardMetadata.lisan.panelCount, 50, 'Lisan source panel metadata retains its original 50-panel series');
mainPanels.forEach((a,i) => {
  assert.equal(a.storyboardOrder, i + 1, 'Original panel order is not interleaved with the separate scene');
  assert.equal(a.storyboardPosition, Number((i / 35 * 100).toFixed(4)), 'Original range percentages remain unchanged');
});
for (const id of sequence.assetIDs) assert.equal(byID.get(id).storyboardPosition, undefined, 'New scene references receive no implied song/source-range position');
api.setState({view:'storyboard',storyStart:50,storyEnd:60,storyStage:'all',storyLayout:'panels'});api.renderMain();
assert(page.html().includes('4 matching panels'), 'The existing 50–60% slice still contains the same four source panels');
const sequenceStory=catalog.storyboardStories.find(s=>s.sequenceID===sequence.id);assert(sequenceStory,'Independent scene has a selectable story');
assert(page.html().includes('data-story-card="'+sequenceStory.id+'"'),'Untimed scene remains reachable from a landing card while browsing a song range');
assert(page.html().includes('#'+[sequenceStory.project,'storyboard','story:'+sequenceStory.id].map(encodeURIComponent).join('/')),'Story card carries its shareable destination');
api.setState({storyLayout:'progress'});api.renderMain();
assert(!page.html().includes('id="shot-work-'+sequence.id+'"'),'Independent scene progress does not mix into song progress');
api.setState({album:'story:'+sequenceStory.id,storyLayout:'panels'});api.renderMain();
assert(page.toggles(sequence.id).length>=1,'Selected independent story retains its source and history collection');
assert(page.html().includes('id="shot-work-'+sequence.id+'"'),'Existing placement-pending progress card remains under its selected story');
assert(page.html().includes('data-scene-id="'+sequence.id+'"'),'Existing scene readiness controls remain reachable under that story');
assert(!page.html().includes('id="story-start"'),'Song range does not filter independent scene');
api.setState({view:'all',album:'',storyStart:0,storyEnd:100,storyLayout:'panels'});api.expandedCollections.clear();api.renderMain();
checks++;

api.setState({project:'lisan',view:'all',search:'',album:null});api.expandedCollections.clear();api.renderMain();
for (const group of catalog.sharedReferenceCollections.filter(g => g.project === 'lisan')) {
  assert(page.toggles(group.id).length >= 1, 'Lisan reference collection expands inline: ' + group.id);
  expectCollapsed(group.id);
  for (const id of group.assetIDs) assert(!page.html().includes('class="media-open" data-open="' + id + '"'), 'Lisan views start collapsed without duplicate flat cards');
  page.toggle(group.id);
  for (const id of group.assetIDs) assert(page.html().includes('class="media-open" data-open="' + id + '"'), 'Each received Lisan view is reachable inline: ' + id);
  page.toggle(group.id);
  expectCollapsed(group.id);
}
api.setState({project:'hon',view:'all'});api.expandedCollections.clear();api.renderMain();
checks++;

assert.deepEqual(clone(api.reviewPayload().items), initialReview, 'Collection navigation does not mutate reviews, notes, scopes or approvals');
assert.deepEqual(Object.fromEntries(page.storage), initialStorage, 'Collection navigation leaves saved favorites, review and basket storage untouched');
assert.equal(page.writes.length, 0, 'Pure browsing does not write storage');
assert.deepEqual(clone(api.reviewPayload().favorites).map(a => a.id), ['HD-DROP-0d83180f0903']);
assert.deepEqual(clone(api.basketPayload(true).items).map(a => a.id), ['HD-DROP-0d83180f0903']);
checks++;

console.log(JSON.stringify({passed:true,checks,castCovers:Object.keys(expectedCovers).length,detailCovers:catalog.detailDisplayGroups.length,detailAssets:detailMembers.size,mouthMembers:mouth.assetIDs.length,browserVisualQA:false}));
