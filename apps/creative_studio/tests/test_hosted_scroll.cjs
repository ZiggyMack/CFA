/* Hosted navigation scroll behavior; no reviews or browser storage are touched. */
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const events={},calls=[],attrs={};
const app={scrollTop:300,scrollTo(v){calls.push(v);this.scrollTop=v.top;},setAttribute(k,v){attrs[k]=v;}};
const context={URL,window:{REVIEW_CATALOG:{hostedMirror:{availablePaths:[]}},addEventListener(k,fn){events[k]=fn;}},document:{currentScript:{src:'https://example.test/hosted.js'},getElementById(id){assert.equal(id,'app');return app;},querySelectorAll(){return [];},querySelector(){return null;}},MutationObserver:class{observe(){}},requestAnimationFrame(){throw Error('Unexpected scheduled scroll');}};
vm.runInNewContext(fs.readFileSync(path.join(__dirname,'../hosted_dashboard.js'),'utf8'),context);
assert.equal(app.scrollTop,300,'Loading hosted presentation preserves scroll');
assert.equal(attrs['aria-label'],'Visual library scroll area');
assert.equal(app.tabIndex,0,'Scroll region is keyboard reachable');
assert(!events.resize&&!events.message,'Host renders and resize cannot reset reading position');
events.hashchange();assert.equal(app.scrollTop,0,'Route navigation returns to the top');assert.equal(calls.length,1);
console.log('Hosted scroll navigation and keyboard reachability checks passed.');
