/* Visual re-encoding aliases only migrate browsing and saved review choices.
   Actual library.js runs in the existing Node DOM harness; no source writes. */
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const L=__dirname,clone=x=>JSON.parse(JSON.stringify(x));
const REVIEW_KEY='cfa-visual-review-v1',FAVORITES_KEY='cfa-visual-favorites-v1',BASKET_KEY='cfa-visual-export-v1';
const canonicalID='HD-B-91ef00348229',oldID='HD-MOUTH-UPDATE-20261009-01';
const canonicalHash='91ef0034822997d4d78a583ffb9c5aba09470b841b713d5396f07890aa790c86',oldHash='b3a89714149fb27240728959f818c803d745165c8ab27ee884f6612052eff7cb';
const alias={id:oldID,sha256:oldHash,canonicalID,canonicalSHA256:canonicalHash,kind:'visual_duplicate_reencoding'};
const assets=[{id:canonicalID,sha256:canonicalHash,project:'hon',category:'comfy',kind:'image',album:'hon:mouths',title:'Locked mouth',filename:'canonical.jpg',repoPath:'test/canonical.jpg',src:'canonical.jpg',thumb:'canonical.jpg'}];
const canonical={id:canonicalID,sha256:canonicalHash,status:'keep',note:'Latest canonical decision',shotPlan:null,updatedAt:'2026-10-14T12:00:00Z',likenessRating:5,workingReferenceScope:'detail'};
const old={id:oldID,sha256:oldHash,status:'needs_fixes',note:'Historical duplicate decision',shotPlan:{destinations:['Grok'],idea:'Earlier idea'},updatedAt:'2026-10-13T12:00:00Z',likenessRating:2};
const catalog={projects:[{id:'hon',name:'Hon Dolo',subtitle:'Test'}],categories:[['comfy','Comfy targets']],assets,albums:[{id:'hon:mouths',project:'hon',category:'comfy',title:'Mouth references',assetIDs:[canonicalID]}],assetAliases:[alias],reviewDecisions:[canonical,old]};
const source=fs.readFileSync(path.join(L,'library.js'),'utf8'),test=fs.readFileSync(path.join(L,'test_reference_scope.cjs'),'utf8');
const originalHook='window.__scopeTest={openViewer,reviewRecord,reviewPayload,importReview,exportReference,inReviewQueue,whenFileWritesSettle(){return fileWriteChain;}};';
const hook='window.__scopeTest={C,dialog,byID,matchingAsset,openViewer,reviewRecord,reviewPayload,importReview,exportReference,inReviewQueue,mergeValidation,validationLatest,validationAssessment,parseHash,render,getCurrentID(){return currentID;},navigate(hash){location.hash=hash;parseHash();render();},whenFileWritesSettle(){return fileWriteChain;}};';
const body=test.slice(test.indexOf('function boot('),test.indexOf('async function main()'));
assert(body.includes(originalHook));
const boot=new Function('source','catalog','clone','assert','vm','REVIEW_KEY','FAVORITES_KEY','assets',body.replace(originalHook,hook)+';return boot;')(source,catalog,clone,assert,vm,REVIEW_KEY,FAVORITES_KEY,assets);
const reviewExport=items=>({format:REVIEW_KEY,items,favorites:[],exportBasket:[]});
let checks=0;

// Catalog order cannot let an older alias overwrite a newer canonical choice.
for(const decisions of [[canonical,old],[old,canonical]]){
 const page=boot({}, {...catalog,reviewDecisions:decisions});
 assert.equal(page.record(canonicalID).note,canonical.note);
 assert.equal(page.record(canonicalID).status,'keep');
 assert.equal(page.record(canonicalID).shotPlan,null);
 assert.equal(page.api.byID.has(oldID),false,'Never insert aliases into evidence byID');
 const archive=clone(page.api.reviewPayload().validationEvidence.legacyReviewArchive);
 assert(archive.some(x=>JSON.stringify(x)===JSON.stringify(old)),'Original old ID/hash/review retained verbatim');
 checks++;
}
const newerOld={...old,updatedAt:'2026-10-15T12:00:00Z',note:'Newest user choice',shotPlan:null};
for(const decisions of [[canonical,newerOld],[newerOld,canonical]]){
 const page=boot({}, {...catalog,reviewDecisions:decisions});
 assert.equal(page.record(canonicalID).note,newerOld.note);
 assert.equal(page.record(canonicalID).status,'needs_fixes');
 assert.equal(page.record(canonicalID).shotPlan,null);
 assert.deepEqual(clone(page.api.reviewPayload().items.map(x=>[x.id,x.sha256])),[[canonicalID,canonicalHash]]);
 checks++;
}
for(const decisions of [[canonical,{...old,updatedAt:canonical.updatedAt}],[{...old,updatedAt:canonical.updatedAt},canonical]]){
 const page=boot({}, {...catalog,reviewDecisions:decisions});
 assert.equal(page.record(canonicalID).note,canonical.note,'Canonical record wins timestamp ties');checks++;
}

