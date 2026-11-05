// Focused evidence reader behavior: exact-version attribution and safe return to image drafts.
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const path=require('node:path');
const source=fs.readFileSync(path.join(__dirname,'library.js'),'utf8');
const block=source.slice(source.indexOf('  function intakeEvidenceMatches('),source.indexOf('  function renderMain(){'));
assert(block.includes('function openIntakeEvidence'));
const shaA='a'.repeat(64),shaB='b'.repeat(64),shaC='c'.repeat(64);
const original={id:'original',sha256:shaA,title:'Original frame',src:'../original.jpg'};
const repaired={id:'repair',sha256:shaB,title:'Repaired frame',src:'../repair.jpg'};
const family={id:'family:frame',frameID:'FRAME-001',project:'hon',original:{sha256:shaA},currentCandidate:{sha256:shaB},providerReview:{qaGrade:'STRONG',qaScoreSuggestion:4,qaBasis:'Preliminary self-score',reason:'Original has a missing nose piercing.',humanQuestion:'Original chest decision'},versions:[
  {assetID:'original',sha256:shaA,availability:'available',role:'original',providerReview:{}},
  {assetID:'repair',sha256:shaB,availability:'available',role:'repair',providerReview:{stage:'scoped pass',verdict:'PASS',scope:'chest correction only',advisory:'Earring not checked'}}
]};
const C={reviewIntake:{families:[family],assetMetadata:{original:{sha256:shaA,familyIDs:[family.id]},repair:{sha256:shaB,familyIDs:[family.id]}}},reviewSupplements:[{id:'later',items:[{id:'winner',exactAssetID:'repair',sha256:shaB,title:'Repaired frame',group:'validated',vVerdict:'PASS-ADVISORY',reviewScope:'chest only',advisories:'Soft spire at 6x',sourceEvidence:'receipt row 1'}]}]};
const stored={status:'keep',note:'Chest accepted; piercing still absent.'},before=JSON.stringify(C),choiceBefore=JSON.stringify(stored);
const imageViewer={innerHTML:'live image viewer with unsaved validation draft',open:true};
let created,focusReturns=0;
class EvidenceDialog {
  constructor(){this.events={};this.open=false;this.closeButton={};}
  setAttribute(){}
  addEventListener(event,callback){this.events[event]=callback;}
  querySelector(selector){assert.equal(selector,'[data-evidence-close]');return this.closeButton;}
  querySelectorAll(){return [];}
  showModal(){this.open=true;}
  close(){this.open=false;this.events.close?.();}
}
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const context={C,byID:new Map([['original',original],['repair',repaired]]),esc,intakeFamilies:()=>C.reviewIntake.families,reviewSupplements:()=>C.reviewSupplements,reviewRecord:()=>stored,statusLabels:{keep:'Keep'},intakeText:v=>typeof v==='object'?JSON.stringify(v):String(v),intakeFields:v=>'<dl class="intake-fields">'+esc(JSON.stringify(v))+'</dl>',supplementURL:v=>v&&!v.startsWith('javascript:')?v:'',supplementLinks:()=>'<details><summary>Source details · optional</summary></details>',href:v=>v,dialog:imageViewer,state:{},route(){throw Error('Unexpected route change');},document:{body:{append(){}},createElement(){created=new EvidenceDialog();return created;},activeElement:null},window:{}};
vm.runInNewContext(block+'\nwindow.api={intakeAssetEvidence,intakeEvidencePanel,intakeEvidenceVersion,openIntakeEvidence};',context);
const api=context.window.api;
const compact=api.intakeAssetEvidence(repaired);
assert(compact.includes('Read full review'));
assert(compact.includes('Later winners supplement · exact image match'));
assert(!compact.includes('<dl'),'Narrow sidebar contains no raw metadata tables');
assert(!compact.includes('Original has a missing nose piercing.'),'Long findings live in wide panel');
assert.equal(api.intakeAssetEvidence({...repaired,sha256:shaC}),'','Mismatched asset hash cannot inherit evidence');
const panel=api.intakeEvidencePanel(repaired);
assert(panel.includes('This exact version'));
assert(panel.includes('Family / original findings'));
assert(panel.indexOf('Original has a missing nose piercing.')>panel.indexOf('Family / original findings'));
assert(panel.includes('chest correction only'));
assert(panel.includes('PASS-ADVISORY'));
assert(panel.includes('Soft spire at 6x'));
assert(panel.includes('Your saved decision'));
assert(panel.includes('Chest accepted; piercing still absent.'));
assert(panel.includes('Source details · optional'));
assert(!panel.includes('<details class="evidence-source" open'));
assert(panel.includes('Original / delivered base'));
assert(panel.includes('Provider current candidate'));
assert(panel.includes('href="../repair.jpg"'));
assert(!api.intakeEvidenceVersion({assetID:'repair',sha256:shaA,availability:'available'},'Wrong binding',shaA).includes('href='),'No full-image link for mismatched ID/hash');
api.openIntakeEvidence('repair',{focus(){focusReturns++;}});
assert(created.open);
assert(created.innerHTML.includes('Repaired frame'));
assert.equal(imageViewer.innerHTML,'live image viewer with unsaved validation draft');
created.closeButton.onclick();
assert(!created.open);
assert.equal(focusReturns,1);
assert.equal(imageViewer.innerHTML,'live image viewer with unsaved validation draft','Return never rebuilds viewer forms');
assert.equal(imageViewer.open,true);
assert.equal(JSON.stringify(C),before,'Evidence read cannot mutate delivered records');
assert.equal(JSON.stringify(stored),choiceBefore,'Evidence read cannot mutate user choice');
assert(source.includes("!dialog.open||intakeEvidenceDialog?.open||"),'Image arrow navigation pauses while reading evidence');
const unsafe=api.intakeEvidencePanel({...repaired,title:'<script>bad()</script>'});
assert(!unsafe.includes('<script>'));
console.log('Evidence reader: compact sidebar, wide findings, exact-version binding, optional provenance, and preserved image drafts passed.');
