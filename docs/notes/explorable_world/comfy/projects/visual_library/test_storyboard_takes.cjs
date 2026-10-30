'use strict';
const assert=require('node:assert/strict');
const crypto=require('node:crypto');
const fs=require('node:fs');
const vm=require('node:vm');
const T=require('./storyboard_takes.js');
const clone=v=>JSON.parse(JSON.stringify(v));
const scope=['hon','hon:strictly-business','S01-1'];
const shot={shotID:'S01-1',revision:'take 1',stage:'production',title:'The mouth · café 😀',
  source:{path:'writer/shot.md',sha256:'a'.repeat(64),line:5,endLine:19},
  fields:[{key:'camera',text:'Locked',status:'accepted',evidence:[{path:'writer/shot.md'}]},
    {key:'prompt_clip',text:'Hold the grin.',status:'accepted',evidence:[{path:'old_prompt.txt'}]},
    ...['settings','results','acceptance'].map(key=>({key,text:'OLD '+key,status:'accepted',evidence:[{path:'old_result.mp4'}],reviewer:'Ziggy'}))],
  materials:[{assetID:'old-video',role:'result_on_disk'},{assetID:'face',role:'identity_reference'}],
  kitchenWritten:true,kitchen:[{key:'11.10',text:'Old copy-ready prompt',status:'accepted',evidence:[{path:'old_prompt.txt'}]}]};
const foundation={state:'detailed',label:'Detailed foundation',inputs:[{assetID:'face',bytes:100}],notes:[],dependencyReviewNeeded:false};
const options=(id='take-2',changeNote='Let the grin arrive later.')=>({project:scope[0],storyID:scope[1],shot,foundation,id,changeNote,recordedAt:'2026-10-29T20:00:00Z'});
const initial=T.empty(),before=JSON.stringify({initial,shot,foundation});
assert.equal(T.current(initial,...scope),null);
assert.deepEqual(T.forShot(initial,...scope),[]);
assert.equal(JSON.stringify({initial,shot,foundation}),before,'reading must not initialize records');
const second=T.plan(initial,options()),source=second.takes.find(r=>r.state==='written'),active=T.current(second,...scope);
assert.equal(second.takes.length,2);
assert.deepEqual(source.snapshot,{shot,foundation});
assert.equal(source.number,1);assert.equal(active.number,2);assert.equal(active.parentID,source.id);assert.equal(active.state,'planned');
assert.equal(JSON.stringify({initial,shot,foundation}),before,'planning must not mutate the original source or ledger');
assert.equal(active.snapshot.shot.stage,'preliminary');assert.equal(active.snapshot.shot.kitchenWritten,false);
assert.equal(active.snapshot.shot.handoffNeedsReconciliation,true);assert.equal(active.snapshot.foundation.dependencyReviewNeeded,true);
for(const key of ['settings','results','acceptance'])assert.deepEqual(active.snapshot.shot.fields.find(f=>f.key===key),{key,text:'',status:'unknown',evidence:[],note:'Not recorded for this planned take. Earlier evidence remains with its original take.'});
assert.equal(active.snapshot.shot.fields.find(f=>f.key==='prompt_clip').status,'draft');
assert.match(active.snapshot.shot.fields.find(f=>f.key==='prompt_clip').note,/change note/);
assert.equal(active.snapshot.shot.kitchen[0].status,'draft');
assert.equal(active.snapshot.shot.fields.find(f=>f.key==='camera').status,'draft');
assert.deepEqual(active.snapshot.shot.materials,[{assetID:'face',role:'identity_reference'}]);
const gaps=clone(shot);gaps.fields=gaps.fields.filter(f=>!['prompt_still','prompt_clip'].includes(f.key));
gaps.fields.push({key:'prompt_still',text:'Missing start frame',status:'missing'},{key:'prompt_clip',text:'CFA Nova zone',status:'unknown'});
gaps.kitchen=[{key:'11.1',text:'Missing start frame',status:'missing'},{key:'11.2',text:'CFA Nova zone',status:'unknown'},
  {key:'11.3',text:'Not required for this route',status:'not_needed'},{key:'11.4',text:'Supplied lock text',status:'present'},
  {key:'11.5',text:' ',status:'accepted'}];
