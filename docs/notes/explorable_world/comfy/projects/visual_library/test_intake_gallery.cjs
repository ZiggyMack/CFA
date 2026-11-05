/* Gallery and Evidence browse the same frozen intake families and asset reviews.
   Real renderer/handlers run with isolated DOM and storage; no source is written. */
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const clone=value=>JSON.parse(JSON.stringify(value));
const source=fs.readFileSync(path.join(__dirname,'library.js'),'utf8');
const raw=fs.readFileSync(path.join(__dirname,'catalog.js'),'utf8');
const catalog=JSON.parse(raw.slice(raw.indexOf('=')+1).trim().replace(/;$/,''));
const REVIEW_KEY='cfa-visual-review-v1',FAVORITES_KEY='cfa-visual-favorites-v1',EXPORT_KEY='cfa-visual-export-v1';
const byID=new Map(catalog.assets.map(a=>[a.id,a]));
let harness=fs.readFileSync(path.join(__dirname,'test_collections_navigation.cjs'),'utf8');
harness=harness.slice(harness.indexOf('function boot() {'),harness.indexOf('\nconst page = boot(), api = page.api;'));
harness=harness.replace('function boot() {','function boot(seed={},chosenCatalog=catalog) {')
 .replace('new Map(Object.entries(saved))','new Map(Object.entries({...saved,...seed}))')
 .replace('REVIEW_CATALOG:clone(catalog)','REVIEW_CATALOG:clone(chosenCatalog)')
 .replace('querySelectorAll() {return [];}','querySelectorAll(selector) {return selectAll(selector).filter(e=>this.children.has(e));}')
 .replace('window.__collectionsTest={','window.__collectionsTest={dialog,openViewer,updateReview,intakeFamilies,intakeWorkspace,intakeFamily,intakeGalleryFamily,intakeBatchKey,getDisplayed(){return displayed;},getViewerID(){return currentID;},')
 .replace('html:() => nodes.get','nodes,selectAll,context,html:() => nodes.get');
const boot=eval('('+harness.replace(/^function boot/,'function')+')');
const families=catalog.reviewIntake.families,checks=[];
const decode=value=>value.replace(/&quot;/g,'"').replace(/&#39;/g,"'").replace(/&amp;/g,'&').replace(/&lt;/g,'<').replace(/&gt;/g,'>');
const ids=(html,layout)=>[...html.matchAll(/<(?:article|section)\b([^>]*data-intake-family-id="([^"]+)"[^>]*)>/g)].filter(m=>{
 const classes=m[1].match(/\bclass="([^"]+)"/)?.[1].split(/\s+/)||[];return classes.includes('intake-family')===(layout==='evidence');
}).map(m=>decode(m[2]));
const sameIDs=(actual,expected,message)=>assert.deepEqual([...actual].sort(),[...expected].sort(),message);
const renderedIDs=(p,layout)=>ids(p.html(),layout);
function change(p,id,value){const n=p.nodes.get('#'+id);assert(n,'Control exists: '+id);n.value=value;n.onchange?.({target:n});for(const f of n.listeners.get('change')||[])f({target:n});}
function click(p,attribute,value){const n=p.selectAll('['+attribute+']').find(n=>n.attributes[attribute]===value);assert(n,'Action exists: '+attribute+'='+value);n.click();}
function show(p,patch={}){p.api.setState({project:'hon',view:'intake',album:'',search:'',intakeLayout:'gallery',intakeDataset:'all',intakeFilter:'all',intakeDecision:'all',intakeBatch:'all',intakePage:0,...patch});p.api.renderMain();}
function collect(p,layout,expectedCount){
 p.api.setState({intakeLayout:layout,intakePage:0});p.api.renderMain();const out=[];
 for(let page=0;page<Math.max(1,Math.ceil(expectedCount/(layout==='gallery'?36:12)));page++){
  if(page){p.api.setState({intakePage:page});p.api.renderMain();}
  out.push(...renderedIDs(p,layout));
 }
 return out;
}
function check(name,fn){fn();checks.push(name);}

