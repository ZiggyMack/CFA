const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const root=__dirname,clone=x=>JSON.parse(JSON.stringify(x));
const source=fs.readFileSync(path.join(root,'library.js'),'utf8');
const raw=fs.readFileSync(path.join(root,'catalog.js'),'utf8');
const catalog=JSON.parse(raw.slice(raw.indexOf('=')+1).trim().replace(/;$/,''));
const byID=new Map(catalog.assets.map(a=>[a.id,a]));
const REVIEW_KEY='cfa-visual-review-v1',FAVORITES_KEY='cfa-visual-favorites-v1',EXPORT_KEY='cfa-visual-export-v1';
const shared=fs.readFileSync(path.join(root,'test_collections_navigation.cjs'),'utf8');
let bootSource=shared.slice(shared.indexOf('function boot()'),shared.indexOf('const page = boot()'));
assert(bootSource.includes('window.__collectionsTest={'));
bootSource=bootSource.replace('window.__collectionsTest={',
  'window.__collectionsTest={missionTaskPresentation,missionReviewProgress,missionTaskCard,missionPriorityCard,sharedCollectionReference,openTest(id){const b=[...document.querySelectorAll("[data-open]")].find(b=>b.dataset.open===id);if(!b||typeof b.onclick!=="function")throw Error("Missing bound action: "+id);b.click();return currentID;},');
const boot=new Function('source','catalog','byID','clone','assert','vm','REVIEW_KEY','FAVORITES_KEY','EXPORT_KEY',bootSource+';return boot;')(
  source,catalog,byID,clone,assert,vm,REVIEW_KEY,FAVORITES_KEY,EXPORT_KEY);
