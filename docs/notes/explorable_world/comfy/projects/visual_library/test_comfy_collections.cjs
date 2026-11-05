/* Comfy root grouping against the real renderer and collection DOM/storage double.
   Verifies navigation and preservation; no browser, build or source-media writes. */
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const clone=value=>JSON.parse(JSON.stringify(value));
const read=name=>fs.readFileSync(path.join(__dirname,name),'utf8');
const source=read('library.js'),catalog=JSON.parse(read('catalog.js').split('=').slice(1).join('=').trim().replace(/;$/,''));
const catalogBefore=JSON.stringify(catalog),byID=new Map(catalog.assets.map(a=>[a.id,a]));
const harness=read('test_collections_navigation.cjs'),start=harness.indexOf('function boot() {'),end=harness.indexOf('\nconst page = boot(), api = page.api;');
assert(start>=0&&end>start,'Existing DOM/storage harness is available');
let bootSource=harness.slice(start,end);
const anchor="html:() => nodes.get('#main').innerHTML,";
assert(bootSource.includes(anchor));
bootSource=bootSource.replace(anchor,anchor+'\n    selectAll,');
assert(bootSource.includes('reviewPayload,basketPayload,'));
bootSource=bootSource.replace('reviewPayload,basketPayload,','reviewPayload,basketPayload,dialog,');
function boot(C=catalog){
 return new Function('source','catalog','byID','clone','assert','vm','URL','Intl','console','REVIEW_KEY','FAVORITES_KEY','EXPORT_KEY',bootSource+'\nreturn boot();')(
  source,C,new Map(C.assets.map(a=>[a.id,a])),clone,assert,vm,URL,Intl,console,'cfa-visual-review-v1','cfa-visual-favorites-v1','cfa-visual-export-v1');
}
function snapshot(p){
 const review=clone(p.api.reviewPayload());for(const key of ['exported','exportedAt','exportedAtUTC'])delete review[key];
 return {review,basket:clone(p.api.basketPayload(true).items),storage:Object.fromEntries(p.storage),writes:p.writes.length,catalog:clone(p.C)};
}
function navigate(p,project,album='',search=''){
 p.api.setState({search});
 p.location.hash='#'+[project,'comfy',album].filter(Boolean).map(encodeURIComponent).join('/');
 p.api.parseHash();p.api.renderMain();
 assert.equal(p.api.getState().view,'comfy');assert.equal(p.api.getState().album,album);
}
function click(p,attribute,value){
 const button=p.selectAll('['+attribute+']').find(e=>e.attributes[attribute]===value);
 assert(button,'Bound control exists: '+attribute+'='+value);button.click();
}
function collapsed(p,id){
 const panel='collection-'+id.replace(/[^a-z0-9_-]/gi,'-');
 assert(p.html().includes('<div id="'+panel+'" class="collection-inline-views" hidden></div>'),'Child content is lazy and collapsed: '+id);
 assert(p.toggles(id).length>0,'Child retains actual album ID: '+id);
 for(const button of p.toggles(id))assert.equal(button.attributes['aria-expanded'],'false');
}
const leaves=p=>new Set([...p.html().matchAll(/class="media-open" data-open="([^"]+)"/g)].map(m=>m[1]));
const currentMembers=(p,al)=>al.assetIDs.map(id=>byID.get(id)).filter(a=>a&&!['document','pdf'].includes(a.kind)&&p.api.normalVisible(a));
const expectedRelated={
 hon:['hon:mouth-reference-updates','hon:head-library-evidence','hon:mouth-v003-candidates','hon:mouth-v003-sheets','hon:head-anchor-b-candidates','hon:mouth-continuity-candidates'],
 lisan:['lisan:breather-natural-teeth-partial','lisan:mouth-natural-teeth-partial','lisan:mouth-optional-grill-partial']
};
const base='file:///D:/Documents/CFA/docs/notes/explorable_world/comfy/projects/visual_library/';
let checks=0,albumRoutes=0,childCollections=0,searches=0;
for(const project of ['hon','lisan']){
 const p=boot(),before=snapshot(p),albums=catalog.albums.filter(al=>al.project===project&&al.category==='comfy');
 const related=albums.filter(al=>/mouth|head|viseme|breather/i.test(al.id+' '+al.title)&&currentMembers(p,al).length);
 for(const id of expectedRelated[project])assert((project==='hon'?albums:related).some(al=>al.id===id),'Real mouth/head intake remains recorded: '+id);
 const other=albums.filter(al=>!related.includes(al)&&currentMembers(p,al).length);
 navigate(p,project);const rootHash=p.location.hash,parent=project+':comfy:root:comfy-mouth-references';
 for(const al of other){
  assert(p.html().includes('data-album="'+al.id+'"'),'Other Comfy target retains its existing group: '+al.id);
  for(const a of currentMembers(p,al))assert(leaves(p).has(a.id),'Other Comfy target remains visible: '+a.id);
 }
 if(project==='hon'){
  assert.equal(p.selectAll('[data-browse-bucket]').filter(e=>e.dataset.browseBucket===parent).length,0,'Hon no longer repeats the mouth/head parent');
  assert(!p.html().includes('Mouth &amp; head references'));
  for(const al of related){assert.equal(p.toggles(al.id).length,0);for(const a of currentMembers(p,al))assert(!leaves(p).has(a.id),'Hon mouth reference is absent from ordinary Comfy: '+a.id);}
  assert(!leaves(p).has('HD-LIKENESS-02'),'Original group photo stays in Archive');checks++;
 }else{
 assert.equal(p.selectAll('[data-browse-bucket]').filter(e=>e.dataset.browseBucket===parent).length,1,'One mouth/head parent');
 assert(p.html().includes('Mouth &amp; head references'));
 assert.equal(p.selectAll('[data-browse-bucket="'+parent+'"]')[0].attributes['aria-expanded'],'true');
 const parentIndex=p.html().indexOf('data-browse-bucket="'+parent+'"');
 for(const al of related){
  collapsed(p,al.id);
  assert(p.html().indexOf('data-collection="'+al.id+'"')>parentIndex,'Child appears within the mouth/head parent');
  for(const a of currentMembers(p,al))assert(!leaves(p).has(a.id),'Individual reference starts hidden: '+a.id);
 }
 click(p,'data-browse-bucket',parent);
 assert.equal(p.location.hash,rootHash);
 assert.equal(p.selectAll('[data-browse-bucket="'+parent+'"]')[0].attributes['aria-expanded'],'false');
 for(const al of related)assert.equal(p.toggles(al.id).length,0,'Closing parent removes nested controls');
 for(const al of other)for(const a of currentMembers(p,al))assert(leaves(p).has(a.id),'Closing references preserves other targets');
 click(p,'data-browse-bucket',parent);
 for(const al of related)collapsed(p,al.id);
 checks++;
 for(const al of related){
  p.toggle(al.id);assert.equal(p.location.hash,rootHash,'Child expansion stays on Comfy root');
  for(const a of currentMembers(p,al))assert(leaves(p).has(a.id),'Every visible reference remains reachable: '+a.id);
  const a=currentMembers(p,al)[0];click(p,'data-open',a.id);
  assert(p.api.dialog.open);assert(p.api.dialog.innerHTML.includes(new URL(a.src,base).href),'Bound viewer opens full original');
  p.api.dialog.close();
  click(p,'data-browse-bucket',parent);click(p,'data-browse-bucket',parent);
  assert.equal(p.toggles(al.id)[0].attributes['aria-expanded'],'true','Parent reopen preserves child expansion');
  p.toggle(al.id);collapsed(p,al.id);childCollections++;
 }
 checks++;
 for(const al of related){
  const a=currentMembers(p,al)[0];navigate(p,project,'',a.filename);collapsed(p,al.id);p.toggle(al.id);
  assert(leaves(p).has(a.id),'Filename search preserves matching reference: '+a.id);
  for(const id of leaves(p)){const found=byID.get(id);assert(found&&[found.title,found.filename,found.album,found.note,found.beat,found.lyric,p.api.reviewRecord(id).note,...(found.tags||[])].join(' ').toLowerCase().includes(a.filename.toLowerCase()),'Search does not expose nonmatching media: '+id);}
  p.toggle(al.id);searches++;
 }
 }
 navigate(p,project,'','NO_SUCH_COMFY_REFERENCE_7dbdce0c');
 assert.equal(leaves(p).size,0);assert.equal(p.toggles(related[0].id).length,0);
 checks++;
 for(const al of albums.filter(al=>currentMembers(p,al).length)){
  p.api.expandedCollections.clear();navigate(p,project,al.id);
  assert.equal(p.location.hash,'#'+project+'/comfy/'+encodeURIComponent(al.id),'Old album bookmark is preserved');
  assert.equal(p.selectAll('[data-browse-bucket]').filter(e=>e.dataset.browseBucket.endsWith(':comfy-mouth-references')).length,0,'Root parent does not replace direct album pages');
  if(p.toggles(al.id).length)p.toggle(al.id);
  for(const a of currentMembers(p,al))assert(leaves(p).has(a.id),'Old album route retains its media: '+a.id);
  albumRoutes++;
 }
 assert.deepEqual(snapshot(p),before,'Browsing preserves reviews, scopes, favorites, basket and entire catalog');
 assert.equal(p.writes.length,0);checks++;
}
// No current album is named solely for visemes. Exercise that intake label using
// an existing original in a cloned catalog, without introducing media or reviews.
for(const project of ['hon','lisan']){
 const C=clone(catalog),original=C.albums.find(al=>al.id===(project==='hon'?'hon:mouth-v003-candidates':expectedRelated[project][0]));
 const id=project+':viseme-regression-fixture';C.albums.push({id,project,category:'comfy',title:'Viseme references',description:'Synthetic test album only.',assetIDs:[original.assetIDs[0]]});
 const p=boot(C),before=snapshot(p);navigate(p,project);
 if(project==='hon'){
  assert.equal(p.toggles(id).length,0,'Hon also suppresses new mouth-related groups from ordinary Comfy');
  navigate(p,project,id);assert(leaves(p).has(original.assetIDs[0]),'Existing direct reference routes remain reviewable');
 }else{
  collapsed(p,id);p.toggle(id);assert(leaves(p).has(original.assetIDs[0]),'Lisan viseme-only album joins parent without new media');
 }
 assert.deepEqual(snapshot(p),before);assert.equal(p.writes.length,0);checks++;
}
assert.equal(JSON.stringify(catalog),catalogBefore,'Shared source catalog was never mutated');
console.log(JSON.stringify({passed:true,checks,projects:['hon','lisan'],childCollections,albumRoutes,searches,visemeFixtures:2,storageWrites:0,browserVisualQA:false}));