check('Gallery opens with thirty-six families and Evidence remains selectable with twelve',()=>{
 const p=boot();assert.equal(p.api.getState().intakeLayout,'gallery');show(p);assert.equal(renderedIDs(p,'gallery').length,36,'Fresh intake opens the batch gallery');assert(!p.html().includes('Frozen handoff r002'),'The frozen handoff notice does not obstruct the workspace');show(p,{intakeLayout:'evidence'});assert.equal(p.api.getState().intakeBatch,'all');
 assert.equal(renderedIDs(p,'evidence').length,12);change(p,'intake-layout','gallery');
 assert.equal(renderedIDs(p,'gallery').length,36);assert.equal(renderedIDs(p,'evidence').length,0);
 assert(p.nodes.has('#intake-layout')&&p.nodes.has('#intake-dataset')&&p.nodes.has('#intake-filter'));
 const first=renderedIDs(p,'gallery');click(p,'data-intake-page','1');assert.equal(p.api.getState().intakePage,1);assert.equal(renderedIDs(p,'gallery').length,36);
 assert(!renderedIDs(p,'gallery').some(id=>first.includes(id)),'Pagination advances across families');
 const second=renderedIDs(p,'gallery');change(p,'intake-layout','evidence');assert.equal(p.api.getState().intakeLayout,'evidence');assert.equal(p.api.getState().intakePage,3,'Layout changes preserve the starting family');assert.equal(renderedIDs(p,'evidence').length,12);
 sameIDs(renderedIDs(p,'evidence'),second.slice(0,12),'The equivalent evidence page starts at the same family');
 change(p,'intake-layout','gallery');assert.equal(p.api.getState().intakePage,1);sameIDs(renderedIDs(p,'gallery'),second,'Returning to Gallery retains the current location');
});

check('both views retain the same family set after dataset batch search and repair filters',()=>{
 const p=boot(),category='C13-sandworm-rising',batch='LAG-1K::'+category;
 show(p,{project:'lisan',intakeDataset:'LAG-1K',intakeBatch:batch});
 for(const filter of ['all','repairs','unavailable']){
  const expected=families.filter(f=>f.project==='lisan'&&f.dataset==='LAG-1K'&&f.category===category&&(filter!=='repairs'||f.versions.length>1)&&(filter!=='unavailable'||f.versions.some(v=>v.availability!=='available'))).map(f=>f.id);
  p.api.setState({intakeFilter:filter,intakeBatch:batch,search:''});
  sameIDs(collect(p,'gallery',expected.length),expected,'Gallery filtered membership: '+filter);
  sameIDs(collect(p,'evidence',expected.length),expected,'Evidence filtered membership: '+filter);
 }
 const sought=families.find(f=>f.dataset==='LAG-1K'&&f.category===category),query=sought.frameID;
 const expected=families.filter(f=>f.project==='lisan'&&f.dataset==='LAG-1K'&&f.category===category&&JSON.stringify([f.frameID,f.category,f.providerReview,f.versions.map(v=>[v.filename,v.sha256])]).toLowerCase().includes(query.toLowerCase())).map(f=>f.id);
 p.api.setState({intakeFilter:'all',intakeBatch:batch,search:query});
 sameIDs(collect(p,'gallery',expected.length),expected,'Gallery honors search within the batch');sameIDs(collect(p,'evidence',expected.length),expected,'Evidence honors the same search');
});

