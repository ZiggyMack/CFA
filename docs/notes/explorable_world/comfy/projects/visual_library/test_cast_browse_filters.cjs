/* Character browse filters use recorded provenance and story links only.
   Real renderer and bound handlers run in an isolated DOM/storage harness. */
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const clone=value=>JSON.parse(JSON.stringify(value));
const source=fs.readFileSync(path.join(__dirname,'library.js'),'utf8');
const raw=fs.readFileSync(path.join(__dirname,'catalog.js'),'utf8');
const catalog=JSON.parse(raw.slice(raw.indexOf('=')+1).trim().replace(/;$/,''));
const REVIEW_KEY='cfa-visual-review-v1',FAVORITES_KEY='cfa-visual-favorites-v1',EXPORT_KEY='cfa-visual-export-v1';
const byID=new Map(catalog.assets.map(a=>[a.id,a]));
let harness=fs.readFileSync(path.join(__dirname,'test_collections_navigation.cjs'),'utf8');
harness=harness.slice(harness.indexOf('function boot() {'),harness.indexOf('\nconst page = boot(), api = page.api;'));
harness=harness.replace('function boot() {','function boot(chosenCatalog=catalog) {')
 .replace('REVIEW_CATALOG:clone(catalog)','REVIEW_CATALOG:clone(chosenCatalog)')
 .replace('querySelectorAll() {return [];}','querySelectorAll(selector) {return selectAll(selector).filter(e=>this.children.has(e));}')
 .replace('child.disabled =',"for(const bare of match[2].matchAll(/(?:^|\\s)(data-[\\w-]+)(?=\\s|$)/g))child.setAttribute(bare[1],'');child.disabled =")
 .replace('window.__collectionsTest={','window.__collectionsTest={castBrowseFacts,castBrowseContext,')
 .replace('html:() => nodes.get','nodes,selectAll,html:() => nodes.get');
const boot=eval('('+harness.replace(/^function boot/,'function')+')');
const checks=[],bosses=['hon:boss-round01','hon:cast-bartender','hon:cast-bouncer'];
const sameIDs=(actual,expected,message)=>assert.deepEqual([...actual].sort(),[...expected].sort(),message);
const renderedIDs=p=>[...p.html().matchAll(/<article\b[^>]*data-collection="([^"]+)"/g)].map(m=>m[1]);
function show(p,patch={}){p.api.setState({project:'hon',view:'cast',album:'',search:'',castFilter:'all',castSource:'all',...patch});p.api.renderMain();}
function click(p,attribute,value){const n=p.selectAll('['+attribute+']').find(n=>value===undefined||n.attributes[attribute]===value);assert(n,'Action exists: '+attribute+'='+value);n.click();}
function change(p,id,value){const n=p.nodes.get('#'+id);assert(n,'Control exists: '+id);n.value=value;n.onchange?.({target:n});for(const f of n.listeners.get('change')||[])f({target:n});}
function facts(p,id){const g=p.api.castHubGroups(id).find(g=>g.id===id);assert(g,'Character is available: '+id);return p.api.castBrowseFacts(g);}
function check(name,fn){fn();checks.push(name);}

check('default cast remains the complete character grid with separate creature ideas',()=>{
 const p=boot();assert.equal(p.api.getState().castFilter,'all');assert.equal(p.api.getState().castSource,'all');show(p);
 const groups=p.api.castHubGroups();assert.equal(groups.length,11);sameIDs(renderedIDs(p),groups.map(g=>g.id),'Every current character has one card');
 assert(p.html().includes('creature-boss-ideas'),'Creature concept collection remains separately accessible by default');
 for(const [id,count] of [['all',11],['roles',3],['planned',2],['linked',1]]){
  const n=p.selectAll('[data-cast-filter]').find(n=>n.dataset.castFilter===id);assert(n,'Filter exists: '+id);
  assert(new RegExp('data-cast-filter="'+id+'"[^>]*>[^<]* · '+count+'<').test(p.html()),'Filter count represents characters: '+id);
 }
 assert(p.nodes.has('#cast-source'));assert(p.html().includes('hon:cast-unnamed-informant'),'Fallback character albums are not lost');
});

check('origin run groups the three original boss choices without broad intake false matches',()=>{
 const p=boot();show(p);change(p,'cast-source','hon:boss-round01');assert.equal(p.api.getState().castSource,'hon:boss-round01');
 sameIDs(renderedIDs(p),bosses,'Discovery run groups crocodile, bartender and rhino');
 assert(!renderedIDs(p).includes('hon:caleb-return'),'Caleb shares the broad intake but came from another run');
 assert(!p.html().includes('class="collapsible-section creature-boss-ideas"'),'Unrelated creature studies do not fill a filtered result');
 click(p,'data-cast-filter','planned');sameIDs(renderedIDs(p),['hon:cast-bartender','hon:cast-bouncer'],'Source and story filters intersect');
 click(p,'data-cast-filter','linked');assert.equal(renderedIDs(p).length,0);assert(p.html().includes('No characters match these filters.'));
 click(p,'data-cast-reset');assert.equal(p.api.getState().castFilter,'all');assert.equal(p.api.getState().castSource,'all');assert.equal(renderedIDs(p).length,11);
});

