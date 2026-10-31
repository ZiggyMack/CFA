const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const listeners = new Map(), messages = [];
const parent = {postMessage(value, origin) { messages.push({value, origin}); }};
const location = {hash:'#hon/intake', origin:'https://studio.example'};
const window = {parent, addEventListener(type, fn) {
  listeners.set(type, [...(listeners.get(type) || []), fn]);
}};
const context = {window, location, document:{referrer:'https://studio.example/Full_Visual_Library'}, URL,
  queueMicrotask: fn => fn()};
vm.runInNewContext(fs.readFileSync(path.join(__dirname, '../full_dashboard_bridge.js'), 'utf8'), context);
const emit = (type, event={}) => (listeners.get(type) || []).forEach(fn => fn(event));
const config = {projects:['hon', 'lisan', 'criminal_mind'], views:['all', 'intake', 'project_home', 'casa_baldadoon', 'documents']};
const render = (initialRoute, extra={}, requestID=null) => emit('message', {source:parent, origin:'https://studio.example',
  data:{type:'streamlit:render', args:{initialRoute, requestID, routeConfig:config, height:700}}, ...extra});
const reported = () => messages.filter(m => m.value.type === 'streamlit:setComponentValue');

render('#criminal_mind/project_home', {origin:'https://other.example'});
assert.equal(location.hash, '#hon/intake');
assert.equal(reported().length, 0);
render('#criminal_mind/project_home', {source:{}});
assert.equal(location.hash, '#hon/intake');
render('#criminal_mind/project_home');
assert.equal(location.hash, '#criminal_mind/project_home');
assert.equal(reported().at(-1).value.value.route, '#criminal_mind/project_home');
assert.equal(reported().at(-1).value.value.requestedRoute, '#criminal_mind/project_home');
const count = reported().length;
render('#criminal_mind/project_home');
assert.equal(reported().length, count, 'Repeated renders must not loop');
location.hash = '#criminal_mind/casa_baldadoon';
emit('hashchange');
assert.equal(reported().at(-1).value.value.route, location.hash);
render('#criminal_mind/project_home');
assert.equal(location.hash, '#criminal_mind/casa_baldadoon', 'Old outer arguments must not undo new navigation');
render('#criminal_mind/casa_baldadoon');
assert.equal(reported().at(-1).value.value.requestedRoute, '#criminal_mind/casa_baldadoon');
render('#lisan/documents');
assert.equal(location.hash, '#lisan/documents', 'A fresh valid direct-link request must apply');
render('#missing/documents');
assert.equal(location.hash, '#lisan/documents');
const before = reported().length;
location.hash = '#criminal_mind/documents/a%2Fb';
emit('hashchange');
assert.equal(reported().length, before, 'Malformed routes must not reach parent query parameters');

// A route reflected to Streamlit's URL is only an acknowledgement. Between two
// rerenders the reader can already have moved again; neither may rewind them.
render('#hon/all', {}, 1);
assert.equal(location.hash, '#hon/all');
location.hash = '#criminal_mind/all';
emit('hashchange');
const projectReport = reported().at(-1).value.value;
assert.equal(projectReport.requestedRoute, '#hon/all');
assert.equal(projectReport.requestID, 1);
location.hash = '#criminal_mind/casa_baldadoon';
emit('hashchange');
render('#hon/all', {}, 1); // Server finishes reflecting the project click.
assert.equal(location.hash, '#criminal_mind/casa_baldadoon');
location.hash = '#hon/all';
emit('hashchange');
render('#hon/all', {}, 1); // Server finishes reflecting the Casa click.
assert.equal(location.hash, '#hon/all');
location.hash = '#criminal_mind/casa_baldadoon';
emit('hashchange');
const repeated = reported().length;
render('#hon/all', {}, 1);
assert.equal(location.hash, '#criminal_mind/casa_baldadoon');
assert.equal(reported().length, repeated, 'Acknowledgement rerenders do not create a reporting loop');
// A real outer Back/direct-link request may return to the SAME initial route.
render('#hon/all', {}, 2);
assert.equal(location.hash, '#hon/all', 'A fresh request token must apply even when its route was requested earlier');
assert.equal(reported().at(-1).value.value.requestID, 2);
console.log('Hosted dashboard bridge: deep links, rapid project/Casa navigation, URL acknowledgements, Back requests, origin checks and route validation passed.');
