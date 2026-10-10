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
const hook='window.__collectionsTest={C,collaboratorsWorkspace,collaboratorProfile,providerKey,renderMain,reviewPayload,setState(p){Object.assign(state,p);},getState(){return state;},chooseProvider(id){const button=[...document.querySelectorAll("[data-collaborator-provider]")].find(b=>b.dataset.collaboratorProvider===id);if(!button)throw Error("Tab missing: "+id);button.click();},chooseSection(id){const button=[...document.querySelectorAll("[data-collaborator-section]")].find(b=>b.dataset.collaboratorSection===id);if(!button)throw Error("Section missing: "+id);button.click();},keySection(key){const button=[...document.querySelectorAll("[data-collaborator-section]")].find(b=>b.dataset.collaboratorSection===state.collaboratorSection);let prevented=false;button.onkeydown({key,preventDefault(){prevented=true;}});return prevented;}};';
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
 assert.equal(api.getState().collaboratorSection,'work','Each provider opens on work and handoffs');
 let html=page.html();
 assert(html.includes('data-collaborator-profile="'+p.id+'"'),'Selected provider is rendered: '+p.name);
 assert(html.includes('role="tablist"')&&html.includes('role="tabpanel"'),'Nested sections expose accessible tab roles');
 for(const id of ['work','profile','scorecard','roles'])assert(html.includes('data-collaborator-section="'+id+'"'),'Section is reachable: '+id);
 assert(!html.includes('class="role-scorecard-table"')&&!html.includes('class="collaborator-profile"'),'Default work view excludes résumé and role table');
 if(p.id==='ComfyUI')assert(html.indexOf('class="production-workflow"')<html.indexOf('collaborator-work-links'),'Existing workflow cards remain first');
 if(p.id==='Grok')assert(html.indexOf('class="mission-task"')<html.indexOf('collaborator-work-links'),'Current Grok handoffs remain first');
 if(p.id==='PanhandlerNova'){
  assert(html.includes('data-mission-export="PanhandlerNova"'),'Legacy review export remains compatible');
  assert(html.includes('Manual CFA/Panhandlers progress return')||html.includes('Received by Claude')||html.includes('Done'),'Completed Claude task remains visible');
 }
 api.chooseSection('profile');html=page.html();
 assert.equal(api.getState().collaboratorSection,'profile');
 assert(html.includes('class="collaborator-profile"')&&!html.includes('class="role-scorecard-table"'),'Profile remains separate from role grading');
 assert(html.includes('Self-reported strengths')&&html.includes('Recorded capability evidence'),'Claimed and recorded capabilities are separate');
 assert(html.includes('Role preferences are self-reported, not earned grades.'));
 assert(html.includes('Communication & mailbox'),'Communication details remain available');
 if(p.id==='DeepSeek'){
  const tools=api.collaboratorProfile(p.id).match(/<div class="tools">(.*?)<\/div>/s)[1];
  assert(tools.includes('DeepSeek I_AM'),'The named DeepSeek identity link remains');
  assert(!tools.includes('Read authored I_AM'),'The duplicate generic identity link is omitted');
  assert.equal((tools.match(/<a\b[^>]*href="[^"]*\/identity\/deepseek\/I_AM\.md"/g)||[]).length,1,'The DeepSeek introduction has one action link');
 }
 api.chooseSection('scorecard');html=page.html();
 assert.equal(api.getState().collaboratorSection,'scorecard');
 assert(html.includes('class="role-scorecard-table"')&&!html.includes('class="collaborator-profile"'),'Grades use a separate compact table');
 assert.equal((html.match(/<th scope="row">/g)||[]).length,p.scorecards.length,'Every role has one scannable row');
 assert.equal((html.match(/<details class="scorecard-evidence">/g)||[]).length,p.scorecards.length,'Evidence and dimensions remain behind collapsed details');
 assert(!/<details[^>]*\sopen(?:\s|>)/.test(html),'Assessment dimensions are collapsed initially');
 for(const card of p.scorecards)assert(html.includes(card.grade||'Ungraded'));
 if(p.id==='Grok')assert(html.includes('A-')&&html.includes('Human assessment')&&html.includes('Ziggy'),'Actual human assessment remains attributed');
 api.chooseSection('roles');html=page.html();
 assert.equal(api.getState().collaboratorSection,'roles');
 assert(html.includes('Production readiness · B or better'),'Scene readiness gate remains available');
 for(const role of roster.roleDefinitions)assert(html.includes('<summary>'+role.label+'</summary>'),'Role definition remains accessible: '+role.label);
 assert(api.keySection('Home'));assert.equal(api.getState().collaboratorSection,'work','Home returns to the first nested tab');
 assert(api.keySection('End'));assert.equal(api.getState().collaboratorSection,'roles','End selects the last nested tab');
 assert(api.keySection('ArrowRight'));assert.equal(api.getState().collaboratorSection,'work','Right arrow wraps across nested tabs');
 assert(api.keySection('ArrowLeft'));assert.equal(api.getState().collaboratorSection,'roles','Left arrow wraps across nested tabs');
}
assert.equal(api.providerKey('Claude'),'PanhandlerNova','Claude maps to the existing provider key');
const grades=roster.providers.flatMap(p=>(p.scorecards||[]).filter(c=>c.grade).map(c=>({provider:p.id,...c})));
assert.equal(grades.length,1,'Only the actual human assessment earns a grade');
assert.equal(grades[0].provider,'Grok');assert.equal(grades[0].category,'casting');assert.equal(grades[0].grade,'A-');assert.equal(grades[0].assessedBy,'Ziggy');
assert.equal(grades[0].status,'human_assessment');
for(const card of roster.providers.flatMap(p=>p.scorecards||[]))for(const v of Object.values(card.metrics||{}))assert.equal(v,null,'Benchmark measurements are unknown until tested');
const after=clone(api.reviewPayload());delete after.exported;assert.deepEqual(after,initial,'Switching collaborator tabs does not mutate reviews or scene grades');
assert.deepEqual(clone(api.C.assets),originals,'Profiles do not replace source asset metadata');
console.log(JSON.stringify({passed:true,profiles:roster.providers.length,tabHandlers:roster.providers.length,nestedSections:4,nestedSectionChecks:roster.providers.length*4,keyboardNavigation:true,actualHumanGrades:grades.length,browserVisualQA:false}));
