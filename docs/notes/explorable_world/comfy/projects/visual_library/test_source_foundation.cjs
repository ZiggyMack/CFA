const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const f=require('./source_foundation.js');
const cases=JSON.parse(fs.readFileSync(path.join(__dirname,'test_source_foundation_cases.json'),'utf8'));
for(const c of cases){const a=c.arguments,before=JSON.stringify(a);const out=f.derive(a.model,a.shot,a.project,a.storyID,a.assets,a.reviews,a.sceneReviews);assert.equal(out.state,c.expectedState,c.name);assert.equal(JSON.stringify(a),before,'Read-only '+c.name);}
const a=cases[0].arguments,model={...a.model,checkpoints:f.checkpoint(a.model.bindings,a.assets)};
const loaded=JSON.parse(JSON.stringify(model)),changed=structuredClone(a.assets);changed[0].sha256='b'.repeat(64);
assert(f.derive(loaded,a.shot,a.project,a.storyID,changed).dependencyReviewNeeded);
console.log(cases.length+' source-foundation JS fixtures passed; read-only and changed checkpoint checks passed.');
