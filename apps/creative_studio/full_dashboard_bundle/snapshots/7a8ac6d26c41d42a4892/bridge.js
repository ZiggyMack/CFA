/* Streamlit v1 component handshake only. The existing dashboard owns reviews. */
(() => {
  const parentOrigin = (() => {
    try { return new URL(document.referrer).origin; } catch { return location.origin; }
  })();
  const send = (type, extra = {}) => window.parent.postMessage({isStreamlitMessage: true, type, ...extra}, parentOrigin);
  let routeConfig = null, requestedRoute = null, requestID = null, lastRequest, lastReported = '';
  const validRoute = value => {
    if (!routeConfig || typeof value !== 'string' || !value.startsWith('#') || value.length > 700) return null;
    let parts;
    try { parts = value.slice(1).split('/').map(decodeURIComponent); } catch { return null; }
    if (![2, 3].includes(parts.length) || !routeConfig.projects?.includes(parts[0]) || !routeConfig.views?.includes(parts[1])) return null;
    if (parts.some(part => !part || /[\x00-\x1f/\\?#]/.test(part))) return null;
    return '#' + parts.map(encodeURIComponent).join('/');
  };
  const reportRoute = () => {
    const route = validRoute(location.hash);
    if (!route) return;
    const value = {route, requestedRoute, requestID};
    const encoded = JSON.stringify(value);
    if (encoded === lastReported) return;
    lastReported = encoded;
    send('streamlit:setComponentValue', {value, dataType:'json'});
  };
  const resize = requested => {
    const height = Math.max(480, Math.min(1400, Number(requested) || 850));
    send('streamlit:setFrameHeight', {height});
  };
  window.addEventListener('message', event => {
    if (event.source !== window.parent || event.origin !== parentOrigin || event.data?.type !== 'streamlit:render') return;
    resize(event.data.args?.height);
    routeConfig = event.data.args?.routeConfig || null;
    requestedRoute = validRoute(event.data.args?.initialRoute);
    requestID = event.data.args?.requestID ?? null;
    // Apply each outer navigation request once. Ordinary rerenders must not
    // reset a route the reader has just chosen inside the library.
    const request = JSON.stringify([requestID, requestedRoute]);
    if (request !== lastRequest) {
      lastRequest = request;
      if (requestedRoute && validRoute(location.hash) !== requestedRoute) location.hash = requestedRoute;
    }
    queueMicrotask(reportRoute);
  });
  window.addEventListener('hashchange', () => queueMicrotask(reportRoute));
  send('streamlit:componentReady', {apiVersion: 1});
  resize(850);
})();
