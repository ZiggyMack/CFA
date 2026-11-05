/* Location Scout regression checks against the real catalog.
   The DOM double verifies markup, handlers and persistence semantics; browser layout is checked separately. */
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');
const clone=value=>JSON.parse(JSON.stringify(value));
const source=fs.readFileSync(path.join(__dirname,'library.js'),'utf8');
const catalog=JSON.parse(fs.readFileSync(path.join(__dirname,'catalog.js'),'utf8').split('=').slice(1).join('=').trim().replace(/;$/,''));
const REVIEW_KEY='cfa-visual-review-v1';

function boot(saved={},hash='#criminal_mind/locations'){
  const elements=new Set(),nodes=new Map(),storage=new Map(Object.entries(saved)),writes=[];
  const decode=value=>value.replace(/&quot;/g,'"').replace(/&#39;/g,"'").replace(/&amp;/g,'&').replace(/&lt;/g,'<').replace(/&gt;/g,'>');
  const dataKey=name=>name.replace(/^data-/,'').replace(/-([a-z])/g,(_,letter)=>letter.toUpperCase());
  class Element{
    constructor(tag='div'){
      this.tag=tag;this.dataset={};this.attributes={};this.children=new Set();this.listeners=new Map();this._html='';this.value='';this.open=false;
      this.classList={toggle(){},add(){},remove(){},contains:name=>(this.attributes.class||'').split(/\s+/).includes(name)};elements.add(this);
    }
    set innerHTML(html){
      for(const child of this.children)elements.delete(child);this.children.clear();this._html=html;
      for(const match of html.matchAll(/<([a-z][\w-]*)\b([^>]*)>/gi)){
        const child=new Element(match[1]);
        for(const attribute of match[2].matchAll(/([\w-]+)="([^"]*)"/g))child.setAttribute(attribute[1],decode(attribute[2]));
        child.disabled=/(?:^|\s)disabled(?:\s|$)/.test(match[2]);this.children.add(child);
      }
    }
    get innerHTML(){return this._html;}
    setAttribute(name,value){this.attributes[name]=String(value);if(name.startsWith('data-'))this.dataset[dataKey(name)]=String(value);else if(name==='id'){this.id=String(value);nodes.set('#'+this.id,this);}else this[name]=value;}
    addEventListener(name,callback){if(!this.listeners.has(name))this.listeners.set(name,[]);this.listeners.get(name).push(callback);}
    click(){if(this.disabled)return;const event={target:this,preventDefault(){}};this.onclick?.(event);for(const callback of this.listeners.get('click')||[])callback(event);}
    append(child){this.children.add(child);if(child.id)nodes.set('#'+child.id,child);}
    querySelector(){return null;}querySelectorAll(){return [];}getBoundingClientRect(){return {top:100};}focus(){this.focused=true;}showModal(){this.open=true;}close(){this.open=false;}remove(){elements.delete(this);}
  }
  nodes.set('#app',new Element());
  const selectAll=selector=>{const match=/^\[([\w-]+)(?:="([^"]*)")?\]$/.exec(selector);if(!match)return[];return[...elements].filter(element=>Object.hasOwn(element.attributes,match[1])&&(match[2]===undefined||element.attributes[match[1]]===match[2]));};
  const document={currentScript:{src:'file:///D:/Documents/CFA/docs/notes/explorable_world/comfy/projects/visual_library/library.js'},body:new Element('body'),createElement:tag=>new Element(tag),addEventListener(){},querySelector:selector=>nodes.get(selector)||selectAll(selector)[0]||null,querySelectorAll:selectAll};
  const location={hash},window={REVIEW_CATALOG:clone(catalog),REVIEW_INITIAL:{project:'criminal_mind',view:'locations'},addEventListener(){},scrollTo(){},scrollBy(){}};
  const context={window,document,location,URL,Blob,Intl,console,setTimeout(){return 1;},clearTimeout(){},localStorage:{getItem:key=>storage.get(key)??null,setItem(key,value){storage.set(key,value);writes.push([key,value]);}},sessionStorage:{getItem(){return null;},setItem(){}}};
  const hook=`window.__locationTest={C,route,renderMain,locationFamilies,locationFamilyCount,storyboardSequenceCount,supportingCastCount,outfitCollectionCount,accessoryUnitCount,workingReferenceSetCount,locationScoutSelection,reviewRecord,reviewPayload,importReview,updateReview,selectedReviewScope,getState:()=>state,setCasaStage(value){state.casaStages=state.casaStages||{};state.casaStages[state.project]=value;},setReviewIdentity(project,actor,scope){actorSelections.set(project,actor);scopeSelections.set(project,scope);}};`;
  const instrumented=source.replace(/\}\)\(\);\s*$/,hook+'})();');assert.notEqual(instrumented,source,'Location test hook attached');vm.runInNewContext(instrumented,context);
  return{
    api:window.__locationTest,location,writes,storage,
    html:()=>nodes.get('#main').innerHTML,shell:()=>nodes.get('#app').innerHTML,
    click(attribute,value){const control=selectAll('['+attribute+']').find(element=>element.attributes[attribute]===value);assert(control,'Control exists: '+attribute+'='+value);control.click();},
    snapshot:()=>Object.fromEntries(storage)
  };
}

