// Danfo Craze offline cache: the game works with no data after the first visit.
// - Pages: network first (3 s limit on weak connections), then the cached copy.
// - Game files: served from the cache straight away and refreshed in the background.
// - Party music: kept in its own small cache (last few clips only) that survives updates.
const CACHE = 'danfo-craze-v17', MUSIC = 'danfo-music', MUSIC_MAX = 6;
const CORE = ['./', 'index.html', 'quiz.js', 'music/tracks.json', 'manifest.webmanifest', 'brand/logo.svg', 'favicon.png', 'apple-touch-icon.png', 'icon-192.png', 'icon-512.png',
  'fonts/bungee-latin-400-normal.woff2', 'fonts/bungee-latin-ext-400-normal.woff2', 'fonts/baloo-2-latin-600-normal.woff2', 'fonts/baloo-2-latin-ext-600-normal.woff2',
  'fonts/baloo-2-latin-800-normal.woff2', 'fonts/baloo-2-latin-ext-800-normal.woff2'];
self.addEventListener('install', e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(CORE)).then(() => self.skipWaiting())); });
self.addEventListener('activate', e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE && k !== MUSIC).map(k => caches.delete(k)))).then(() => self.clients.claim())); });
function timeout(ms) { return new Promise((_, rej) => setTimeout(() => rej(new Error('slow')), ms)); }
async function trimMusic(c) { const ks = await c.keys(); for (let i = 0; i < ks.length - MUSIC_MAX; i++) await c.delete(ks[i]); }
self.addEventListener('fetch', e => {
  const req = e.request, url = new URL(req.url);
  if (req.method !== 'GET' || url.origin !== location.origin) return;
  if (req.mode === 'navigate') {
    e.respondWith(Promise.race([fetch(req), timeout(3000)]).then(r => { const copy = r.clone(); caches.open(CACHE).then(c => c.put('index.html', copy)); return r; })
      .catch(() => caches.match('index.html')));
    return;
  }
  if (/\/music\/party-\d+\.mp3$/.test(url.pathname)) {
    e.respondWith(caches.open(MUSIC).then(c => c.match(req).then(m => m || fetch(req).then(r => { if (r.ok) c.put(req, r.clone()).then(() => trimMusic(c)); return r; }))).catch(() => Response.error()));
    return;
  }
  e.respondWith(caches.open(CACHE).then(c => c.match(req).then(m => {
    const net = fetch(req).then(r => { if (r.ok) c.put(req, r.clone()); return r; });
    return m ? (net.catch(() => {}), m) : net;
  })).catch(() => Response.error()));
});