const page=boot(),api=page.api,before=clone(page.C);
const reviews=clone(api.reviewPayload().items),storage=Object.fromEntries(page.storage);
const originalID='HD-RETURN-957897bd45c4',draftID='LAG-JAMES-NOGUN-0223fd8d0c6f',crocID='HD-RETURN-8421e7cfa1a0';
const original=page.C.assets.find(a=>a.id===originalID),originalReview=clone(api.reviewRecord(originalID));
assert.equal(original.project,'hon');
assert.equal(original.sha256,'957897bd45c4fc03d685c4a40af7670385ab3970108cdbd319d839385dceacc1');
api.setState({project:'hon',view:'mission_control',album:'',search:''});api.renderMain();
const disclosures=[...page.html().matchAll(/<details\b[^>]*class="mission-(?:priority-task|task)"[^>]*>/g)];
assert(disclosures.length);
for(const [tag] of disclosures)assert(!/\sopen(?:\s|>|=)/.test(tag));
for(const task of page.C.missionControl.tasks){
  assert(!/\sopen(?:\s|>|=)/.test(api.missionTaskCard(task).match(/^<details[^>]*>/)[0]));
  assert(!/\sopen(?:\s|>|=)/.test(api.missionPriorityCard(task).match(/<details class="mission-priority-task"[^>]*>/)[0]));
}
const comfy=page.C.missionControl.tasks.find(t=>t.id==='comfy-report-decisions-20261013');
assert.equal(comfy.priority,'normal');assert.equal(comfy.status,'needs_input');
assert.equal(comfy.comparisonInHistory,true);
assert(comfy.links.some(l=>l.assetID==='FLOW-LAG-SW2-001'));
assert(!/before Start|must still be verified/.test(JSON.stringify(comfy.missing)));
const comfyHTML=api.missionTaskCard(comfy);
assert(comfyHTML.includes('<details class="mission-review-history"><summary>Selected starting image and earlier comparison</summary>'));
assert(comfyHTML.indexOf('data-open="FLOW-LAG-SW2-001"')<comfyHTML.indexOf('class="source-comparison-preview"'));
assert.equal(api.openTest('FLOW-LAG-SW2-001'),'FLOW-LAG-SW2-001');
assert(!page.C.reviewDecisions.some(r=>r.id==='FLOW-LAG-SW2-001'&&r.status==='keep'));
const bossTask=page.C.missionControl.tasks.find(t=>t.id==='grok-boss-discovery');
assert.notEqual(bossTask.status,'needs_input');
assert.equal(bossTask.userSelection.finalBossSelected,true);
assert.equal(bossTask.userSelection.selectedAssetID,crocID);
assert(!/\b(?:choose|select)\b[^.]*\bboss\b|final boss selection/i.test(bossTask.nextAction+' '+JSON.stringify(bossTask.missing)));
api.setState({project:'hon',view:'cast',album:'',search:''});
const boss=page.C.castCollections.find(g=>g.project==='hon'&&(g.representativeID||g.coverID)===crocID);
assert(boss);assert(/select/i.test(JSON.stringify([boss.role,boss.description,boss.notes])));
const bossHub=api.castHubGroups(boss.id)[0];assert.equal(bossHub.cover.id,crocID);
assert(!boss.preferredIDs?.length);
const bossWorking=api.castWorkingGroups(boss.id)[0];
assert(bossWorking.items.some(a=>a.id===crocID));
const history=bossWorking.sections.filter(s=>s.history).flatMap(s=>s.assetIDs).filter(id=>id!==crocID);
assert(history.length);
assert(boss.historyIDs.every(id=>!bossHub.items.some(a=>a.id===id)),'Earlier discovery candidates stay outside the selected character hub');
assert(boss.sceneAssetIDs.filter(id=>api.normalVisible(page.C.assets.find(a=>a.id===id))).every(id=>bossHub.items.some(a=>a.id===id)),'The current crocodile scene and repair grouping remains reachable');
api.expandedCollections.add(bossWorking.id);
assert(/<details class="collection-history"\s*>/.test(api.collectionCards([bossWorking])));
api.expandedCollections.clear();
const james=page.C.castCollections.find(g=>g.project==='lisan'&&/james/i.test(g.id+' '+g.title));assert(james);
const reference=james.sharedReferences?.find(r=>r.assetID===originalID);assert(reference);
assert.equal(reference.sourceProject,'hon');assert.equal(reference.sha256,original.sha256);
api.setState({project:'lisan',view:'cast',album:'',search:''});
assert(api.sharedCollectionReference(james,original));
assert(api.collectionGroups([james],[]).some(g=>g.items.some(a=>a.id===originalID)));
for(const refs of [[],[{...reference,sha256:'0'.repeat(64)}],[{...reference,sourceProject:'lisan'}]]){
  const altered={...james,sharedReferences:refs};
  assert(!api.sharedCollectionReference(altered,original));
  assert(!api.collectionGroups([altered],[]).some(g=>g.items.some(a=>a.id===originalID)));
}
api.renderMain();assert(api.castHubGroups(james.id)[0]);
page.toggle(james.id);
assert(page.html().includes('data-open="'+originalID+'"'));
assert.equal(api.openTest(originalID),originalID);
const draft=page.C.assets.find(a=>a.id===draftID);assert(draft);
assert.equal(draft.project,'lisan');
assert.equal(draft.sha256,'0223fd8d0c6f4c8af225a19daca05d213dd9d261322953aa89c04e6ed2b30a79');
assert(/draft|needs.?fixes/i.test([draft.title,draft.sourceStatus,draft.note].join(' ')));
assert.notEqual(api.reviewRecord(draftID).status,'keep');
assert.notEqual(api.reviewRecord(draftID).storyboardStage,'production');
assert.notEqual(draft.storyboardStage,'production');
assert.notEqual(draft.masterApproved,true);assert.notEqual(draft.productionReady,true);
assert(draft.parentAssetID===originalID||(draft.sourceAssetIDs||[]).includes(originalID));
assert.equal(page.C.assets.filter(a=>a.id===originalID).length,1);
assert.deepEqual(clone(api.reviewRecord(originalID)),originalReview);
assert.deepEqual(clone(page.C),before);
assert.deepEqual(clone(api.reviewPayload().items),reviews);
assert.deepEqual(Object.fromEntries(page.storage),storage);assert.equal(page.writes.length,0);
assert.equal(fs.readFileSync(path.join(root,'library.js'),'utf8'),source);
assert.equal(fs.readFileSync(path.join(root,'catalog.js'),'utf8'),raw);
const lisanTask=page.C.missionControl.tasks.find(t=>t.id==='grok-lisan-mouth65-available');
const savedReviews=clone(api.reviewPayload().items),savedTasks=clone(page.C.missionControl.tasks);
let shown=api.missionTaskPresentation(lisanTask);
assert.equal(shown.reviewProgress.requested,7);assert.equal(shown.reviewProgress.answered,7);
assert.equal(shown.previewAssetIDs.length,0);assert.equal(shown.priority,'normal');assert.equal(shown.status,'in_progress');
assert.equal(shown.reviewedPreviewAssetIDs.length,7);
assert(api.missionTaskCard(shown).includes('Recorded decisions · 7'));
assert.equal(page.C.albums.find(a=>a.id==='lisan:mouth-complete-20261012').assetIDs.length,65,'The full collection remains, without becoming new review obligations');
const falcon=page.C.missionControl.tasks.find(t=>t.id==='grok-falcon-extension40-available');
shown=api.missionTaskPresentation(falcon);
assert.equal(shown.reviewProgress.requested,15);assert.equal(shown.reviewProgress.answered,15);assert.equal(shown.previewAssetIDs.length,0);
assert(!shown.previewAssetIDs.includes('HD-FALCON-11868f1948c1cebf'),'Remove is answered');
assert(!shown.previewAssetIDs.includes('HD-FALCON-580d85f3fa90e675'),'Needs fixes is answered');
const reopened=lisanTask.previewAssetIDs[0],savedRecord=clone(api.reviewRecord(reopened));
api.reviews.set(reopened,{...savedRecord,status:null});
shown=api.missionTaskPresentation(lisanTask);assert.deepEqual(clone(shown.previewAssetIDs),[reopened]);assert.equal(shown.status,'needs_input');assert.equal(shown.priority,lisanTask.priority);
api.setState({project:'lisan',view:'mission_control',album:'',search:''});api.renderMain();assert.equal(api.openTest(reopened),reopened);
for(const status of ['keep','needs_fixes','remove']){
 api.reviews.set(reopened,{...savedRecord,status});shown=api.missionTaskPresentation(lisanTask);assert.equal(shown.previewAssetIDs.length,0);assert.equal(shown.reviewProgress.answered,7);
}
api.reviews.set(reopened,savedRecord);
const falconRecords=falcon.previewAssetIDs.map(id=>[id,clone(api.reviewRecord(id)),api.reviews.has(id)]);
falconRecords.forEach(([id,r],i)=>api.reviews.set(id,{...r,status:i<8?'keep':null}));
shown=api.missionTaskPresentation(falcon);
assert.deepEqual(clone(shown.previewAssetIDs),clone(falcon.previewAssetIDs.slice(8)),'Answered records are filtered before the first seven preview slots');
for(const [id,r,existed] of falconRecords)if(existed)api.reviews.set(id,r);else api.reviews.delete(id);
const malformed={...lisanTask,previewAssetIDs:[reopened,reopened,'missing-image-id']};const progress=api.missionReviewProgress(malformed);
assert.equal(progress.requested,2);assert.equal(progress.answered,1);assert.deepEqual(clone(progress.unavailableIDs),['missing-image-id']);

