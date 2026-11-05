/* Mission Control hash links stay on the current viewer, under file and HTTP.
   Uses the real catalog and library with the existing DOM double; no browser QA. */
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const clone=value=>JSON.parse(JSON.stringify(value));
const source=fs.readFileSync(path.join(__dirname,'library.js'),'utf8');
const raw=fs.readFileSync(path.join(__dirname,'catalog.js'),'utf8');
const catalog=JSON.parse(raw.slice(raw.indexOf('=')+1).trim().replace(/;$/,''));
const byID=new Map(catalog.assets.map(a=>[a.id,a]));
const REVIEW_KEY='cfa-visual-review-v1',FAVORITES_KEY='cfa-visual-favorites-v1',EXPORT_KEY='cfa-visual-export-v1';
const existing=fs.readFileSync(path.join(__dirname,'test_collections_navigation.cjs'),'utf8');
let bootSource=existing.slice(existing.indexOf('function boot()'),existing.indexOf('const page = boot()'));
const oldHook='window.__collectionsTest={normalVisible,collectionCards,collectionGroups,sharedCharacterReferences,castExplorer,castHubGroups,castWorkingGroups,parseHash,detailAlbumGroups,renderMain,expandedCollections,reviews,reviewRecord,reviewPayload,basketPayload,setState(p){Object.assign(state,p);},getState(){return state;}};';
const hook='window.__collectionsTest={C,safeMissionHref,missionTaskLinks,parseHash,renderMain,falconReferenceGroups,expandedCollections,reviewPayload,basketPayload,getCurrentID(){return currentID;},viewerHTML(){return dialog.innerHTML;},viewerOpen(){return dialog.open;},setState(p){Object.assign(state,p);},getState(){return state;},clickPreview(id){const button=[...document.querySelectorAll("[data-open]")].find(b=>b.dataset.open===id);if(!button)throw new Error("Preview is bound: "+id);button.click();}};';
assert(bootSource.includes(oldHook),'The shared DOM harness hook is present');
bootSource=bootSource.replace(oldHook,hook);
const patches=[
  ['function boot() {','function boot(viewerURL) {\n  const viewer=new URL(viewerURL),scriptURL=new URL("visual_library/library.js",viewer);'],
  ["currentScript:{src:'file:///D:/Documents/CFA/docs/notes/explorable_world/comfy/projects/visual_library/library.js'},",'URL:viewer.href,currentScript:{src:scriptURL.href},'],
  ["const location = {hash:'#hon/all'};",'const location = {href:viewer.href,hash:viewer.hash};'],
  ['C:window.REVIEW_CATALOG, location,writes,storage,scrolls,','C:window.REVIEW_CATALOG, location,document,scriptURL,writes,storage,scrolls,']
];
for(const [before,after] of patches){assert(bootSource.includes(before),'Shared harness adaptation exists: '+before);bootSource=bootSource.replace(before,after);}
const boot=new Function('source','catalog','byID','clone','assert','vm','REVIEW_KEY','FAVORITES_KEY','EXPORT_KEY',bootSource+';return boot;')(source,catalog,byID,clone,assert,vm,REVIEW_KEY,FAVORITES_KEY,EXPORT_KEY);
const stablePayload=value=>{const payload=clone(value);delete payload.exported;return payload;};
const decodeHTML=value=>value.replace(/&amp;/g,'&').replace(/&quot;/g,'"').replace(/&#39;/g,"'");
function renderedHref(html,label){
  const links=[...html.matchAll(/<a\b[^>]*href="([^"]+)"[^>]*>(.*?)<\/a>/gs)];
  const link=links.find(m=>m[2].replace(/<[^>]*>/g,'').startsWith(label));
  assert(link,'Rendered Mission Control link: '+label);return decodeHTML(link[1]);
}
const viewerURLs=[
  'file:///D:/Documents/CFA/docs/notes/explorable_world/comfy/projects/index.html#hon/mission_control',
  'http://localhost:8765/creative-studio/index.html#hon/mission_control'
];
const routeDefinitions=[
  {label:'All 40 additional images',album:'hon:falcon-group1-extension40',count:40},
  {label:'Complete 90-image group',album:'hon:falcon-group1-current90',count:90}
];
const checkedOrigins=[];let routeChecks=0;
for(const viewerURL of viewerURLs){
  const page=boot(viewerURL),api=page.api,currentViewer=new URL(viewerURL);
  assert.equal(page.document.URL,viewerURL,'The harness supplies the actual document URL');
  const assetsBefore=clone(api.C.assets),albumsBefore=clone(api.C.albums);
  const reviewsBefore=stablePayload(api.reviewPayload()),basketBefore=stablePayload(api.basketPayload(true));
  const storageBefore=Object.fromEntries(page.storage);
  const task=api.C.missionControl.tasks.find(t=>t.id==='grok-falcon-extension40-available');assert(task,'The live extension task exists');
  assert.equal(task.additionalCount,40);assert.equal(task.receivedCount,90);
  const first50=api.C.albums.find(a=>a.id==='hon:falcon-group1').assetIDs;
  const additional40=api.C.albums.find(a=>a.id==='hon:falcon-group1-extension40').assetIDs;
  const current90=api.C.albums.find(a=>a.id==='hon:falcon-group1-current90').assetIDs;
  assert.equal(new Set(current90).size,90);assert.equal(new Set(additional40).size,40);
  assert.deepEqual([...new Set([...first50,...additional40])].sort(),[...current90].sort(),'The 90-image route reuses the original 50 and adds exactly 40');
  assert(additional40.every(id=>!first50.includes(id)),'The additional route does not ask for the first 50 again');
  api.setState({project:'hon',view:'mission_control',album:'',search:''});api.renderMain();
  const missionHTML=page.html();
  for(const definition of routeDefinitions){
    const link=task.links.find(l=>l.label===definition.label);assert(link);
    const expected=new URL(link.href,currentViewer).href;
    assert.equal(api.safeMissionHref(link.href),expected);
    assert.equal(renderedHref(missionHTML,definition.label),expected,'Rendered link retains the current HTML pathname');
    const target=new URL(expected);
    assert.equal(target.pathname,currentViewer.pathname);assert.equal(target.origin,currentViewer.origin);assert.equal(target.protocol,currentViewer.protocol);
    assert(!target.pathname.endsWith('/visual_library/'),'Hash navigation must not resolve to the script directory');
    // The same fix works when only document.URL is available to the browser adapter.
    const savedHref=page.location.href;delete page.location.href;
    assert.equal(api.safeMissionHref(link.href),expected,'Actual document URL is the fallback for hash-only navigation');page.location.href=savedHref;
    // Follow the rendered link through the real hash parser and scoped storyboard renderer.
    page.location.href=target.href;page.location.hash=target.hash;page.document.URL=target.href;
    api.expandedCollections.clear();api.setState({search:'',storyStage:'all',storyTheme:'all'});api.parseHash();api.renderMain();
    assert.equal(api.getState().project,'hon');assert.equal(api.getState().view,'storyboard');assert.equal(api.getState().album,definition.album);
    const album=api.C.albums.find(a=>a.id===definition.album);assert.equal(album.assetIDs.length,definition.count);
    const visibleIDs=album.assetIDs.filter(id=>{const a=api.C.assets.find(a=>a.id===id);return a&&!a.archived&&api.reviewPayload().items.find(r=>r.id===id)?.status!=='remove';});
    const groups=api.falconReferenceGroups(undefined,definition.album);
    assert.equal(groups.length,1);assert.equal(groups[0].items.length,visibleIDs.length,'The actual route honors saved removal choices while retaining the full album');
    assert.equal(new Set(groups[0].items.map(a=>a.id)).size,visibleIDs.length);
    page.toggle(definition.album);
    for(const child of groups[0].children)page.toggle(child.id);
    const actions=[...page.html().matchAll(/data-open="([^"]+)"/g)].map(m=>m[1]);
    for(const id of actions)assert(byID.has(id),'Every media or document action resolves to a catalog record: '+id);
    // Storyboard briefing documents share data-open with image previews.
    const leaves=actions.filter(id=>byID.get(id).kind!=='document');
    assert.equal(leaves.length,visibleIDs.length,'All visible scoped thumbnails become available inside their category drawers');
    assert.deepEqual([...leaves].sort(),[...visibleIDs].sort(),'No unrelated or removed reference is pulled into this route');
    api.clickPreview(leaves[0]);assert.equal(api.getCurrentID(),leaves[0]);assert(api.viewerOpen(),'Thumbnail opens the existing viewer');
    const viewerHTML=api.viewerHTML();
    for(const control of ['reference-likeness-rating','reference-scene-quality-rating','reference-storyboard-stage'])assert(viewerHTML.includes('id="'+control+'"'),'Existing review control is retained: '+control);
    assert(viewerHTML.includes('id="full-image"'),'The existing image preview is used');routeChecks++;
    // Restore the page address before checking the next Mission Control destination.
    page.location.href=viewerURL;page.location.hash=currentViewer.hash;page.document.URL=viewerURL;
  }
  const briefTask=api.C.missionControl.tasks.find(t=>t.id==='gemini-notebook-system');
  const brief=briefTask.links.find(l=>l.label==='Notebook setup and current limitations');assert(brief);
  const briefExpected=new URL(brief.href,new URL('.',page.scriptURL)).href;
  assert.equal(api.safeMissionHref(brief.href),briefExpected,'Relative prepared files retain their script-directory base');
  assert.equal(renderedHref(api.missionTaskLinks(briefTask),brief.label),briefExpected);
  for(const unsafe of ['', 'javascript:alert(1)', 'https://example.test/private', 'data:text/plain,test', '//example.test/x', '/absolute/path', '../unsafe\\path', '../%0Ahidden', '../%5Cunsafe', '#hon/storyboard/%ZZ'])assert.equal(api.safeMissionHref(unsafe),'','Unsafe or malformed link is rejected: '+unsafe);
  const unsafeFixture={links:[{label:'Blocked javascript',href:'javascript:alert(1)'},{label:'Blocked malformed',href:'#hon/storyboard/%ZZ'}]};
  assert.equal(api.missionTaskLinks(unsafeFixture),'','Rejected links do not render clickable anchors');
  assert.deepEqual(clone(api.C.assets),assetsBefore,'Navigation leaves media metadata unchanged');
  assert.deepEqual(clone(api.C.albums),albumsBefore,'Navigation leaves memberships and counts unchanged');
  assert.deepEqual(stablePayload(api.reviewPayload()),reviewsBefore,'Opening thumbnails does not rescore or approve references');
  assert.deepEqual(stablePayload(api.basketPayload(true)),basketBefore,'Navigation leaves export choices unchanged');
  assert.deepEqual(Object.fromEntries(page.storage),storageBefore,'No stored review or selection was rewritten');assert.equal(page.writes.length,0,'No boot or navigation writes');
  checkedOrigins.push(currentViewer.protocol==='file:'?'file:':'localhost http:');
}
console.log(JSON.stringify({passed:true,origins:checkedOrigins,routeChecks,routeCounts:[40,90],hashLinksTargetCurrentViewer:true,relativeBriefBasePreserved:true,unsafeLinksRejected:true,likenessAndSceneControls:true,reviewWrites:0,browserVisualQA:false}));
