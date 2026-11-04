/* Run before library.js: carry the local session into a genuinely new browser. */
(() => {
  'use strict';
  const catalog = window.REVIEW_CATALOG;
  const seed = catalog?.reviewSessionSeed;
  if (!seed || !Array.isArray(seed.favorites) || !Array.isArray(seed.exportBasket)) return;
  const keys = ['cfa-visual-review-v1', 'cfa-visual-favorites-v1', 'cfa-visual-export-v1', 'cfa-hosted-session-seed-v1'];
  try {
    // Even an empty stored array is the user's existing choice. A new snapshot
    // must never resurrect favorites or basket entries they cleared on a phone.
    if (keys.some(key => localStorage.getItem(key) !== null)) return;
    const assets = new Map(catalog.assets.map(asset => [asset.id, asset]));
    const verified = rows => rows.filter(row => row && typeof row.id === 'string' && row.sha256 && assets.get(row.id)?.sha256 === row.sha256);
    localStorage.setItem(keys[1], JSON.stringify([...new Set(verified(seed.favorites).map(row => row.id))]));
    localStorage.setItem(keys[2], JSON.stringify({format: keys[2], items: verified(seed.exportBasket)}));
    localStorage.setItem(keys[3], JSON.stringify({id: seed.id || null, seededAt: new Date().toISOString()}));
  } catch {
    // The shared dashboard reports unavailable browser storage and retains its
    // normal JSON export path. Do not replace or fabricate review decisions.
  }
})();
