/* Execute the actual renderer against the source-backed proposed/published data. */
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const L=__dirname,clone=v=>JSON.parse(JSON.stringify(v)),REVIEW_KEY='cfa-visual-review-v1',FAVORITES_KEY='cfa-visual-favorites-v1';
const file=process.argv[2]||path.join(L,'catalog.js'),raw=fs.readFileSync(file,'utf8');
const catalog=JSON.parse(file.endsWith('.js')?raw.slice(raw.indexOf('=')+1).trim().replace(/;$/,''):raw),assets=catalog.assets;
const prior=JSON.stringify(catalog),source=fs.readFileSync(path.join(L,'source_foundation.js'),'utf8')+'\n'+fs.readFileSync(path.join(L,'library.js'),'utf8');
const harness=fs.readFileSync(path.join(L,'test_reference_scope.cjs'),'utf8');
const old='window.__scopeTest={openViewer,reviewRecord,reviewPayload,importReview,exportReference,inReviewQueue,whenFileWritesSettle(){return fileWriteChain;}};';
const replacement='window.__scopeTest={C,route,renderMain,structureGaps,storyStructure,selectedStoryboardStory,reviewPayload,setState(v){Object.assign(state,v);}};';
const boot=harness.slice(harness.indexOf('function boot('),harness.indexOf('async function main()')).replace(old,replacement);
const createPage=input=>new Function('source','catalog','clone','assert','vm','REVIEW_KEY','FAVORITES_KEY','assets',boot+';return boot;')(source,input,clone,assert,vm,REVIEW_KEY,FAVORITES_KEY,input.assets)({},input);
const page=createPage(catalog);
const api=page.api,html=()=>page.node('#main').innerHTML,reviews=JSON.stringify(api.reviewPayload());
const shotIDs=value=>[...value.matchAll(/data-structure-shot="([^"]+)"/g)].map(match=>match[1]);
const selectedPill=(value,key)=>new RegExp('id="structure-status-'+key+'"[^>]*aria-pressed="true"').test(value);
const pillCount=(value,key)=>Number(value.match(new RegExp('id="structure-status-'+key+'"[^>]*>[^<]* · (\\d+)</button>'))?.[1]);
api.route('hon','storyboard','structure:hon:strictly-business');
assert.equal((html().match(/data-structure-shot=/g)||[]).length,70);
assert.equal((html().match(/data-structure-sequence=/g)||[]).length,14);
assert.equal((html().match(/data-foundation="no_frame"/g)||[]).length,70);
assert.equal((html().match(/<details class="structure-context-fields">/g)||[]).length,70,'A–D context is collapsed for every real shot by default');
assert(!html().includes('class="structure-context-fields" open'));
for(const phase of ['creative','generation','results']){
  assert.equal((html().match(new RegExp('<details class="structure-'+phase+'-fields">','g'))||[]).length,70,phase+' is collapsed for every real shot by default');
  assert(!html().includes('class="structure-'+phase+'-fields" open'));
}
const coverage=html().match(/<section class="structure-plan-coverage"[\s\S]*?<\/section>/)?.[0]||'';
assert(coverage.includes('Story plan & coverage'));
assert(coverage.includes('Written coverage does not mean every shot has an image or an aligned song cue.'));
const honRecord=catalog.storyboardStructure.stories.find(story=>story.storyID==='hon:strictly-business');
assert(coverage.includes('data-open="'+honRecord.source.assetID+'"'),'Story coverage opens its recorded source');
const s07=html().split('data-structure-shot="S07-4"')[1].split('data-structure-shot="S07-5"')[0];
const s07Data=honRecord.shots.find(shot=>shot.shotID==='S07-4');
const phaseOrder=['structure-context-fields','structure-creative-fields','structure-generation-fields','structure-results-fields','structure-take-history','structure-kitchen'].map(name=>s07.indexOf('class="'+name+'"'));
assert(phaseOrder.every((position,index)=>position>=0&&(!index||position>phaseOrder[index-1])),'Kitchen is last, after takes/results/review and its retained history');
assert(!html().includes('<details class="structure-history"'),'No duplicate standalone history drawer');
assert(s07.includes('<summary>Takes, results &amp; review · 10–11</summary>'));
assert(s07.includes('Earlier results and human reviews are retained; timings are never moved automatically.'));
for(const [phase,keys] of [['creative',['start_frame','lighting','camera','character','background','beats','cue','prompt_still']],['generation',['prompt_clip','settings']],['results',['results','acceptance']]]){
  const group=s07.split('class="structure-'+phase+'-fields"')[1].split('</details>')[0];
  assert.deepEqual([...group.matchAll(/data-structure-field="([^"]+)"/g)].map(match=>match[1]),keys,'Phase membership uses stable keys');
}
assert(s07.includes('Coverage notes · '+s07Data.coverageAsOf));
assert(!s07.includes('<p class="notice">'),'Per-shot repeated maturity notice is removed');
assert(!s07.includes('fields with content'),'Per-shot generic field count is removed');
assert(s07.includes('Kitchen / handoff structure · 0/12 sections written'),'Unwritten kitchen is counted as zero written sections');
const linkedStart=s07.indexOf('class="structure-sources structure-linked-references"'),contextStart=s07.indexOf('class="structure-context-fields"');
assert(linkedStart>=0&&s07.indexOf('class="structure-coverage-update"')>linkedStart&&s07.indexOf('class="structure-coverage-update"')<contextStart,'Coverage notes live in Linked references');
assert(s07.indexOf('class="structure-sources source-foundation"')>linkedStart&&s07.indexOf('class="structure-sources source-foundation"')<contextStart,'Source foundation lives in Linked references');
assert(s07.indexOf('class="structure-context"')>contextStart&&s07.indexOf('class="structure-context"')<s07.indexOf('class="structure-creative-fields"'),'Sequence context lives inside A–D');
assert(s07.includes('the card&#39;s &#39;no accepted anatomy&#39; hold is superseded'));
assert(s07.indexOf('class="structure-coverage-update"')<s07.indexOf('data-structure-field="lineage"'),'Dated coverage precedes older field wording');
assert(s07.includes('no accepted Chewbacca production reference exists.'),'Older field text remains traceable');
assert(s07.includes('data-open="'+s07Data.coverageEvidence.assetID+'"')&&s07.includes('data-open="'+s07Data.source.assetID+'"'),'Both dated source documents remain linked');
const startField=s07.split('data-structure-field="start_frame"')[1].split('</section>')[0];
assert(startField.indexOf('Planning context · no field-specific material recorded')<startField.indexOf('class="structure-evidence"'),'Empty starting frame labels planning context before its source link');
const foundation=page.node('#structure-foundation');foundation.value='detailed';foundation.fire('change');
assert.equal((html().match(/data-structure-shot=/g)||[]).length,0);
const missingFoundation=page.node('#structure-foundation');missingFoundation.value='no_frame';missingFoundation.fire('change');
assert.equal((html().match(/data-structure-shot=/g)||[]).length,70);
assert(html().includes('Earlier shot-plan crosswalk'));
assert(html().includes('P-6b')&&html().includes('11 kitchen blocks documented'));
assert(html().includes('Intentionally not needed')&&html().includes('dental_mouth_only'));
assert(selectedPill(html(),'all'),'Field status starts with no restriction');
assert(html().includes('16 main storyboard fields; kitchen subfields are excluded'));
const hon=api.storyStructure(api.selectedStoryboardStory()),defs=catalog.storyboardStructure.fields;
const hasStatus=(shot,status)=>defs.some(def=>{
  const field=shot.fields.find(field=>field.key===def.key);
  return (field?.status||'unknown')===status;
});
page.node('#structure-status-missing').click();
assert.deepEqual(shotIDs(html()),hon.shots.filter(shot=>hasStatus(shot,'missing')).map(shot=>shot.shotID),'Missing filters the real main fields');
assert(selectedPill(html(),'missing'));
assert(html().includes('class="structure-field is-status-match"'),'Matching main fields have an accent');
assert(!html().includes('class="structure-status status-missing" data-'),'Individual field badges remain informational');
page.node('#structure-status-missing').click();
assert.equal(shotIDs(html()).length,70,'Clicking the active status clears it');
assert(selectedPill(html(),'all'));
assert(!html().includes('is-status-match'));
const focus=page.node('#structure-filter');focus.value='camera';focus.fire('change');
assert(!html().includes('data-structure-shot="S02-9"'),'Written camera is not in missing-camera focus');
api.setState({structureFilter:'prompt'});api.renderMain();
assert(html().includes('data-structure-shot="S02-6"')&&html().includes('data-structure-shot="S02-9"'));
assert(!html().includes('data-structure-shot="S02-8"'));
const sequence=page.node('#structure-sequence');sequence.value='S02';sequence.fire('change');
const scoped=hon.shots.filter(shot=>shot.sectionID==='S02'&&api.structureGaps(shot).prompt);
page.node('#structure-status-draft').click();
assert.deepEqual(shotIDs(html()),scoped.filter(shot=>hasStatus(shot,'draft')).map(shot=>shot.shotID),'Status intersects sequence, gap focus and source foundation');
assert.equal(pillCount(html(),'all'),scoped.length,'Counts use the other active filters');
assert.equal(pillCount(html(),'missing'),scoped.filter(shot=>hasStatus(shot,'missing')).length);
page.node('#structure-status-all').click();
assert.deepEqual(shotIDs(html()),scoped.map(shot=>shot.shotID),'All clears only the field status restriction');
assert.equal(page.node('#structure-sequence').value,'S02');
assert.equal(page.node('#structure-filter').value,'prompt');
assert.equal(page.node('#structure-foundation').value,'no_frame');
page.node('#structure-status-accepted').click();
assert.equal(shotIDs(html()).length,0,'A status with no main-field matches has an honest empty result');
assert(selectedPill(html(),'accepted'));
api.route('hon','storyboard','template');
assert(html().includes('data-structure-demo="true"'));
assert(html().includes('<h3>Kitchen / handoff structure</h3>')&&!html().includes('11 · Kitchen / handoff structure'),'Kitchen is a separate group, independent of main-field numbering');
assert(!html().includes('Writings ·'), 'Blank template cannot inherit story writings');
assert.equal((html().match(/data-structure-shot=/g)||[]).length,0);
assert.equal((html().match(/data-structure-field=/g)||[]).length,28);
assert(!html().includes('structure-foundation'),'Blank template has no source decisions');
assert(!html().includes('structure-status-all')&&!html().includes('is-status-match'),'Blank template has no filtering controls or selected-state accent');
assert(!html().includes('structure-context-fields')&&!html().includes('structure-plan-coverage')&&!html().includes('structure-planning-context'),'Blank template remains fully visible and has no real planning evidence');
assert(html().includes('<h3>Creative direction · 0–7</h3>')&&html().includes('<h3>Generation handoff · 8–9</h3>')&&html().includes('<h3>Takes, results &amp; review · 10–11</h3>'),'Blank template has the same phase headings without collapsed drawers');
const blankOrder=['Context &amp; references · A–D','Creative direction · 0–7','Generation handoff · 8–9','Takes, results &amp; review · 10–11','Kitchen / handoff structure'].map(label=>html().indexOf('<h3>'+label+'</h3>'));
assert(blankOrder.every((position,index)=>position>=0&&(!index||position>blankOrder[index-1])),'Blank template has the same Kitchen-last order');
assert(!html().includes('class="structure-creative-fields"')&&!html().includes('class="structure-results-fields"'));
assert(!html().includes('data-scene-field=')&&!html().includes('data-open="demo'));
api.route('lisan','storyboard','structure:lisan:story-01');
assert.equal(api.selectedStoryboardStory().id,'lisan:story-01');
assert.equal((html().match(/data-structure-shot=/g)||[]).length,38);
assert(selectedPill(html(),'all'),'Changing story resets field-status filtering');
assert.equal(JSON.stringify(api.C),prior,'Rendering never writes catalog metadata');
// Timestamp on export changes naturally; review records and scene reviews do not.
const a=JSON.parse(reviews),b=api.reviewPayload();
for(const k of ['items','sceneReviews','favorites','exportBasket'])assert.deepEqual(clone(b[k]),a[k]);
// Synthetic statuses exercise all seven options without editing any source records.
const fixture=clone(catalog),record=fixture.storyboardStructure.stories.find(story=>story.storyID==='hon:strictly-business');
const statusKeys=['missing','draft','present','verified','accepted','unknown','not_needed'];
record.shots=statusKeys.map((status,index)=>({...clone(hon.shots[0]),shotID:'status-'+status,sectionID:index<4?'A':'B',title:status,
  fields:defs.map(def=>({key:def.key,status,text:'Fixture '+status,evidence:[]})),
  kitchen:fixture.storyboardStructure.kitchenFields.map(def=>({key:def.key,status:status==='draft'?'accepted':'draft',text:'Kitchen only',evidence:[]}))}));
record.shots.find(shot=>shot.shotID==='status-unknown').fields=[];
record.sections=[{id:'A',title:'First section',shotIDs:record.shots.slice(0,4).map(shot=>shot.shotID)},
  {id:'B',title:'Second section',shotIDs:record.shots.slice(4).map(shot=>shot.shotID)}];
const fixtureBefore=JSON.stringify(fixture),fixturePage=createPage(fixture),fixtureHTML=()=>fixturePage.node('#main').innerHTML;
fixturePage.api.route('hon','storyboard','structure:hon:strictly-business');
for(const status of statusKeys){
  fixturePage.node('#structure-status-'+status).click();
  assert.deepEqual(shotIDs(fixtureHTML()),['status-'+status],status+' filters actual main-field maturity, excluding kitchen');
  assert.equal(pillCount(fixtureHTML(),status),1,'One shot counts once even with sixteen matching fields');
  assert(selectedPill(fixtureHTML(),status));
  assert.equal((fixtureHTML().match(/class="structure-field is-status-match"/g)||[]).length,16,'Only the sixteen matching main fields are highlighted');
  assert(fixtureHTML().includes('class="structure-context-fields" open'),'A–D expands when the active status matches its fields');
  for(const phase of ['creative','generation','results'])assert(fixtureHTML().includes('class="structure-'+phase+'-fields" open'),'Each matching phase opens under the status filter');
}
fixturePage.node('#structure-status-all').click();
assert.equal(shotIDs(fixtureHTML()).length,7);
fixturePage.api.setState({search:'not_needed'});fixturePage.api.renderMain();
assert.deepEqual(shotIDs(fixtureHTML()),['status-not_needed']);
assert.equal(pillCount(fixtureHTML(),'all'),1,'Search also scopes field-status counts');
assert.equal(pillCount(fixtureHTML(),'accepted'),0);
assert.equal(JSON.stringify(fixturePage.api.C),fixtureBefore,'Filtering never edits fixture records');
assert.equal(fixturePage.writes.length,0,'Filtering creates no review/storage writes');
// A match in numbered production fields must not unfold unrelated context.
const numberedFixture=clone(fixture),numberedRecord=numberedFixture.storyboardStructure.stories.find(story=>story.storyID==='hon:strictly-business');
numberedRecord.shots=numberedRecord.shots.slice(0,1);
numberedRecord.shots[0].fields=defs.map((def,index)=>({key:def.key,status:index<4?'draft':'missing',text:'Numbered fixture',evidence:[]}));
numberedRecord.sections=[{id:'A',title:'Numbered fields',shotIDs:[numberedRecord.shots[0].shotID]}];
const numberedPage=createPage(numberedFixture);numberedPage.api.route('hon','storyboard','structure:hon:strictly-business');
numberedPage.node('#structure-status-missing').click();
const numberedHTML=numberedPage.node('#main').innerHTML;
assert(numberedHTML.includes('class="structure-context-fields">'),'A match only in 0–11 keeps A–D collapsed');
assert(!numberedHTML.includes('class="structure-context-fields" open'));
assert.equal((numberedHTML.match(/class="structure-field is-status-match"/g)||[]).length,12);
// Results and generation retain filtering membership without opening unrelated phases.
const phasesFixture=clone(numberedFixture),phasesRecord=phasesFixture.storyboardStructure.stories.find(story=>story.storyID==='hon:strictly-business');
phasesRecord.shots[0].fields=defs.map(def=>({key:def.key,status:def.key==='acceptance'?'accepted':def.key==='prompt_clip'?'verified':'draft',text:'Phase fixture',evidence:[]}));
phasesRecord.shots[0].revisions=[{label:'Prior phase fixture',note:'History must survive the grouped display.',source:honRecord.source,parent:honRecord.shots[0].source}];
phasesRecord.shots[0].priorDependencyEvidence=[honRecord.source];
const phasesBefore=JSON.stringify(phasesFixture),phasesPage=createPage(phasesFixture);phasesPage.api.route('hon','storyboard','structure:hon:strictly-business');
for(const [status,matchedPhase] of [['accepted','results'],['verified','generation']]){
  phasesPage.node('#structure-status-'+status).click();
  const phaseHTML=phasesPage.node('#main').innerHTML;
  assert.equal(shotIDs(phaseHTML).length,1);
  assert.equal(pillCount(phaseHTML,status),1);
  for(const phase of ['context','creative','generation','results'])assert.equal(phaseHTML.includes('class="structure-'+phase+'-fields" open'),phase===matchedPhase,'Only the matching phase opens');
  const takeReview=phaseHTML.split('class="structure-results-fields"')[1].split('</details>')[0];
  assert(takeReview.includes('Prior phase fixture')&&takeReview.includes('History must survive the grouped display.'),'Merged group preserves revision labels and notes');
  assert(takeReview.includes('data-open="'+honRecord.source.assetID+'"')&&takeReview.includes('data-open="'+honRecord.shots[0].source.assetID+'"'),'Merged group preserves dependency/source/parent evidence');
}
assert.equal(JSON.stringify(phasesPage.api.C),phasesBefore,'Phase grouping changes no source metadata');
assert.equal(phasesPage.writes.length,0,'Phase filtering writes no reviews');
console.log('Storyboard phases, collapsed drawers, dated coverage, sixteen-field status filters, empty template and preservation passed.');
