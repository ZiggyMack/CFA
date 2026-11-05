/* Intake completion tracks explicit decisions on current exact-image targets.
   Catalogs and browser storage are isolated fixtures; no production data is written. */
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const clone=value=>JSON.parse(JSON.stringify(value));
const source=fs.readFileSync(path.join(__dirname,'library.js'),'utf8');
const raw=fs.readFileSync(path.join(__dirname,'catalog.js'),'utf8');
const catalog=JSON.parse(raw.slice(raw.indexOf('=')+1).trim().replace(/;$/,''));
const REVIEW_KEY='cfa-visual-review-v1',FAVORITES_KEY='cfa-visual-favorites-v1',EXPORT_KEY='cfa-visual-export-v1';
const byID=new Map(catalog.assets.map(a=>[a.id,a]));
let harness=fs.readFileSync(path.join(__dirname,'test_collections_navigation.cjs'),'utf8');
harness=harness.slice(harness.indexOf('function boot() {'),harness.indexOf('\nconst page = boot(), api = page.api;'));
harness=harness.replace('function boot() {','function boot(chosenCatalog=catalog) {')
 .replace('REVIEW_CATALOG:clone(catalog)','REVIEW_CATALOG:clone(chosenCatalog)')
 .replace('querySelectorAll() {return [];}','querySelectorAll(selector) {return selectAll(selector).filter(e=>this.children.has(e));}')
 .replace('window.__collectionsTest={','window.__collectionsTest={dialog,updateReview,openViewer,intakeReviewTargets,intakeReviewProgress,intakeReviewTotals,intakeGalleryFamily,getDisplayed(){return displayed;},getViewerID(){return currentID;},')
 .replace('html:() => nodes.get','nodes,selectAll,context,html:() => nodes.get');
const boot=eval('('+harness.replace(/^function boot/,'function')+')'),checks=[];
const assetPool=[...new Map(catalog.reviewIntake.families.filter(f=>f.project==='hon').flatMap(f=>f.versions).filter(v=>v.availability==='available'&&byID.get(v.assetID)?.sha256===v.sha256).map(v=>[v.assetID,byID.get(v.assetID)])).values()].slice(0,12);
const pointer=a=>({assetID:a.id,sha256:a.sha256});
const version=(a,role='original')=>({assetID:a.id,sha256:a.sha256,availability:'available',role,filename:a.filename,providerReview:{verdict:'PASS',stage:'Provider pass'}});
const unavailable=(sha,role='original')=>({assetID:null,sha256:sha,availability:'deferred_history',role,filename:'Unavailable history.jpg'});
function fixture(){
 const c=clone(catalog),a=assetPool,ids=new Set(a.map(a=>a.id));c.reviewDecisions=c.reviewDecisions.filter(r=>!ids.has(r.id));c.reviewSupplements=[];
 const family=(name,versions,original,current=null,category='Batch A')=>({id:'TEST-PROGRESS:'+name,frameID:name,project:'hon',dataset:'TEST-DATA',category,versions,original,currentCandidate:current,providerReview:{verdict:'PASS'},siteValidation:'not_performed'});
 c.reviewIntake.families=[
  family('Original and current',[version(a[0]),version(a[1],'repair'),version(a[2],'repair'),unavailable('e'.repeat(64),'repair')],pointer(a[0]),pointer(a[1])),
  family('Single original',[version(a[3])],pointer(a[3])),
  family('Shared exact original',[version(a[3])],pointer(a[3])),
  family('Unavailable only',[unavailable('d'.repeat(64))],{assetID:null,sha256:'d'.repeat(64)}),
  family('Fallback repair',[unavailable('c'.repeat(64)),unavailable('b'.repeat(64),'repair'),version(a[4],'repair')],{assetID:null,sha256:'c'.repeat(64)},{assetID:null,sha256:'b'.repeat(64)},'Batch B'),
  family('Candidate only',[unavailable('a'.repeat(64)),version(a[5],'comparison_sheet')],{assetID:null,sha256:'a'.repeat(64)},pointer(a[5]),'Batch B'),
  family('Same original and candidate',[version(a[6]),version(a[6],'repair')],pointer(a[6]),pointer(a[6])),
  family('Version only base',[version(a[7],'version_only_base')],null)
 ];
 return c;
}
const family=p=>p.C.reviewIntake.families;
const setDecision=(p,a,status,extra={})=>p.api.reviews.set(a.id,{id:a.id,sha256:a.sha256,status,origin:'user',...extra});
const sameIDs=(actual,expected,message)=>assert.deepEqual([...actual].sort(),[...expected].sort(),message);
const renderedIDs=p=>[...p.html().matchAll(/<(?:section|article)\b[^>]*data-intake-family-id="([^"]+)"/g)].map(m=>m[1]);
function show(p,patch={}){p.api.setState({project:'hon',view:'intake',album:'',search:'',intakeLayout:'gallery',intakeDataset:'all',intakeFilter:'all',intakeDecision:'pending',intakeBatch:'all',intakePage:0,...patch});p.api.renderMain();}
function change(p,id,value){const n=p.nodes.get('#'+id);assert(n,'Control exists: '+id);n.value=value;n.onchange?.({target:n});for(const fn of n.listeners.get('change')||[])fn({target:n});}
function check(name,fn){fn();checks.push(name);}