const page=boot(),api=page.api;
const families=clone(api.locationFamilies('criminal_mind',false));
assert.equal(families.length,24,'Forty-four albums consolidate into 24 explicit location families');
assert.equal(families.reduce((count,family)=>count+family.items.length,0),956,'All 956 logical assets remain in the scout inventory');
assert.equal(new Set(families.flatMap(family=>family.items.map(asset=>asset.id))).size,956,'Only asset IDs are deduplicated');
assert.equal(new Set(families.flatMap(family=>family.items.map(asset=>asset.sha256))).size,954,'Same-hash logical records remain separate');
assert.equal(api.storyboardSequenceCount('criminal_mind'),41,'Storyboard navigation counts authored sequences, not 165 planned shots');
assert.equal(api.locationFamilyCount('criminal_mind'),24,'Locations navigation counts unique recorded places, not 956 references');
assert.equal(api.supportingCastCount('criminal_mind'),33,'Supporting cast navigation counts unique characters, not their artifacts');
assert.deepEqual(['hon','lisan','criminal_mind'].map(project=>[project,api.outfitCollectionCount(project),api.accessoryUnitCount(project),api.workingReferenceSetCount(project)]),[
  ['hon',22,18,11],['lisan',51,11,2],['criminal_mind',0,0,0]
],'Outfits, Accessories and Working references count their browse units across projects');
assert.match(page.shell(),/data-view="locations"[^>]*>Locations <span class="count">24<\/span>/);
assert.match(page.shell(),/data-view="storyboard"[^>]*>Storyboard<span class="count">41<\/span>/);
assert.match(page.shell(),/data-view="cast"[^>]*>Supporting cast<span class="count">33<\/span>/);
const honNav=boot({},'#hon/all'),lisanNav=boot({},'#lisan/all');
for(const [shell,counts] of [[honNav.shell(),{working:11,outfits:22,details:18}],[lisanNav.shell(),{working:2,outfits:51,details:11}]])for(const [view,count] of Object.entries(counts))assert.match(shell,new RegExp('data-view="'+view+'"[^>]*>[^<]+<span class="count">'+count+'<\\/span>'));
const emptyWorking=boot({},'#criminal_mind/working');assert(!emptyWorking.html().includes('criminal_mind:character-bom'),'Unrelated Criminal Mind media cannot fabricate a Working-reference character card');
assert.equal(families.find(family=>family.id==='TCM-SET-HENDERSON-EXTERIOR').albums.length,2,'Base-look and camera albums share their recorded family');
assert.equal(families.find(family=>family.id==='TCM-SET-HENDERSON-EXTERIOR').lanes.look.length,10);
assert(families.find(family=>family.id==='TCM-SET-HENDERSON-EXTERIOR').lanes.coverage.length>10);
assert.match(page.html(),/24 recorded places/);assert.match(page.html(),/Story &amp; coverage brief|Story & coverage brief/);
assert.equal([...page.html().matchAll(/data-location-asset=/g)].length<=11,true,'Initial filmstrip is bounded');
assert.equal([...page.html().matchAll(/class="location-hero"/g)].length,1,'Only one hero reference is mounted');
assert(!page.html().includes('class="media-card"'),'The location room no longer mounts the generic 956-card gallery');

