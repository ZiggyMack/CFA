/* Note presets are browser helpers, never shared references in saved reviews.
   Exercise the real library and bound controls using isolated DOM/storage only. */
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const clone=value=>JSON.parse(JSON.stringify(value));
const source=fs.readFileSync(path.join(__dirname,'library.js'),'utf8');
const raw=fs.readFileSync(path.join(__dirname,'catalog.js'),'utf8');
const catalog=JSON.parse(raw.slice(raw.indexOf('=')+1).trim().replace(/;$/,''));
const REVIEW_KEY='cfa-visual-review-v1',FAVORITES_KEY='cfa-visual-favorites-v1',EXPORT_KEY='cfa-visual-export-v1',PRESETS_KEY='cfa-review-note-presets-v1';
const byID=new Map(catalog.assets.map(a=>[a.id,a]));
let harness=fs.readFileSync(path.join(__dirname,'test_collections_navigation.cjs'),'utf8');
harness=harness.slice(harness.indexOf('function boot() {'),harness.indexOf('\nconst page = boot(), api = page.api;'));
harness=harness.replace('function boot() {','function boot(seed={}) {')
 .replace('new Map(Object.entries(saved))','new Map(Object.entries({...saved,...seed}))')
 .replace('querySelectorAll() {return [];}','querySelectorAll(selector) {return selectAll(selector).filter(e=>this.children.has(e));}')
 .replace('window.__collectionsTest={','window.__collectionsTest={dialog,openViewer,updateReview,importReview,exportReview,notePresetsControls,bindNotePresets,saveNotePreset,deleteNotePreset,clearNotePresets,undoClearNotePresets,applyNotePreset,getNotePresets(){return notePresets;},')
 .replace('html:() => nodes.get','nodes,selectAll,context,html:() => nodes.get');
const rawBoot=eval('('+harness.replace(/^function boot/,'function')+')');
function boot(seed={}){
 const p=rawBoot(seed),downloads=[];
 p.context.Blob=Blob;
 p.context.URL=class extends URL {static createObjectURL(blob){downloads.push(blob);return 'blob:synthetic-preset-export';}static revokeObjectURL(){}};
 p.downloads=downloads;return p;
}
const imageID='HD-DROP-0d83180f0903',videoID=catalog.assets.find(a=>a.kind==='video'&&a.project==='hon'&&a.sha256)?.id;
assert(byID.has(imageID)&&videoID,'Real image and video fixtures exist');
const presets=p=>clone(p.api.getNotePresets());
const node=(p,id)=>{const value=p.nodes.get('#'+id);assert(value,'Control exists: '+id);return value;};
function change(p,id,value){const control=node(p,id);control.value=value;control.onchange?.({target:control});for(const listener of control.listeners.get('change')||[])listener({target:control});return control;}
function open(p,id){
 p.api.openViewer(id);
 // The small shared DOM double does not parse textarea defaultValue as a browser does.
 node(p,'review-note').value=p.api.reviewRecord(id).note||'';
}
function unchangedFields(record){const copy=clone(record);for(const field of ['note','updatedAt','origin','reviewer','reviewerControllerID','projectControllerID','decisionAuthorityControllerID','decisionScope','humanReview'])delete copy[field];copy.sha256=copy.sha256||byID.get(record.id).sha256;copy.shotPlan=copy.shotPlan||null;return copy;}
function saveNew(p,label,text){const before=new Set(presets(p).map(r=>r.id));assert.equal(p.api.saveNotePreset('',label,text),true);const row=presets(p).find(r=>!before.has(r.id));assert(row,'A unique preset ID was created');return row;}
const checks=[];function check(name,fn){fn();checks.push(name);}

check('opening image and video preset controls never writes review or preset storage',()=>{
 const p=boot(),before=Object.fromEntries(p.storage),reviews=clone(p.api.reviewPayload().items);
 for(const id of [imageID,videoID]){open(p,id);for(const control of ['note-preset-select','note-preset-editor-select','note-preset-label','note-preset-text','note-preset-save','note-preset-from-note'])node(p,control);}
 assert.deepEqual(Object.fromEntries(p.storage),before);assert.equal(p.writes.length,0);
 assert.deepEqual(clone(p.api.reviewPayload().items),reviews);assert.equal(presets(p).length,0);
 assert(!Object.hasOwn(p.api.reviewPayload(),'notePresets'),'Preset library is separate from exported review decisions');
});

