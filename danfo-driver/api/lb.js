// Danfo Craze online leaderboard (Vercel function + Vercel Blob).
// One JSON file holds every entry. Writes use the file's ETag, so two
// players saving at the same moment never overwrite each other.
//   GET    /api/lb?cc=NG        boards: World, Clean runs, My country
//   POST   /api/lb              { pid, n, cc, s, d, t, pax, k, diff, pl, rk, lk, gold }
//   POST   /api/lb?report=HASH  { pid }
//   DELETE /api/lb              { pid }   removes the player's entry
import { get, put, BlobPreconditionFailedError } from '@vercel/blob';
import { createHash } from 'node:crypto';

const FILE = 'lb/board.json', KEEP = 1000, TOP = 50, HIDE_AT = 3, WAIT_MS = 15000;
const BAD = /(fuck|shit|bitch|cunt|nigg|fag|dick|pussy|porn|sex|rape|nazi|hitler|ashawo|olosho|mumu|werey|oloshi|puta|merde|salope|connard|pute|bastard|slut|whore)/i;
const hash = pid => createHash('sha256').update('danfo:' + pid).digest('base64url').slice(0, 10);
const clip = (v, n) => String(v ?? '').replace(/[\u0000-\u001f<>"'`\\]/g, '').trim().slice(0, n);
const num = (v, max) => { const x = Number(v); return Number.isFinite(x) && x >= 0 ? Math.min(Math.floor(x), max) : 0; };

async function load() {
  const r = await get(FILE, { access: 'public', useCache: false }).catch(() => null);
  if (!r || r.statusCode !== 200) return { data: { e: {} }, etag: null };
  const txt = await new Response(r.stream).text();
  try { return { data: JSON.parse(txt), etag: r.blob.etag }; } catch { return { data: { e: {} }, etag: r.blob.etag }; }
}
async function save(data, etag) {
  await put(FILE, JSON.stringify(data), { access: 'public', contentType: 'application/json', addRandomSuffix: false, allowOverwrite: true, cacheControlMaxAge: 60, ...(etag ? { ifMatch: etag } : {}) });
}
// read, change, write; retry if someone else wrote first
async function update(fn) {
  for (let i = 0; i < 5; i++) {
    const { data, etag } = await load(); data.e = data.e || {};
    const out = fn(data); if (out && out.error) return out;
    try { await save(data, etag); return out || { ok: true }; }
    catch (err) { if (!(err instanceof BlobPreconditionFailedError) && !/precondition|etag|412/i.test(String(err && err.message))) throw err; }
  }
  return { error: 'busy', status: 503 };
}
const pub = (h, e, clean) => ({ h, n: e.n, cc: e.cc, s: clean ? e.cs : e.s, k: clean ? 0 : e.k, diff: clean ? e.cdiff : e.diff, pl: e.pl, rk: e.rk, lk: e.lk, gold: !!e.gold });
function boards(data, cc) {
  const all = Object.entries(data.e).filter(([, e]) => (e.rep || []).length < HIDE_AT);
  const top = (list, clean) => list.sort((a, b) => (clean ? b[1].cs - a[1].cs : b[1].s - a[1].s)).slice(0, TOP).map(([h, e]) => pub(h, e, clean));
  return {
    world: top(all.slice(), false),
    clean: top(all.filter(([, e]) => e.cs > 0), true),
    country: cc ? top(all.filter(([, e]) => e.cc === cc), false) : [],
    total: all.length,
  };
}
function check(b) {
  const t = num(b.t, 36000), d = num(b.d, 3e6), pax = num(b.pax, 1e5), s = num(b.s, 1e8);
  if (t < 5) return 'too short';
  if (d > t * 62 + 50) return 'too far';
  if (pax > t * 1.5 + 5) return 'too many passengers';
  if (s > d * .1 + pax * 1000 + t * 40 + 2000) return 'score too high';
  return '';
}
export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(204).end();
  if (!process.env.BLOB_READ_WRITE_TOKEN) return res.status(503).json({ error: 'not set up' });
  try {
    const q = req.query || {}, b = typeof req.body === 'string' ? JSON.parse(req.body || '{}') : (req.body || {});
    if (req.method === 'GET') {
      const { data } = await load();
      res.setHeader('Cache-Control', 'public, s-maxage=20, stale-while-revalidate=60');
      return res.status(200).json(boards(data, clip(q.cc, 6).toUpperCase()));
    }
    const pid = clip(b.pid, 40);
    if (!/^[A-Za-z0-9_-]{16,40}$/.test(pid)) return res.status(400).json({ error: 'bad id' });
    const me = hash(pid);
    if (req.method === 'DELETE') {
      const out = await update(data => { delete data.e[me]; });
      return res.status(out.status || 200).json(out);
    }
    if (req.method !== 'POST') return res.status(405).json({ error: 'method' });
    if (q.report) {
      const who = clip(q.report, 12);
      const out = await update(data => { const e = data.e[who]; if (!e || who === me) return { error: 'no entry', status: 404 }; e.rep = e.rep || []; if (!e.rep.includes(me)) e.rep.push(me); });
      return res.status(out.status || 200).json(out.error ? out : { ok: true });
    }
    const why = check(b); if (why) return res.status(422).json({ error: why });
    const n = clip(b.n, 14) || 'Driver', pl = clip(b.pl, 8).toUpperCase().replace(/[^A-Z0-9 ]/g, '');
    if (BAD.test(n.replace(/[^a-z]/gi, '')) || BAD.test(pl.replace(/ /g, ''))) return res.status(422).json({ error: 'name' });
    const s = num(b.s, 1e8), k = num(b.k, 99), diff = ['easy', 'normal', 'hard'].includes(b.diff) ? b.diff : 'normal';
    let lk = {}; try { lk = typeof b.lk === 'object' && b.lk ? JSON.parse(JSON.stringify(b.lk).slice(0, 600)) : {}; } catch { lk = {}; }
    const now = Date.now();
    const out = await update(data => {
      const e = data.e[me] || { s: 0, cs: 0, rep: [] };
      if (now - (e.at || 0) < WAIT_MS) return { error: 'wait', status: 429 };
      Object.assign(e, { n, cc: clip(b.cc, 6).toUpperCase(), pl, rk: clip(b.rk, 14), lk, gold: !!b.gold, at: now });
      if (n !== e.lastN) { e.rep = []; e.lastN = n; }
      if (s > e.s) { e.s = s; e.k = k; e.diff = diff; }
      if (!k && s > (e.cs || 0)) { e.cs = s; e.cdiff = diff; }
      data.e[me] = e;
      const ids = Object.keys(data.e);
      if (ids.length > KEEP) ids.sort((a, b2) => data.e[a].s - data.e[b2].s).slice(0, ids.length - KEEP).forEach(id => { if (id !== me) delete data.e[id]; });
      const rank = Object.values(data.e).filter(x => x.s > e.s).length + 1;
      return { ok: true, me, best: e.s, rank };
    });
    return res.status(out.status || 200).json(out);
  } catch (err) {
    console.error('lb', err);
    return res.status(500).json({ error: 'server' });
  }
}