check('batch keys include dataset and batch selection filters before pagination',()=>{
 const c=clone(catalog),base=clone(families.find(f=>f.project==='hon')),category='Shared source category <A & B>';
 c.reviewSupplements=[];c.reviewIntake.families=[];
 for(const dataset of ['TEST-BATCH-A','TEST-BATCH-B'])for(let n=0;n<40;n++)c.reviewIntake.families.push({...clone(base),id:dataset+':'+n,frameID:'Frame '+n,dataset,category});
 const p=boot({},c);show(p);const batchA='TEST-BATCH-A::'+category,batchB='TEST-BATCH-B::'+category;
 assert.equal(p.api.intakeBatchKey(c.reviewIntake.families[0]),batchA);assert.notEqual(batchA,batchB);
 assert(p.selectAll('[data-intake-batch]').some(n=>n.dataset.intakeBatch===batchA));assert(p.selectAll('[data-intake-batch]').some(n=>n.dataset.intakeBatch===batchB));
 assert(!p.html().includes('Shared source category <A & B>'),'Source batch title is escaped');
 click(p,'data-intake-batch',batchB);assert.equal(p.api.getState().intakeBatch,batchB);assert.equal(p.api.getState().intakePage,0);
 sameIDs(renderedIDs(p,'gallery'),c.reviewIntake.families.filter(f=>f.dataset==='TEST-BATCH-B').slice(0,36).map(f=>f.id),'Selected batch supplies the full first page');
 click(p,'data-intake-page','1');assert.equal(renderedIDs(p,'gallery').length,4);assert(renderedIDs(p,'gallery').every(id=>id.startsWith('TEST-BATCH-B:')));
 change(p,'intake-dataset','TEST-BATCH-A');assert.equal(p.api.getState().intakeBatch,'all');assert.equal(p.api.getState().intakePage,0);assert(renderedIDs(p,'gallery').every(id=>id.startsWith('TEST-BATCH-A:')));
});

check('one original card remains visible and exact unique repair versions stay collapsed',()=>{
 const p=boot(),sourceFamily=families.find(f=>f.original&&f.currentCandidate&&f.original.sha256!==f.currentCandidate.sha256&&f.versions.filter(v=>v.availability==='available'&&v.assetID).length>=3);
 assert(sourceFamily,'A real original and multiple repair versions exist');
 const f=clone(sourceFamily),duplicate=clone(f.versions.find(v=>v.sha256===f.currentCandidate.sha256));duplicate.filename='same-exact-version-alias.jpg';f.versions.push(duplicate);
 const frozen=JSON.stringify(f),html=p.api.intakeGalleryFamily(f),related=html.match(/<details\b([^>]*)>([\s\S]*?)<\/details>/);
 assert(related,'Related versions have an optional drawer');assert(!/\bopen\b/.test(related[1]),'Related versions start collapsed');
 const main=html.replace(related[0],'');assert.equal((main.match(/data-review-card=/g)||[]).length,1,'Only the original is displayed in the family overview');
 assert(main.includes('data-review-card="'+f.original.assetID+'"'),'Original is never silently replaced by the provider candidate');
 for(const assetID of new Set(f.versions.filter(v=>v.availability==='available'&&byID.get(v.assetID)?.sha256===v.sha256).map(v=>v.assetID))){
  assert.equal((html.match(new RegExp('data-review-card="'+assetID+'"','g'))||[]).length,1,'Each exact available version has one normal image card');
 }
 assert(html.includes('data-intake-detail="'+f.id+'"'),'Full evidence remains reachable');assert.equal(JSON.stringify(f),frozen,'Rendering does not alter lineage');
 const evidence=p.api.intakeFamily(sourceFamily);assert(evidence.includes(sourceFamily.original.sha256)&&evidence.includes(sourceFamily.currentCandidate.sha256),'Existing Evidence view retains both original and repair hashes');
});

check('unavailable originals stay identifiable and every unavailable family can open evidence',()=>{
 const c=clone(catalog),f=clone(families.find(f=>f.project==='hon'));f.id='TEST-UNAVAILABLE:family';f.frameID='Unavailable test family';
 f.versions=f.versions.map(v=>({...v,assetID:null,availability:'declared_not_on_disk'}));f.original={...f.original,assetID:null};f.currentCandidate=null;c.reviewIntake.families=[f];c.reviewSupplements=[];
 const p=boot({},c);show(p);const html=p.html();assert.equal(renderedIDs(p,'gallery').length,1);assert(!html.includes('data-review-card='));assert(!html.includes('src="null"'));assert(html.includes('Unavailable test family'));
 click(p,'data-intake-detail',f.id);assert.equal(p.api.getState().album,f.id);assert.equal(p.api.getState().project,'hon');sameIDs(renderedIDs(p,'evidence'),[f.id],'An unavailable family remains navigable');
 assert(p.html().includes('media is not included locally'));
});

