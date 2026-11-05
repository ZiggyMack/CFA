/* Use the existing DOM double to check actual render, grouping, routes and storage. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const helper = fs.readFileSync(path.join(__dirname, 'test_compact_browse.cjs'), 'utf8').split('const page = boot(), api = page.api;')[0];
const sandbox = {require, __dirname, console, URL};
vm.runInNewContext(helper + '\nglobalThis.harness = {boot, clone, catalog};', sandbox);
const {boot, clone, catalog} = sandbox.harness;
const page = boot(), api = page.api;
const before = clone({assets:page.C.assets, reviews:api.reviewPayload(), basket:api.basketPayload(true), storage:Object.fromEntries(page.storage)});
const outputIDs = ['HD-COMFY-MOTION-V001','HD-COMFY-RELIGHT-V001','HD-COMFY-RELIGHT-V002','HD-COMFY-IDENTITY-V001'];
const leaf = id => page.html().includes('class="media-open" data-open="'+id+'"');
const render = (project='hon', search='') => {api.setState({project,view:'comfy',album:'',search});api.renderMain();};
render();
for(const id of outputIDs)assert(leaf(id), 'Saved Comfy result visible: '+id);
assert(page.html().indexOf('Comfy outputs') < page.html().indexOf('Likeness targets'));
assert(page.html().includes('href="#hon/working"'));
const recipes=page.html().split('<section class="comfy-recipes">')[1].split('<details class="detail-drawer">')[0];
assert.equal((recipes.match(/class="workflow-diagram"/g)||[]).length,6);
assert(!recipes.includes('<img'),'Recipes use linked ingredient diagrams rather than duplicate image galleries');
assert(recipes.includes('MEASURED_RETURN_20261012.txt'),'Actor replacement evidence remains linked');
assert(!recipes.includes('comfy-mouth-reference-review'),'Reference-review wrapper is not presented as an executed recipe');
assert(leaf('LEIA-LIKENESS-01') && leaf('LUKE-LIKENESS-01'), 'Singleton targets open directly');
assert.equal(page.toggles('hon:comfy-likeness-LEIA').length,0);
assert(page.toggles('hon:comfy-likeness-HON-DOLO').length);
page.toggle('hon:comfy-likeness-HON-DOLO');
for(const id of catalog.albums.find(a=>a.id==='hon:comfy-likeness-HON-DOLO').assetIDs)assert(leaf(id));
const outputSection=page.html().split('<section class="comfy-outputs">')[1].split('</section>')[0];
for(const id of ['GEM-C0823C60','HD-COMFY-RELIGHT-V002-CONTROL','HD-AUDIO-REPLACE-V001']) {
  assert(leaf(id), 'Technical input or finishing retained');
  assert(!outputSection.includes('data-open="'+id+'"'), 'Separate from actual results');
}
assert(page.html().includes('<details class="detail-drawer"><summary>Source clips &amp; control guides'));
assert(page.html().includes('<details class="detail-drawer"><summary>Local finishing'));
const mouthIDs=catalog.albums.filter(a=>a.project==='hon'&&a.category==='comfy'&&/mouth|head|viseme/i.test(a.id+' '+a.title)).flatMap(a=>a.assetIDs);
for(const id of mouthIDs)assert(!leaf(id), 'Working library not duplicated: '+id);
assert(!leaf('HD-LIKENESS-02'), 'Archived original group photo not reintroduced');
render('hon','no-such-result-xyz');
assert(!outputIDs.some(leaf), 'Search filters outputs');
render('lisan');
assert(page.html().includes('No Comfy outputs saved for this project yet.'));
assert(page.html().includes('href="#lisan/working"'));
assert(!page.html().includes('class="media-open"'), 'No mouth libraries disguised as Lisan Comfy outputs');
const after=clone({assets:page.C.assets, reviews:api.reviewPayload(), basket:api.basketPayload(true), storage:Object.fromEntries(page.storage)});
for(const record of [before,after]){delete record.reviews.exported;delete record.basket.exported;}
assert.deepEqual(after,before,'Browsing leaves catalog, review decisions, favorite/basket selections and storage untouched');
assert.equal(page.writes.length,0);
console.log(JSON.stringify({passed:true,outputs:outputIDs.length,targetGroups:3,browserVisualQA:false}));
