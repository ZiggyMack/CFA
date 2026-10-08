(() => {
  'use strict';
  const base = new URL('.', document.currentScript.src);
  const C = window.REVIEW_CATALOG;
  const byID = new Map(C.assets.map(a => [a.id, a]));
  const cats = Object.fromEntries(C.categories);
  const esc = v => String(v ?? '').replace(/[&<>"']/g, x => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[x]));
  const href = p => new URL(p, base).href;
  const isDoc = a => ['document','pdf'].includes(a.kind);
  const initial = window.REVIEW_INITIAL || {project:'hon', view:'all'};
  let state = {...initial, album:'', search:''}, currentID = '', displayed = [], toastTimer;
  let favorites = new Set(), storageOK = true;
  try { const saved=JSON.parse(localStorage.getItem('cfa-visual-favorites-v1') || '[]'); if(Array.isArray(saved))favorites=new Set(saved.filter(id=>byID.has(id))); } catch {storageOK=false;}
  const iconStar = id => favorites.has(id) ? '★' : '☆';
  function notice(message) {let t=document.querySelector('.toast');if(!t){t=document.createElement('div');t.className='toast';t.setAttribute('role','status');document.body.append(t);}t.textContent=message;clearTimeout(toastTimer);toastTimer=setTimeout(()=>t.remove(),3500);}
  function saveFavorites(){try{localStorage.setItem('cfa-visual-favorites-v1',JSON.stringify([...favorites]));}catch{storageOK=false;notice('Browser storage unavailable. Export favorites to keep your selections.');}}
  function toggleFavorite(id){favorites.has(id)?favorites.delete(id):favorites.add(id);saveFavorites();document.querySelectorAll('[data-favorite]').forEach(b=>{const on=favorites.has(b.dataset.favorite);b.classList.toggle('on',on);b.textContent=iconStar(b.dataset.favorite);b.setAttribute('aria-pressed',String(on));b.setAttribute('aria-label',(on?'Remove favorite: ':'Favorite: ')+byID.get(b.dataset.favorite).title);});const count=document.querySelector('[data-view="favorites"] .count');if(count)count.textContent=projectAssets().filter(a=>favorites.has(a.id)).length;if(state.view==='favorites'&&!currentID)renderMain();}
  function queryMatch(a){const text=[a.title,a.filename,a.note,a.beat,a.lyric,...(a.tags||[])].join(' ').toLowerCase();return text.includes(state.search.toLowerCase().trim());}
  function projectAssets(){return C.assets.filter(a=>a.project===state.project);}
  function route(project,view='all',album=''){state={...state,project,view,album,search:''};location.hash=[project,view,album].filter(Boolean).map(encodeURIComponent).join('/');render();window.scrollTo({top:0,behavior:'instant'});}
  function parseHash(){const [p,v,a]=location.hash.slice(1).split('/').map(decodeURIComponent);if(C.projects.some(x=>x.id===p)){state.project=p;state.view=['all','favorites','documents',...Object.keys(cats)].includes(v)?v:'all';state.album=a||'';}}
  function render(){
    const p=C.projects.find(p=>p.id===state.project);const all=projectAssets();
    document.title=p.name+' · Visual library';
    document.querySelector('#app').innerHTML=`<div class="shell"><aside class="sidebar"><p class="brand">CFA / VISUAL LIBRARY</p><div class="project-picker">${C.projects.map(x=>`<button data-project="${x.id}" class="${state.project===x.id?'active':''}">${esc(x.name)}<small>${esc(x.subtitle)}</small></button>`).join('')}</div><nav class="nav" aria-label="Media categories"><button data-view="all" class="${state.view==='all'?'active':''}">All files <span class="count">${all.filter(a=>!isDoc(a)).length} visuals</span></button>${C.categories.map(([id,name])=>{const albums=C.albums.filter(x=>x.project===state.project&&x.category===id);const count=new Set(albums.flatMap(x=>x.assetIDs)).size;return count?`<button data-view="${id}" class="${state.view===id?'active':''}">${esc(name)}<span class="count">${count}</span></button>`:'';}).join('')}<button data-view="favorites" class="${state.view==='favorites'?'active':''}">☆ Favorites <span class="count">${all.filter(a=>favorites.has(a.id)).length}</span></button><button data-view="documents" class="${state.view==='documents'?'active':''}">Documents <span class="count">${all.filter(isDoc).length}</span></button></nav><div class="sidebar-foot"><button id="export">↓ Export favorites</button><button id="import">↑ Import favorites</button><p>Stars make a review shortlist, not final approvals. Export to keep a portable copy.</p></div></aside><div class="workspace"><div class="topbar"><span class="breadcrumb">${esc(p.name)} / ${esc(cats[state.view]||({'all':'All files','favorites':'Favorites','documents':'Documents'}[state.view]))}</span><input class="search" id="search" type="search" placeholder="Search looks, scenes, details…" aria-label="Search library" value="${esc(state.search)}"></div><main class="main" id="main"></main></div></div>`;
    document.querySelectorAll('[data-project]').forEach(b=>b.onclick=()=>route(b.dataset.project));
    document.querySelectorAll('[data-view]').forEach(b=>b.onclick=()=>route(state.project,b.dataset.view));
    document.querySelector('#search').oninput=e=>{state.search=e.target.value;renderMain();};
    document.querySelector('#export').onclick=exportFavorites;document.querySelector('#import').onclick=()=>document.querySelector('#import-file').click();
    renderMain();
  }
  function card(a){if(!displayed.includes(a.id))displayed.push(a.id);return `<article class="media-card"><button class="favorite ${favorites.has(a.id)?'on':''}" data-favorite="${esc(a.id)}" aria-label="${favorites.has(a.id)?'Remove favorite: ':'Favorite: '}${esc(a.title)}" aria-pressed="${favorites.has(a.id)}">${iconStar(a.id)}</button><button class="media-open" data-open="${esc(a.id)}"><div class="media-thumb"><img loading="lazy" src="${esc(href(a.thumb))}" alt="${esc(a.title)}">${a.kind==='video'||a.kind==='gif'?`<span class="play">${a.kind==='video'?'▶':'GIF'} ${Math.round(a.duration||0)}s</span>`:''}</div><div class="media-copy"><b>${esc(a.title)}</b><small>${esc(a.sceneID?a.lyric||'Storyboard idea':C.albums.find(x=>x.id===a.album)?.title||a.filename)}</small></div></button></article>`;}
  function mediaGroup(title,description,items,albumID=''){
    if(!items.length)return '';
    return `<section class="story-section"><div class="section-head"><h2>${esc(title)}</h2>${albumID?`<button class="subtle-button" data-album="${esc(albumID)}">Open group · ${items.length}</button>`:`<span class="muted">${items.length}</span>`}</div>${description?`<p>${esc(description)}</p>`:''}<div class="gallery">${items.map(card).join('')}</div></section>`;
  }
  function documentGroups(items){
    if(!items.length)return '';
    const groups=[...new Set(items.map(a=>a.album))].sort((a,b)=>{const rank=x=>x.includes('Gemini')?0:x.includes('Story')?1:x.includes('Helper')?9:3;return rank(a)-rank(b)||a.localeCompare(b);});
    return `<section class="documents-section"><div class="section-head"><h2>Documents & notes</h2><span class="muted">${items.length} files</span></div><p class="intro">Open a group, then read its notes here. Source records and helpers stay separate from the artwork.</p><div class="doc-list">${groups.map(g=>`<details class="doc-group"><summary>${esc(g)} <span class="muted">${items.filter(a=>a.album===g).length}</span></summary><div>${items.filter(a=>a.album===g).map(a=>`<button class="doc-row" data-open="${esc(a.id)}"><b>${esc(a.title)}</b><small>${esc(a.inert?'Helper script · text preview only':a.filename)}</small></button>`).join('')}</div></details>`).join('')}</div></section>`;
  }
  function renderMain(){
    displayed=[];const p=C.projects.find(p=>p.id===state.project);const all=projectAssets().filter(queryMatch);const docs=all.filter(isDoc);const media=all.filter(a=>!isDoc(a));
    const heading=state.album?C.albums.find(a=>a.id===state.album)?.title:cats[state.view]||{all:p.name+' reference library',favorites:'Your favorites',documents:'Documents & notes'}[state.view];
    let html=`<p class="eyebrow">${esc(p.subtitle)}</p><h1>${esc(heading)}</h1><p class="intro">${state.view==='all'?'Artwork first, grouped by purpose. Click a preview to enlarge it; star anything you want to revisit.':state.view==='favorites'?'Your review shortlist. These stars do not change the character locks or original files.':state.view==='documents'?'Notes are grouped by subject. Click a file to read a preview without leaving the library.':'Choose a group or browse the previews below.'}</p>`;
    if(!storageOK)html+='<p class="notice">Browser storage is unavailable. Export your favorites to keep them.</p>';
    if(state.album)html+=`<p><button class="subtle-button" id="back-group">← Back to ${esc(cats[state.view]||'all files')}</button></p>`;
    if(state.view==='favorites'){
      const fav=media.filter(a=>favorites.has(a.id));html+=fav.length?`<div class="tools"><span>${fav.length} selected</span><button class="pill" id="export-main">Export favorites</button></div><div class="gallery">${fav.map(card).join('')}</div>`:'<div class="empty">No favorites yet. Click ☆ on an image or video to add it here.</div>';
    } else if(state.view==='documents')html+=documentGroups(docs);
    else {
      let albums=C.albums.filter(a=>a.project===state.project&&(state.view==='all'||a.category===state.view)&&(!state.album||a.id===state.album));
      if(state.view==='storyboard')html+='<p class="notice">Story ideas grouped by beat. Panel numbers identify the source; song timings are still to be aligned.</p>';
      if(state.view==='details')html+='<p class="notice">Use each reference for its selected detail. A tattoo or piercing example does not replace the whole character.</p>';
      if(state.view!=='all'&&!state.album&&albums.length>1)html+=`<div class="video-filter">${albums.map(a=>`<button class="pill" data-album="${esc(a.id)}">${esc(a.title)}</button>`).join('')}</div>`;
      const categoryOrder=Object.keys(cats);
      albums.sort((a,b)=>categoryOrder.indexOf(a.category)-categoryOrder.indexOf(b.category));
      let shown=0;
      for(const al of albums){
        const items=media.filter(a=>state.view==='all'?a.album===al.id:al.assetIDs.includes(a.id));
        if(!items.length)continue;
        shown+=items.length;html+=mediaGroup(al.title,state.view==='all'?'':al.description,items,al.id);
      }
      if(!shown)html+='<div class="empty">No matching previews. Try another category or search.</div>';
      if(state.view==='all'&&!state.album)html+=documentGroups(docs);
    }
    document.querySelector('#main').innerHTML=html;
    document.querySelectorAll('[data-open]').forEach(b=>b.onclick=()=>openViewer(b.dataset.open));
    document.querySelectorAll('[data-favorite]').forEach(b=>b.onclick=()=>toggleFavorite(b.dataset.favorite));
    document.querySelectorAll('[data-album]').forEach(b=>b.onclick=()=>{const a=C.albums.find(x=>x.id===b.dataset.album);route(state.project,a.category,a.id);});
    document.querySelector('#back-group')?.addEventListener('click',()=>route(state.project,state.view));
    document.querySelector('#export-main')?.addEventListener('click',exportFavorites);
  }
  const dialog=document.createElement('dialog');dialog.className='viewer';dialog.setAttribute('aria-label','Media preview');document.body.append(dialog);
  function openViewer(id){
    const a=byID.get(id);if(!a)return;currentID=id;const i=displayed.indexOf(id),doc=isDoc(a);
    const media=a.kind==='video'?`<video controls playsinline preload="metadata" poster="${esc(href(a.thumb))}" src="${esc(href(a.src))}"></video>`:a.kind==='pdf'?`<iframe title="PDF preview" src="${esc(href(a.src))}"></iframe>`:a.kind==='document'?`<pre>${esc(a.text)}</pre>`:`<img src="${esc(href(a.src))}" alt="${esc(a.title)}" id="full-image">`;
    dialog.innerHTML=`<div class="viewer-body"><div class="viewer-head"><span>${doc?'Document preview':`${Math.max(i+1,1)} / ${displayed.length} · ${a.kind==='video'?'Video':'Image'} preview`}</span><div class="view-nav">${!doc?`<button id="previous" aria-label="Previous image" ${i<=0?'disabled':''}>←</button><button id="next" aria-label="Next image" ${i<0||i>=displayed.length-1?'disabled':''}>→</button>`:''}${['image','gif'].includes(a.kind)?'<button id="zoom" aria-label="Toggle full-size zoom">Zoom</button>':''}<button id="close-viewer" aria-label="Close preview">✕</button></div></div><div class="stage">${media}</div><aside class="viewer-info"><p class="label">${esc(cats[a.category]||'Document')}</p><h2>${esc(a.title)}</h2><p class="filename">${esc(a.filename)}</p>${a.lyric?`<p class="label">Lyric connection</p><p>${esc(a.lyric)}</p>`:''}${a.beat?`<p>${esc(a.beat)}</p>`:''}${a.motion?`<p class="label">Motion idea</p><p>${esc(a.motion)}</p>`:''}${a.note?`<p class="label">Review note</p><p>${esc(a.note)}</p>`:''}${a.inert?'<p>Preserved helper script. This viewer only displays its text.</p>':''}${!doc?`<button class="action" id="viewer-favorite">${favorites.has(id)?'★ Favorited':'☆ Add to favorites'}</button>`:''}<a class="small-link" href="${esc(href(a.src))}" target="_blank" rel="noopener" ${a.inert?'download':''}>Open original file ↗</a><details><summary>File details</summary><p>${esc(a.repoPath)}</p>${a.sha256?`<p>SHA-256<br>${esc(a.sha256)}</p>`:''}<p>${esc(typeof a.sourceStatus==='string'?a.sourceStatus:'Source record retained')}</p></details></aside></div>`;
    document.querySelector('#close-viewer').onclick=()=>dialog.close();
    document.querySelector('#previous')?.addEventListener('click',()=>openViewer(displayed[i-1]));
    document.querySelector('#next')?.addEventListener('click',()=>openViewer(displayed[i+1]));
    document.querySelector('#zoom')?.addEventListener('click',()=>document.querySelector('#full-image').classList.toggle('zoomed'));
    document.querySelector('#viewer-favorite')?.addEventListener('click',e=>{toggleFavorite(id);e.target.textContent=favorites.has(id)?'★ Favorited':'☆ Add to favorites';});
    if(!dialog.open)dialog.showModal();
  }
  dialog.addEventListener('close',()=>{dialog.querySelector('video')?.pause();dialog.innerHTML='';currentID='';if(state.view==='favorites')renderMain();});
  dialog.addEventListener('click',e=>{if(e.target===dialog)dialog.close();});
  document.addEventListener('keydown',e=>{if(!dialog.open)return;const i=displayed.indexOf(currentID);if(e.key==='ArrowRight'&&i>=0&&i<displayed.length-1){e.preventDefault();openViewer(displayed[i+1]);}if(e.key==='ArrowLeft'&&i>0){e.preventDefault();openViewer(displayed[i-1]);}});
  function exportFavorites(){const items=[...favorites].map(id=>byID.get(id)).filter(Boolean).map(a=>({id:a.id,project:a.project,filename:a.filename,path:a.repoPath,sha256:a.sha256||null,role:a.category}));const blob=new Blob([JSON.stringify({format:'cfa-visual-favorites-v1',exported:new Date().toISOString(),status:'user review shortlist; not automatic final approval',items},null,2)],{type:'application/json'});const u=URL.createObjectURL(blob),a=document.createElement('a');a.href=u;a.download='CFA-favorites-'+new Date().toISOString().slice(0,10)+'.json';a.click();setTimeout(()=>URL.revokeObjectURL(u),3000);notice('Favorites exported. Keep this file to share your selections.');}
  const input=document.createElement('input');input.type='file';input.accept='.json,application/json';input.id='import-file';input.hidden=true;document.body.append(input);
  input.onchange=async()=>{try{const data=JSON.parse(await input.files[0].text());if(data.format!=='cfa-visual-favorites-v1'||!Array.isArray(data.items))throw Error();let n=0;for(const x of data.items){const a=byID.get(x.id);if(a&&(!x.sha256||x.sha256===a.sha256)){favorites.add(x.id);n++;}}saveFavorites();render();notice(n+' matching favorites imported.');}catch{notice('That file is not a valid exported favorites list.');}finally{input.value='';}};
  window.addEventListener('hashchange',()=>{parseHash();render();});parseHash();render();
})();
