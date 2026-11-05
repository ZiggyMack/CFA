const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const source = fs.readFileSync(path.join(__dirname, '../hosted_dashboard_seed.js'), 'utf8');
const key = 'cfa-visual-favorites-v1';
const catalog = {assets:[{id:'one',sha256:'abc'},{id:'two',sha256:'def'}],reviewSessionSeed:{id:'seed1',favorites:[{id:'one',sha256:'abc'},{id:'two',sha256:'old'}],exportBasket:[{id:'one',sha256:'abc'}]}};
function run(initial = new Map(), input = catalog) {
  const state = new Map(initial);
  vm.runInNewContext(source,{window:{REVIEW_CATALOG:input},localStorage:{getItem:key=>state.has(key)?state.get(key):null,setItem:(key,value)=>state.set(key,value)}});
  return state;
}
const fresh = run();
assert.deepEqual(JSON.parse(fresh.get(key)), ['one']);
assert.deepEqual(JSON.parse(fresh.get('cfa-visual-export-v1')).items, [{id:'one',sha256:'abc'}]);
for (const [existingKey, value] of [[key,'[]'],['cfa-visual-review-v1','{"items":[]}'],['cfa-visual-export-v1','{"format":"cfa-visual-export-v1","items":[]}'],['cfa-hosted-session-seed-v1','{}']]) {
  const previous = new Map([[existingKey,value]]);
  assert.deepEqual(run(previous), previous);
}
assert.deepEqual(run(fresh,{...catalog,reviewSessionSeed:{...catalog.reviewSessionSeed,id:'new snapshot',favorites:[{id:'two',sha256:'def'}]}}),fresh);
console.log('Hosted session seed: exact identity, new browser, empty-state preservation, snapshot persistence passed.');