// Browser restoration and explicit imports use exact historical hash bindings.
const page=boot({[REVIEW_KEY]:JSON.stringify(reviewExport([old])),[FAVORITES_KEY]:JSON.stringify([oldID,'unknown']),[BASKET_KEY]:JSON.stringify({format:BASKET_KEY,items:[{id:oldID,sha256:oldHash},{id:oldID,sha256:canonicalHash},{id:oldID}]})});
assert.equal(page.record(canonicalID).note,canonical.note);
assert.deepEqual(clone(page.api.reviewPayload().favorites.map(x=>x.id)),[canonicalID]);
assert.deepEqual(clone(page.api.reviewPayload().exportBasket.map(x=>[x.id,x.sha256])),[[canonicalID,canonicalHash]]);
page.api.importReview(reviewExport([newerOld]));
assert.equal(page.record(canonicalID).note,newerOld.note);
page.api.importReview(reviewExport([old]));
assert.equal(page.record(canonicalID).note,newerOld.note,'Older later import cannot resurrect prior decision');
const before=clone(page.record(canonicalID));
page.api.importReview(reviewExport([{...newerOld,sha256:canonicalHash,note:'Wrong hash',updatedAt:'2026-10-16T00:00:00Z'},{...newerOld,sha256:undefined,note:'Missing hash'}]));
assert.deepEqual(page.record(canonicalID),before,'Wrong/missing alias hash is rejected for reviews');
assert(page.api.reviewPayload().validationEvidence.legacyReviewArchive.some(x=>x.id===oldID&&x.sha256===oldHash&&x.note===newerOld.note));
checks+=5;

// Legacy ID-only favorites remain usable; hashed selections still reject mismatches.
const selections=boot();
selections.api.importReview({format:FAVORITES_KEY,items:[oldID,{id:oldID,sha256:oldHash},{id:oldID,sha256:canonicalHash}]});
assert.deepEqual(clone(selections.api.reviewPayload().favorites.map(x=>x.id)),[canonicalID]);
selections.api.importReview({format:BASKET_KEY,items:[{id:oldID,sha256:oldHash},{id:oldID,sha256:'bad'},{id:oldID}]});
assert.deepEqual(clone(selections.api.reviewPayload().exportBasket.map(x=>x.id)),[canonicalID]);
selections.api.importReview({format:FAVORITES_KEY,exported:'2026-10-16T00:00:00Z',items:[],notes:{[oldID]:'Historical favorite note'},note_refs:{[oldID]:oldHash}});
assert.equal(selections.record(canonicalID).note,'Historical favorite note');
assert.equal(selections.api.reviewPayload().items.length,1,'Favorite notes never create a dangling old-ID review');
checks+=3;

// Alias validity is fail-closed, including an outdated destination hash.
for(const aliases of [[{...alias,canonicalSHA256:'0'.repeat(64)}],[{...alias,kind:'byte_duplicate'}],[{...alias,canonicalID:'missing'}],[alias,{...alias,sha256:'1'.repeat(64)}]]){
 const rejected=boot({[FAVORITES_KEY]:JSON.stringify([oldID])},{...catalog,assetAliases:aliases});
 assert.equal(rejected.api.matchingAsset({id:oldID,sha256:oldHash}),null);
 assert.equal(rejected.api.reviewPayload().favorites.length,0);
 rejected.api.openViewer(oldID);assert.equal(rejected.api.getCurrentID(),'');checks++;
}
assert.equal(page.api.matchingAsset({id:'unknown',sha256:oldHash}),null);
assert.equal(page.api.matchingAsset({id:oldID,sha256:canonicalHash}),null);
const changed=boot();changed.api.byID.get(canonicalID).sha256='9'.repeat(64);
assert.equal(changed.api.matchingAsset({id:oldID,sha256:oldHash}),null,'Changed canonical bytes invalidate alias resolution');
checks+=2;

// Buttons and old asset URLs open the canonical viewer without duplicate media.
const viewer=boot();viewer.open(oldID);assert.equal(viewer.api.getCurrentID(),canonicalID);
for(const view of ['comfy','asset']){
 viewer.api.navigate('#hon/'+view+'/'+encodeURIComponent(oldID));
 assert.equal(viewer.api.getCurrentID(),canonicalID);
 assert(/<img src="[^"]*\/canonical\.jpg"[^>]*id="full-image"/.test(viewer.api.dialog.innerHTML));
 checks++;
}

// Immutable validation records retain the original old-ID/hash binding. They
// cannot become current evidence for the visually similar canonical image.
const binding={assetID:oldID,sha256:oldHash,version:'sha256:'+oldHash};
const evidence={schemaVersion:1,id:'old-image-evidence',axis:'character',applicability:'not_applicable',status:'not_checked',target:binding,scope:{id:'mouth',kind:'detail'},reviewer:{name:'Reviewer',model:'human',surface:'original',reviewedAtUTC:'2026-10-13T00:00:00Z'},imagesSeen:[{...binding,accessible:true,view:'original'}],criteriaResults:[],provenance:{source:'Original review record'},evidence:'Original bytes were reviewed',uncertainty:''};
viewer.api.mergeValidation({format:'cfa-reference-validation-v1',schemaVersion:1,assessments:[evidence]});
assert.deepEqual(clone(viewer.api.reviewPayload().validationEvidence.assessments),[evidence]);
assert.equal(viewer.api.validationLatest(canonicalID,'character').length,0);
assert.equal(viewer.api.validationAssessment(evidence).current,false);
assert(viewer.api.validationAssessment(evidence).reasons.includes('Target image is missing.'));
assert.equal(viewer.api.byID.has(oldID),false);
checks+=2;
console.log(JSON.stringify({status:'passed',checks,behavior:'Visual duplicate review/favorite/basket/navigation compatibility; immutable evidence bindings remain separate.'}));
