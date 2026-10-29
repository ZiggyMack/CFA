/* Hosted-only presentation. The shared local dashboard owns review records. */
(() => {
  'use strict';
  const base = new URL('.', document.currentScript.src);
  const available = new Set(window.REVIEW_CATALOG?.hostedMirror?.availablePaths || []);
  const replacements = new Map([
    ['Open original file ↗', 'Open hosted review copy ↗'],
    ['Open local original ↗', 'Open hosted review copy ↗'],
    ['Full image verified locally.', 'Hosted review copy · original identity verified.'],
    ['Preview only · full image is not available locally.', 'Preview only · full review image is not in this delivery.'],
    ['Supplied winners index ↗', 'Winners visual index ↗']
  ]);
  let pending = false;
  const adapt = () => {
    pending = false;
    for (const node of document.querySelectorAll('a,p')) {
      if (!node.children.length && replacements.has(node.textContent.trim())) {
        node.textContent = replacements.get(node.textContent.trim());
      }
    }
    // A few shared widgets synthesize repository links from provenance paths.
    // Keep their labels as context, but never pretend those files were deployed.
    for (const link of document.querySelectorAll('a[href]')) {
      let url;
      try { url = new URL(link.getAttribute('href'), base); } catch { continue; }
      if (['blob:', 'data:'].includes(url.protocol) || url.protocol === 'https:' && url.origin !== base.origin) continue;
      const relative = url.origin === base.origin && url.pathname.startsWith(base.pathname) ? decodeURIComponent(url.pathname.slice(base.pathname.length)) : null;
      if (relative !== null && available.has(relative || 'index.html')) continue;
      link.removeAttribute('href');
      link.removeAttribute('download');
      link.setAttribute('aria-disabled', 'true');
      link.title = 'This source file is available in the local library; it is not in this hosted publication.';
      if (!link.children.length) link.textContent = link.textContent.replace(/\s*↗$/, '') + ' · local only';
    }
    const footer = document.querySelector('.sidebar-foot');
    if (footer && !footer.querySelector('.hosted-storage-note')) {
      const note = document.createElement('p');
      note.className = 'hosted-storage-note';
      note.textContent = 'Hosted review copies. Decisions stay in this browser; Export review to bring them back to the local library.';
      footer.append(note);
    }
  };
  new MutationObserver(() => {
    if (!pending) { pending = true; requestAnimationFrame(adapt); }
  }).observe(document.getElementById('app'), {childList:true, subtree:true});
  adapt();
})();