// Generic gates follow exact image/video versions and explicit human decisions.
const gateIDs=['HD-FALCON-af69f68b13ef0012','HD-FALCON-ee485849b0e6528a','FLOW-LAG-SW2-001'];
const gateRecords=gateIDs.map(id=>[id,clone(api.reviewRecord(id)),api.reviews.has(id)]);
const gateTask={id:'review-gate-regression',provider:'Grok',project:'hon',status:'needs_input',priority:'top',
 title:'Old review request',summary:'Old summary',nextAction:'Review all',missing:['Review all'],
 sourceMessageID:'original-dispatch',receiptState:'received_unaccepted',
 reviewGate:{label:'Returned versions',targets:gateIDs.map(assetID=>({assetID,sha256:byID.get(assetID).sha256})),
 completed:{title:'Returned versions · review recorded',statusLabel:'Review recorded · follow-up not sent',
 summary:'The review is recorded; sending feedback and choosing a replacement remain separate.',
 nextAction:'Prepare the recorded correction for the team.',missing:['A replacement decision is separate.']}}};
const gateBefore=clone(gateTask);
for(const [index,id] of gateIDs.entries())api.reviews.set(id,{id,sha256:byID.get(id).sha256,status:['keep','remove','needs_fixes'][index],collectionState:index===1?'archived':'working'});
shown=api.missionTaskPresentation(gateTask);
assert.equal(shown.reviewProgress.answered,3);assert.deepEqual(clone(shown.previewAssetIDs),[]);
assert.deepEqual(clone(shown.reviewedPreviewAssetIDs),gateIDs,'Removed and archived decisions remain answered history');
assert.equal(shown.status,'in_progress');assert.equal(shown.priority,'normal');
assert.equal(shown.statusLabel,gateTask.reviewGate.completed.statusLabel);
assert.equal(shown.title,gateTask.reviewGate.completed.title);assert.deepEqual(clone(shown.missing),gateTask.reviewGate.completed.missing);
assert.equal(shown.sourceMessageID,'original-dispatch');assert.equal(shown.receiptState,'received_unaccepted');
assert(!Object.hasOwn(shown,'approval')&&!Object.hasOwn(shown,'feedbackSent'),'Review completion does not manufacture acceptance or transmission');
const gateHTML=api.missionTaskCard(shown);
assert(gateHTML.includes('Recorded decisions · 3'));
assert(api.missionPriorityCard(shown).includes(gateTask.reviewGate.completed.statusLabel),'Priority cards display the same review/follow-up state');
for(const id of gateIDs)assert(gateHTML.includes('data-open="'+id+'"'),'Each answered version can still be inspected');

