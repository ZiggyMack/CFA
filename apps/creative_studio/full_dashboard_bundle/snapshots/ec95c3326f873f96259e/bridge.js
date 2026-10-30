/* Streamlit v1 component handshake only. The existing dashboard owns reviews. */
(() => {
  const parentOrigin = (() => {
    try { return new URL(document.referrer).origin; } catch { return location.origin; }
  })();
  const send = (type, extra = {}) => window.parent.postMessage({isStreamlitMessage: true, type, ...extra}, parentOrigin);
  const resize = requested => {
    const height = Math.max(480, Math.min(1400, Number(requested) || 850));
    send('streamlit:setFrameHeight', {height});
  };
  window.addEventListener('message', event => {
    if (event.source !== window.parent || event.origin !== parentOrigin || event.data?.type !== 'streamlit:render') return;
    resize(event.data.args?.height);
  });
  send('streamlit:componentReady', {apiVersion: 1});
  resize(850);
})();