check('current targets are exact original and current versions with a bounded fallback',()=>{
 const p=boot(fixture()),f=family(p),targets=i=>p.api.intakeReviewTargets(f[i]).map(a=>a.id);
 sameIDs(targets(0),[assetPool[0].id,assetPool[1].id],'Original and nominated repair need separate decisions');
 assert(!targets(0).includes(assetPool[2].id),'Earlier available repair is evidence, not a new required assignment');
 sameIDs(targets(4),[assetPool[4].id],'First available repair is fallback only when both nominated targets are unavailable');
 sameIDs(targets(5),[assetPool[5].id],'Available nominated comparison remains actionable without its original');
 sameIDs(targets(6),[assetPool[6].id],'Original and current exact same image count once');
 sameIDs(targets(7),[assetPool[7].id],'Version-only base is actionable');
 assert.equal(targets(3).length,0);assert.equal(p.api.intakeReviewProgress(f[3]).unavailable,true);assert.equal(p.api.intakeReviewProgress(f[3]).complete,false);
 const wrong=clone(f[0]);wrong.versions[0].sha256='0'.repeat(64);wrong.original.sha256='0'.repeat(64);
 sameIDs(p.api.intakeReviewTargets(wrong).map(a=>a.id),[assetPool[1].id],'A wrong hash cannot reuse the original asset decision');
});

check('only explicit triage completes targets and each current version remains independent',()=>{
 const p=boot(fixture()),f=family(p),a=assetPool;
 setDecision(p,a[3],null,{note:'Already inspected',likenessRating:5,sceneQualityRating:5,variant:'prime',storyboardStage:'production',shotPlan:{status:'planned',destinations:['Grok'],idea:'Use it',prompt:''}});
 assert.equal(p.api.intakeReviewProgress(f[1]).complete,false,'Notes ratings stage and plan are not triage');
 for(const status of ['keep','needs_fixes','remove']){setDecision(p,a[3],status);assert.equal(p.api.intakeReviewProgress(f[1]).complete,true,status+' completes this review pass');}
 setDecision(p,a[3],null);assert.equal(p.api.intakeReviewProgress(f[1]).pending.length,1,'Clear decision reopens the target');
 setDecision(p,a[0],'keep');let progress=p.api.intakeReviewProgress(f[0]);assert.equal(progress.complete,false);sameIDs(progress.pending.map(a=>a.id),[a[1].id]);
 setDecision(p,a[1],'needs_fixes');progress=p.api.intakeReviewProgress(f[0]);assert.equal(progress.complete,true);assert.equal(progress.reviewed.length,2);
 assert.equal(p.api.reviewRecord(a[2].id).status,null,'Completion does not decide historical versions');
 setDecision(p,a[0],null);p.C.reviewSupplements=[{id:'LATER',items:[{familyIDs:[f[0].id],exactAssetID:a[8].id,sha256:a[8].sha256,humanAcceptance:{accepted:true,kind:'chest_correction'},vVerdict:'PASS'}]}];setDecision(p,a[8],'keep');
 assert.equal(p.api.intakeReviewProgress(f[0]).complete,false,'A later scoped winner cannot complete the frozen original');
});

check('remaining image totals deduplicate shared assets while family totals track each family',()=>{
 const p=boot(fixture()),f=family(p),before=JSON.stringify(p.C.reviewIntake);
 assert.deepEqual(clone(p.api.intakeReviewTotals(f)),{total:7,done:0,remaining:7,familiesPending:7,familiesReviewed:0,unavailable:1});
 setDecision(p,assetPool[3],'remove');assert.deepEqual(clone(p.api.intakeReviewTotals(f)),{total:7,done:1,remaining:6,familiesPending:5,familiesReviewed:2,unavailable:1});
 setDecision(p,assetPool[0],'needs_fixes');assert.deepEqual(clone(p.api.intakeReviewTotals(f)),{total:7,done:2,remaining:5,familiesPending:5,familiesReviewed:2,unavailable:1});
 assert.equal(JSON.stringify(p.C.reviewIntake),before,'Progress derives from reviews without rewriting the intake');
});

check('pending reviewed and all apply after the existing batch search and structural filters',()=>{
 const p=boot(fixture()),f=family(p);assert.equal(p.api.getState().intakeDecision,'pending');setDecision(p,assetPool[3],'keep');show(p);
 const pending=[0,4,5,6,7].map(i=>f[i].id);sameIDs(renderedIDs(p),pending);assert(p.html().includes('6 images left'));assert(p.html().includes('1 awaiting files'));
 change(p,'intake-decision-filter','reviewed');sameIDs(renderedIDs(p),[f[1].id,f[2].id]);change(p,'intake-decision-filter','all');sameIDs(renderedIDs(p),f.map(f=>f.id));
 change(p,'intake-layout','evidence');sameIDs(renderedIDs(p),f.map(f=>f.id),'Both layouts have identical all-family membership');change(p,'intake-decision-filter','pending');sameIDs(renderedIDs(p),pending);
 show(p,{intakeBatch:'TEST-DATA::Batch B'});sameIDs(renderedIDs(p),[f[4].id,f[5].id]);assert(p.html().includes('2 images left'),'Counter describes the selected batch');
 show(p,{search:'Original and current',intakeFilter:'repairs'});sameIDs(renderedIDs(p),[f[0].id]);assert(p.html().includes('2 images left'));
 show(p,{intakeFilter:'unavailable'});sameIDs(renderedIDs(p),[f[0].id,f[4].id,f[5].id],'Unavailable-only placeholder is excluded from actionable pending');
 change(p,'intake-decision-filter','all');sameIDs(renderedIDs(p),[f[0].id,f[3].id,f[4].id,f[5].id]);
});