check('real editor can copy a note save a new preset and reload it without altering the image',()=>{
 const p=boot();open(p,imageID);const original=clone(p.api.reviewRecord(imageID)),before=Object.fromEntries(p.storage);
 node(p,'review-note').value='Current visible note\nwith another line';node(p,'note-preset-from-note').click();
 assert.equal(node(p,'note-preset-text').value,'Current visible note\nwith another line');
 assert.equal(node(p,'note-preset-editor-select').value,'');assert.equal(presets(p).length,0);
 assert.deepEqual(Object.fromEntries(p.storage),before,'Copy only fills the editor');
 node(p,'note-preset-label').value='Face detail';node(p,'note-preset-save').click();
 assert.equal(presets(p).length,1);const row=presets(p)[0];assert.equal(row.label,'Face detail');assert.equal(row.text,'Current visible note\nwith another line');
 assert.deepEqual(clone(p.api.reviewRecord(imageID)),original,'Saving a preset does not save the visible draft onto the image');
 const saved=JSON.parse(p.storage.get(PRESETS_KEY));assert.equal(saved.format,PRESETS_KEY);assert.deepEqual(saved.items,[row]);
 const restart=boot(Object.fromEntries(p.storage));assert.deepEqual(presets(restart),[row]);assert.equal(restart.writes.length,0,'Loading existing presets is read-only');
});

check('select handler appends literal text to the visible note for images and videos',()=>{
 const p=boot(),row=saveNew(p,'Piercings','Keep the nose ring.\nCheck both ears.');
 for(const id of [imageID,videoID]){
  open(p,id);const before=unchangedFields(p.api.reviewRecord(id));
  const draft='Existing note for '+byID.get(id).kind+'\nVisible unsaved addition';node(p,'review-note').value=draft;
  change(p,'note-preset-select',row.id);const expected=draft+'\n'+row.text;
  assert.equal(node(p,'review-note').value,expected);assert.equal(p.api.reviewRecord(id).note,expected);
  assert.equal(node(p,'note-preset-select').value,'','Applying resets the chooser');
  assert.deepEqual(unchangedFields(p.api.reviewRecord(id)),before,'Preset application changes no decision, rating, plan or role');
  const receipt=clone(p.api.reviewRecord(id).humanReview);
  assert.deepEqual(receipt.fields,['note'],'Human attribution covers only the note changed by the preset');
  assert.equal(receipt.reviewerControllerID,'ziggy');assert.equal(receipt.assetID,id);assert.equal(receipt.sha256,byID.get(id).sha256);
  assert.equal(receipt.decisionScope,'project_decision');assert.equal(receipt.project,'hon');assert(Number.isFinite(Date.parse(receipt.updatedAt)));
  assert.equal(p.api.reviewPayload().items.find(a=>a.id===id).note,expected,'Export uses actual text, not a preset ID');
 }
 assert(p.writes.filter(([key])=>key===REVIEW_KEY).length>=2,'Both media notes use the normal review persistence');
});

check('editing deleting clearing and undoing presets never rewrites prior reviews',()=>{
 const p=boot(),row=saveNew(p,'Original label','Original reusable text');open(p,imageID);node(p,'review-note').value='Existing note';change(p,'note-preset-select',row.id);
 const reviews=clone(p.api.reviewPayload().items),reviewStorage=p.storage.get(REVIEW_KEY);
 change(p,'note-preset-editor-select',row.id);assert.equal(node(p,'note-preset-label').value,row.label);assert.equal(node(p,'note-preset-text').value,row.text);
 node(p,'note-preset-label').value='Edited label';node(p,'note-preset-text').value='Replacement reusable text';node(p,'note-preset-save').click();
 assert.equal(presets(p)[0].id,row.id);assert.equal(presets(p)[0].text,'Replacement reusable text');
 change(p,'note-preset-editor-select',row.id);node(p,'note-preset-delete').click();assert.equal(presets(p).length,0);
 saveNew(p,'One','One');saveNew(p,'Two','Two');open(p,imageID);const beforeClear=presets(p);
 node(p,'note-presets-clear').click();assert.equal(presets(p).length,0);
 node(p,'note-presets-undo').click();assert.deepEqual(presets(p),beforeClear);
 assert.deepEqual(clone(p.api.reviewPayload().items),reviews);assert.equal(p.storage.get(REVIEW_KEY),reviewStorage,'Preset management never rewrites the saved review envelope');
});

check('blank and oversized saves reject atomically and optional labels derive from text',()=>{
 const p=boot(),row=saveNew(p,'','A useful fallback label\nMore detail');assert(row.label&&row.label.length<=80);assert(row.label.startsWith('A useful fallback label'));
 for(const [label,text] of [['Empty',''],['Whitespace',' \n\t '],['L'.repeat(81),'text'],['Too long','x'.repeat(20001)]]){
  const before=presets(p),stored=p.storage.get(PRESETS_KEY);assert.equal(p.api.saveNotePreset('',label,text),false);
  assert.deepEqual(presets(p),before);assert.equal(p.storage.get(PRESETS_KEY),stored,'Rejected new save is not partially persisted');
  assert.equal(p.api.saveNotePreset(row.id,label,text),false);assert.deepEqual(presets(p),before,'Rejected edit keeps the prior preset');
 }
 assert.equal(p.api.saveNotePreset(row.id,'L'.repeat(80),'x'.repeat(20000)),true,'Exact field limits are accepted');
 assert.equal(presets(p)[0].text.length,20000);
});

