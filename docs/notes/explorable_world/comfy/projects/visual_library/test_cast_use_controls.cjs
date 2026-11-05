/* Exact-version cast decisions through the real renderer, isolated from user storage. */
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const L=__dirname,clone=v=>JSON.parse(JSON.stringify(v)),REVIEW_KEY='cfa-visual-review-v1',FAVORITES_KEY='cfa-visual-favorites-v1';
const raw=fs.readFileSync(path.join(L,'catalog.js'),'utf8'),catalog=JSON.parse(raw.slice(raw.indexOf('=')+1).trim().replace(/;$/,'')),assets=catalog.assets,source=fs.readFileSync(path.join(L,'library.js'),'utf8');
const harness=fs.readFileSync(path.join(L,'test_reference_scope.cjs'),'utf8'),old='window.__scopeTest={openViewer,reviewRecord,reviewPayload,importReview,exportReference,inReviewQueue,whenFileWritesSettle(){return fileWriteChain;}};';
const replacement='window.__scopeTest={C,route,openViewer,reviewRecord,reviewPayload,importReview,exportReview,exportReference,castHubGroups,castBrowseFacts,effectiveCastUse,normalizedCastUse,setCastUse,linkCastShot,unlinkCastShot,castStoryTargets,chooseReviewFile,whenFileWritesSettle(){return fileWriteChain;}};';
const boot=harness.slice(harness.indexOf('function boot('),harness.indexOf('async function main()')).replace(old,replacement).replace('this.children.clear(); this._html = html;',`this.children.clear(); this._html = html;
      if(this.tag==='select'){this.options=[...html.matchAll(/<option[^>]*value="([^"]*)"/g)].map(m=>m[1]);this._value=this.options[0]||'';}`);
