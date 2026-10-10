/* Actual collaborator tab handlers against the existing collection DOM double.
   Verifies profiles and capability/grade separation, not browser layout. */
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const clone=value=>JSON.parse(JSON.stringify(value));
const root=__dirname,source=fs.readFileSync(path.join(root,'library.js'),'utf8');
const raw=fs.readFileSync(path.join(root,'catalog.js'),'utf8');
const catalog=JSON.parse(raw.slice(raw.indexOf('=')+1).trim().replace(/;$/,''));
const byID=new Map(catalog.assets.map(a=>[a.id,a]));
const REVIEW_KEY='cfa-visual-review-v1',FAVORITES_KEY='cfa-visual-favorites-v1',EXPORT_KEY='cfa-visual-export-v1';
const existing=fs.readFileSync(path.join(root,'test_collections_navigation.cjs'),'utf8');
const bootSource=existing.slice(existing.indexOf('function boot()'),existing.indexOf('const page = boot()'));
const oldHook='window.__collectionsTest={collectionCards,collectionGroups,sharedCharacterReferences,castExplorer,detailAlbumGroups,renderMain,expandedCollections,reviews,reviewRecord,reviewPayload,basketPayload,setState(p){Object.assign(state,p);},getState(){return state;}};';
const hook='window.__collectionsTest={C,collaboratorsWorkspace,collaboratorProfile,providerKey,renderMain,reviewPayload,setState(p){Object.assign(state,p);},getState(){return state;},chooseProvider(id){const button=[...document.querySelectorAll("[data-collaborator-provider]")].find(b=>b.dataset.collaboratorProvider===id);if(!button)throw Error("Tab missing: "+id);button.click();}};';
assert(bootSource.includes(oldHook));
const boot=new Function('source','catalog','byID','clone','assert','vm','REVIEW_KEY','FAVORITES_KEY','EXPORT_KEY',bootSource.replace(oldHook,hook)+';return boot;')(source,catalog,byID,clone,assert,vm,REVIEW_KEY,FAVORITES_KEY,EXPORT_KEY);
const page=boot(),api=page.api,roster=api.C.providerScorecards;
assert(roster&&Array.isArray(roster.providers),'Final provider config is in the catalog');
assert.equal(roster.providers.length,9,'Nine collaborator/tool surfaces have explicit profiles');
assert(!api.C.categories.some(([id])=>/roles|scorecards|providers/.test(id)),'Roles remain inside Collaborators');
const initial=clone(api.reviewPayload()),originals=clone(api.C.assets);delete initial.exported;
api.setState({view:'collaborators',project:'hon',search:''});api.renderMain();
for(const p of roster.providers){
 api.chooseProvider(p.id);
 assert.equal(api.getState().collaborator,p.id,'Actual bound tab handler selects '+p.name);
 const html=page.html();
 assert(html.includes('data-collaborator-profile="'+p.id+'"'),'Selected profile is rendered: '+p.name);
 assert(html.includes('Role scorecards')&&html.includes('Roles · what each review covers'));
 assert(html.includes('Self-reported strengths')&&html.includes('Recorded capability evidence'),'Claimed and recorded capabilities are separate');
 if(p.id==='ComfyUI')assert(html.indexOf('class="production-workflow"')<html.indexOf('data-collaborator-profile='),'Existing workflow cards remain first');
 if(p.id==='Grok')assert(html.indexOf('class="mission-task"')<html.indexOf('data-collaborator-profile='),'Current Grok handoffs remain first');
 if(p.id==='PanhandlerNova'){
  assert(html.includes('data-mission-export="PanhandlerNova"'),'Legacy review export remains compatible');
  assert(html.includes('Manual CFA/Panhandlers progress return')||html.includes('Received by Claude')||html.includes('Done'),'Completed Claude task remains visible');
 }
}
assert.equal(api.providerKey('Claude'),'PanhandlerNova','Claude maps to the existing provider key');
const grades=roster.providers.flatMap(p=>(p.scorecards||[]).filter(c=>c.grade).map(c=>({provider:p.id,...c})));
assert.equal(grades.length,1,'Only the actual human assessment earns a grade');
assert.equal(grades[0].provider,'Grok');assert.equal(grades[0].category,'casting');assert.equal(grades[0].grade,'A-');assert.equal(grades[0].assessedBy,'Ziggy');
assert.equal(grades[0].status,'human_assessment');
for(const card of roster.providers.flatMap(p=>p.scorecards||[]))for(const v of Object.values(card.metrics||{}))assert.equal(v,null,'Benchmark measurements are unknown until tested');
const after=clone(api.reviewPayload());delete after.exported;assert.deepEqual(after,initial,'Switching collaborator tabs does not mutate reviews or scene grades');
assert.deepEqual(clone(api.C.assets),originals,'Profiles do not replace source asset metadata');
console.log(JSON.stringify({passed:true,profiles:roster.providers.length,tabHandlers:roster.providers.length,actualHumanGrades:grades.length,browserVisualQA:false}));