const gapTake=T.current(T.plan(initial,{...options('gaps-2'),shot:gaps}),...scope).snapshot.shot;
assert.deepEqual(gapTake.kitchen.map(f=>f.status),['missing','unknown','not_needed','draft','unknown']);
assert.equal(gapTake.fields.find(f=>f.key==='prompt_still').status,'missing');
assert.equal(gapTake.fields.find(f=>f.key==='prompt_clip').status,'unknown');
assert.deepEqual(gaps.kitchen.map(f=>f.status),['missing','unknown','not_needed','present','accepted'],'gap source remains untouched');
const frozenSecond=clone(second),changed=clone(shot);changed.fields[0].text='A newer writer changed the camera.';
const third=T.plan(second,{...options('take-3','Hold the end longer.'),shot:changed});
const fourth=T.plan(third,options('take-4','Test the original framing.'));
assert.deepEqual(second,frozenSecond);
for(const row of second.takes)assert.deepEqual(fourth.takes.find(r=>r.id===row.id),row);
assert.equal(T.current(fourth,...scope).number,4);
assert.equal(T.current(fourth,...scope).snapshot.shot.fields.find(f=>f.key==='camera').text,'Locked','later source revisions cannot overwrite the frozen parent');
assert.deepEqual(T.merge(JSON.parse(JSON.stringify(fourth)),second,initial),fourth);
const altered=clone(second);altered.takes.find(r=>r.id==='take-2').changeNote='Silently overwritten';
assert.throws(()=>T.merge(second,altered),/immutable record conflict/);
const alternative=T.plan(initial,options('alternate-2','A concurrent alternative.')),branched=T.merge(second,alternative);
assert.equal(branched.takes.length,3);assert.equal(T.current(branched,...scope),null);
assert.throws(()=>T.plan(branched,options('take-3')),/conflicting branches/);
assert.deepEqual(T.merge(branched),branched,'conflicting leaves survive import; no silent winner');
assert.throws(()=>T.plan(initial,options('x','  ')),/describe what changes/);
assert.throws(()=>T.plan(second,options()),/already exists/);
assert.throws(()=>T.merge({format:second.format,takes:[active]}),/missing or cross-shot parent/);
const cross=clone(second);cross.takes.find(r=>r.id==='take-2').project='lisan';assert.throws(()=>T.merge(cross),/cross-shot/);
const cycle=clone(second);cycle.takes.find(r=>r.state==='written').parentID='take-2';assert.throws(()=>T.merge(cycle));
const unknown=T.plan(initial,{...options('unknown-1'),shot:{...shot,shotID:'FUTURE-99',revision:'posted scene card'}});
assert.equal(T.current(unknown,'hon',scope[1],'FUTURE-99').number,1);assert.equal(T.merge(second,unknown).takes.length,4);
const malicious=clone(second);malicious.takes[0].snapshot.shot.danger=Infinity;assert.throws(()=>T.merge(malicious),/finite/);
const sandbox={window:{},TextEncoder};vm.runInNewContext(fs.readFileSync(require.resolve('./storyboard_takes.js'),'utf8'),sandbox);assert.equal(sandbox.window.CFA_STORYBOARD_TAKES.empty().format,initial.format);
// Verify the synchronous source hash against Node's standard implementation.
const stable=v=>v===null||typeof v!=='object'?JSON.stringify(v):Array.isArray(v)?'['+v.map(stable).join(',')+']':'{'+Object.keys(v).sort().map(k=>JSON.stringify(k)+':'+stable(v[k])).join(',')+'}';
const identity={project:scope[0],storyID:scope[1],shotID:scope[2],snapshot:{shot,foundation}};
assert.equal(source.id,'source:'+crypto.createHash('sha256').update(stable(identity)).digest('hex'));
if(process.argv[2]==='--fixture')process.stdout.write(JSON.stringify({options:options(),ledger:second}));
else console.log('Storyboard take ledger: immutable history, conflicts, imports, reset semantics and browser UMD passed.');