check('family deep links force Evidence and do not get hidden by stale gallery filters',()=>{
 const p=boot(),f=families.find(f=>f.project==='hon');
 show(p,{intakeLayout:'gallery',intakeBatch:'unrelated::batch',intakeFilter:'repairs',intakeDataset:'LAG-1K',search:'does-not-match'});
 p.location.hash='#hon/intake/'+encodeURIComponent(f.id);p.api.parseHash();p.api.renderMain();
 sameIDs(renderedIDs(p,'evidence'),[f.id],'The requested family opens directly even after browse filters');assert.equal(renderedIDs(p,'gallery').length,0);
 assert(p.html().includes('Original / delivered base')&&p.html().includes('Provider review and open choices'));
 change(p,'intake-layout','gallery');assert.equal(p.api.getState().album,'');assert.equal(p.api.getState().intakeBatch,p.api.intakeBatchKey(f));assert.equal(p.api.getState().intakeDataset,f.dataset);assert.equal(p.api.getState().search,'');
 assert(renderedIDs(p,'gallery').includes(f.id),'Switching from a focused family returns to its batch gallery');
});

check('gallery card and Evidence share exact asset review state without duplicating reviews',()=>{
 const p=boot(),f=families.find(f=>f.project==='hon'&&f.original?.assetID&&f.versions.some(v=>v.assetID===f.original.assetID&&v.availability==='available')),id=f.original.assetID;
 show(p,{intakeBatch:p.api.intakeBatchKey(f)});const open=p.selectAll('[data-open]').find(n=>n.dataset.open===id);assert(open,'Original card uses the existing asset viewer');open.click();
 assert(p.api.dialog.open);assert(p.api.dialog.innerHTML.includes(byID.get(id).sha256),'Viewer retains the exact version hash');
 const keep=p.selectAll('[data-review-status]').find(n=>n.dataset.reviewStatus==='keep');assert(keep);keep.click();
 assert.equal(p.api.reviewRecord(id).status,'keep');assert.equal(p.api.reviewPayload().items.filter(r=>r.id===id).length,1,'One review per exact asset');
 assert(p.api.intakeGalleryFamily(f).includes('review-chip keep'));assert(p.api.intakeFamily(f).includes('review-chip keep'),'Both views reflect the same existing review');
 const originalCount=p.api.intakeFamilies().length;change(p,'intake-layout','evidence');change(p,'intake-layout','gallery');assert.equal(p.api.intakeFamilies().length,originalCount,'A decision changes no family counts');
 assert.equal(p.api.reviewPayload().items.filter(r=>r.id===id).length,1);
});

