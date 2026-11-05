/* Local render/behavior regression check. This is a fake DOM, not browser QA. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const source = fs.readFileSync(path.join(__dirname, 'library.js'), 'utf8');
const catalogText = fs.readFileSync(path.join(__dirname, 'catalog.js'), 'utf8');
const catalog = JSON.parse(catalogText.split('=').slice(1).join('=').trim().replace(/;$/, ''));
const nodes = new Map();
const writes = [];
function element() {
  return {innerHTML:'', value:'', dataset:{}, classList:{toggle(){}},
    setAttribute(){}, addEventListener(){}, append(){}, querySelector(){return null;},
    querySelectorAll(){return [];}, showModal(){this.open=true;}, close(){this.open=false;}};
}
const document = {
  currentScript:{src:'file:///D:/Documents/CFA/docs/notes/explorable_world/comfy/projects/visual_library/library.js'},
  body:element(), createElement:element, addEventListener(){},
  querySelector(selector){if(!nodes.has(selector))nodes.set(selector,element());return nodes.get(selector);},
  querySelectorAll(){return [];}
};
const window = {REVIEW_CATALOG:catalog, REVIEW_INITIAL:{project:'hon',view:'all'}, addEventListener(){},scrollTo(){},scrollBy(){}};
const context = {window,document,location:{hash:'#hon/all'},URL,Intl,console,setTimeout,clearTimeout,
  localStorage:{getItem(){return null;},setItem(...args){writes.push(args);}},
  sessionStorage:{getItem(){return null;},setItem(){}}};
const exposed = source.replace(/\}\)\(\);\s*$/, `window.__outfitTest={normalVisible,outfitGroups,outfitCover,outfitExplorer,sharedCharacterAlbums,renderMain,expandedOutfits,expandedCollections,reviews,reviewRecord,setState(p){Object.assign(state,p);},getState(){return state;}};})();`);
vm.runInNewContext(exposed,context);
const api=window.__outfitTest;
const media=catalog.assets.filter(a=>a.project==='hon'&&!a.archived&&a.kind==='image');
const groups=api.outfitGroups(media), armor=groups.find(g=>g.al.id==='hon:outfit-armor');
assert(armor && armor.items.length>=6, 'Actual armored outfit views are present');
assert.equal(api.outfitCover(armor.items).id,'HD-DROP-89ca1a75a89d','Choose the portrait instead of the first source/full-body image');
assert(groups.find(g=>g.al.id==='hon:outfit-pinstripe').items.some(a=>a.propState==='with_gun'),'Gun variant remains in the original outfit');
let html=nodes.get('#main').innerHTML;
assert.equal((html.match(/data-outfit-collection=/g)||[]).length,groups.length,'All files has one compact entry per outfit');
assert(!html.includes('data-open="HD-DROP-3abfbd30bd96"'),'Collapsed armor does not dump its full-body view');
assert(html.includes('Verbose BOM'),'Detailed shared references appear once');
assert.equal((html.match(/aria-label="Verbose BOM"/g)||[]).length,1);
assert(html.includes('data-album="hon:outfit-armor"'),'Cover opens outfit collection');
api.expandedOutfits.add('hon:outfit-armor');api.renderMain();html=nodes.get('#main').innerHTML;
assert(html.includes('data-open="HD-DROP-3abfbd30bd96"'),'Expanding exposes individual reviewable views');
const expandedOutfitControls=[...html.matchAll(/<button\b[^>]*data-outfit-toggle="([^"]+)"[^>]*>/g)].filter(match=>/aria-expanded="true"/.test(match[0])).map(match=>match[1]);
assert.deepEqual(expandedOutfitControls,['hon:outfit-armor'],'Only the requested outfit expands; independent browse buckets are not outfits');
api.expandedOutfits.clear();api.setState({outfitLayout:'all'});api.renderMain();html=nodes.get('#main').innerHTML;
assert(html.includes('data-open="HD-DROP-3abfbd30bd96"'),'Show all views retains individual media access');
assert(!html.includes('data-outfit-collection='));
api.setState({view:'outfits',album:'hon:outfit-yellow',outfitLayout:'compact'});api.renderMain();html=nodes.get('#main').innerHTML;
assert(html.includes('Gun variants')&&html.includes('Other views &amp; revisions'),'Opening outfit preserves prop grouping');
assert(html.includes('data-open="HD-DROP-6c2e98bd1125"'),'Opening card lands on view gallery, not a singleton modal');
const portrait=armor.items.find(a=>a.id==='HD-DROP-89ca1a75a89d');
api.reviews.set(portrait.id,{id:portrait.id,status:'remove',note:'keep my note'});
assert(!api.outfitGroups(media).find(g=>g.al.id===armor.al.id).items.some(a=>a.id===portrait.id),'Removal filter applies to covers and views');
assert.equal(api.reviewRecord(portrait.id).note,'keep my note','Browsing preserves review note');
api.reviews.delete(portrait.id);
const gun=groups.find(g=>g.al.id==='hon:outfit-yellow').items.find(a=>a.propState==='with_gun');
const filtered=api.outfitGroups([gun]);
assert.equal(filtered.length,1);assert.equal(filtered[0].al.id,'hon:outfit-yellow');assert.equal(filtered[0].items.length,1);
api.setState({view:'all',album:'',search:'mouth',outfitLayout:'compact'});api.renderMain();html=nodes.get('#main').innerHTML;
const mouth=catalog.assets.find(a=>a.project==='hon'&&a.kind==='image'&&api.normalVisible(a)&&/mouth/i.test(a.album)&&catalog.sharedReferenceCollections.some(g=>(g.assetIDs||[]).includes(a.id)));
const mouthCollection=catalog.sharedReferenceCollections.find(g=>(g.assetIDs||[]).includes(mouth?.id));
assert(mouth&&mouthCollection&&html.includes('data-collection-toggle="'+mouthCollection.id+'"'),'Search finds the matching shared mouth collection');
api.expandedCollections.add(mouthCollection.id);api.renderMain();html=nodes.get('#main').innerHTML;
assert(html.includes('data-open="'+mouth.id+'"'),'Matching shared mouth media remains reviewable after inline expansion');
for(const project of ['hon','lisan']){
 api.setState({project,view:'outfits',album:'',search:'',outfitLayout:'compact'});api.renderMain();html=nodes.get('#main').innerHTML;
 for(const unwanted of ['shared-character-references','mouth-coverage-board','accessory-explorer'])assert(!html.includes(unwanted),project+' outfit index stays scoped: '+unwanted);
 const album=catalog.albums.find(a=>a.project===project&&a.category==='outfits'&&(project!=='hon'||a.id==='hon:outfit-vest'));
 assert(album);api.setState({album:album.id});api.renderMain();html=nodes.get('#main').innerHTML;
 const displayedIDs=[...html.matchAll(/data-open="([^"]+)"/g)].map(m=>m[1]);assert(displayedIDs.length);
 assert(displayedIDs.every(id=>album.assetIDs.includes(id)),project+' collection shows only its own assets');
 for(const unwanted of ['shared-character-references','mouth-coverage-board','accessory-explorer'])assert(!html.includes(unwanted));
 if(project==='hon')assert.equal(new Set(displayedIDs).size,8,'Smuggler vest has its eight views only');
}
api.setState({project:'hon',view:'working',album:'',search:''});api.expandedCollections.add('hon:character-bom');api.expandedCollections.add('hon:permanent-accessories');api.renderMain();html=nodes.get('#main').innerHTML;
assert(html.includes('shared-character-references')&&html.includes('mouth-coverage-board'),'Shared reference overview is accessible in Working references');
assert(html.includes('collection-sections-grid'),'Accessory categories use a responsive category grid');
for(const title of ['Locked wrist jewelry','Existing hand/ring context','Chain-mouth interaction candidate'])assert(html.includes(title));
api.setState({view:'details',detailLayout:'all'});api.expandedCollections.add('hon:piercings');api.renderMain();html=nodes.get('#main').innerHTML;
assert(html.includes('Piercings and jewelry')&&!html.includes('accessory-explorer'),'Details puts jewelry under one category, with character specifics inside');
for(const title of ['Locked wrist jewelry','Existing hand/ring context','Chain-mouth interaction candidate'])assert(html.includes('Dolo · '+title),'Existing accessory category remains nested and accessible');
assert.equal(writes.length,0,'Browsing never rewrites review or favorite storage');
console.log(JSON.stringify({passed:true,outfits:groups.length,armorViews:armor.items.length,checks:15,browserVisualQA:false}));
