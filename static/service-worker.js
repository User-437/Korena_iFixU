/* PharmaLedger PWA service worker: NEVER cache accounting or authenticated pages. */
const CACHE = 'korena-pwa-shell-v1';
const ASSETS = ['/static/style.css', '/static/pwa.js', '/static/icons/icon-192.png', '/static/icons/icon-512.png'];
self.addEventListener('install', event => {
  event.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', event => {
  event.waitUntil(caches.keys().then(names => Promise.all(names.filter(n => n !== CACHE).map(n => caches.delete(n)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', event => {
  const req = event.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;
  if (url.pathname === '/static/style.css' || url.pathname === '/static/pwa.js' || url.pathname.startsWith('/static/icons/')) {
    event.respondWith(fetch(req).then(res => {
      if (res.ok) { const copy = res.clone(); caches.open(CACHE).then(c => c.put(req,copy)); }
      return res;
    }).catch(() => caches.match(req)));
  }
  // Always fetch protected pages and API results directly from server; offline requests fail closed.
});
