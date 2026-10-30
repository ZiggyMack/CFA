const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const {webcrypto} = require('node:crypto');
const source = fs.readFileSync(path.join(__dirname, '../collaborator_review_storage/index.html'), 'utf8').match(/<script>([\s\S]*?)<\/script>/)[1];
const key = 'cfa-collaborator-reviews-v1';
const delay = () => new Promise(resolve => setTimeout(resolve, 15));
const until = async check => { for (let i = 0; i < 100 && !check(); i++) await delay(); assert.ok(check(), 'storage event arrived'); };

function browser(storage, failWrite=false) {
  const events = {}, output = [], writes = [];
  const parent = {postMessage: message => output.push(message)};
  const window = {parent, addEventListener: (kind, fn) => events[kind] = fn};
  const localStorage = {
    getItem: name => storage.has(name) ? storage.get(name) : null,
    setItem: (name, value) => {
      if (failWrite) throw new Error('Quota exceeded');
      storage.set(name, value); writes.push(value);
    }
  };
  vm.runInNewContext(source, {window, localStorage, crypto: webcrypto, TextEncoder, Uint8Array});
  return {writes, event: () => output.filter(row => row.type === 'streamlit:setComponentValue').at(-1)?.value,
    render: async args => {events.message({source: parent, data: {type: 'streamlit:render', args}}); await delay();},
    external: async raw => {storage.set(key, raw); events.storage({key, newValue: raw}); await delay();}};
}

(async () => {
  const storage = new Map();
  const first = browser(storage);
  const record = {task: {state: 'draft', answers: {q: 'synthetic'}}};
  await first.render({enabled: true, records: record});
  assert.equal(first.event().kind, 'loaded');
  assert.equal(first.event().raw, null);
  assert.equal(first.writes.length, 0, 'no write before Python validation/acknowledgement');
  await first.render({enabled: true, records: record, ack: first.event().token});
  await until(() => first.event()?.kind === 'saved');
  assert.equal(first.event().kind, 'saved');
  assert.deepEqual(JSON.parse(storage.get(key)), record);
  const refreshed = browser(storage);
  await refreshed.render({enabled: true, records: {}});
  await until(() => refreshed.event()?.kind === 'loaded');
  assert.equal(refreshed.event().kind, 'loaded');
  assert.deepEqual(JSON.parse(refreshed.event().raw), record, 'fresh session restores draft instead of replacing it with empty source data');
  assert.equal(refreshed.writes.length, 0);
  const oldAck = refreshed.event().token;
  const later = {task: {state: 'ready', answers: {q: 'newer'}}};
  await refreshed.external(JSON.stringify(later));
  await refreshed.render({enabled: true, records: record, ack: oldAck});
  assert.equal(refreshed.event().kind, 'loaded');
  assert.deepEqual(JSON.parse(storage.get(key)), later, 'unseen second-tab data is not overwritten');
  assert.equal(refreshed.writes.length, 0);
  storage.set(key, '{broken backup');
  const broken = browser(storage);
  await broken.render({enabled: true, records: {}});
  await until(() => broken.event()?.kind === 'loaded');
  assert.equal(broken.event().raw, '{broken backup');
  await broken.render({enabled: false, records: {}, ack: broken.event().token});
  assert.equal(storage.get(key), '{broken backup', 'malformed backup remains untouched');
  const quotaStore = new Map();
  const quota = browser(quotaStore, true);
  await quota.render({enabled: true, records: record});
  await quota.render({enabled: true, records: record, ack: quota.event().token});
  await until(() => quota.event()?.kind === 'error');
  assert.equal(quota.event().kind, 'error');
  assert.match(quota.event().message, /Quota/);
  assert.equal(quotaStore.size, 0);
  console.log('PASS collaborator browser backup: handshake, refresh, cross-tab, malformed preservation and quota status');
})().catch(error => {console.error(error); process.exitCode = 1;});