const before=clone(api.reviewPayload()),catalogBefore=JSON.stringify(api.C);delete before.exported;
page.click('data-location-family','TCM-SET-IMPALA');page.click('data-location-lane','coverage');
let selection=api.locationScoutSelection();assert.equal(selection.family.id,'TCM-SET-IMPALA');assert.equal(selection.lane,'coverage');assert(selection.positions.length>1,'Recorded camera positions become a camera map');
const nextPosition=selection.positions.find(value=>value!==selection.position);page.click('data-location-position',nextPosition);selection=api.locationScoutSelection();assert.equal(selection.position,nextPosition);
if(selection.items.length>1){const first=selection.asset.id;page.click('data-location-step','1');assert.notEqual(api.locationScoutSelection().asset.id,first,'Reference stepping changes only UI focus');}
const after=clone(api.reviewPayload());delete after.exported;assert.deepEqual(after,before,'Family, lane, camera-position and reference navigation do not mutate reviews');
assert.equal(JSON.stringify(api.C),catalogBefore,'Display regrouping never mutates catalog metadata');assert.equal(page.writes.length,0,'Pure scout navigation performs no storage writes');

api.setCasaStage('locations');api.route('criminal_mind','casa_baldadoon');assert.match(page.html(),/Director’s chair · Location scout/);assert.match(page.html(),/Open shared Locations library/);assert.equal(api.locationScoutSelection().family.id,'TCM-SET-IMPALA','Casa reuses the shared scout selection and inventory');
for(const project of ['hon','lisan']){api.route(project,'locations');assert.equal(api.getState().view,'locations');assert.match(page.html(),/No location families have been recorded for this project yet/);}

api.route('criminal_mind','locations');
const henderson='TCM-SET-HENDERSON-EXTERIOR-L03',sibling='TCM-SET-HENDERSON-EXTERIOR-L02',sourceAsset=api.C.assets.find(asset=>asset.id===henderson);
assert(sourceAsset.relayedAuthorChoiceSignal,'The narrowly scoped relayed author signal remains catalog evidence');
assert.equal(sourceAsset.relayedAuthorChoiceSignal.reviewEvidenceStatus,'recovered_favorite_or_basket_only_no_attributed_saved_review');
assert.equal(api.reviewRecord(henderson).note,'','No missing Henderson note is invented or misattributed');
page.click('data-location-family','TCM-SET-HENDERSON-EXTERIOR');page.click('data-location-lane','look');page.click('data-location-asset',henderson);page.click('data-location-review',henderson);
assert.equal(api.selectedReviewScope('criminal_mind'),'location','The scout review entry point preselects an exact location decision scope');assert.equal(api.reviewRecord(henderson).note,'');
api.setReviewIdentity('criminal_mind','baldadoon','location');
assert.equal(api.updateReview(henderson,{note:'Synthetic location-only direction for round-trip testing.'}),true);
let record=clone(api.reviewRecord(henderson));assert.equal(record.decisionScope,'location');assert.equal(record.reviewerControllerID,'baldadoon');assert.equal(record.humanReview.assetID,henderson);assert.equal(record.humanReview.sha256,sourceAsset.sha256);assert.equal(record.status,null,'A note does not choose a review outcome');assert.equal(api.reviewRecord(sibling).note,'','Sibling options remain untouched');
api.route('criminal_mind','all');api.route('criminal_mind','locations');assert.equal(api.reviewRecord(henderson).note,record.note,'Location-only note survives navigation');
const exported=clone(api.reviewPayload()),restored=boot({},'#criminal_mind/locations');restored.api.importReview(exported);record=clone(restored.api.reviewRecord(henderson));assert.equal(record.note,'Synthetic location-only direction for round-trip testing.');assert.equal(record.decisionScope,'location');assert.equal(record.humanReview.assetID,henderson);assert.equal(record.humanReview.sha256,sourceAsset.sha256);assert.equal(restored.api.reviewRecord(sibling).note,'');

console.log(JSON.stringify({passed:true,families:families.length,assets:956,uniqueHashes:954,boundedFilmstrip:11,sharedProjects:3,locationNoteRoundTrip:true,browserVisualQA:false}));