check('collision checked IDs stay unique and fifty presets permits edits but rejects a new entry',()=>{
 const freeze=p=>{p.context.Date=class extends Date {constructor(...args){super(...(args.length?args:['2026-10-28T12:00:00Z']));}static now(){return 1793188800000;}};};let p=boot();freeze(p);
 const first=saveNew(p,'Preset 0','Text 0');p=boot(Object.fromEntries(p.storage));freeze(p);
 for(let i=1;i<50;i++)saveNew(p,'Preset '+i,'Text '+i);
 const rows=presets(p);assert.equal(new Set(rows.map(r=>r.id)).size,50,'Same-timestamp additions retain unique IDs');
 assert.deepEqual(rows[0],first,'A same-timestamp restart does not overwrite the stored ID');
 const stored=p.storage.get(PRESETS_KEY);assert.equal(p.api.saveNotePreset('','Overflow','Overflow'),false);assert.equal(p.storage.get(PRESETS_KEY),stored);
 assert.equal(p.api.saveNotePreset(rows[0].id,'Updated at capacity','Updated'),true);assert.equal(presets(p).length,50);assert.equal(presets(p)[0].text,'Updated');
});

check('append length limit rejects rather than truncates and preserves existing visible draft',()=>{
 const p=boot(),row=saveNew(p,'One character','x');open(p,imageID);
 node(p,'review-note').value='a'.repeat(19998);change(p,'note-preset-select',row.id);
 assert.equal(p.api.reviewRecord(imageID).note,'a'.repeat(19998)+'\nx');assert.equal(node(p,'review-note').value.length,20000);
 const before=clone(p.api.reviewRecord(imageID)),stored=p.storage.get(REVIEW_KEY),visible=node(p,'review-note').value;
 change(p,'note-preset-select',row.id);assert.equal(node(p,'review-note').value,visible);assert.deepEqual(clone(p.api.reviewRecord(imageID)),before);assert.equal(p.storage.get(REVIEW_KEY),stored);
 node(p,'review-note').value='';change(p,'note-preset-select',row.id);assert.equal(p.api.reviewRecord(imageID).note,'x','Empty notes receive no leading newline');
 node(p,'review-note').value='Existing\n';change(p,'note-preset-select',row.id);assert.equal(p.api.reviewRecord(imageID).note,'Existing\nx','An existing newline is not doubled');
});

check('markup in labels and text is escaped for display while stored and applied text stays literal',()=>{
 const p=boot(),label='<b>Ring & "ear"</b>',text='<img id="preset-injected" src=x onerror="bad()">\n</textarea><script>bad()</script>&';
 const row=saveNew(p,label,text);open(p,imageID);
 const html=p.api.dialog.innerHTML;assert(!html.includes(label));assert(html.includes('&lt;b&gt;Ring &amp; &quot;ear&quot;&lt;/b&gt;'));
 change(p,'note-preset-editor-select',row.id);assert.equal(node(p,'note-preset-label').value,label);assert.equal(node(p,'note-preset-text').value,text);
 node(p,'review-note').value='';change(p,'note-preset-select',row.id);assert.equal(p.api.reviewRecord(imageID).note,text);
 open(p,imageID);assert(!p.api.dialog.innerHTML.includes('<script>bad()'));assert(!p.nodes.has('#preset-injected'));assert(p.api.dialog.innerHTML.includes('&lt;img id=&quot;preset-injected&quot;'));
 assert.equal(p.api.reviewPayload().items.find(a=>a.id===imageID).note,text);
});

check('unreadable preset storage stays untouched until an explicit clear resets it',()=>{
 const malformed='{not valid json',p=boot({[PRESETS_KEY]:malformed});open(p,imageID);
 assert.equal(p.storage.get(PRESETS_KEY),malformed);assert.equal(p.writes.length,0);
 assert.equal(p.api.saveNotePreset('','New','New'),false);assert.equal(p.storage.get(PRESETS_KEY),malformed,'A save cannot silently overwrite an unread library');
 node(p,'note-presets-clear').click();assert.equal(presets(p).length,0);assert.equal(p.api.saveNotePreset('','After reset','New text'),true);
});

(async()=>{
 const p=boot(),row=saveNew(p,'Export fixture','Literal saved review text\nSecond line');open(p,imageID);node(p,'review-note').value='Existing';change(p,'note-preset-select',row.id);
 const expected='Existing\n'+row.text;p.api.exportReview();assert.equal(p.downloads.length,1,'Real export handler created one download');
 const exported=JSON.parse(await p.downloads[0].text());assert.equal(exported.items.find(a=>a.id===imageID).note,expected);assert(!Object.hasOwn(exported,'notePresets'));
 const imported=boot();imported.api.importReview(exported);assert.equal(imported.api.reviewRecord(imageID).note,expected);assert.equal(presets(imported).length,0,'Review imports do not create a linked preset library');
 const restarted=boot(Object.fromEntries(p.storage));assert.equal(restarted.api.reviewRecord(imageID).note,expected);assert.deepEqual(presets(restarted),[row]);
 checks.push('real review download import and restart retain literal notes independently of preset storage');
 console.log(JSON.stringify({passed:true,checks:checks.length,names:checks,productionFilesWritten:false}));
})().catch(error=>{console.error(error);process.exitCode=1;});
