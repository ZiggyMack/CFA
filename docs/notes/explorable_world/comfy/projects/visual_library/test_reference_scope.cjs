/* Execute the real library against a small DOM/storage double. Not browser QA. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const source = fs.readFileSync(path.join(__dirname, 'library.js'), 'utf8');
const REVIEW_KEY = 'cfa-visual-review-v1';
const FAVORITES_KEY = 'cfa-visual-favorites-v1';
const clone = value => JSON.parse(JSON.stringify(value));
const assets = ['detail', 'requested', 'approved', 'other'].map((id, index) => ({
  id, sha256:String(index + 1).repeat(64), project:'hon', category:'review',
  kind:'image', album:'test:references', title:id, filename:id + '.jpg',
  repoPath:'test/' + id + '.jpg', src:id + '.jpg', thumb:id + '.jpg'
}));
const priorPlan = {status:'planned', destinations:['Flow'], idea:'Keep the tattoo only.', prompt:'Preserve the linework.'};
const seed = (id, fields) => ({id, sha256:assets.find(a => a.id === id).sha256, origin:'user', ...fields});
const catalog = {
  projects:[{id:'hon', name:'Hon Dolo', subtitle:'Test references'}],
  categories:[['review', 'Needs review']], assets,
  albums:[{id:'test:references', project:'hon', category:'review', title:'References', assetIDs:assets.map(a => a.id)}],
  reviewDecisions:[
    seed('detail', {status:'keep', note:'Only the tattoo is relevant.', shotPlan:priorPlan}),
    seed('requested', {workingReference:{status:'requested', scope:'scene'}}),
    seed('approved', {workingReference:{status:'approved', scope:'identity'}})
  ]
};

function boot(saved = {}, catalogInput = catalog, options = {}) {
  const nodes = new Map(), storage = new Map(Object.entries(saved)), writes = [], downloads = [], blobs = new Map();
  const timers = new Map(), fileWrites = [];
  let timer = 0;
  class Element {
    constructor(tag = 'div') {
      this.tag = tag; this.dataset = {}; this.listeners = new Map(); this.children = new Set();
      this.classList = {toggle(){}, remove(){}, add(){}};
      this._value = ''; this._html = ''; this.open = false;
    }
    get innerHTML() { return this._html; }
    set innerHTML(html) {
      // Replacing a viewer removes the old control nodes and their listeners.
      for (const id of this.children) nodes.delete('#' + id);
      this.children.clear(); this._html = html;
      for (const match of html.matchAll(/<([a-z][\w-]*)\b[^>]*\bid="([^"]+)"[^>]*>/gi)) {
        const child = new Element(match[1]); child.id = match[2];
        child.disabled = /\bdisabled(?:\s|>)/.test(match[0]);
        nodes.set('#' + child.id, child); this.children.add(child.id);
      }
      for (const match of html.matchAll(/<select\b[^>]*\bid="([^"]+)"[^>]*>([\s\S]*?)<\/select>/gi)) {
        const select = nodes.get('#' + match[1]);
        const options = [...match[2].matchAll(/<option\b[^>]*\bvalue="([^"]*)"([^>]*)>/gi)];
        select.options = options.map(option => option[1]);
        select._value = (options.find(option => /\bselected\b/.test(option[2])) || options[0])?.[1] || '';
      }
    }
    get value() { return this._value; }
    set value(value) { this._value = this.options && !this.options.includes(value) ? '' : value; }
    setAttribute(name, value) { this[name] = value; }
    addEventListener(name, callback) {
      if (!this.listeners.has(name)) this.listeners.set(name, []);
      this.listeners.get(name).push(callback);
    }
    fire(name) {
      const event = {target:this, preventDefault(){}};
      let result = this['on' + name]?.(event);
      for (const callback of this.listeners.get(name) || []) result = callback(event);
      return result;
    }
    click() {
      if (this.tag === 'a') downloads.push({name:this.download, blob:blobs.get(this.href)});
      if (!this.disabled) return this.fire('click');
    }
    append(child) { if (child.id) nodes.set('#' + child.id, child); }
    querySelector() { return null; }
    querySelectorAll() { return []; }
    showModal() { this.open = true; }
    close() { this.open = false; this.fire('close'); }
    remove() {}
  }
  nodes.set('#app', new Element());
  const document = {
    currentScript:{src:'file:///D:/Documents/CFA/docs/notes/explorable_world/comfy/projects/visual_library/library.js'},
    body:new Element('body'), createElement:tag => new Element(tag), addEventListener(){},
    querySelector:selector => nodes.get(selector) || null, querySelectorAll:() => []
  };
  const window = {REVIEW_CATALOG:clone(catalogInput), REVIEW_INITIAL:{project:'hon', view:'all'}, addEventListener(){}, scrollTo(){}};
  if (options.fileAutosave) window.showSaveFilePicker = async () => ({
    name:'test-review.json',
    async createWritable() {
      let pending;
      return {async write(contents){pending = contents;}, async close(){fileWrites.push(pending);}, async abort(){}};
    }
  });
  class TestURL extends URL {
    static createObjectURL(blob) { const url = 'blob:test-' + blobs.size; blobs.set(url, blob); return url; }
    static revokeObjectURL() {}
  }
  const context = {window, document, location:{hash:'#hon/all'}, URL:TestURL, Blob, Intl, console,
    setTimeout(callback){timers.set(++timer, callback); return timer;}, clearTimeout:id => timers.delete(id),
    localStorage:{getItem:key => storage.get(key) ?? null, setItem(key, value){storage.set(key, value); writes.push([key, value]);}},
    sessionStorage:{getItem:() => null, setItem(){}}
  };
  const instrumented = source.replace(/\}\)\(\);\s*$/, 'window.__scopeTest={openViewer,reviewRecord,reviewPayload,importReview,exportReference,inReviewQueue,whenFileWritesSettle(){return fileWriteChain;}};})();');
  assert.notEqual(instrumented, source, 'Library test hook attached');
  vm.runInNewContext(instrumented, context);
  return {
    api:window.__scopeTest, storage, writes, downloads, fileWrites,
    node(selector) { const result = nodes.get(selector); assert(result, 'Rendered control exists: ' + selector); return result; },
    open(id) { window.__scopeTest.openViewer(id); },
    change(value) { const select = this.node('#working-reference-scope'); select.value = value; select.fire('change'); },
    record(id) { return clone(window.__scopeTest.reviewRecord(id)); },
    snapshot() { return Object.fromEntries(storage); },
    async flushTimers() {
      for (const [id, callback] of [...timers]) { timers.delete(id); await callback(); }
      await window.__scopeTest.whenFileWritesSettle();
    }
  };
}

async function main() {
  let checks = 0;
  const originalFavorites = JSON.stringify(['detail']);
  const page = boot({[FAVORITES_KEY]:originalFavorites});
  page.open('detail');
  assert.equal(page.node('#working-reference-scope').value, 'complete_look');
  page.change('detail');
  let record = page.record('detail');
  assert.equal(record.workingReferenceScope, 'detail', 'Actual dropdown change listener saves the selection');
  assert.equal(record.workingReference, undefined, 'Choosing a scope does not create a request or approval');
  assert.equal(page.api.inReviewQueue(assets[0]), false, 'A scope choice alone does not enter the request queue');
  assert.equal(record.note, 'Only the tattoo is relevant.');
  assert.equal(record.status, 'keep');
  assert.deepEqual(record.shotPlan, priorPlan);
  assert.equal(page.storage.get(FAVORITES_KEY), originalFavorites);
  checks++;

  page.open('other');
  assert.equal(page.node('#working-reference-scope').value, 'complete_look', 'Another asset has its own selection');
  page.open('detail');
  assert.equal(page.node('#working-reference-scope').value, 'detail', 'Recreated viewer restores the selected scope');
  checks++;

  const reloaded = boot(page.snapshot());
  reloaded.open('detail');
  assert.equal(reloaded.node('#working-reference-scope').value, 'detail', 'A fresh JS context restores browser storage');
  assert.equal(reloaded.record('detail').workingReference, undefined);
  assert.deepEqual(reloaded.record('detail').shotPlan, priorPlan);
  assert.equal(reloaded.record('detail').note, record.note);
  checks++;

  // Click the actual export button and import its generated JSON into a clean session.
  reloaded.node('#viewer-export-review').click();
  assert.equal(reloaded.downloads.length, 1);
  assert.equal(reloaded.downloads[0].name, 'cfa-review.json');
  const portable = JSON.parse(await reloaded.downloads[0].blob.text());
  assert.equal(portable.format, REVIEW_KEY);
  assert.equal(portable.items.find(item => item.id === 'detail').workingReferenceScope, 'detail');
  const imported = boot({}, {...catalog, reviewDecisions:[]});
  imported.api.importReview(portable);
  imported.open('detail');
  assert.equal(imported.node('#working-reference-scope').value, 'detail', 'Export/import survives normalization');
  assert.equal(imported.record('detail').workingReference, undefined);
  assert.deepEqual(imported.record('detail').shotPlan, priorPlan);
  assert.equal(imported.record('detail').status, 'keep');
  assert.equal(imported.record('detail').note, record.note);
  assert.deepEqual(JSON.parse(imported.storage.get(FAVORITES_KEY)), ['detail']);
  checks++;

  page.open('requested');
  assert.equal(page.node('#working-reference-scope').value, 'scene', 'Legacy requested scope remains selected');
  page.change('detail');
  assert.deepEqual(page.record('requested').workingReference, {status:'requested', scope:'scene'}, 'Draft selection does not silently change a queued request');
  assert.match(page.node('#working-reference-status').textContent, /Earlier request retained/);
  assert.equal(page.node('#working-reference-scope').value, 'detail');
  assert.throws(() => page.node('#request-working-reference'), /Rendered control exists/, 'Redundant request action is absent');
  assert.throws(() => page.node('#clear-working-reference'), /Rendered control exists/, 'Redundant cancel action is absent');
  page.open('other'); page.open('requested');
  assert.equal(page.node('#working-reference-scope').value, 'detail', 'Selected scope survives while the historical request is retained');
  checks++;

  page.open('approved');
  assert.equal(page.node('#working-reference-scope').value, 'identity', 'Legacy approval supplies its scope');
  page.change('detail');
  assert.deepEqual(page.record('approved').workingReference, {status:'approved', scope:'identity'}, 'Changing draft does not alter an approval');
  assert.match(page.node('#working-reference-status').textContent, /Recorded role: identity/);
  const exportedReference = clone(page.api.exportReference(assets[2]));
  assert.equal(exportedReference.workingReferenceScope, 'detail');
  assert.deepEqual(exportedReference.workingReference, {status:'approved', scope:'identity'}, 'Handoffs distinguish selected scope from approved scope');
  checks++;

  const beforeInvalid = page.storage.get(REVIEW_KEY), writesBeforeInvalid = page.writes.length;
  page.change('unsupported');
  assert.equal(page.storage.get(REVIEW_KEY), beforeInvalid, 'Invalid selection does not write review state');
  assert.equal(page.writes.length, writesBeforeInvalid);
  page.open('other'); page.open('approved');
  assert.equal(page.node('#working-reference-scope').value, 'detail');
  for (const invalid of ['unsupported', '__proto__', 'toString', null, {}, ['detail']]) {
    const input = {format:REVIEW_KEY, items:[seed('other', {workingReferenceScope:invalid})], favorites:[]};
    const invalidPage = boot({}, {...catalog, reviewDecisions:[]});
    invalidPage.api.importReview(input);
    invalidPage.open('other');
    assert.equal(invalidPage.node('#working-reference-scope').value, 'complete_look', 'Invalid imported scope is ignored: ' + JSON.stringify(invalid));
    assert.equal(Object.hasOwn(invalidPage.record('other'), 'workingReferenceScope'), false);
  }
  checks++;

  const autosave = boot({}, catalog, {fileAutosave:true});
  autosave.open('detail');
  await autosave.node('#viewer-save-review').click();
  assert.equal(autosave.fileWrites.length, 1, 'Choosing the review file makes an initial committed save');
  autosave.change('detail');
  autosave.change('outfit');
  assert.equal(autosave.fileWrites.length, 1, 'Dropdown file save is debounced');
  await autosave.flushTimers();
  assert.equal(autosave.fileWrites.length, 2, 'Latest dropdown selection is autosaved once after the timer');
  const fileRecord = JSON.parse(autosave.fileWrites[1]).items.find(item => item.id === 'detail');
  assert.equal(fileRecord.workingReferenceScope, 'outfit');
  assert.equal(fileRecord.workingReference, undefined, 'File autosave still does not request approval');
  assert.equal(fileRecord.note, 'Only the tattoo is relevant.');
  assert.deepEqual(fileRecord.shotPlan, priorPlan);
  checks++;

  console.log(JSON.stringify({passed:true, scenarios:checks, browserVisualQA:false}));
}

main().catch(error => { console.error(error); process.exitCode = 1; });