const makePage=new Function('source','catalog','clone','assert','vm','REVIEW_KEY','FAVORITES_KEY','assets',boot+';return boot;')(source,catalog,clone,assert,vm,REVIEW_KEY,FAVORITES_KEY,assets);
const wifeID='HD-DROP-5171bb20c773',wifeGroup='hon:cast-ivory',otherWife=catalog.castCollections.find(g=>g.id===wifeGroup).currentIDs.find(id=>id!==wifeID&&catalog.assets.some(a=>a.id===id)),crocID='HD-RETURN-8421e7cfa1a0';
const unchanged=r=>JSON.stringify(['status','note','shotPlan','likenessRating','sceneQualityRating','workingReference','workingReferenceScope','storyboardStage','variant'].map(key=>r[key]??null));
function facts(page,id){return page.api.castBrowseFacts(page.api.castHubGroups(id).find(g=>g.id===id));}
function count(page,key){return Number(page.node('#main').innerHTML.match(new RegExp('data-cast-filter="'+key+'"[^>]*>[^<]* · (\\d+)<'))?.[1]);}
function toggle(page,id,checked){const input=page.node('#'+id);input.checked=checked;input.fire('change');}
async function main(){
  const p=makePage({},catalog,{fileAutosave:true});p.api.route('hon','cast');
  assert.equal(count(p,'planned'),2);assert.equal(count(p,'roles'),3);assert.equal(count(p,'linked'),1);
  const catalogBefore=JSON.stringify(p.api.C),wifeBefore=unchanged(p.api.reviewRecord(wifeID));p.open(wifeID);
  assert(p.node('#cast-storyboard-planned'),'Exact-version plan lever exists');
  await p.api.chooseReviewFile();toggle(p,'cast-storyboard-planned',true);await p.flushTimers();
  assert.equal(count(p,'planned'),3,'Wife planning adds one character');
  assert.equal(count(p,'linked'),1,'Plan without a shot does not fabricate a link');
  assert.equal(p.api.reviewRecord(wifeID).castUse.storyboardPlanned,true);
  assert.equal(unchanged(p.api.reviewRecord(wifeID)),wifeBefore,'No rating, triage, image approval or generator task changes');
  assert.equal(JSON.parse(p.fileWrites.at(-1)).items.find(row=>row.id===wifeID).castUse.storyboardPlanned,true,'Cast changes use common review-file autosave');
  p.open(otherWife);toggle(p,'cast-storyboard-planned',true);
  assert.equal(count(p,'planned'),3,'Another version of the same wife counts only once');
  p.open(wifeID);toggle(p,'cast-role-selected',true);
  const role=p.node('#cast-role');role.value="Dolo's wife";role.fire('change');
  assert.equal(count(p,'roles'),4,'A reviewed version can select a role');assert.equal(p.api.reviewRecord(wifeID).castUse.role,"Dolo's wife");
  const story=p.node('#cast-link-story');story.value='hon:strictly-business';story.fire('change');
  const shot=p.node('#cast-link-shot');shot.value='S07-4';shot.fire('change');p.node('#cast-link-add').click();
  assert.equal(count(p,'linked'),2,'Valid exact shot link adds one character');
  assert.deepEqual(clone(p.api.reviewRecord(wifeID).castUse.storyboardLinks),[{storyID:'hon:strictly-business',shotID:'S07-4'}]);
  const beforeBad=JSON.stringify(p.api.reviewPayload().items),writes=p.writes.length;
  assert.throws(()=>p.api.linkCastShot(wifeID,'lisan:story-01','1'),/existing story and shot/);
  assert.throws(()=>p.api.linkCastShot(wifeID,'hon:strictly-business','invented'),/existing story and shot/);
  assert.equal(p.writes.length,writes);assert.equal(JSON.stringify(p.api.reviewPayload().items),beforeBad);
  p.api.linkCastShot(wifeID,'hon:strictly-business','S07-4');assert.equal(p.api.reviewRecord(wifeID).castUse.storyboardLinks.length,1,'Duplicate exact links collapse');
  toggle(p,'cast-storyboard-planned',false);assert.equal(count(p,'planned'),3,'Valid linked shot still implies planned');
  p.api.unlinkCastShot(wifeID,'hon:strictly-business','S07-4');assert.equal(count(p,'linked'),1);
  p.open(otherWife);toggle(p,'cast-storyboard-planned',false);assert.equal(count(p,'planned'),2,'Clearing both personal versions removes wife from planned filter');
  p.open(crocID);toggle(p,'cast-storyboard-planned',true);assert.equal(p.api.reviewRecord(crocID).castUse.roleSelected,true,'First plan edit retains preexisting source role choice');
  toggle(p,'cast-role-selected',false);assert.equal(facts(p,'hon:boss-round01').roles,false,'Explicit false overrides this version’s source role');
  p.node('#cast-use-reset').click();assert.equal(facts(p,'hon:boss-round01').roles,true,'Reset restores source settings');
  const bar=p.api.castHubGroups('hon:cast-bartender')[0].representativeID,barPlans=facts(p,'hon:cast-bartender').planned.length;
  p.api.setCastUse(bar,{storyboardPlanned:false,storyboardLinks:[]});assert.equal(facts(p,'hon:cast-bartender').planned.length,barPlans,'Source-authored plans cannot be removed by clearing manual flags');
  const unassigned=catalog.albums.find(g=>g.id==='hon:cast-unnamed-informant').assetIDs[1];assert(unassigned!==p.api.castHubGroups('hon:cast-unnamed-informant')[0].representativeID);p.api.setCastUse(unassigned,{storyboardPlanned:true});assert(facts(p,'hon:cast-unnamed-informant').planned.some(row=>row.manual&&row.assetID===unassigned),'Non-cover fallback album versions update the character filter');
  p.api.setCastUse(wifeID,{storyboardPlanned:true});p.api.linkCastShot(wifeID,'hon:strictly-business','S07-4');
  p.api.exportReview();const exported=JSON.parse(await p.downloads.at(-1).blob.text());
  assert.deepEqual(exported.items.find(row=>row.id===wifeID).castUse,clone(p.api.exportReference(catalog.assets.find(a=>a.id===wifeID)).castUse));
  const restored=makePage(p.snapshot(),catalog);restored.api.route('hon','cast');assert.equal(facts(restored,wifeGroup).roles,true);assert(facts(restored,wifeGroup).linked.some(row=>row.manual));
  const imported=makePage({},catalog);imported.api.importReview(exported);imported.api.route('hon','cast');assert.deepEqual(clone(imported.api.reviewRecord(wifeID).castUse),exported.items.find(row=>row.id===wifeID).castUse);
  imported.api.importReview({format:REVIEW_KEY,items:[{id:crocID,sha256:catalog.assets.find(a=>a.id===crocID).sha256,castUse:{storyboardPlanned:true,extra:{source:'manual'},storyboardLinks:[{storyID:'unavailable',shotID:'old',why:'retained'}]}}]});
  assert.equal(imported.api.effectiveCastUse(catalog.assets.find(a=>a.id===crocID)).roleSelected,true,'Partial import inherits source role');
  assert.equal(imported.api.reviewRecord(crocID).castUse.extra.source,'manual');assert.equal(imported.api.reviewRecord(crocID).castUse.storyboardLinks[0].why,'retained');
  assert(!facts(imported,'hon:boss-round01').linked.some(row=>row.manual),'Unresolved imported links are preserved but not counted');
  const malformedBefore=JSON.stringify(imported.api.reviewPayload().items);
  assert.throws(()=>imported.api.importReview({format:REVIEW_KEY,items:[{id:wifeID,sha256:catalog.assets.find(a=>a.id===wifeID).sha256,note:'Should not apply',castUse:{roleSelected:'yes'}}]}),/invalid character-use/);
  assert.equal(JSON.stringify(imported.api.reviewPayload().items),malformedBefore,'Malformed cast data is rejected before any review mutation');
  const sharedID='HD-RETURN-957897bd45c4';
  imported.api.importReview({format:REVIEW_KEY,items:[{id:sharedID,sha256:catalog.assets.find(a=>a.id===sharedID).sha256,castUse:{roleSelected:true,role:'Hon reference role',storyboardPlanned:true,storyboardLinks:[]}}]});
  imported.api.route('lisan','cast');const james=facts(imported,'lisan:cast-james');
  assert(!james.choices.some(a=>a.id===sharedID),'A shared source reference does not inherit a different project’s role choice');
  assert(!james.planned.some(row=>row.manual&&row.assetID===sharedID),'A Hon review does not create a Lisan storyboard plan through shared-reference membership');
  assert.equal(JSON.stringify(p.api.C),catalogBefore,'Cast flags never rewrite source collections or authored links');
  console.log('Cast use controls passed: exact-version roles/plans/links, unique counts, target validation, source preservation, common autosave/export/import, partial/unresolved records and reset.');
}
main().catch(error=>{console.error(error);process.exitCode=1;});
