/* Real-catalog Chewy hub and Working reference navigation.
   DOM-double checks verify routes, reachability and review safety, not browser layout. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const clone = value => JSON.parse(JSON.stringify(value));
const source = fs.readFileSync(path.join(__dirname, 'library.js'), 'utf8');
const catalog = JSON.parse(fs.readFileSync(path.join(__dirname, 'catalog.js'), 'utf8').split('=').slice(1).join('=').trim().replace(/;$/, ''));
const intake = JSON.parse(fs.readFileSync(path.join(__dirname, 'cast_scene_intake_20261012.json'), 'utf8'));
const byID = new Map(catalog.assets.map(a => [a.id, a]));
const REVIEW_KEY = 'cfa-visual-review-v1';
const FAVORITES_KEY = 'cfa-visual-favorites-v1';
const EXPORT_KEY = 'cfa-visual-export-v1';
const cast = catalog.castCollections.find(g => g.id === 'hon:cast-dj');
assert(cast, 'Real Chewy character collection exists');
const mapping = intake.castCollectionMapping;
const grokVideoIDs = ['HD-INTAKE-3dc76f7d9d325f21cd1b','HD-INTAKE-3ea5959c05259fd65f8d'];
for (const field of ['sceneAssetIDs','setupAssetIDs','workingReferenceIDs','historicalReferenceIDs','videoAssetIDs','relatedAssetIDs']) {
  assert(Array.isArray(cast[field]), 'Root-built catalog contains Chewy ' + field);
  const expected = field === 'videoAssetIDs' ? [...mapping[field],...grokVideoIDs] : mapping[field];
  assert.deepEqual(cast[field], expected, 'Original verified map plus the exact Grok video appearances: ' + field);
  assert.equal(new Set(cast[field]).size, cast[field].length, 'No repeated IDs in ' + field);
  cast[field].forEach(id => assert(byID.has(id), 'Referenced media exists in actual catalog: ' + id));
}
assert.equal(cast.workingReferenceIDs.length, 7, 'User-selected design set retains all seven exact views');
assert.equal(cast.representativeID || cast.coverID, 'HD-DROP-ca406436d384', 'Existing selected cover is preserved');
assert.equal(cast.sceneAssetIDs.length, 274);
assert.equal(cast.setupAssetIDs.length, 51);
assert.equal(cast.historicalReferenceIDs.length, 4);
assert.equal(cast.videoAssetIDs.length, 3);
assert(cast.sourceAlbumIDs.includes('hon:video-grok-tests'), 'Grok run is traceable from the character hub');
assert(grokVideoIDs.every(id=>!cast.workingReferenceIDs.includes(id)), 'Scene clips do not become character model references');
assert.equal(cast.relatedAssetIDs.length, 1);
assert(intake.assets.every(a => byID.has(a.id)), 'Every deduplicated intake original is indexed');
assert.equal(intake.audit.sourceFileCount, 323);
assert.equal(intake.assets.length, 321, 'Same-byte source aliases do not create duplicate media records');
const navigationTest = fs.readFileSync(path.join(__dirname, 'test_collections_navigation.cjs'), 'utf8');
let bootSource = navigationTest.slice(navigationTest.indexOf('function boot()'), navigationTest.indexOf('const page = boot()'));
assert(bootSource.includes('window.__collectionsTest={'), 'Existing no-write DOM harness is available');
bootSource = bootSource.replace('window.__collectionsTest={', 'window.__collectionsTest={openCharacterReview,castHubGroups,castWorkingGroups,workingReferenceVisibleIDs,normalizedPlan,viewerHTML(){return dialog.innerHTML;},clickPreview(id){const target=[...document.querySelectorAll("[data-open]")].find(b=>b.dataset.open===id);if(!target)throw Error("Missing preview: "+id);target.click();},');
const boot = new Function('source','catalog','byID','clone','assert','vm','REVIEW_KEY','FAVORITES_KEY','EXPORT_KEY', bootSource + ';return boot;')(source,catalog,byID,clone,assert,vm,REVIEW_KEY,FAVORITES_KEY,EXPORT_KEY);
const page = boot(), api = page.api;
const before = {reviews:clone(api.reviewPayload().items),assets:clone(page.C.assets),albums:clone(page.C.albums),cast:clone(page.C.castCollections),storage:Object.fromEntries(page.storage)};
let checks = 0;
const sceneSet = new Set(cast.sceneAssetIDs), setupSet = new Set(cast.setupAssetIDs);
assert(cast.setupAssetIDs.every(id => !sceneSet.has(id)), 'Setup candidates are separate from scene appearances');
assert(cast.sceneAssetIDs.every(id => !setupSet.has(id)));
for (const id of ['GEM-25E5C0EC','GEM-58AEA1E7','HD-TATGUIDE-3046dd64faa8']) {
  assert(![...cast.sceneAssetIDs,...cast.videoAssetIDs,...cast.relatedAssetIDs].includes(id), 'Retired Chewie lettering on Dolo is not a cast appearance');
}
for (const incoming of intake.assets) {
  const actual = byID.get(incoming.id);
  assert.equal(actual.sha256, incoming.sha256, 'Source byte identity is retained');
  assert(actual.storyboardOrder == null, 'New source candidates do not receive original song order');
  assert(actual.storyboardPosition == null, 'New source candidates do not receive invented song range');
}
checks++;
api.setState({project:'hon',view:'cast',album:'',search:''});api.expandedCollections.clear();api.renderMain();
assert.equal(page.toggles(cast.id).length, 2, 'One character collection with its two expand controls');
const hub = api.castHubGroups(cast.id)[0];
const expectedHubIDs = [...new Set([cast.representativeID || cast.coverID,...cast.sceneAssetIDs,...cast.videoAssetIDs,...cast.relatedAssetIDs])];
assert.equal(hub.cover.id, 'HD-DROP-ca406436d384');
assert(hub.coverPreviewOnly, 'Selected representative is a preview, not an invented approval');
assert.deepEqual(clone(hub.items.map(a => a.id)).sort(), expectedHubIDs.sort(), 'Hub includes representative and exact connected scene/video/context material');
assert.equal(hub.items.length, 279);
page.toggle(cast.id);
assert(page.html().includes('#hon/working/hon%3Acast-dj'), 'Hub links directly to this character Working collection');
assert(page.html().includes('Scene appearances'));
assert(page.html().includes('Video appearances'));
for (const id of [...cast.workingReferenceIDs.slice(1),...cast.setupAssetIDs,...cast.historicalReferenceIDs]) {
  assert(!page.html().includes('data-open="' + id + '"'), 'Full design/setup sets stay out of Supporting cast: ' + id);
}
for (const id of expectedHubIDs) {
  assert.equal([...page.html().matchAll(new RegExp('data-open="' + id + '"', 'g'))].length, 1, 'Each connected media reference appears once in the expanded hub: ' + id);
}
checks++;
page.location.hash = '#hon/cast/hon%3Acast-dj';api.parseHash();api.renderMain();
assert.equal(api.castHubGroups(cast.id).length, 1, 'Direct character hub route isolates Chewy');
assert(page.html().includes('Character hub'));
const sceneID = cast.sceneAssetIDs[0], scene = byID.get(sceneID);
api.setState({search:scene.filename});api.renderMain();
assert(api.castHubGroups(cast.id)[0].items.some(a => a.id === sceneID), 'Filename search keeps exact scene reachable');
if (!page.html().includes('data-open="' + sceneID + '"')) page.toggle(cast.id);
api.clickPreview(sceneID);
assert(api.viewerHTML().includes('character-context-viewer'),'Character hub opens read-only context');
assert(!api.viewerHTML().includes('reference-likeness-rating'),'Hub browsing does not expose review edits');
api.openCharacterReview(sceneID);
assert(api.viewerHTML().includes('reference-likeness-rating'), 'Scene opens its existing likeness controls');
assert(api.viewerHTML().includes('scene-quality-rating'), 'Scene opens separate scene craft controls');
assert(api.viewerHTML().includes('data-shot-destination="ComfyUI"'), 'Scene planning permits explicit ComfyUI destination');
page.location.hash = '#hon/cast/hon%3Acast-dj';api.parseHash();api.setState({search:''});api.renderMain();
if (!page.html().includes('data-open="' + cast.videoAssetIDs[0] + '"')) page.toggle(cast.id);
api.clickPreview(cast.videoAssetIDs[0]);
assert(api.viewerHTML().includes('<video'), 'Video appearance opens the existing player');
assert(!api.viewerHTML().includes('creative-review'),'Video hub context is read-only');
api.openCharacterReview(cast.videoAssetIDs[0]);
assert(api.viewerHTML().includes('creative-review'), 'Explicit review action keeps Creative review available');
checks++;
page.location.hash = '#hon/working/hon%3Acast-dj';api.parseHash();api.expandedCollections.clear();api.renderMain();
assert(!page.html().includes('data-open="' + cast.workingReferenceIDs[1] + '"'), 'Full design set starts inside one Working collection');
page.toggle(cast.id + '-working');
const work = api.castWorkingGroups(cast.id)[0];
assert.equal(work.items.length, 58, 'Working holds the selected seven and 51 setup candidates; four earlier studies are archived');
assert.equal(work.sections.find(s => s.title === 'Selected design references').assetIDs.length, 7);
assert.equal(work.sections.find(s => s.title === 'Animation/setup candidates').assetIDs.length, 51);
assert.equal(work.sections.find(s => s.title === 'Earlier studies').assetIDs.length, 4);
assert(work.role.includes('Approval not recorded'),'Collection selection remains distinct from per-image approval');
assert(page.html().includes('Candidate inclusion does not approve the design'),'Expanded gallery retains its non-acceptance context');
assert(page.html().includes('#hon/cast/hon%3Acast-dj'), 'Working collection links back to Chewy hub');
for (const id of [...cast.workingReferenceIDs,...cast.setupAssetIDs]) {
  assert.equal([...page.html().matchAll(new RegExp('data-open="' + id + '"', 'g'))].length, 1, 'Each current design/setup original stays reachable once: ' + id);
  assert(api.workingReferenceVisibleIDs().includes(id), 'Working count includes the design/setup reference: ' + id);
}
for (const id of cast.historicalReferenceIDs) {
  assert(!api.normalVisible(byID.get(id)), 'Earlier study is archived by the current browse policy: ' + id);
  assert(!page.html().includes('data-open="' + id + '"'), 'Archived study stays out of Working: ' + id);
  assert(!api.workingReferenceVisibleIDs().includes(id), 'Archived study is not counted as a current Working reference: ' + id);
}
page.location.hash = '#hon/archive';api.parseHash();api.renderMain();
for (const id of cast.historicalReferenceIDs) assert(page.html().includes('data-open="' + id + '"'), 'Archive retains each exact earlier study: ' + id);
page.location.hash = '#hon/working/hon%3Acast-dj';api.parseHash();api.renderMain();
checks++;
api.setState({search:byID.get(cast.setupAssetIDs[0]).filename});api.renderMain();
assert(api.castWorkingGroups(cast.id)[0].items.some(a => a.id === cast.setupAssetIDs[0]), 'Setup filename search works inside Working');
api.setState({view:'all',album:'',search:'',allPurpose:'details'});api.expandedCollections.clear();api.renderMain();
for (const id of cast.setupAssetIDs) assert(!page.html().includes('data-open="' + id + '"'), 'Setup does not leak into ordinary All files Details');
api.setState({allPurpose:'working'});api.renderMain();
assert.equal(page.toggles(cast.id + '-working').length, 0, 'All files does not duplicate Working references');
api.setState({view:'working',album:''});api.renderMain();
assert(page.toggles(cast.id + '-working').length >= 1, 'Dedicated Working references still reaches selected/setup collection');
checks++;
assert.equal(api.normalizedPlan(null), null, 'Browsing does not automatically create a shot plan');
assert.deepEqual(clone(api.normalizedPlan({status:'planned',destinations:['ComfyUI','Unknown provider'],idea:'Cantina toast',prompt:''})).destinations, ['ComfyUI'], 'ComfyUI is accepted only as an explicitly selected destination');
assert.deepEqual(clone(api.reviewPayload().items), before.reviews, 'No decisions, stars, stages, Creative review or scope changes');
assert.deepEqual(clone(page.C.assets), before.assets, 'No source media metadata changes');
assert.deepEqual(clone(page.C.albums), before.albums, 'No catalog album changes');
assert.deepEqual(clone(page.C.castCollections), before.cast, 'No cast/source membership changes');
assert.deepEqual(Object.fromEntries(page.storage), before.storage, 'Saved reviews, favorites and basket remain byte-equivalent');
assert.equal(page.writes.length, 0, 'Browsing does not write local storage');
checks++;
console.log(JSON.stringify({passed:true,checks,sourceFiles:intake.audit.sourceFileCount,newUniqueAssets:intake.assets.length,hubReferences:hub.items.length,selectedDesignReferences:cast.workingReferenceIDs.length,setupCandidates:cast.setupAssetIDs.length,workingReferences:work.items.length,comfyUIDestination:true,reviewWrites:0,browserVisualQA:false}));
