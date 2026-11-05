/* DOM/storage double only; no browser/build/evidence writes. */
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),crypto=require('node:crypto');
const {pathToFileURL}=require('node:url');
const clone=x=>JSON.parse(JSON.stringify(x));
const read=n=>fs.readFileSync(path.join(__dirname,n),'utf8');
const source=read('library.js'),catalog=JSON.parse(read('catalog.js').replace(/^window\.REVIEW_CATALOG = /,'').trim().replace(/;$/,''));
const manifest=JSON.parse(read('source_comparisons.json')),pair=manifest.comparisons.find(p=>p.id==='c13-original-patch-c');
const root=path.resolve(__dirname,'../../../../../..'),base=pathToFileURL(__dirname+path.sep).href;
const expected=[['LAG-C13-ORIGINAL-7eafd9ac048d','ORIGINAL','C13-04_Z_1.jpg',268027,'7eafd9ac048dc6d6125dc38281c1b664f7ae0cac1159909c34d90a5e3eef93a3'],['LAG-C13-PATCH-C-23817577d3d3','REPAIRED patch-c','C13-04_Z_1_R1-try5-patch-c.jpg',447799,'23817577d3d32f0df03d57ac1e49c4c85246e86c405b13c492194f7aa2f52bad']];
assert(pair);assert.equal(pair.status,'source_selected');assert.equal(pair.missionTaskID,'comfy-report-decisions-20261013');
assert.equal(pair.sourceChoice.selectedAssetID,expected[1][0]);assert.equal(pair.sourceChoice.scope,'prototype_video_source');
const receipt=pair.sourceChoice.record,receiptRaw=fs.readFileSync(path.join(root,receipt.path)),decision=JSON.parse(receiptRaw);
assert.equal(receiptRaw.length,receipt.bytes);assert.equal(crypto.createHash('sha256').update(receiptRaw).digest('hex'),receipt.sha256);
assert.equal(decision.selectedSource.assetID,expected[1][0]);assert.deepEqual(decision.retainedSources.map(s=>s.assetID),expected.map(e=>e[0]));
assert.deepEqual(catalog.sourceComparisons,manifest.comparisons);
assert.deepEqual(pair.items.map(i=>[i.assetID,i.label]),expected.map(e=>e.slice(0,2)));
for(const [id,label,filename,bytes,sha256] of expected){
 const m=manifest.media.find(a=>a.id===id),a=catalog.assets.find(a=>a.id===id);assert(m&&a);
 assert.equal(path.basename(m.path),filename);assert.equal(a.repoPath,m.path);assert.equal(a.bytes,bytes);assert.equal(a.sha256,sha256);
 const raw=fs.readFileSync(path.join(root,m.path));assert.equal(raw.length,bytes);assert.equal(crypto.createHash('sha256').update(raw).digest('hex'),sha256);
 for(const f of ['workingReference','likenessRating','sceneQualityRating','storyboardStage','componentApprovals'])assert.equal(Object.hasOwn(a,f),false);
}
const harness=read('test_collections_navigation.cjs'),start=harness.indexOf('function boot() {'),end=harness.indexOf('\nconst page = boot(), api = page.api;');
assert(start>=0&&end>start);
let bootSource=harness.slice(start,end);const hook="html:() => nodes.get('#main').innerHTML,";assert(bootSource.includes(hook));bootSource=bootSource.replace(hook,hook+'\n    selectAll,');
function boot(C){return new Function('source','catalog','byID','clone','assert','vm','URL','Intl','console','REVIEW_KEY','FAVORITES_KEY','EXPORT_KEY',bootSource+'\nreturn boot();')(source,C,new Map(C.assets.map(a=>[a.id,a])),clone,assert,vm,URL,Intl,console,'cfa-visual-review-v1','cfa-visual-favorites-v1','cfa-visual-export-v1');}
function snapshot(p){const payload=clone(p.api.reviewPayload());delete payload.exported;delete payload.exportedAt;delete payload.exportedAtUTC;return {payload,basket:clone(p.api.basketPayload(true).items),storage:Object.fromEntries(p.storage),writes:p.writes.length};}
const attrs=tag=>Object.fromEntries([...tag.matchAll(/([\w-]+)="([^"]*)"/g)].map(m=>[m[1],m[2].replace(/&amp;/g,'&')]));
function exercise(C,distinct,status='Saved video source: REPAIRED patch-c'){
 const p=boot(C),before=snapshot(p);p.api.setState({project:'hon',view:'mission_control',album:'',search:''});p.api.renderMain();
 const task=p.html(),preview=[...task.matchAll(/<section class="source-comparison-preview">[\s\S]*?<\/section>/g)].map(m=>m[0]).find(section=>section.includes('data-source-comparison="'+pair.id+'"'));assert(preview,'The C13 task has its own comparison preview');
 const button=p.selectAll('[data-source-comparison="'+pair.id+'"]').at(0);assert(button,'Actual task button exists');button.click();
 assert.equal(p.location.hash.replace(/^#/,''),'lisan/review_queue');assert.equal(p.api.getState().project,'lisan');assert.equal(p.api.getState().view,'review_queue');
 const markup=p.html().match(/<section\b[^>]*id="source-comparison-c13-original-patch-c"[\s\S]*?<\/section>/)?.[0];assert(markup);assert.match(markup,/source-comparison-pair/);assert(markup.includes(status));assert(preview.includes(status));
 assert.equal((markup.match(/Selected for video/g)||[]).length,status.startsWith('Saved')?1:0);
 if(status.startsWith('Saved')){assert(!preview.includes('Pending comparison'));assert(!markup.includes('Pending comparison'));}
 if(status==='Pending comparison')assert(markup.includes('Pending comparison'),'The C13 panel reports its own pending state');
 const figures=[...markup.matchAll(/<figure\b([^>]*)>([\s\S]*?)<\/figure>/g)];assert.equal(figures.length,2);const images=[];
 figures.forEach(([tag,attr,body],i)=>{const [id,label]=expected[i],a=C.assets.find(a=>a.id===id),url=new URL(a.src,base).href;assert.equal(attrs(attr)['data-comparison-asset'],id);assert(body.includes(label));const image=attrs(body.match(/<img\b[^>]*>/)?.[0]||'');assert.equal(image.src,url);if(distinct)assert.notEqual(image.src,new URL(a.thumb,base).href);assert([...body.matchAll(/<a\b[^>]*>/g)].map(m=>attrs(m[0])).some(l=>l.href===url&&l.target==='_blank'));images.push({id,label,src:url,sha256:a.sha256,bytes:a.bytes});});
 assert.deepEqual(snapshot(p),before);assert.equal(p.writes.length,0);for(const [id] of expected)assert(!p.api.reviewPayload().items.some(i=>i.id===id));
 return {rendererDOMDoubleMarkup:markup,taskDOMDoubleMarkup:task,images,route:'#lisan/review_queue',storageWrites:0};
}
const distinct=clone(catalog);for(const [id] of expected)distinct.assets.find(a=>a.id===id).thumb='test-only-thumbnails/'+id+'.jpg';exercise(distinct,true);
const pending=clone(catalog);const pendingPair=pending.sourceComparisons.find(p=>p.id===pair.id);pendingPair.status='pending_comparison';delete pendingPair.sourceChoice;exercise(pending,false,'Pending comparison');
const invalid=clone(catalog);invalid.sourceComparisons.find(p=>p.id===pair.id).sourceChoice.sha256='0'.repeat(64);exercise(invalid,false,'Source choice needs verification');
// A returned repair is reviewable without inheriting its original's decision or becoming a replacement.
const repairPair=manifest.comparisons.find(p=>p.id==='hon-c04-002-original-v003');assert(repairPair);
const originalID='HD-FALCON-1f55da287bbf7416',repairIDs=['HD-FALCON-ee485849b0e6528a','HD-FALCON-af69f68b13ef0012'];
assert.equal(repairPair.status,'pending_comparison');assert.equal(Object.hasOwn(repairPair,'sourceChoice'),false);
assert.deepEqual(repairPair.items.map(i=>i.assetID),[originalID,repairIDs[1]]);
const repairTask=catalog.missionControl.tasks.find(t=>t.id===repairPair.missionTaskID);assert(repairTask);
assert.equal(repairTask.priority,'normal');assert.equal(repairTask.status,'in_progress');
assert(repairTask.reviewGate,'Returned versions have an explicit exact-version review gate');
for(const id of [originalID,...repairIDs])assert(repairTask.links.some(link=>link.assetID===id),'The repair task retains all three exact image links');
const canonicalPath=path.join(root,'docs/notes/explorable_world/comfy/projects/hon_dolo_strictly_business/feedback/review_decisions.json');
const canonicalRaw=fs.readFileSync(canonicalPath),canonical=JSON.parse(canonicalRaw.toString('utf8').replace(/^\uFEFF/,''));
const originalDecision=canonical.items.find(r=>r.id===originalID);assert(originalDecision);
assert.deepEqual(catalog.reviewDecisions.find(r=>r.id===originalID),originalDecision,'Catalog preserves the complete original decision and shot plan');
const repairPage=boot(catalog),repairBefore=snapshot(repairPage),assetsBefore=clone(repairPage.C.assets),originalBefore=clone(repairPage.api.reviewRecord(originalID));
for(const id of repairIDs){
 const a=catalog.assets.find(a=>a.id===id),m=manifest.media.find(a=>a.id===id);assert(a&&m);
 const raw=fs.readFileSync(path.join(root,m.path));assert.equal(raw.length,m.bytes);assert.equal(crypto.createHash('sha256').update(raw).digest('hex'),m.sha256);
 assert.equal(a.sha256,m.sha256);assert.equal(a.sourceStatus,'Pending comparison');assert.equal(a.acceptance,'not_accepted');
 assert.equal(a.storyboardStage,'preliminary');assert.equal(a.masterApproved,false);assert.equal(a.productionReady,false);assert.equal(a.approvalScope,null);
 assert.deepEqual(a.sourceAssetIDs,[originalID]);
 for(const field of ['likenessRating','sceneQualityRating','componentApprovals'])assert.equal(Object.hasOwn(a,field),false,'Provider assessments do not seed '+field);
 const recorded=canonical.items.find(r=>r.id===id);assert(recorded,'The later exact-version human review is now canonical');
 assert.deepEqual(catalog.reviewDecisions.find(r=>r.id===id),recorded,'Catalog retains the later review without copying the original disposition');
 assert.equal(repairPage.api.reviewRecord(id).status,id===repairIDs[0]?'keep':'needs_fixes');
 assert.equal(repairPage.api.reviewRecord(id).sha256,a.sha256);
 const request=catalog.reviewRequests.find(r=>r.id===id);assert(request);assert.equal(request.sha256,a.sha256);assert.equal(request.type,'missing_decision');
}
repairPage.api.setState({project:'lisan',view:'mission_control',album:'',search:''});repairPage.api.renderMain();
const repairPreview=repairPage.html().match(/<section class="source-comparison-preview">[\s\S]*?data-source-comparison="hon-c04-002-original-v003"[\s\S]*?<\/section>/)?.[0];assert(repairPreview);
assert(repairPreview.includes('Original · Keep'),'Task preview uses the current original decision');
assert(!repairPreview.includes('Original · Needs fixes'),'Historical comparison labels cannot contradict a later review');
assert(repairPreview.includes('Reviews recorded · no source or replacement selected'));
const repairButton=repairPage.selectAll('[data-source-comparison="'+repairPair.id+'"]').at(0);assert(repairButton,'Repair comparison is accessible across project tabs');repairButton.click();
assert.equal(repairPage.location.hash.replace(/^#/,''),'hon/review_queue');assert.equal(repairPage.api.getState().project,'hon');assert.equal(repairPage.api.getState().view,'review_queue');
const repairMarkup=repairPage.html().match(/<section\b[^>]*id="source-comparison-hon-c04-002-original-v003"[\s\S]*?<\/section>/)?.[0];assert(repairMarkup);
assert(repairMarkup.includes('Reviews recorded · no source or replacement selected'));assert(!repairMarkup.includes('Selected for video'));
assert(repairMarkup.includes('<strong>Original · Keep</strong>'));
assert(!repairMarkup.includes('Original · Needs fixes'));
assert(repairMarkup.includes('v003 · unaccepted repair · Needs fixes'),'Repair review is shown separately from replacement selection');
assert.deepEqual([...repairMarkup.matchAll(/data-comparison-asset="([^"]+)"/g)].map(m=>m[1]),[originalID,repairIDs[1]]);
for(const image of [...repairMarkup.matchAll(/<img\b[^>]*>/g)].map(m=>attrs(m[0])))assert(image.alt.endsWith(repairPair.title),'Repair alt text uses its own comparison title');
assert(!repairPage.html().includes('data-review-card="'+repairIDs[0]+'"'),'A saved Keep is not presented as an unanswered review');
assert(repairPage.html().includes('data-review-card="'+repairIDs[1]+'"'),'The recorded repair remains in saved Needs fixes history');
const storedOriginal=clone(repairPage.api.reviews.get(originalID));
repairPage.api.reviews.set(originalID,{...storedOriginal,status:null});repairPage.api.renderMain();
const clearedMarkup=repairPage.html().match(/<section\b[^>]*id="source-comparison-hon-c04-002-original-v003"[\s\S]*?<\/section>/)?.[0];assert(clearedMarkup);
assert(clearedMarkup.includes('<strong>Original</strong>'),'Clear removes the live triage suffix');
assert(!clearedMarkup.includes('Original · Keep')&&!clearedMarkup.includes('Original · Needs fixes'),'Clear never revives the stale source label');
assert(clearedMarkup.includes('Pending comparison')&&!clearedMarkup.includes('Selected for video'),'An unanswered image reopens review without selecting a replacement');
repairPage.api.setState({view:'mission_control'});repairPage.api.renderMain();
const clearedPreview=repairPage.html().match(/<section class="source-comparison-preview">[\s\S]*?data-source-comparison="hon-c04-002-original-v003"[\s\S]*?<\/section>/)?.[0];assert(clearedPreview);
assert(clearedPreview.includes('<span>Original</span>'));
assert(!clearedPreview.includes('Original · Keep')&&!clearedPreview.includes('Original · Needs fixes'));
repairPage.api.reviews.set(originalID,storedOriginal);
assert.deepEqual(clone(repairPage.api.reviewRecord(originalID)),originalBefore,'Navigation preserves the original review and planned shot');
assert.deepEqual(clone(repairPage.C.assets),assetsBefore,'Navigation never archives or supersedes an image');
assert.deepEqual(snapshot(repairPage),repairBefore,'Repair navigation preserves saved reviews, favorites, basket and storage');
assert.deepEqual(fs.readFileSync(canonicalPath),canonicalRaw,'Canonical decisions are read-only in this test');
const evidence=exercise(catalog,false),result={passed:true,checks:['exact sources and labels','task route','full-source pair','independent source links','thumbnail/source separation','review/favorite/basket/scope preservation','C04 recorded reviews without replacement selection','current Keep and explicit Clear captions','returned candidate neutrality','original decision and shot-plan preservation'],catalogMode:'generated catalog',browserVisualQA:false,route:evidence.route,images:evidence.images,storageWrites:0};
if(process.argv.includes('--evidence-stdout'))Object.assign(result,evidence,{evidenceLimit:'Real renderer and bound handler executed against a DOM/storage double; no browser rendering or screenshot.'});console.log(JSON.stringify(result));
