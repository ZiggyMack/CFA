/* Real renderer with DOM/storage doubles. No browser or screenshot evidence. */
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),crypto=require('node:crypto');
const {pathToFileURL,fileURLToPath}=require('node:url');
const clone=x=>JSON.parse(JSON.stringify(x)),read=n=>fs.readFileSync(path.join(__dirname,n),'utf8');
const source=read('library.js'),catalog=JSON.parse(read('catalog.js').replace(/^window\.REVIEW_CATALOG = /,'').trim().replace(/;$/,''));
const definition=JSON.parse(read('writer_development.json')),byID=new Map(catalog.assets.map(a=>[a.id,a]));
const sourceStories=JSON.parse(read('storyboard_stories.json')).stories,stories=catalog.storyboardStories;
const safeManifest=JSON.parse(fs.readFileSync(path.join(__dirname,'../collaborators/storyboard_implementation_20261014/site_safe_writer/SITE_SAFE_WRITER_SOURCES.json'),'utf8'));
const root=path.resolve(__dirname,'../../../../../..'),base=pathToFileURL(__dirname+path.sep).href;
const escape=x=>String(x).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;');
let checks=0;
for(const d of definition.documents){
 const id=d.project+':doc:'+d.path,a=byID.get(id);assert(a,id);
 assert.equal(catalog.assets.filter(a=>a.id===id).length,1);
 const raw=fs.readFileSync(path.join(root,d.path));
 const live=d.liveSource||d;
 assert.equal(raw.length,live.bytes);assert.equal(crypto.createHash('sha256').update(raw).digest('hex'),live.sha256);
 const publication=d.publication||d,published=fs.readFileSync(path.join(root,publication.path)),text=published.toString('utf8').replace(/^\uFEFF/,'').replace(/\r\n/g,'\n').replace(/\r/g,'\n');
 assert.equal(published.length,publication.bytes);assert.equal(crypto.createHash('sha256').update(published).digest('hex'),publication.sha256);
 assert.equal(a.repoPath,publication.path);assert.equal(a.sha256,publication.sha256);assert.equal(a.bytes,publication.bytes);
 assert.equal(a.text,d.fullTextPreview?text:text.slice(0,40000));assert.equal(a.author,d.author);assert.equal(a.documentCategory,d.documentCategory);
 const linked=fs.readFileSync(fileURLToPath(new URL(a.src,base)));
 assert.equal(crypto.createHash('sha256').update(linked).digest('hex'),publication.sha256);
 if(d.publication){
  const provenance=safeManifest.records.find(r=>r.documentID===id);assert(provenance,'Explicit safe-publication provenance '+id);
  assert.deepEqual(provenance.source,{path:d.path,bytes:d.bytes,sha256:d.sha256});assert.deepEqual(provenance.publication,d.publication);
  assert.equal(a.historicalRepoPath,publication.path);assert.equal(a.filename,path.posix.basename(publication.path));
  assert.notEqual(new URL(a.src,base).href,pathToFileURL(path.join(root,d.path)).href,'Original writer-only source is not a download');
  for(const excluded of safeManifest.excludedDocumentBasenames)assert(!a.text.includes(excluded),'Excluded source name absent from safe reading excerpt');
 }
}
for(const d of definition.excludedSources)assert(!catalog.assets.some(a=>a.repoPath===d.path),'Excluded source not registered');
for(const expected of definition.projects){
 const actual=catalog.writerDevelopment.projects.find(p=>p.id===expected.id);assert(actual,'Writer project '+expected.id);
 for(const key of ['title','description','featuredDocumentIDs','contextDocumentIDs'])assert.deepEqual(actual[key],expected[key],expected.id+' '+key);
 for(const group of expected.groups)assert.deepEqual(actual.groups.find(g=>g.id===group.id),group,expected.id+' writer group '+group.id);
}
for(const expected of sourceStories){
 const actual=catalog.storyboardStories.find(s=>s.id===expected.id);assert(actual,'Published story '+expected.id);
 for(const [key,value] of Object.entries(expected))if(key!=='documentIDs')assert.deepEqual(actual[key],value,expected.id+' '+key);
 assert.deepEqual(actual.documentIDs.slice(0,expected.documentIDs.length),expected.documentIDs,expected.id+' keeps explicit source writings in order');
}
assert.equal(new Set(catalog.storyboardStories.map(s=>s.id)).size,catalog.storyboardStories.length,'Published story IDs remain unique');
checks++;
const harness=read('test_collections_navigation.cjs'),start=harness.indexOf('function boot() {'),end=harness.indexOf('\nconst page = boot(), api = page.api;');
assert(start>=0&&end>start);let bootSource=harness.slice(start,end);
const hook="html:() => nodes.get('#main').innerHTML,";assert(bootSource.includes(hook));bootSource=bootSource.replace(hook,hook+'\n    selectAll,nodes,');
const selector='querySelectorAll() {return [];}';assert(bootSource.includes(selector));bootSource=bootSource.replace(selector,'querySelectorAll(selector) {return selectAll(selector).filter(element=>this.children.has(element));}');
const exportHook='window.__collectionsTest={';assert(bootSource.includes(exportHook));bootSource=bootSource.replace(exportHook,exportHook+'dialog,openViewer,');
const page=new Function('source','catalog','byID','clone','assert','vm','URL','Intl','console','REVIEW_KEY','FAVORITES_KEY','EXPORT_KEY',bootSource+'\nreturn boot();')(source,catalog,byID,clone,assert,vm,URL,Intl,console,'cfa-visual-review-v1','cfa-visual-favorites-v1','cfa-visual-export-v1');
const api=page.api;
function snapshot(){const reviews=clone(api.reviewPayload());delete reviews.exported;return {reviews,basket:clone(api.basketPayload(true).items),storage:Object.fromEntries(page.storage),writes:page.writes.length};}
const before=snapshot(),markup={};
function render(project,view,search='',storyID=''){api.dialog.innerHTML='';api.dialog.close();api.setState({project,view,album:storyID?'story:'+storyID:'',search,storyTheme:'all',storyStage:'all',storyStart:0,storyEnd:100,storyLayout:'panels',collaborator:'PanhandlerNova',collaboratorSection:'work'});api.renderMain();return page.html();}
function renderStoryWithDocument(id,search=''){const story=stories.find(s=>s.documentIDs.includes(id));assert(story,'Writing has a story destination '+id);return render(story.project,'storyboard',search,story.id);}
function open(id,inDialog=false){const candidates=inDialog?api.dialog.querySelectorAll('[data-open]'):page.selectAll('[data-open]');const b=candidates.find(e=>e.dataset.open===id);assert(b,'Bound document/source button '+id);assert.equal(typeof b.onclick,'function');b.click();assert(api.dialog.open);const a=byID.get(id);assert(api.dialog.innerHTML.includes(escape(a.title)));return api.dialog.innerHTML;}
for(const project of definition.projects){
 for(const view of ['documents','collaborators']){
  const html=render(project.id,view);markup[project.id+'/'+view]=html;
  const ids=project.groups.flatMap(g=>g.documentIDs);
  for(const id of ids)assert(html.includes('data-open="'+escape(id)+'"'),view+' uses canonical doc '+id);
  const id=project.featuredDocumentIDs[0],a=byID.get(id),viewer=open(id);
  assert(viewer.includes('href="'+escape(new URL(a.src,base).href)+'"'));
  assert(viewer.includes('Open original file'));
 }
 const projectStories=stories.filter(s=>s.project===project.id),linked=new Set(projectStories.flatMap(s=>s.documentIDs));
 for(const id of project.groups.filter(g=>g.storyboard).flatMap(g=>g.documentIDs))assert(linked.has(id),'Former storyboard writing keeps a reachable story destination '+id);
 for(const story of projectStories){
  const html=render(project.id,'storyboard','',story.id);markup[project.id+'/storyboard/'+story.id]=html;
  assert(html.includes('data-selected-story="'+escape(story.id)+'"'));
  const writings=html.split('data-story-writings="'+escape(story.id)+'"')[1]?.split('</section>')[0]||'';
  for(const id of story.documentIDs){assert(byID.has(id),'Story document resolves '+id);assert(writings.includes('data-open="'+escape(id)+'"'),'Selected story uses canonical doc '+id);}
  for(const id of linked)if(!story.documentIDs.includes(id))assert(!writings.includes('data-open="'+escape(id)+'"'),'Other story writings do not flood selected story '+id);
  if(story.kind==='prose')assert(html.includes('No panels yet.'));
  const id=story.documentIDs[0];if(id){const a=byID.get(id),viewer=open(id);assert(viewer.includes('href="'+escape(new URL(a.src,base).href)+'"'));assert(viewer.includes('Open original file'));}
 }
}
checks++;
for(const assoc of catalog.writerDevelopment.associations){
 assert(byID.has(assoc.assetID));assert(byID.has(assoc.documentID));assert.equal(byID.get(assoc.assetID).project,byID.get(assoc.documentID).project);
}
for(const fragment of ['SCENE_CARD_SANDWORM.md','STORY_01_JET_BLACK_INTRODUCTION.md','SEED_09_THE_ECHO_20261013.md']){
 const assoc=catalog.writerDevelopment.associations.find(a=>a.documentID.endsWith(fragment));assert(assoc);
 renderStoryWithDocument(assoc.documentID);open(assoc.documentID);let html=open(assoc.assetID,true);
 assert(html.includes(new URL(byID.get(assoc.assetID).src,base).href));
 html=open(assoc.documentID,true);assert(html.includes('Related source references'));
}
checks++;
const decisions=definition.documents.find(d=>d.project==='lisan'&&d.path.endsWith('/DECISIONS_20261012.md')),decisionID=decisions.project+':doc:'+decisions.path;
render('lisan','documents');const preview=open(decisionID),a=byID.get(decisionID);
assert(a.text.length>40000);assert(!preview.includes('Preview shortened'));assert(preview.includes(escape(a.text.trim().split('\n').at(-1))),'Full safe dated history reaches its final line');assert(a.text.includes('47.'));assert(preview.includes('Open original file'));
const valis=definition.documents.find(d=>d.path.endsWith('/RESEARCH_VALIS_20261013.md'));
assert.equal(valis.bytes,16241);assert.equal(valis.sha256,'1104a098148eb26296a60e4db41eb6caa66c575aeba98b23ac4cab130ab0f8eb');
renderStoryWithDocument('lisan:doc:'+valis.path);const valisViewer=open('lisan:doc:'+valis.path);assert(valisViewer.includes('Six integration proposals remain proposals'));
checks++;
const echoID=definition.documents.find(d=>d.path.endsWith('/SEED_09_THE_ECHO_20261013.md')).project+':doc:'+definition.documents.find(d=>d.path.endsWith('/SEED_09_THE_ECHO_20261013.md')).path;
const echoHTML=renderStoryWithDocument(echoID,'The Echo');assert(echoHTML.includes('data-open="'+escape(echoID)+'"'));assert(echoHTML.includes('No panels yet.'));
const songHTML=render('lisan','storyboard','The Echo');assert(!songHTML.includes('data-open="'+escape(echoID)+'"'),'Search stays scoped to selected song; Echo remains in its prose story');
const honHTML=render('hon','storyboard','The Echo');assert(!honHTML.includes('data-open="'+escape(echoID)+'"'));
checks++;
assert.deepEqual(snapshot(),before);assert.equal(page.writes.length,0);checks++;
const result={passed:true,checks,writerDocuments:definition.documents.length-1,sharedMethodDocuments:1,stories:stories.length,safePublications:definition.documents.filter(d=>d.publication).length,excludedSources:definition.excludedSources.length,exactAssociations:catalog.writerDevelopment.associations.length,storageWrites:0,browserVisualQA:false,evidenceLimit:'Actual renderer and bound click handlers exercised with DOM/storage doubles; no browser visual rendering, screenshots or native details/anchor behavior tested.'};
if(process.argv.includes('--evidence-stdout'))result.rendererDOMDoubleMarkup=markup;
console.log(JSON.stringify(result));
