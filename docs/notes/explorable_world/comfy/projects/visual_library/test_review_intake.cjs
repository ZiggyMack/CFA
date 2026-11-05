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
  const instrumented = source.replace(/\}\)\(\);\s*$/, 'window.__collectionsTest={renderMain,intakeFamily,intakeAssetEvidence,supplementPanel,supplementCard,expandedCollections,collapsedBrowseBuckets,reviews,reviewRecord,reviewPayload,basketPayload,setState(p){Object.assign(state,p);},getState(){return state;}};})();');
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


const page=boot(),api=page.api;
const before=clone(api.reviewPayload()),basket=clone(api.basketPayload(true));
const all=catalog.reviewIntake.families;
assert(all.length>2200);
api.setState({project:'hon',view:'intake',album:'',search:'C04-006',intakeDataset:'all',intakeDecision:'all'});api.renderMain();
assert(page.html().includes('C04-006'));assert(page.html().includes('Provider current candidate'));
assert(!page.html().includes('undefined'));assert(!page.html().includes('src="null"'));
const repaired=all.find(f=>f.dataset==='LAG-1K'&&f.frameID==='C37-06_Z_4_FAIL');
assert(repaired);const html=api.intakeFamily(repaired);
assert(html.includes('Original / delivered base'));assert(html.includes('Provider current candidate'));
assert(html.includes(repaired.original.sha256));assert(html.includes(repaired.currentCandidate.sha256));
assert(html.includes('Earlier versions and other candidates'));
assert(html.includes('<details class="detail-drawer"><summary>Earlier versions'), 'Version history starts collapsed');
const unavailable=all.find(f=>f.versions.some(v=>v.availability==='deferred_history'));
const missing=unavailable.versions.find(v=>v.availability==='deferred_history');
assert.equal(missing.assetID,null);assert(api.intakeFamily(unavailable).includes('media is not included locally'));
const placeholder=all.find(f=>f.versions.some(v=>v.availability==='declared_not_on_disk'));
assert(api.intakeFamily(placeholder).includes('declared not on disk'));
api.setState({project:'lisan',view:'intake',album:'',search:'',intakeDataset:'GROK-HD-FALCON-1000'});api.renderMain();
assert.equal(api.getState().intakeDataset,'all');assert(page.html().includes('Lisan scenes'));
assert.equal((page.html().match(/class="intake-family"/g)||[]).length,12);
const match=Object.entries(catalog.reviewIntake.assetMetadata).find(([id])=>id.startsWith('HD-FALCON-'))||Object.entries(catalog.reviewIntake.assetMetadata)[0];
assert(api.intakeAssetEvidence(byID.get(match[0])).includes('Read full review'));
assert.equal(api.intakeAssetEvidence({...byID.get(match[0]),sha256:'0'.repeat(64)}),'');
// Later supplements are passive source evidence, independent of frozen intake and local choices.
const frozenBefore=JSON.stringify(page.C.reviewIntake),existing=byID.get(match[0]);
const fixture={id:'supplement-fixture',title:'Winners supplement',goldReferenceStatus:'provider_links_with_inferences',indexURL:'../fixture/index.html',csvURL:'../fixture/list.csv',receiptURL:'../fixture/receipt.txt',items:[
  {id:'preview-fixture',project:'hon',title:'C04-005 later chest',version:'v005',label:'V-validated (scoped), awaiting Ziggy',group:'validated',sha256:'a'.repeat(64),thumbURL:'../fixture/thumb.jpg',fullImageURL:null,availability:'preview_only',exactAssetID:null,familyIDs:[unavailable.id],familyLinkBasis:'Named frame; no exact-version match',vVerdict:'PASS-ADVISORY',advisories:'Spires soft at 6x',goldReferences:'INFERRED pilot',reviewScope:'Chest only',sourceEvidence:'V-team round 2',referenceLinks:[{label:'Pilot',sha256:'b'.repeat(64),url:'../fixture/pilot.jpg',availability:'local_original_verified',matchBasis:'unique_hash_prefix_from_provider'}]},
  {id:'exact-fixture',project:'hon',title:'Recorded chain pick',version:'v002',label:'APPROVED BY ZIGGY',group:'approved',sha256:existing.sha256,thumbURL:'../fixture/chain.jpg',fullImageURL:existing.src,availability:'local_original_verified',exactAssetID:existing.id,familyIDs:[]},
  {id:'other-project-fixture',project:'lisan',title:'Lisan mouth pick',version:'v001',label:'PRELIMINARY',group:'preliminary',sha256:'c'.repeat(64),thumbURL:'../fixture/lisan.jpg',availability:'preview_only',familyIDs:[]}
]};
page.C.reviewSupplements=[fixture];
api.setState({project:'hon',view:'intake',album:'',search:'',intakeDataset:'all'});api.renderMain();
let panel=api.supplementPanel();
assert(panel.includes('Golden references · 1'));assert(panel.includes('V-Team scoped passes · 1'));
assert(!panel.includes('other-project-fixture'),'Supplement groups follow project');
assert(!panel.includes('class="supplement-group" open'),'Supplement groups start collapsed');
assert(panel.includes('Some gold-reference assignments are inferred'));
const preview=api.supplementCard(fixture.items[0]);
assert(preview.includes('Preview only'));assert(preview.includes('PASS-ADVISORY'));assert(preview.includes('Spires soft at 6x'));
assert(preview.includes('INFERRED pilot'));assert(preview.includes('provider’s unique hash prefix'));assert(preview.includes('pilot.jpg'));
assert(preview.includes('Full image local'));assert(!preview.includes('local_original_verified'));
const sourced=api.supplementCard({...fixture.items[0],notes:'Box only. Original provider note.',sourceLinks:[{label:'Chain winner notes',url:'../fixture/NOTES.md',sha256:'e'.repeat(64),matchBasis:'unique_hash_prefix_from_provider'}]});
assert(sourced.includes('Cited source documents'));assert(sourced.includes('NOTES.md'));assert(sourced.includes('e'.repeat(64)));
assert(sourced.indexOf('Box only. Original provider note.')>sourced.indexOf('Source and version evidence'),'Stale provider notes stay attributed inside evidence');
assert(sourced.includes('Provider note (as supplied)'));
assert(!preview.includes('data-open='));assert(!preview.includes('data-review-status='));assert(!preview.includes('Open local original'));
assert(panel.includes('data-open="'+existing.id+'"'),'Exact verified supplement image opens the existing review');
assert(api.intakeFamily(unavailable).includes('The comparison below remains the frozen r002 handoff'));
assert(api.intakeAssetEvidence(existing).includes('Later winners supplement · exact image match'));
assert(!api.intakeAssetEvidence({...existing,sha256:'d'.repeat(64)}).includes('Later winners supplement'));
page.click('data-intake-family',unavailable.id);
assert.equal(api.getState().album,unavailable.id,'Supplement family link opens the frozen comparison');
assert.equal(api.getState().intakeFilter,'all');
api.setState({search:'a'.repeat(16)});panel=api.supplementPanel();
assert(panel.includes('preview-fixture'));assert(!panel.includes('exact-fixture'),'Search finds supplement version hashes');
assert(panel.includes('class="supplement-group" open'),'Search reveals matching supplement entries');
const unsafe=api.supplementCard({...fixture.items[0],title:'<script>unsafe()</script>',thumbURL:'javascript:unsafe()',sourceEvidence:'<img onerror="unsafe()">'});
assert(!unsafe.includes('<script>'));assert(!unsafe.includes('javascript:'));assert(unsafe.includes('&lt;script&gt;'));
assert.equal(JSON.stringify(page.C.reviewIntake),frozenBefore,'Later evidence cannot rewrite frozen r002');
const after=clone(api.reviewPayload()),basketAfter=clone(api.basketPayload(true));
delete after.exported;delete before.exported;delete basketAfter.exported;delete basket.exported;
assert.equal(JSON.stringify(after)===JSON.stringify(before),true,'Existing review choices stay unchanged');
assert.equal(JSON.stringify(basketAfter)===JSON.stringify(basket),true,'Basket stays unchanged');
assert.equal(page.writes.length,0,'Browsing intake must not write review choices');
console.log('10 intake checks and supplement grouping, provenance, exact-hash, search and decision-preservation checks passed');