check('gallery viewer navigation excludes hidden cards and includes expanded versions once',()=>{
 const p=boot(),f=families.find(f=>f.dataset==='LAG-1K'&&f.frameID==='C13-05_Z_1');assert(f?.currentCandidate);
 show(p,{project:f.project,intakeDataset:f.dataset,intakeBatch:p.api.intakeBatchKey(f)});
 const other=families.find(other=>other.id!==f.id&&p.api.intakeBatchKey(other)===p.api.intakeBatchKey(f)&&other.original?.assetID&&other.versions.some(v=>v.sha256===other.original.sha256&&v.availability==='available'));
 const mediaButton=id=>{const button=p.selectAll('[data-open]').find(n=>n.dataset.open===id&&n.attributes.class==='media-open');assert(button,'Rendered gallery image: '+id);return button;};
 const original=mediaButton(f.original.assetID),repair=mediaButton(f.currentCandidate.assetID),neighbor=mediaButton(other.original.assetID);
 const saved=Object.fromEntries(p.storage),reviews=clone(p.api.reviewPayload().items);let expanded=false;
 // Supply the ancestry/visibility that the intentionally flat DOM double lacks.
 for(const button of [original,repair,neighbor])button.closest=selector=>selector==='.intake-gallery-family'?{}:selector==='details:not([open])'&&button===repair&&!expanded?{}:null;
 const query=p.context.document.querySelectorAll;
 p.context.document.querySelectorAll=selector=>selector==='.intake-gallery .media-open'?[original,repair,neighbor,original]:query(selector);
 assert(p.api.getDisplayed().length>3,'Initial rendering includes other batches/supplement or hidden-version images');
 original.click();assert.deepEqual(clone(p.api.getDisplayed()),[f.original.assetID,other.original.assetID],'Only visible gallery image IDs enter the sequence');
 assert(p.api.dialog.innerHTML.includes('1 / 2'),'Viewer count describes the visible gallery');
 p.nodes.get('#next').click();assert.equal(p.api.getViewerID(),other.original.assetID,'Next skips collapsed repair and unrelated rendered cards');
 p.nodes.get('#previous').click();assert.equal(p.api.getViewerID(),f.original.assetID);
 expanded=true;original.click();assert.deepEqual(clone(p.api.getDisplayed()),[f.original.assetID,f.currentCandidate.assetID,other.original.assetID],'Expanded repair joins the sequence without duplicating an asset');
 p.nodes.get('#next').click();assert.equal(p.api.getViewerID(),f.currentCandidate.assetID,'Next can visit an expanded related version');
 assert.deepEqual(Object.fromEntries(p.storage),saved);assert.deepEqual(clone(p.api.reviewPayload().items),reviews,'Navigation makes no decisions');
 const sequence=clone(p.api.getDisplayed()),keep=p.selectAll('[data-review-status]').find(n=>n.dataset.reviewStatus==='keep');keep.click();
 assert.equal(p.api.reviewRecord(f.currentCandidate.assetID).status,'keep','The explicit review action is saved for the selected version');
 assert.deepEqual(clone(p.api.getDisplayed()),sequence,'A review-triggered rerender preserves the chosen gallery sequence');
 p.nodes.get('#next').click();assert.equal(p.api.getViewerID(),other.original.assetID,'Next still follows the gallery after saving a decision');
});

check('browsing modes batches pages and family evidence leaves source and saved choices untouched',()=>{
 const p=boot(),sourceBefore=JSON.stringify(p.C.reviewIntake),reviewsBefore=clone(p.api.reviewPayload().items),storageBefore=Object.fromEntries(p.storage),basketBefore=clone(p.api.basketPayload(true).items);
 show(p);const batch=p.api.intakeBatchKey(families.find(f=>f.project==='hon'));click(p,'data-intake-batch',batch);change(p,'intake-layout','evidence');change(p,'intake-filter','repairs');change(p,'intake-filter','all');change(p,'intake-layout','gallery');
 const f=families.find(f=>f.project==='hon'&&p.api.intakeBatchKey(f)===batch);click(p,'data-intake-detail',f.id);
 assert.equal(p.api.getState().album,f.id);assert.equal(p.api.getState().project,'hon');assert(p.location.hash.includes(encodeURIComponent(f.id)));
 assert.equal(JSON.stringify(p.C.reviewIntake),sourceBefore);assert.deepEqual(clone(p.api.reviewPayload().items),reviewsBefore);assert.deepEqual(clone(p.api.basketPayload(true).items),basketBefore);
 assert.deepEqual(Object.fromEntries(p.storage),storageBefore);assert.equal(p.writes.length,0,'Browsing is not a review decision or a storage mutation');
});

console.log(JSON.stringify({passed:true,checks:checks.length,names:checks,productionFilesWritten:false}));