check('pending gallery promotes the undecided current version and All restores the original cover',()=>{
 const p=boot(fixture()),f=family(p)[0];setDecision(p,assetPool[0],'keep');show(p);
 const cover=html=>html.split('<details')[0].match(/data-review-card="([^"]+)"/)?.[1];
 let html=p.api.intakeGalleryFamily(f);assert.equal(cover(html),assetPool[1].id);assert(html.includes('1 of 2 review targets decided'));
 for(const id of [assetPool[0].id,assetPool[2].id])assert(html.includes('data-open="'+id+'"'),'Related original and history remain accessible');
 p.api.setState({intakeDecision:'all'});assert.equal(cover(p.api.intakeGalleryFamily(f)),assetPool[0].id);
});

check('reviewing a card decrements progress without breaking viewer next in either layout',()=>{
 for(const layout of ['gallery','evidence']){
  const c=fixture();c.reviewIntake.families=[c.reviewIntake.families[1],c.reviewIntake.families[7]];
  const p=boot(c),f=family(p),ids=[assetPool[3].id,assetPool[7].id];show(p,{intakeLayout:layout});
  const buttons=ids.map(id=>{const b=p.selectAll('[data-open]').find(n=>n.dataset.open===id&&n.attributes.class==='media-open');assert(b);return b;});
  const scope=layout==='gallery'?'.intake-gallery-family':'.intake-family',selector=layout==='gallery'?'.intake-gallery .media-open':'.intake-family .media-open';
  for(const b of buttons)b.closest=s=>s===scope?{}:null;
  const query=p.context.document.querySelectorAll;p.context.document.querySelectorAll=s=>s===selector?buttons:query(s);
  buttons[0].click();sameIDs(p.api.getDisplayed(),ids);assert(p.api.dialog.innerHTML.includes('1 / 2'));assert(p.html().includes('2 images left'));
  p.selectAll('[data-review-status]').find(n=>n.dataset.reviewStatus==='keep').click();
  assert.equal(p.api.getViewerID(),ids[0],'Viewer stays open for the current image after its card disappears');assert.equal(p.api.dialog.open,true);
  sameIDs(renderedIDs(p),[f[1].id]);assert(p.html().includes('1 images left'));assert(p.nodes.get('#app').innerHTML.includes('1 left'));
  sameIDs(p.api.getDisplayed(),ids,'Stable viewer snapshot survives filtered rerender');p.nodes.get('#next').click();assert.equal(p.api.getViewerID(),ids[1],'Next visits the original neighbor without skipping');
  p.api.updateReview(ids[1],{status:'needs_fixes'});assert.equal(renderedIDs(p).length,0);assert(p.html().includes('0 images left'));assert.equal(p.api.getState().intakePage,0);
  p.api.updateReview(ids[0],{status:null});sameIDs(renderedIDs(p),[f[0].id],'Clear makes a decided family actionable again');
 }
});

check('direct family evidence bypasses completion filters and unavailable files remain inspectable',()=>{
 const p=boot(fixture()),f=family(p);setDecision(p,assetPool[3],'keep');
 show(p,{album:f[1].id,intakeDecision:'pending',intakeFilter:'unavailable',search:'nonmatching',intakeBatch:'different::batch'});sameIDs(renderedIDs(p),[f[1].id]);assert(p.html().includes('1 of 1 review targets decided'));
 show(p,{album:f[3].id,intakeDecision:'reviewed'});sameIDs(renderedIDs(p),[f[3].id]);assert(p.html().includes('Waiting for a full image'));
});

check('decision filter changes and progress inspection never write review or source data',()=>{
 const p=boot(fixture()),saved=Object.fromEntries(p.storage),reviews=clone(p.api.reviewPayload().items),sourceBefore=JSON.stringify(p.C);show(p);
 for(const value of ['reviewed','all','pending'])change(p,'intake-decision-filter',value);
 for(const f of family(p))p.api.intakeReviewProgress(f);p.api.intakeReviewTotals(family(p));
 assert.equal(JSON.stringify(p.C),sourceBefore);assert.deepEqual(clone(p.api.reviewPayload().items),reviews);assert.deepEqual(Object.fromEntries(p.storage),saved);assert.equal(p.writes.length,0);
});

for(const name of checks)console.log('PASS '+name);
console.log('Intake progress checks passed: '+checks.length);
