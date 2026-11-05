/* Hon outfit category controls against actual catalog + library.js.
   Node DOM harness only; no live browser, review writes, or catalog changes. */
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const L=__dirname,clone=x=>JSON.parse(JSON.stringify(x));
const raw=fs.readFileSync(path.join(L,'catalog.js'),'utf8'),catalog=JSON.parse(raw.slice(raw.indexOf('=')+1).trim().replace(/;$/,'')),source=fs.readFileSync(path.join(L,'library.js'),'utf8');
const REVIEW_KEY='cfa-visual-review-v1',FAVORITES_KEY='cfa-visual-favorites-v1';
const reference=fs.readFileSync(path.join(L,'test_reference_scope.cjs'),'utf8');
let body=reference.slice(reference.indexOf('function boot('),reference.indexOf('async function main()')).replace(/\r\n/g,'\n');
const oldHook='window.__scopeTest={openViewer,reviewRecord,reviewPayload,importReview,exportReference,inReviewQueue,whenFileWritesSettle(){return fileWriteChain;}};';
const hook='window.__scopeTest={C,outfitGroups,outfitCategoryGroups,renderMain,reviews,expandedOutfits,reviewRecord,reviewPayload,setState(p){Object.assign(state,p);},control(selector,value){return document.querySelectorAll(selector).find(b=>Object.values(b.dataset).includes(value));},whenFileWritesSettle(){return fileWriteChain;}};';
assert(body.includes(oldHook));body=body.replace(oldHook,hook);
// Parse the real buttons so tests click the same handlers used by the page.
const insertion=String.raw`      for(const tag of html.matchAll(/<button\b[^>]*>/gi)) {
        if(!/\bdata-/.test(tag[0]))continue;
        const id=/\bid="([^"]+)"/.exec(tag[0])?.[1]||'test-control-'+this.children.size;
        const child=nodes.get('#'+id)||new Element('button');child.id=id;
        child.disabled=/\bdisabled(?:\s|>)/.test(tag[0]);
        for(const attr of tag[0].matchAll(/data-([a-z-]+)="([^"]*)"/g))child.dataset[attr[1].replace(/-([a-z])/g,(_,c)=>c.toUpperCase())]=attr[2];
        nodes.set('#'+id,child);this.children.add(id);
      }
`;
const setterEnd='    }\n    get value() { return this._value; }';
assert(body.includes(setterEnd));body=body.replace(setterEnd,insertion+setterEnd);
body=body.replace('    setAttribute(name, value) { this[name] = value; }','    setAttribute(name, value) { this[name] = value; }\n    getBoundingClientRect(){return {top:0};}\n    focus(){}');
body=body.replace('querySelectorAll:() => []',String.raw`querySelectorAll:selector => {
      const attribute=/^\[data-([a-z-]+)\]$/.exec(selector);if(!attribute)return [];
      const key=attribute[1].replace(/-([a-z])/g,(_,c)=>c.toUpperCase());
      return [...nodes.values()].filter(node=>Object.hasOwn(node.dataset,key));
    }`);
body=body.replace('scrollTo(){}','scrollTo(){}, scrollBy(){}');
const boot=new Function('source','catalog','clone','assert','vm','REVIEW_KEY','FAVORITES_KEY','assets',body+';return boot;')(source,catalog,clone,assert,vm,REVIEW_KEY,FAVORITES_KEY,catalog.assets);
const page=boot(),api=page.api,before=JSON.stringify(api.reviewPayload().items),original=JSON.stringify(api.C);
const html=()=>page.node('#main').innerHTML;
const shown=()=>[...html().matchAll(/data-outfit-collection="([^"]+)"/g)].map(m=>m[1]);
const tag=id=>page.node('#outfit-category-tag-'+id);
const heading=id=>api.control('[data-browse-bucket]','hon:outfits:root:outfit-category:'+id);
let checks=0;
api.setState({project:'hon',view:'outfits',album:'',search:'',outfitLayout:'compact'});api.renderMain();
const groups=api.outfitGroups(api.C.assets.filter(a=>a.project==='hon')),categories=api.outfitCategoryGroups(groups);
assert.equal(groups.length,22);
assert.deepEqual(clone(categories.map(g=>[g.title,g.outfits.length])),[['Formal attire',6],['Casual',8],['Scoundrel gear',8]]);
const assigned=categories.flatMap(g=>g.outfits.map(x=>x.al.id));assert.equal(new Set(assigned).size,22);assert.equal(assigned.length,22);
assert.equal(shown().length,22,'Initial categories expose the whole wardrobe');
for(const id of ['formal','casual','scoundrel'])assert(heading(id),'Each bucket has an independent expand/collapse button');
checks+=4;

