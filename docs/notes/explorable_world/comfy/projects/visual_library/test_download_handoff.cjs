/* Exercise the real download functions without generating user review files. */
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const source=fs.readFileSync(path.join(__dirname,'library.js'),'utf8');
const start=source.indexOf('  let activeDownload=null;'),end=source.indexOf('  function importReview(data)',start);
assert(start>=0&&end>start);
const payload={format:'cfa-visual-review-v1',items:[{id:'fixture-image',note:'Keep the neighborhood dense.'}],locationReviews:[{project:'criminal_mind',note:'Direction only',attributionStatus:'draft'}]};
const children=new Set(),blobs=new Map(),revoked=[],clicked=[],notices=[];
const document={body:{append(link){children.add(link);}},createElement(tag){assert.equal(tag,'a');return {setAttribute(){},remove(){children.delete(this);},click(){assert(children.has(this),'Download anchor is attached at activation');clicked.push({link:this,url:this.href,filename:this.download});}};}};
const URL={createObjectURL(blob){const url='blob:fixture-'+blobs.size;blobs.set(url,blob);return url;},revokeObjectURL(url){revoked.push(url);blobs.delete(url);}};
const context={document,URL,Blob,reviewPayload:()=>structuredClone(payload),notice:text=>notices.push(text)};
vm.runInNewContext(source.slice(start,end)+'\nglobalThis.test={exportReview,exportLocationReview};',context);
(async()=>{
 context.test.exportReview();
 assert.equal(clicked[0].filename,'cfa-review.json');
 assert.deepEqual(JSON.parse(await blobs.get(clicked[0].url).text()),payload,'The review payload is unchanged');
 assert.equal(children.size,1,'One visible direct retry link remains');
 assert.equal(revoked.length,0,'Blob stays valid for a delayed manual download');
 clicked[0].link.click();assert.equal(clicked[1].url,clicked[0].url,'Manual retry downloads the same snapshot');
 assert.match(notices[0],/Download requested/);assert(!notices[0].includes('Review exported'));
 context.test.exportLocationReview('criminal_mind');
 assert.equal(children.size,1,'A new export replaces the previous retry link');
 assert.deepEqual(revoked,[clicked[0].url],'Previous Blob is released when replaced');
 const latest=clicked.at(-1),download=JSON.parse(await blobs.get(latest.url).text());
 assert.equal(latest.filename,'cfa-criminal_mind-location-review.json');
 assert.deepEqual(download.items,payload.items);assert.deepEqual(download.locationReviews,payload.locationReviews);
 assert.match(download.handoff.status,/prepared for download/);assert.match(notices.at(-1),/Check your browser downloads/);
 console.log('Download handoff: attached anchor, persistent direct retry, unchanged JSON, cleanup and truthful status passed. Browser disk delivery still needs browser verification.');
})().catch(error=>{console.error(error);process.exitCode=1;});
