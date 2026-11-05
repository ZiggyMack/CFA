/* Explicit Grok video planning stays separate from legacy still plans and source attribution. */
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const clone=value=>JSON.parse(JSON.stringify(value));
const source=fs.readFileSync(path.join(__dirname,'library.js'),'utf8');
const catalog=JSON.parse(fs.readFileSync(path.join(__dirname,'catalog.js'),'utf8').replace(/^.*?=\s*/s,'').replace(/;\s*$/,''));
const byID=new Map(catalog.assets.map(a=>[a.id,a]));
const REVIEW_KEY='cfa-visual-review-v1',FAVORITES_KEY='cfa-visual-favorites-v1',EXPORT_KEY='cfa-visual-export-v1';
const harness=fs.readFileSync(path.join(__dirname,'test_collections_navigation.cjs'),'utf8');
let bootSource=harness.slice(harness.indexOf('function boot()'),harness.indexOf('const page = boot()'));
const start=bootSource.indexOf('window.__collectionsTest={'),end=bootSource.indexOf(';})();',start);
bootSource=bootSource.slice(0,start)+'window.__collectionsTest={C,normalizedPlan,reviewRecord,updateReview,reviewPayload,importReview,shotPlanControls,shotHandoffPayload,exportShotHandoff,missionControl,collaboratorsWorkspace,openViewer,renderMain,setState(p){Object.assign(state,p);},getState(){return state;},node(s){return document.querySelector(s);},all(s){return document.querySelectorAll(s);}}'+bootSource.slice(end);
bootSource=bootSource.replace('const selectAll = selector => {','const selectAll = selector => { if(selector.endsWith(":checked"))return selectAll(selector.slice(0,-8)).filter(n=>n.checked);');
bootSource=bootSource.replace('const elements = new Set(), nodes = new Map(), writes = [], scrolls = [];',
  'const elements = new Set(), nodes = new Map(), writes = [], scrolls = [], downloads = [], blobs = new Map(); class TestBlob {constructor(parts){this.text=parts.join("");}} class TestURL extends URL {static createObjectURL(blob){const url="blob:test-"+blobs.size;blobs.set(url,blob);return url;}static revokeObjectURL(){}}')
  .replace('click() {if (this.disabled) return;', 'click() {if (this.disabled) return; if(this.tag === "a")downloads.push({name:this.download,text:blobs.get(this.href).text});')
  .replace('location,URL,Intl,console,','location,URL:TestURL,Blob:TestBlob,Intl,console,')
  .replace('location,writes,storage,scrolls,','location,writes,storage,scrolls,downloads,');
const boot=new Function('source','catalog','byID','clone','assert','vm','REVIEW_KEY','FAVORITES_KEY','EXPORT_KEY',bootSource+';return boot;')(source,catalog,byID,clone,assert,vm,REVIEW_KEY,FAVORITES_KEY,EXPORT_KEY);
const page=boot(),api=page.api;
const asset=api.C.assets.find(a=>a.id==='HD-FALCON-194702e9e041362d');
assert(asset,'Exact existing source fixture');
const sourceBefore=clone(asset),oldPlan={status:'planned',destinations:['Grok'],idea:'Preserve this exact idea.',prompt:'Original prompt.'};
api.updateReview(asset.id,{status:'keep',variant:'prime',note:'Exact existing note.',likenessRating:4,sceneQualityRating:5,shotPlan:oldPlan});
const before=clone(api.reviewRecord(asset.id));
api.openViewer(asset.id);
assert(api.shotPlanControls(asset).includes('data-shot-destination="Grok"')&&api.shotPlanControls(asset).includes('Grok stills'));
assert(api.shotPlanControls(asset).includes('data-shot-destination="grok_video"')&&api.shotPlanControls(asset).includes('Grok video'));
api.all('[data-shot-destination]').forEach(n=>n.checked=n.dataset.shotDestination==='Grok');
const video=api.node('[data-shot-destination="grok_video"]');video.checked=true;video.onchange();
assert.deepEqual(clone(api.reviewRecord(asset.id).shotPlan),{...oldPlan,destinations:['Grok','grok_video']},'Explicit video selection preserves the old route and plan text');
for(const field of ['status','note','variant','likenessRating','sceneQualityRating'])assert.deepEqual(api.reviewRecord(asset.id)[field],before[field],'Plan route preserves '+field);
assert.deepEqual(clone(asset),sourceBefore,'Planning cannot change source attribution or source bytes');
assert.deepEqual(clone(api.normalizedPlan({...oldPlan,status:'sent',destinations:['grok_video','grok_video','invented']})),{...oldPlan,destinations:['grok_video']},'Import keeps the explicit video route and cannot claim dispatch');
api.setState({destination:'grok_video',exportIntent:'prime',search:'',project:'hon'});
let out=clone(api.shotHandoffPayload());
assert(out.items.some(x=>x.id===asset.id&&x.sha256===asset.sha256));
assert.equal(out.status,'planned; not sent or generated');
assert(out.items.every(x=>x.shotPlan.destinations.includes('grok_video')),'Video handoff only includes explicit video plans');
api.updateReview(asset.id,{shotPlan:{...oldPlan,destinations:['grok_video']}});
api.setState({destination:'Grok'});
assert(!api.shotHandoffPayload().items.some(x=>x.id===asset.id),'Legacy still export never silently absorbs video');
api.setState({collaborator:'Grok',collaboratorSection:'work'});
assert(api.collaboratorsWorkspace().includes('data-mission-export="grok_video"'),'Grok workspace exposes its video handoff');
assert(api.missionControl().includes('data-mission-export="grok_video"'),'Grok dashboard includes the video route');
api.setState({view:'mission_control',search:'',destination:'Grok'});api.renderMain();
api.node('[data-mission-export="grok_video"]').click();
const download=page.downloads.at(-1);
assert.equal(download.name,'cfa-shot-handoff-all-grok_video.txt','The actual dashboard button exports a distinct video filename');
assert(download.text.includes('Destination: Grok video')&&download.text.includes(asset.id));
assert(download.text.includes('planned; not sent or generated'),'A download cannot claim provider dispatch');
assert.equal(api.getState().destination,'Grok','Export restores the prior route filter');
api.setState({destination:'grok_video'});api.exportShotHandoff('json');
assert.equal(page.downloads.at(-1).name,'cfa-shot-handoff-hon-grok_video.json');
assert.equal(JSON.parse(page.downloads.at(-1).text).destination,'grok_video');
const exported=clone(api.reviewPayload()),reloaded=boot();reloaded.api.importReview(exported);
assert.deepEqual(clone(reloaded.api.reviewRecord(asset.id).shotPlan.destinations),['grok_video'],'Review export/import retains route selection');
console.log('Grok video route: selection, exact export, source preservation, dashboard and portable round-trip passed.');