tag('casual').click();
assert.deepEqual(shown().sort(),categories.find(g=>g.id==='casual').outfits.map(g=>g.al.id).sort());
assert(/id="outfit-category-tag-casual"[^>]*aria-expanded="true"/.test(html()));
for(const id of ['formal','scoundrel'])assert(new RegExp('id="outfit-category-tag-'+id+'"[^>]*aria-expanded="false"').test(html()));
heading('formal').click();assert.equal(shown().length,14,'Individual headers can open an additional bucket');
heading('formal').click();assert.equal(shown().length,8);
tag('scoundrel').click();assert.equal(shown().length,8);assert(shown().includes('hon:outfit-vest')&&!shown().includes('hon:outfit-yellow'));
checks+=4;

// Existing expanded views, gun variants and detail routes remain intact.
tag('formal').click();
const pinstripe=groups.find(g=>g.al.id==='hon:outfit-pinstripe'),gun=pinstripe.items.find(a=>a.propState==='with_gun');assert(gun);
api.control('[data-outfit-toggle]','hon:outfit-pinstripe').click();
assert(html().includes('data-open="'+gun.id+'"'));
for(const asset of pinstripe.items)assert(html().includes('data-open="'+asset.id+'"'));
tag('casual').click();tag('formal').click();assert(html().includes('data-open="'+gun.id+'"'),'Per-outfit expansion survives category changes');
api.setState({outfitLayout:'all'});api.renderMain();assert(!html().includes('data-outfit-collection='));assert(html().includes('data-open="'+gun.id+'"'));
api.setState({album:'hon:outfit-pinstripe',outfitLayout:'compact'});api.renderMain();assert(!html().includes('data-outfit-category='));assert(html().includes('Gun variants')&&html().includes('Other views &amp; revisions'));
const detailIDs=[...html().matchAll(/data-open="([^"]+)"/g)].map(m=>m[1]);assert(detailIDs.every(id=>pinstripe.al.assetIDs.includes(id)));
checks+=4;

// A search change reveals matching categories even after another was selected.
api.setState({album:'',search:''});api.renderMain();tag('formal').click();
api.setState({search:'Smuggler vest'});api.renderMain();assert.deepEqual(shown(),['hon:outfit-vest']);assert(tag('formal').disabled&&tag('casual').disabled&&!tag('scoundrel').disabled);
api.setState({search:'no-such-outfit-zzzz'});api.renderMain();assert.equal(shown().length,0);assert(html().includes('No outfits match this search.'));for(const id of ['formal','casual','scoundrel'])assert(tag(id).disabled);
api.setState({search:''});api.renderMain();assert.equal(shown().length,22,'Clearing search restores all categories');
checks+=3;

// Review removals and Archive filter counts and references; no source changes.
const vest=groups.find(g=>g.al.id==='hon:outfit-vest'),saved=vest.items.map(a=>[a.id,api.reviews.get(a.id)]);
for(const a of vest.items)api.reviews.set(a.id,{id:a.id,status:'keep',collectionState:'archived'});
api.renderMain();assert(!shown().includes(vest.al.id));assert(/Scoundrel gear \u00b7 7<\/button>/.test(html()));
for(const a of vest.items)api.reviews.set(a.id,{id:a.id,status:'remove'});
api.renderMain();assert(!shown().includes(vest.al.id));assert(/Scoundrel gear \u00b7 7<\/button>/.test(html()));
for(const [id,record] of saved)record?api.reviews.set(id,record):api.reviews.delete(id);
checks+=2;

// The requested taxonomy is Hon's outfit landing only.
api.setState({project:'lisan',view:'outfits',album:'',search:''});api.renderMain();assert(!html().includes('data-outfit-category='));
api.setState({project:'hon',view:'all',album:'',search:''});api.renderMain();assert(!html().includes('data-outfit-category='));assert.equal(shown().length,22);
assert.equal(JSON.stringify(api.C),original);assert.equal(JSON.stringify(api.reviewPayload().items),before);assert.equal(page.writes.length,0);
checks+=3;
console.log(JSON.stringify({passed:true,checks,outfits:22,categories:{formal:6,casual:8,scoundrel:8},browserVisualQA:false,sourceMutations:0}));
