// Danfo Craze offline cache: the game works with no data after the first visit.
const CACHE = 'danfo-craze-v14';
const CORE = ['./', 'index.html', 'quiz.js', 'music/tracks.json', 'manifest.webmanifest', 'brand/logo.svg', 'favicon.png', 'apple-touch-icon.png', 'icon-192.png', 'icon-512.png'];
self.addEventListener('install', e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(CORE)).then(() => self.skipWaiting())); });
self.addEventListener('activate', e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  // network first so updates arrive; fall back to the cache when offline
  e.respondWith(fetch(e.request).then(r => { const copy = r.clone(); if (r.ok || r.type === 'opaque') caches.open(CACHE).then(c => c.put(e.request, copy)); return r; })
    .catch(() => caches.match(e.request).then(m => m || caches.match('index.html'))));
});
