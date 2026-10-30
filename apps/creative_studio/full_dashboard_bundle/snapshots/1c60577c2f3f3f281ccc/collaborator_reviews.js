/* Persistence-only counterpart of creative_studio/collaborator_review.py. */
(function(root){
  'use strict';
  const FORMAT='cfa-collaborator-review-v1';
  const CHOICES=new Set(['','meets_brief','needs_correction','reject','cannot_assess']);
  const DIRECTIONS=new Set(['','bounded_corrections','hold_clarify','nominate_motion']);
  // Generated from native QUESTIONS/EVIDENCE; parity tests protect this copy.
  const PILOT={"version":"hon-grok-return-20261008-v1","questions":[{"id":"REV-HD-001","title":"Cash-counting vest","assetID":"HD-RETURN-bc5b8c111da7","sha256":"bc5b8c111da73c15d0e0a69462ba2a416e1fc2b7364577354c439509655aeb00","source":{"assetID":"HD-DROP-2691712601a9","sha256":"2691712601a9da9ab3c629b2c1d3204cdd1106cb64c301218aec1eb63182b702"},"request":"Correct visible tattoos and details while preserving the cash-counting vest, money/table, ship interior, composition and lighting.","question":"Does this return deliver the detail correction while keeping the selected cash-counting outfit and scene?","known":"The intake records that REV-HD-001 changed the vest and scene. Review that preservation failure explicitly; a good new image does not by itself fulfill this correction."},{"id":"REV-HD-002","title":"Black overcoat","assetID":"HD-RETURN-cfcf8f8004ef","sha256":"cfcf8f8004ef76784c2867412a2a38648edd170820c1bec17d9b35b0795edb94","source":{"assetID":"HD-DROP-56a50dabe9e0","sha256":"56a50dabe9e0357f3512288b0f5ade4d68d9afa1a080f80d111e047f96827057"},"request":"Correct visible tattoos, mouth and jewelry against the supplied design reference. Preserve the black overcoat, night boarding ramp, composition and atmosphere.","question":"Are the visible details corrected with the selected overcoat and night boarding scene preserved?"},{"id":"REV-HD-003","title":"Pinstripe suit","assetID":"HD-RETURN-9158a4df3f42","sha256":"9158a4df3f4218350a2d30155dbc3c767fb80a01e71ebfb861c1dc416406bd5c","source":{"assetID":"HD-DROP-1966838931ad","sha256":"1966838931adb71d4443b608d65b9c3613bdc7de7fd6ce3e38c9b35e344e51f7"},"request":"Correct visible face/neck, teeth and jewelry. Keep the navy three-piece, tie and tie bar, pocket square, watch, pose and polished office mood. Keep the chest covered.","question":"Does this prepare the pinstripe look without changing the selected wardrobe or exposing covered details?"},{"id":"REV-HD-004","title":"Western fringe / saloon","assetID":"HD-RETURN-26a91590b6c0","sha256":"26a91590b6c03f3c8de62f4ab69e0b4ce7d466b7707a2e9cf426c771a69c79ec","source":{"assetID":"HD-DROP-bb0780a46f7d","sha256":"bb0780a46f7d6f0ef5493939ba1f1920366dd670ff8b5da3738c3c04672ec596"},"request":"Repair the visible blaster/holster and belt attachment. Preserve western fringe, dark shirt, bolo tie, pose and saloon. Match visible character details; the hip side is provisional for this proof.","question":"Is the prop coherent and seated in its holster while the selected saloon look and visible character details stay intact?","known":"The provider reports a revolver-like prop, a re-staged saloon and expression, and overly long canines. This exact image is also cataloged as HIP-SALOON-01; it is byte-identical to the REV-HD-004 return."},{"id":"PROP-HD-HIP","title":"Hip detail","assetID":"HD-RETURN-41b93f64e7ea","sha256":"41b93f64e7ea7199974101575b5704ce037f019e02e507e2b70cb1b499263350","source":{"assetID":"HD-RETURN-26a91590b6c0","sha256":"26a91590b6c03f3c8de62f4ab69e0b4ce7d466b7707a2e9cf426c771a69c79ec"},"request":"Provide a matching detail of the repaired sci-fi blaster/holster, readable attachment and overlap. A labeled crop of the corrected proof is allowed; it is not original hardware artwork.","question":"Does the close view make the intended prop and attachment clear enough, or what must change?","known":"The recorded return is an upscaled crop of generated REV-HD-004. The provider reports a western-revolver appearance and provisional character-left / viewer-right placement. No global side choice is established here."},{"id":"CALEB-K_REF","title":"Caleb character proof","assetID":"HD-RETURN-147fbed5f795","sha256":"147fbed5f795c025ddddaa45598311c7ea40212e8d35f3d50df08bd0ff1b9cd1","request":"Propose one neutral Caleb K reference: a distinct middle-aged white male lawyer, restrained wardrobe, no supplied real-person likeness. Any invented tattoo requires its companion design sheet.","question":"Does this candidate work as the Caleb concept requested, or what should change before using him in the scene?","known":"This is a new character proposal, with no approved likeness in the original brief. Provider notes say no tattoos or piercings were invented."},{"id":"CAL-P01","title":"Hon Dolo + Caleb meeting","assetID":"HD-RETURN-d50fe2346406","sha256":"d50fe23464067486851627ce626652129c51b981bd4041bebb9fafcf2dc4f232","source":{"assetID":"HD-DROP-9cecaad5ed57","sha256":"9cecaad5ed5764a4109c053b17fb09afd7bb0f97557fe61f88a2f72ac73cca5a"},"request":"One friendly saloon master with Hon Dolo and Caleb: distinct faces, clear eyelines and separate hands. Preserve Hon's fringe/bar alpha and visible current details. No invented dialogue, lyric timing or lip-sync.","question":"Does the interaction work, and what continuity fixes are still needed before this scene can move forward?","known":"The intake records tattoo-placement defects in CAL-P01. Caleb's neutral proof is a candidate reference, not an accepted master."}],"evidence":[{"assetID":"hon:doc:docs/notes/explorable_world/comfy/projects/hon_dolo_strictly_business/handoffs/grok_20261008/START_HERE.txt","sha256":"56a80126d9990736496440eb1b511386aee499e4ca2656033f5b5361089a1386","role":"October 8 requested work"},{"assetID":"hon:doc:docs/notes/explorable_world/comfy/projects/hon_dolo_strictly_business/grok_return_20261009/START_HERE.txt","sha256":"dd10817e01ab7bd6d19c76e640c35072e7f6dcf49cba4943ba2a470a9abb2f18","role":"October 9 verified receipt and limits"},{"assetID":"hon:doc:docs/notes/explorable_world/comfy/projects/collaborators/grok_design_instructions.txt","sha256":"938be3298404548c5ea07063d56569369e68d2b3a20f09411ccb444da78d7820","role":"Living design instructions supersede dated detail rules; Hon has four upper gold caps, not the old two-canines-only pattern"}]};
  const object=value=>value!==null&&typeof value==='object'&&!Array.isArray(value);
  const own=(value,key)=>Object.prototype.hasOwnProperty.call(value,key);
  function text(value,label,limit=20000,required=false){
    if(typeof value!=='string'||[...value].length>limit||(required&&!value.trim()))throw Error(`Invalid collaborator review ${label}.`);
    return value;
  }
  function time(value){
    text(value,'timestamp',128,true);
    const match=/^(\d{4})-(\d{2})-(\d{2})[T ](\d{2}):(\d{2})(?::(\d{2})(?:[.,](\d+))?)?(Z|[+-]\d{2}:?\d{2})$/.exec(value);
    if(!match)throw Error('Collaborator review timestamps must include a valid timezone.');
    const [,year,month,day,hour,minute,second='0',fraction='',zone]=match;
    const date=new Date(0);date.setUTCFullYear(+year,+month-1,+day);date.setUTCHours(+hour,+minute,+second,0);
    const offset=zone==='Z'?0:(zone[0]==='-'?-1:1)*(Number(zone.slice(1,3))*60+Number(zone.replace(':','').slice(3,5)));
    if(+year<1||date.getUTCFullYear()!==+year||date.getUTCMonth()!==+month-1||date.getUTCDate()!==+day||+hour>23||+minute>59||+second>59||Math.abs(offset)>=1440||zone!=='Z'&&Number(zone.replace(':','').slice(3,5))>59)throw Error('Collaborator review timestamps must include a valid timezone.');
    return BigInt(date.getTime()-offset*60000)*1000n+BigInt((fraction+'000000').slice(0,6));
  }
  function jsonValue(value){
    if(value===null||typeof value==='string'||typeof value==='boolean')return;
    if(typeof value==='number'&&Number.isFinite(value))return;
    if(Array.isArray(value)){for(const item of value)jsonValue(item);return;}
    if(object(value)&&Object.prototype.toString.call(value)==='[object Object]'){
      for(const item of Object.values(value))jsonValue(item);return;
    }
    throw Error('Collaborator reviews must contain only finite JSON values.');
  }
  const copy=value=>JSON.parse(JSON.stringify(value));
  const stable=value=>JSON.stringify(value,function(key,item){return object(item)?Object.fromEntries(Object.keys(item).sort().map(k=>[k,item[k]])):item;});
  function answers(value){
    if(!object(value)||Object.keys(value).length>100)throw Error('Collaborator review answers must be an object.');
    for(const [key,answer] of Object.entries(value)){
      text(key,'question ID',512,true);
      if(!object(answer)||!CHOICES.has(answer.choice))throw Error('Invalid collaborator review answer.');
      text(answer.note,'note');
      if(!object(answer.reference))throw Error('An answer needs its exact reference.');
      text(answer.reference.assetID,'asset ID',512,true);
      if(typeof answer.reference.sha256!=='string'||!/^[a-f0-9]{64}$/.test(answer.reference.sha256))throw Error('An answer needs its exact reference hash.');
      time(answer.updatedAt);
    }
  }
  function direction(value){
    if(!object(value)||!DIRECTIONS.has(own(value,'choice')?value.choice:''))throw Error('Invalid collaborator review next action.');
    text(own(value,'note')?value.note:'','next-action note');
    if(own(value,'assetID'))text(value.assetID,'nominated asset ID',512);
  }
  function complete(record){
    if(record.questionnaireVersion!==PILOT.version)return false;
    for(const question of PILOT.questions){
      const answer=record.answers[question.id],reference={assetID:question.assetID,sha256:question.sha256};
      if(!answer||stable(answer.reference)!==stable(reference)||!answer.choice||answer.choice!=='meets_brief'&&!answer.note.trim())return false;
    }
    const next=record.direction;
    if(!next.choice||next.choice==='hold_clarify'&&!next.note?.trim())return false;
    if(next.choice==='nominate_motion'){
      const question=PILOT.questions.find(q=>q.assetID===next.assetID&&q.id!=='PROP-HD-HIP');
      if(!question||record.answers[question.id]?.choice!=='meets_brief')return false;
    }
    return true;
  }
  function normalize(value){
    if(!object(value)||Object.keys(value).length>500)throw Error('Collaborator reviews must be an object.');
    jsonValue(value);const result=copy(value);
    for(const [taskID,record] of Object.entries(result)){
      text(taskID,'task ID',512,true);
      if(!object(record)||record.format!==FORMAT||record.taskID!==taskID||!['draft','ready'].includes(record.state))throw Error('Invalid collaborator review record.');
      text(record.questionnaireVersion,'questionnaire version',512,true);time(record.updatedAt);answers(record.answers);direction(record.direction);
      if(!Array.isArray(record.replies)||record.replies.length>1000)throw Error('Collaborator reply history must be a list.');
      const seen=new Set();
      for(const reply of record.replies){
        if(!object(reply))throw Error('Invalid prepared reply.');
        text(reply.id,'reply ID',512,true);
        if(seen.has(reply.id))throw Error('Duplicate immutable reply ID.');seen.add(reply.id);
        time(reply.preparedAt);text(reply.questionnaireVersion,'reply version',512,true);answers(reply.answers);direction(reply.direction);
        if(reply.questionnaireVersion===PILOT.version&&(stable(reply.questions)!==stable(PILOT.questions)||stable(reply.evidence)!==stable(PILOT.evidence)||!complete(reply)))throw Error('Prepared reply does not contain the complete questionnaire and source evidence.');
      }
      if(!own(record,'readyReplyID'))record.readyReplyID=null;
      if(record.state==='ready'){
        const snapshot=record.replies.find(reply=>reply.id===record.readyReplyID);
        if(!snapshot||['questionnaireVersion','answers','direction'].some(key=>stable(snapshot[key])!==stable(record[key])))throw Error('A ready reply must match its frozen answer snapshot.');
        if(record.questionnaireVersion===PILOT.version&&!complete(record))throw Error('A ready reply has unanswered required questions.');
      }else if(record.readyReplyID!==null)throw Error('A draft cannot retain an active ready reply.');
    }
    return result;
  }
  function merge(...mappings){
    const result=Object.create(null);
    for(const mapping of mappings)for(const [taskID,incoming] of Object.entries(normalize(mapping))){
      if(!own(result,taskID)){result[taskID]=incoming;continue;}
      const prior=result[taskID],history=new Map(prior.replies.map(reply=>[reply.id,reply]));
      for(const reply of incoming.replies){
        if(history.has(reply.id)&&stable(history.get(reply.id))!==stable(reply))throw Error('Conflicting immutable collaborator reply ID: '+reply.id);
        history.set(reply.id,reply);
      }
      const oldTime=time(prior.updatedAt),newTime=time(incoming.updatedAt);
      if(oldTime===newTime&&['questionnaireVersion','state','answers','direction','readyReplyID'].some(key=>stable(prior[key])!==stable(incoming[key])))throw Error('Conflicting collaborator answers at the same timestamp: '+taskID);
      result[taskID]=newTime>=oldTime?{...prior,...incoming}:{...incoming,...prior};
      result[taskID].replies=[...history.values()];
    }
    return normalize(result);
  }
  function mergeBackups(...lists){
    const result=[],seen=new Set();
    for(const list of lists){
      if(!Array.isArray(list)||list.length>1000)throw Error('Collaborator review backups must be a list.');
      for(const record of list){
        if(!object(record)||typeof record.origin!=='string'||typeof record.reason!=='string'||!own(record,'data'))throw Error('Invalid collaborator review backup.');
        text(record.origin,'backup origin',512,true);text(record.reason,'backup reason',20000,true);
        jsonValue(record);const key=stable(record);
        if(!seen.has(key)){seen.add(key);result.push(copy(record));}
      }
    }
    return result;
  }
  const api={normalize,merge,mergeBackups};
  if(typeof module==='object'&&module.exports)module.exports=api;
  if(root)root.CFACollaboratorReviews=api;
})(typeof window!=='undefined'?window:globalThis);
