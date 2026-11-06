/* Append-only planning records. This module never dispatches, selects media or writes reviews. */
(function(root,factory){
  'use strict';
  const api=factory();
  if(typeof module==='object'&&module.exports)module.exports=api;
  if(root)root.CFA_STORYBOARD_TAKES=api;
})(typeof window!=='undefined'?window:null,function(){
  'use strict';
  const FORMAT='cfa-storyboard-takes-v1';
  const RESET_NOTE='Not recorded for this planned take. Earlier evidence remains with its original take.';
  const UPDATE_NOTE='Copied direction: update against this take\'s change note before dispatch.';
  const HANDOFF_NOTE='Copied handoff: reconcile inputs, prompts and settings for this planned take.';
  const REVIEW_NOTE='Previous-take assessment does not approve this planned take.';
  const keys=['id','project','storyID','shotID','number','parentID','state','recordedAt','changeNote','snapshot'];
  const own=(v,k)=>Object.prototype.hasOwnProperty.call(v,k);
  const object=v=>v!==null&&typeof v==='object'&&!Array.isArray(v)&&[Object.prototype,null].includes(Object.getPrototypeOf(v));
  const fail=message=>{throw new Error('Storyboard takes: '+message);};
  function canonical(value){
    if(value===null||typeof value==='boolean')return JSON.stringify(value);
    if(typeof value==='string'){
      for(let i=0;i<value.length;i++){const c=value.charCodeAt(i);if(c>=0xd800&&c<=0xdbff){const d=value.charCodeAt(++i);if(!(d>=0xdc00&&d<=0xdfff))fail('invalid Unicode string');}else if(c>=0xdc00&&c<=0xdfff)fail('invalid Unicode string');}
      return JSON.stringify(value);
    }
    if(typeof value==='number'){
      if(!Number.isFinite(value)||(Number.isInteger(value)&&!Number.isSafeInteger(value)))fail('numbers must be finite and safely representable');
      return JSON.stringify(value);
    }
    if(Array.isArray(value))return '['+value.map(canonical).join(',')+']';
    if(object(value))return '{'+Object.keys(value).sort().map(k=>canonical(k)+':'+canonical(value[k])).join(',')+'}';
    fail('records must contain only plain JSON values');
  }
  const copy=value=>JSON.parse(canonical(value));
  const token=(value,name)=>{if(typeof value!=='string'||!value.trim()||value.length>512)fail(name+' must be a nonempty identifier');return value;};
  const scope=row=>JSON.stringify([row.project,row.storyID,row.shotID]);
  function validateSnapshot(snapshot,shotID){
    if(!object(snapshot)||Object.keys(snapshot).length!==2||!own(snapshot,'shot')||!own(snapshot,'foundation')||!object(snapshot.shot)||snapshot.shot.shotID!==shotID||!Array.isArray(snapshot.shot.fields)||!(snapshot.foundation===null||object(snapshot.foundation)))fail('invalid snapshot');
    for(const name of ['fields','kitchen']){
      if(snapshot.shot[name]===undefined&&name==='kitchen')continue;
      if(!Array.isArray(snapshot.shot[name]))fail('invalid snapshot fields');
      for(const field of snapshot.shot[name])if(!object(field)||typeof field.key!=='string'||!field.key||typeof field.text!=='string'||(own(field,'evidence')&&!Array.isArray(field.evidence)))fail('invalid snapshot field');
    }
    if(own(snapshot.shot,'materials')&&(!Array.isArray(snapshot.shot.materials)||snapshot.shot.materials.some(row=>!object(row))))fail('invalid snapshot materials');
    if(snapshot.foundation&&own(snapshot.foundation,'notes')&&!Array.isArray(snapshot.foundation.notes))fail('invalid foundation notes');
    canonical(snapshot);
  }
  // Small synchronous SHA-256 keeps file://, hosted browser and Node records identical.
  function sha256(text){
    const bytes=new TextEncoder().encode(text),length=bytes.length,words=[];
    for(let i=0;i<length;i++)words[i>>2]=(words[i>>2]||0)|(bytes[i]<<(24-(i%4)*8));
    words[length>>2]=(words[length>>2]||0)|(0x80<<(24-(length%4)*8));
    const end=(((length+8)>>6)+1)*16;words[end-2]=Math.floor(length/0x20000000);words[end-1]=(length*8)>>>0;
    const k=[0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2];
    const h=[0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19],rotate=(n,b)=>(n>>>b)|(n<<(32-b));
    for(let offset=0;offset<end;offset+=16){
      const w=new Array(64);for(let i=0;i<16;i++)w[i]=words[offset+i]|0;
      for(let i=16;i<64;i++){const a=w[i-15],b=w[i-2];w[i]=(w[i-16]+(rotate(a,7)^rotate(a,18)^(a>>>3))+w[i-7]+(rotate(b,17)^rotate(b,19)^(b>>>10)))|0;}
      let [a,b,c,d,e,f,g,t]=h;
      for(let i=0;i<64;i++){const x=(t+(rotate(e,6)^rotate(e,11)^rotate(e,25))+((e&f)^(~e&g))+k[i]+w[i])|0,y=((rotate(a,2)^rotate(a,13)^rotate(a,22))+((a&b)^(a&c)^(b&c)))|0;t=g;g=f;f=e;e=(d+x)|0;d=c;c=b;b=a;a=(x+y)|0;}
      [a,b,c,d,e,f,g,t].forEach((v,i)=>{h[i]=(h[i]+v)|0;});
    }
    return h.map(v=>(v>>>0).toString(16).padStart(8,'0')).join('');
  }
  function empty(){return {format:FORMAT,takes:[]};}
  function validateRecord(row){
    if(!object(row)||Object.keys(row).length!==keys.length||keys.some(k=>!own(row,k)))fail('invalid record fields');
    for(const k of ['id','project','storyID','shotID'])token(row[k],k);
    if(!['written','planned'].includes(row.state))fail('unsupported take state');
    if(row.number!==null&&(!Number.isSafeInteger(row.number)||row.number<1))fail('invalid take number');
    if(row.parentID!==null)token(row.parentID,'parentID');
    if(typeof row.changeNote!=='string')fail('invalid change note');
    if(row.state==='written'&&(row.parentID!==null||row.recordedAt!==null))fail('written source must be a root with unknown recording time');
    if(row.state==='planned'){
      if(row.number===null||row.parentID===null||!row.changeNote.trim())fail('planned take needs a number, parent and change note');
      if(typeof row.recordedAt!=='string'||!/^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d{1,6})?(?:Z|[+-]\d\d:\d\d)$/.test(row.recordedAt)||!Number.isFinite(Date.parse(row.recordedAt)))fail('planned take needs an ISO recording time');
    }
    validateSnapshot(row.snapshot,row.shotID);
    canonical(row);
  }
  function merge(...ledgers){
    const rows=new Map();
    for(const ledger of ledgers){
      if(!object(ledger)||ledger.format!==FORMAT||!Array.isArray(ledger.takes))fail('invalid ledger');
      for(const row of ledger.takes){validateRecord(row);const previous=rows.get(row.id);if(previous&&canonical(previous)!==canonical(row))fail('immutable record conflict: '+row.id);rows.set(row.id,copy(row));}
    }
    for(const row of rows.values()){
      if(row.parentID!==null){const parent=rows.get(row.parentID);if(!parent||scope(parent)!==scope(row))fail('missing or cross-shot parent: '+row.id);if(row.number!==(parent.number===null?1:parent.number+1))fail('take number does not follow parent');}
      const visited=new Set([row.id]);let parent=row.parentID;
      while(parent!==null){if(visited.has(parent))fail('cyclic take history');visited.add(parent);parent=rows.get(parent)?.parentID??null;}
    }
    return {format:FORMAT,takes:[...rows.values()].sort((a,b)=>a.id<b.id?-1:a.id>b.id?1:0)};
  }
  function forShot(ledger,project,storyID,shotID){return merge(ledger).takes.filter(row=>row.project===project&&row.storyID===storyID&&row.shotID===shotID);}
  function current(ledger,project,storyID,shotID){
    const rows=forShot(ledger,project,storyID,shotID),parents=new Set(rows.map(row=>row.parentID)),leaves=rows.filter(row=>!parents.has(row.id));
    return leaves.length===1?leaves[0]:null;
  }
  function copiedStatus(field){
    if(['missing','unknown','not_needed'].includes(field.status))return field.status;
    return ['draft','present','verified','accepted'].includes(field.status)&&field.text.trim()?'draft':'unknown';
  }
  function plannedSnapshot(base,number){
    const snapshot=copy(base),shot=snapshot.shot;
    shot.stage='preliminary';shot.revision='take '+number;shot.authoringStatus='Planned take · direction and handoff need reconciliation';shot.kitchenWritten=false;shot.handoffNeedsReconciliation=true;shot.dependencyReviewNeeded=true;
    const reset=new Set(['settings','results','acceptance']);
    shot.fields=shot.fields.filter(f=>!reset.has(f.key));
    for(const key of reset)shot.fields.push({key,text:'',status:'unknown',evidence:[],note:RESET_NOTE});
    for(const field of shot.fields){
      if(['accepted','verified'].includes(field.status)){field.status=copiedStatus(field);field.note=[field.note,REVIEW_NOTE].filter(Boolean).join(' ');}
      if(['prompt_still','prompt_clip'].includes(field.key)){field.status=copiedStatus(field);field.note=UPDATE_NOTE;}
    }
    shot.kitchen=(shot.kitchen||[]).map(field=>({...field,status:copiedStatus(field),note:HANDOFF_NOTE}));
    if(shot.materials)shot.materials=shot.materials.filter(row=>row.role!=='result_on_disk');
    if(snapshot.foundation){snapshot.foundation.dependencyReviewNeeded=true;snapshot.foundation.notes=[...(snapshot.foundation.notes||[]),HANDOFF_NOTE];}
    return snapshot;
  }
  function plan(ledger,options){
    const result=merge(ledger);if(!object(options))fail('planning options required');
    const {project,storyID,shot,foundation=null,id,recordedAt}=options,changeNote=typeof options.changeNote==='string'?options.changeNote.trim():'';
    token(project,'project');token(storyID,'storyID');token(id,'id');
    if(!object(shot)||!Array.isArray(shot.fields))fail('shot fields required');token(shot.shotID,'shotID');if(!changeNote)fail('describe what changes in the next take');
    if(result.takes.some(row=>row.id===id))fail('take ID already exists');
    const rows=forShot(result,project,storyID,shot.shotID);let parent=current(result,project,storyID,shot.shotID);
    if(rows.length&&!parent)fail('conflicting branches must be reconciled before planning');
    if(!parent){
      const snapshot=copy({shot,foundation});validateSnapshot(snapshot,shot.shotID);const match=/^take (\d+)/i.exec(shot.revision||'');
      parent={id:'source:'+sha256(canonical({project,storyID,shotID:shot.shotID,snapshot})),project,storyID,shotID:shot.shotID,number:match?Number(match[1]):null,parentID:null,state:'written',recordedAt:null,changeNote:'',snapshot};
      result.takes.push(parent);
    }
    const number=parent.number===null?1:parent.number+1;
    result.takes.push({id,project,storyID,shotID:shot.shotID,number,parentID:parent.id,state:'planned',recordedAt,changeNote,snapshot:plannedSnapshot(parent.snapshot,number)});
    return merge(result);
  }
  return {empty,merge,forShot,current,plan};
});