check('recorded identity choices do not promote historical shortlists into current selections',()=>{
 const p=boot();show(p);click(p,'data-cast-filter','roles');sameIDs(renderedIDs(p),bosses,'Two assigned roles and one selected visible reference are recorded');
 const croc=facts(p,'hon:boss-round01');assert.equal(croc.choices.length,1);assert.equal(croc.choices[0].id,'HD-RETURN-8421e7cfa1a0');
 assert.equal(facts(p,'hon:cast-bartender').choices[0].roleDecision,'user_assigned');assert.equal(facts(p,'hon:cast-bouncer').choices[0].roleDecision,'user_assigned');
 const c=clone(catalog),selected=c.assets.find(a=>a.id==='HD-RETURN-8421e7cfa1a0');delete selected.selectionStatus;
 const q=boot(c);show(q,{castFilter:'roles'});sameIDs(renderedIDs(q),['hon:cast-bartender','hon:cast-bouncer'],'Removing the current choice does not substitute historical shortlisted bosses');
 assert.equal(facts(q,'hon:boss-round01').roles,false);assert(c.assets.filter(a=>a.selectionStatus==='user_shortlisted_not_approved').length>=3,'Historical shortlist evidence is retained in fixture');
 assert.equal(facts(p,'hon:cast-unnamed-informant').roles,false,'Unstructured source prose is not promoted into a machine-recorded choice');
});

check('planned scene intentions remain distinct from exact linked storyboard panels',()=>{
 const p=boot();show(p);click(p,'data-cast-filter','planned');sameIDs(renderedIDs(p),['hon:cast-bartender','hon:cast-bouncer'],'Only two characters have recorded unplaced plans');
 const bar=facts(p,'hon:cast-bartender'),rhino=facts(p,'hon:cast-bouncer'),croc=facts(p,'hon:boss-round01');
 assert.equal(bar.planned.length,1);assert.equal(rhino.planned.length,2);assert.equal(bar.linked.length+rhino.linked.length,0);
 for(const s of [...bar.planned,...rhino.planned]){assert.equal(s.panelAssetIDs.length,0);assert.equal(s.acceptance,'not_accepted');assert.equal(s.stage,'preliminary');}
 assert.equal(croc.planned.length+croc.linked.length+croc.sequences.length,0,'Thirty-three scene studies do not establish storyboard use');
 click(p,'data-cast-filter','linked');sameIDs(renderedIDs(p),['hon:cast-dj'],'Chewy has recorded storyboard connections');
 const chewy=facts(p,'hon:cast-dj');assert.equal(chewy.linked.length,6);assert(chewy.linked.every(s=>s.panelAssetIDs.length>0));
 const currentPanels=new Set(chewy.linked.flatMap(s=>(s.panelAssetIDs||[]).filter(id=>p.api.castHubGroups('hon:cast-dj')[0].items.some(a=>a.id===id))));
 assert.equal(currentPanels.size,5,'Five unique character panel images link six shot work items');
});

check('exact character route keeps its content and source evidence in place',()=>{
 const p=boot();show(p,{album:'hon:boss-round01',castFilter:'planned',castSource:'hon:cast-ivory'});
 sameIDs(p.api.castHubGroups('hon:boss-round01').map(g=>g.id),['hon:boss-round01'],'Exact character ID takes precedence over shared source album membership');
 assert(p.html().includes('data-character-hub="hon:boss-round01"'),'A direct character route ignores browse filters');assert(!p.html().includes('id="cast-source"'),'Focused hub does not masquerade as a filtered grid');
 assert(!p.html().includes('character-hub-origin'),'The removed Origin drawer does not duplicate the reference gallery');
 assert(p.html().includes('character-hub-references'),'Character reference images remain directly available inside the hub');
 assert(p.C.castCollections.some(group=>group.id==='hon:boss-round01'),'Removing the Origin drawer preserves the source collection identity');
 assert(!p.html().includes('data-character-hub="hon:cast-bartender"'),'Related roles do not replace the current character hub');
});

check('story material membership must be exact and source labels remain escaped',()=>{
 const c=clone(catalog),crocID='HD-RETURN-8421e7cfa1a0';
 const base=clone(c.shotMaterials.shots.find(s=>s.characterCollectionID==='hon:cast-bartender'));
 base.id='TEST-WRONG-HASH-STORY';delete base.characterCollectionID;base.materials=[{assetID:crocID,sha256:'0'.repeat(64)}];base.panelAssetIDs=[];
 c.shotMaterials.shots.push(base);c.albums.find(a=>a.id==='hon:boss-round01').title='Discovery <script> & "source"';
 const p=boot(c);show(p);assert.equal(facts(p,'hon:boss-round01').planned.length,0,'Mismatched material hash does not create a scene plan for the character');
 assert(!p.html().includes('Discovery <script>'),'Source title is not HTML');assert(p.html().includes('Discovery &lt;script&gt; &amp; &quot;source&quot;'));
});

check('browse and provenance controls preserve reviews source metadata and stored decisions',()=>{
 const p=boot(),initialSource=JSON.stringify(p.C),initialReviews=JSON.stringify(p.api.reviewPayload().items),initialStorage=Object.fromEntries(p.storage);show(p);
 for(const filter of ['roles','planned','linked','all'])click(p,'data-cast-filter',filter);
 change(p,'cast-source','hon:boss-round01');p.toggle('hon:cast-bartender');p.toggle('hon:cast-bartender');click(p,'data-cast-reset');
 assert.equal(JSON.stringify(p.C),initialSource,'Filtering never rewrites source or acceptance metadata');assert.equal(JSON.stringify(p.api.reviewPayload().items),initialReviews,'Filtering never changes image decisions');
 assert.deepEqual(Object.fromEntries(p.storage),initialStorage,'Browse choices do not rewrite persisted review data');assert.equal(p.writes.length,0,'No localStorage writes occur while browsing');
});

for(const name of checks)console.log('PASS '+name);
console.log('Supporting cast browse checks passed: '+checks.length);