api.reviews.set(gateIDs[0],{id:gateIDs[0],sha256:byID.get(gateIDs[0]).sha256,status:null,note:'Looks good',likenessRating:5,sceneQualityRating:5,collectionState:'working'});
shown=api.missionTaskPresentation(gateTask);
assert.equal(shown.status,'needs_input');assert.equal(shown.statusLabel,'Needs your input');
assert.deepEqual(clone(shown.previewAssetIDs),[gateIDs[0]],'A clear decision reopens the exact target; notes and scores alone do not finish it');
assert.equal(shown.reviewProgress.answered,2);
api.reviews.set(gateIDs[0],{...api.reviewRecord(gateIDs[0]),status:'keep'});
assert.equal(api.missionTaskPresentation(gateTask).reviewProgress.answered,3);

const wrongTarget=clone(gateTask);wrongTarget.reviewGate.targets[0].sha256='0'.repeat(64);
shown=api.missionTaskPresentation(wrongTarget);
assert.equal(shown.statusLabel,'Reference check needed');assert.deepEqual(clone(shown.reviewProgress.unavailableIDs),[gateIDs[0]]);
assert.equal(shown.reviewProgress.answered,2,'Same asset ID with a different exact hash is not the reviewed version');
api.reviews.set(gateIDs[0],{...api.reviewRecord(gateIDs[0]),sha256:'0'.repeat(64)});
assert.deepEqual(clone(api.missionTaskPresentation(gateTask).reviewProgress.unavailableIDs),[gateIDs[0]],'Mismatched review provenance cannot satisfy the exact gate');
api.reviews.set(gateIDs[0],{...api.reviewRecord(gateIDs[0]),sha256:byID.get(gateIDs[0]).sha256,status:null,collectionState:'archived'});
shown=api.missionTaskPresentation(gateTask);
assert.equal(shown.statusLabel,'Reference check needed');assert.equal(shown.reviewProgress.answered,2,'Archiving without a decision is not an answered review');
api.reviews.set(gateIDs[0],{...api.reviewRecord(gateIDs[0]),status:'keep',collectionState:'working'});

const missingTarget=clone(gateTask);missingTarget.reviewGate.targets.push({assetID:'missing-exact-version',sha256:'f'.repeat(64)});
shown=api.missionTaskPresentation(missingTarget);
assert.equal(shown.reviewProgress.requested,4);assert.deepEqual(clone(shown.reviewProgress.unavailableIDs),['missing-exact-version']);
assert.equal(shown.statusLabel,'Reference check needed');
const duplicateTarget=clone(gateTask);duplicateTarget.reviewGate.targets.push({...duplicateTarget.reviewGate.targets[0],sha256:duplicateTarget.reviewGate.targets[0].sha256.toUpperCase()});
assert.equal(api.missionTaskPresentation(duplicateTarget).reviewProgress.requested,3,'Equivalent uppercase digest and repeated target do not add a new review');
for(const patch of [{label:' '},{targets:[]},{targets:[...gateTask.reviewGate.targets,{assetID:gateIDs[0],sha256:'0'.repeat(64)}]},{completed:'invalid'}]){
 const invalid={...gateTask,reviewGate:{...gateTask.reviewGate,...patch}};
 assert.deepEqual(clone(api.missionTaskPresentation(invalid)),invalid,'A malformed gate never shrinks into a completed scope');
}
const doneGate={...gateTask,status:'done'};assert.deepEqual(clone(api.missionTaskPresentation(doneGate)),doneGate,'Completed handoffs are not reopened');
const ungated={...gateTask};delete ungated.reviewGate;assert.deepEqual(clone(api.missionTaskPresentation(ungated)),ungated);
assert.deepEqual(gateTask,gateBefore,'Rendering does not rewrite the source task or its scope');
for(const [id,r,existed] of gateRecords)if(existed)api.reviews.set(id,r);else api.reviews.delete(id);
assert.deepEqual(clone(api.reviewPayload().items),savedReviews);assert.deepEqual(clone(page.C.missionControl.tasks),savedTasks);assert.equal(page.writes.length,0);
console.log(JSON.stringify({passed:true,missionCardsClosed:true,lisanShortlist:{reviewed:7,pending:0},falconShortlist:{reviewed:15,pending:0},genericGateExactVersions:true,explicitClearReopens:true,removedHistory:true,noApprovalOrDispatchInference:true,filterBeforePreviewLimit:true,reviewTransitions:true,sw2ReceivedReviewLink:true,sourceComparisonClosed:true,selectedBossPreserved:true,bossHistoryPreserved:true,jamesHashBoundSharing:true,jamesDraftUnaccepted:true,honSourceAndReviewUnchanged:true,reviewWrites:0,browserVisualQA:false}));
