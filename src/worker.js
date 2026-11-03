// DrawBird API: anonymous device tokens, birds, votes, flags, flocks, moderation on D1.
import PostalMime from 'postal-mime';
import { STATIC_PAGES, LANGS, WEEK_UI } from './static_pages.js';
import { isBadName, notifyBird, notifyText, connectTelegram, telegramStatus, handleTelegram, sendDigest, setting } from './moderation.js';
const MAX_BIRDS = 8;
const MAX_FLOCKS = 12;
const MAX_IMG = 90_000; // data URL characters (~65 KB image)
const HIDE_FLAGS = 3;
const HIDE_FLAGS_NEW = 2; // birds younger than a day hide sooner
const TRUST_AFTER = 2; // approved birds before an artist skips the review queue
const IP_BAN_MS = 24 * 3600e3;
// SQL for "this bird is hidden by reports", given a birds alias.
const hiddenSql = a => `(SELECT COUNT(*) FROM flags f WHERE f.bird_id = ${a}.id) >= CASE WHEN ${a}.created > (strftime('%s','now') * 1000 - 86400000) THEN ${HIDE_FLAGS_NEW} ELSE ${HIDE_FLAGS} END`;
const PUBLIC_TTL = 10; // seconds the shared part of /api/state is cached at the edge
const NEW_IDS_PER_IP_DAY = 40; // classrooms share one IP, so keep this generous

// Hardening headers for everything the Worker answers.
const CSP = [
  "default-src 'self'", "script-src 'self' 'unsafe-inline'", "style-src 'self' 'unsafe-inline'",
  "font-src 'self'", "img-src 'self' data: blob:", "connect-src 'self'", "manifest-src 'self'",
  "object-src 'none'", "base-uri 'none'", "form-action 'none'", "frame-ancestors 'none'",
].join('; ');
const SECURITY_HEADERS = {
  'x-content-type-options': 'nosniff',
  'referrer-policy': 'strict-origin-when-cross-origin',
  'permissions-policy': 'camera=(), microphone=(), geolocation=(), payment=()',
  'x-frame-options': 'DENY',
  'strict-transport-security': 'max-age=31536000; includeSubDomains',
};
function secure(res) {
  const out = new Response(res.body, res);
  for (const [k, v] of Object.entries(SECURITY_HEADERS)) out.headers.set(k, v);
  const type = out.headers.get('content-type') || '';
  if (type.startsWith('text/html')) out.headers.set('content-security-policy', CSP);
  else if (!out.headers.has('content-security-policy')) out.headers.set('content-security-policy', "default-src 'none'; frame-ancestors 'none'; sandbox");
  return out;
}

// Per-IP limits through Workers Rate Limiting bindings; missing bindings (local dev) never block.
const clientIp = req => req.headers.get('cf-connecting-ip') || 'local';
async function limited(binding, key) {
  if (!binding) return false;
  try { return !(await binding.limit({ key })).success; } catch { return false; }
}

// Exact fixed-window counter in D1 for the costly or sensitive paths (the bindings above are best-effort).
// Keys carry only a salted hash of the IP.
async function overLimit(env, req, kind, limit, windowSec) {
  const now = Date.now();
  const key = kind + ':' + (await sha256(`${clientIp(req)}|${env.ADMIN_KEY || ''}`)).slice(0, 32);
  const n = await env.DB.prepare(`INSERT INTO limits (k, n, exp) VALUES (?, 1, ?)
      ON CONFLICT(k) DO UPDATE SET n = CASE WHEN exp < ? THEN 1 ELSE n + 1 END, exp = CASE WHEN exp < ? THEN ? ELSE exp END
      RETURNING n`).bind(key, now + windowSec * 1000, now, now, now + windowSec * 1000).first('n');
  if (Math.random() < .01) await env.DB.prepare('DELETE FROM limits WHERE exp < ?').bind(now).run();
  return n > limit;
}

const json = (data, status = 200, headers = {}) =>
  new Response(JSON.stringify(data), { status, headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store', ...headers } });
const fail = (status, error) => json({ error }, status);
const clean = (s, n) => String(s ?? '').replace(/[\u0000-\u001f\u007f-\u009f\u00ad\u200b-\u200f\u202a-\u202e\u2060-\u206f\ufeff]/g, '').replace(/\s+/g, ' ').trim().slice(0, n);
const newId = () => crypto.randomUUID().replace(/-/g, '').slice(0, 16);
const ID = /^[a-z0-9]{16}$/;

async function sha256(text) {
  const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(text));
  return [...new Uint8Array(buf)].map(b => b.toString(16).padStart(2, '0')).join('');
}

// Device token -> user row (created on first write). The token itself is never stored.
async function auth(req, env, create) {
  const m = /^Bearer ([A-Za-z0-9_-]{32,128})$/.exec(req.headers.get('authorization') || '');
  if (!m) return null;
  const hash = await sha256(m[1]);
  let row = await env.DB.prepare('SELECT uid, name FROM users WHERE token_hash = ?').bind(hash).first();
  if (!row && create) {
    if (await ipBanned(req, env)) throw { status: 403, error: 'banned' };
    // Cap how many new identities one IP can mint per day (vote and flag stuffing). Only a salted hash of the IP is kept, for two days.
    const day = new Date().toISOString().slice(0, 10);
    const ipHash = (await sha256(`${clientIp(req)}|${day}|${env.ADMIN_KEY || ''}`)).slice(0, 32);
    const n = await env.DB.prepare('INSERT INTO new_ids (day, ip_hash, n) VALUES (?, ?, 1) ON CONFLICT(day, ip_hash) DO UPDATE SET n = n + 1 RETURNING n')
      .bind(day, ipHash).first('n');
    if (Math.random() < .02) await env.DB.prepare('DELETE FROM new_ids WHERE day < ?').bind(new Date(Date.now() - 864e5).toISOString().slice(0, 10)).run();
    if (n === NEW_IDS_PER_IP_DAY + 1) await notifyText(env, '⚠️ Bir ağdan bugün çok sayıda yeni hesap açılmaya çalışıldı (sahte oy/bildirim girişimi olabilir). Yeni hesaplar o ağ için yarına kadar durduruldu.');
    if (n > NEW_IDS_PER_IP_DAY) throw { status: 429, error: 'too_many_new' };
    row = { uid: hash.slice(0, 16), name: '' };
    await env.DB.prepare('INSERT OR IGNORE INTO users (uid, token_hash, name, created) VALUES (?, ?, ?, ?)')
      .bind(row.uid, hash, '', Date.now()).run();
  }
  return row;
}
async function isAdmin(req, env) {
  const given = req.headers.get('x-admin-key');
  if (!env.ADMIN_KEY || !given) return false;
  const enc = t => new TextEncoder().encode(t);
  const [a, b] = await Promise.all([sha256(given), sha256(env.ADMIN_KEY)]);
  return crypto.subtle.timingSafeEqual(enc(a), enc(b));
}
const isBanned = (env, uid) => env.DB.prepare('SELECT 1 FROM bans WHERE uid = ?').bind(uid).first();
const ipKey = async (req, env) => (await sha256(`ip|${clientIp(req)}|${env.ADMIN_KEY || ''}`)).slice(0, 32);
async function ipBanned(req, env) {
  return !!(await env.DB.prepare('SELECT 1 FROM ip_bans WHERE ip_hash = ? AND exp > ?').bind(await ipKey(req, env), Date.now()).first());
}

// The shared part of the sky: same for every viewer, so it is cached briefly at the edge.
const publicKey = url => new Request(new URL('/api/__public', url).toString());
async function publicState(env, url) {
  const cache = caches.default;
  const key = publicKey(url);
  const hit = await cache.match(key);
  if (hit) return hit.json();
  const [birds, users, flocks] = await env.DB.batch([
    env.DB.prepare(`SELECT b.id, b.uid, b.name, b.created,
        COALESCE(SUM(v.v = 1), 0) AS up, COALESCE(SUM(v.v = -1), 0) AS down,
        (SELECT COUNT(*) FROM flags f WHERE f.bird_id = b.id) AS flags
      FROM birds b LEFT JOIN votes v ON v.bird_id = b.id
      WHERE b.status = 'live' AND b.uid NOT IN (SELECT uid FROM bans)
      GROUP BY b.id ORDER BY b.created DESC LIMIT 2000`),
    env.DB.prepare('SELECT uid, name FROM users WHERE uid IN (SELECT DISTINCT uid FROM birds UNION SELECT DISTINCT uid FROM flocks)'),
    env.DB.prepare('SELECT id, uid, name, birds, created, public FROM flocks WHERE public = 1 AND uid NOT IN (SELECT uid FROM bans) ORDER BY created'),
  ]);
  const data = {
    birds: birds.results,
    names: Object.fromEntries(users.results.map(u => [u.uid, u.name])),
    flocks: flocks.results.map(f => ({ ...f, public: true, birds: JSON.parse(f.birds) })),
  };
  data.etag = '"' + (await sha256(JSON.stringify(data))).slice(0, 20) + '"';
  await cache.put(key, new Response(JSON.stringify(data), { headers: { 'content-type': 'application/json', 'cache-control': `public, max-age=${PUBLIC_TTL}` } }));
  return data;
}

// GET /api/sky: the shared sky. Browsers revalidate with If-None-Match, so an unchanged sky costs a 304 and no body.
async function sky(req, env, url) {
  const pub = await publicState(env, url);
  const headers = { etag: pub.etag, 'cache-control': 'no-cache' };
  if (req.headers.get('if-none-match') === pub.etag) return new Response(null, { status: 304, headers });
  const { etag, ...body } = pub;
  return json(body, 200, headers);
}

async function state(req, env, url) {
  const me = await auth(req, env, false);
  const mine = { v: {}, f: {} };
  let flocks = [], pending = [];
  if (me) {
    const [mv, mf, priv, pend] = await env.DB.batch([
      env.DB.prepare('SELECT bird_id, v FROM votes WHERE uid = ?').bind(me.uid),
      env.DB.prepare('SELECT bird_id FROM flags WHERE uid = ?').bind(me.uid),
      env.DB.prepare('SELECT id, uid, name, birds, created, public FROM flocks WHERE uid = ? AND public = 0').bind(me.uid),
      env.DB.prepare("SELECT id, uid, name, created FROM birds WHERE uid = ? AND status = 'pending'").bind(me.uid),
    ]);
    pending = await Promise.all(pend.results.map(async b => ({ ...b, up: 0, down: 0, flags: 0, pending: true, sig: await imgSig(env, b.id) })));
    mv.results.forEach(r => { mine.v[r.bird_id] = r.v; });
    mf.results.forEach(r => { mine.f[r.bird_id] = true; });
    flocks = priv.results.map(f => ({ ...f, public: false, birds: JSON.parse(f.birds) }));
  }
  return json({
    me: me ? { uid: me.uid, name: me.name, banned: !!(await isBanned(env, me.uid)) } : null,
    admin: await isAdmin(req, env),
    readonly: (await setting(env, 'readonly')) === '1',
    hideFlags: HIDE_FLAGS, hideFlagsNew: HIDE_FLAGS_NEW, maxBirds: MAX_BIRDS,
    pending, flocks, mine,
  });
}

// Signed links let the artist, the admin panel and Telegram see a bird that is still waiting for review.
async function imgSig(env, id) { return (await sha256(`img|${id}|${env.ADMIN_KEY || ''}`)).slice(0, 24); }
const imgCacheKey = (url, id) => new Request(new URL(url).origin + '/api/img/' + id);

async function image(req, id, env) {
  const cache = caches.default;
  const key = imgCacheKey(req.url, id);
  const hit = await cache.match(key);
  if (hit) return hit;
  const row = await env.DB.prepare('SELECT img, status FROM birds WHERE id = ?').bind(id).first();
  if (!row) return new Response('not found', { status: 404 });
  const live = row.status === 'live';
  if (!live && new URL(req.url).searchParams.get('s') !== await imgSig(env, id)) return new Response('not found', { status: 404 });
  const m = /^data:(image\/(?:png|webp));base64,([A-Za-z0-9+/=]+)$/.exec(row.img);
  if (!m) return new Response('bad image', { status: 500 });
  const bytes = Uint8Array.from(atob(m[2]), c => c.charCodeAt(0));
  const res = new Response(bytes, { headers: {
    'content-type': m[1], 'cache-control': live ? 'public, max-age=86400' : 'private, no-store',
    'content-security-policy': "default-src 'none'; sandbox", 'content-disposition': 'inline',
  } });
  if (live) await cache.put(key, res.clone());
  return res;
}

// The bytes must really be a PNG or WebP, not something else wearing an image label.
function looksLikeImage(dataUrl) {
  try {
    const head = atob(dataUrl.split(',')[1].slice(0, 24));
    if (dataUrl.startsWith('data:image/png')) return head.startsWith('\x89PNG\r\n\x1a\n');
    return head.startsWith('RIFF') && head.slice(8, 12) === 'WEBP';
  } catch { return false; }
}

async function readBody(req, limit = 120_000) {
  const len = +(req.headers.get('content-length') || 0);
  if (len > limit) throw new Error('too_large');
  const text = await req.text();
  if (text.length > limit) throw new Error('too_large');
  return text ? JSON.parse(text) : {};
}

// ---- moderation actions (admin panel and Telegram buttons share these) ----
async function birdInfo(env, id) {
  return env.DB.prepare(`SELECT b.id, b.uid, b.name, b.status, b.created, u.name AS author,
      (SELECT COUNT(*) FROM flags f WHERE f.bird_id = b.id) AS flags
    FROM birds b LEFT JOIN users u ON u.uid = b.uid WHERE b.id = ?`).bind(id).first();
}
async function deleteBird(env, id, url) {
  if (url) await caches.default.delete(imgCacheKey(url, id));
  await env.DB.batch([
    env.DB.prepare('DELETE FROM birds WHERE id = ?').bind(id),
    env.DB.prepare('DELETE FROM votes WHERE bird_id = ?').bind(id),
    env.DB.prepare('DELETE FROM flags WHERE bird_id = ?').bind(id),
  ]);
}
async function approveBird(env, id) {
  const b = await env.DB.prepare("UPDATE birds SET status = 'live' WHERE id = ? RETURNING uid").bind(id).first();
  if (!b) return;
  await env.DB.prepare(`UPDATE users SET trusted = 1 WHERE uid = ? AND (SELECT COUNT(*) FROM birds WHERE uid = ? AND status = 'live') >= ${TRUST_AFTER}`)
    .bind(b.uid, b.uid).run();
}
async function setBan(env, uid, on) {
  if (on) {
    const u = await env.DB.prepare('SELECT ip_hash FROM users WHERE uid = ?').bind(uid).first();
    const writes = [
      env.DB.prepare('INSERT OR IGNORE INTO bans (uid, created) VALUES (?, ?)').bind(uid, Date.now()),
      env.DB.prepare('UPDATE users SET trusted = 0 WHERE uid = ?').bind(uid),
    ];
    // The ban also covers the network they posted from for a day, so a fresh identity does not help.
    if (u?.ip_hash) writes.push(env.DB.prepare('INSERT INTO ip_bans (ip_hash, exp) VALUES (?, ?) ON CONFLICT(ip_hash) DO UPDATE SET exp = excluded.exp').bind(u.ip_hash, Date.now() + IP_BAN_MS));
    await env.DB.batch(writes);
  } else {
    const u = await env.DB.prepare('SELECT ip_hash FROM users WHERE uid = ?').bind(uid).first();
    await env.DB.batch([
      env.DB.prepare('DELETE FROM bans WHERE uid = ?').bind(uid),
      env.DB.prepare('DELETE FROM ip_bans WHERE ip_hash = ?').bind(u?.ip_hash || ''),
    ]);
  }
}
// kind: ok (approve), no (reject/delete), ban (delete + ban artist), clear (reports were wrong)
async function decide(env, kind, id, url) {
  if (!ID.test(String(id))) return 'Geçersiz kuş';
  const b = await birdInfo(env, id);
  if (!b) return 'Kuş zaten yok';
  if (kind === 'ok') { await approveBird(env, id); await env.DB.prepare('DELETE FROM flags WHERE bird_id = ?').bind(id).run(); return 'Onaylandı'; }
  if (kind === 'clear') { await env.DB.prepare('DELETE FROM flags WHERE bird_id = ?').bind(id).run(); return 'Bildirimler temizlendi'; }
  if (kind === 'no') { await deleteBird(env, id, url); return 'Silindi'; }
  if (kind === 'ban') { await deleteBird(env, id, url); await setBan(env, b.uid, true); return 'Silindi, kuşçu engellendi'; }
  return 'Bilinmeyen işlem';
}

async function adminApi(req, env, path, method, body) {
  if (await limited(env.RL_ADMIN, 'admin:' + clientIp(req))) return fail(429, 'slow_down');
  if (!(await isAdmin(req, env))) {
    // Wrong keys are counted: 20 misses per IP lock admin out for an hour.
    if (await overLimit(env, req, 'adminfail', 20, 3600)) {
      if (!(await overLimit(env, req, 'adminfail-alert', 1, 3600))) await notifyText(env, '🚨 Yönetici anahtarı bir saatte 20 kez yanlış girildi. O ağ bir saat kilitlendi. Sen değilsen anahtarı yenile: npx wrangler secret put ADMIN_KEY');
      return fail(429, 'slow_down');
    }
    return fail(403, 'not_admin');
  }
  if (method === 'GET' && path === '/admin/reports') {
    const [reported, bans] = await env.DB.batch([
      env.DB.prepare(`SELECT b.id, b.uid, b.name, b.created, COUNT(f.uid) AS flags,
          (SELECT name FROM users u WHERE u.uid = b.uid) AS author
        FROM birds b JOIN flags f ON f.bird_id = b.id GROUP BY b.id ORDER BY flags DESC, b.created DESC LIMIT 200`),
      env.DB.prepare('SELECT bans.uid, bans.created, users.name FROM bans LEFT JOIN users ON users.uid = bans.uid ORDER BY bans.created DESC'),
    ]);
    const stats = await env.DB.prepare("SELECT (SELECT COUNT(*) FROM birds) AS birds, (SELECT COUNT(*) FROM users) AS users, (SELECT COUNT(*) FROM votes) AS votes, (SELECT COUNT(*) FROM birds WHERE status = 'pending') AS pending, (SELECT COUNT(*) FROM messages WHERE done = 0) AS messages").first();
    const since = new Date(Date.now() - 13 * 864e5).toISOString().slice(0, 10);
    const [visits, newBirds] = await env.DB.batch([
      env.DB.prepare('SELECT day, n FROM visits WHERE day >= ? ORDER BY day').bind(since),
      env.DB.prepare("SELECT strftime('%Y-%m-%d', created / 1000, 'unixepoch') AS day, COUNT(*) AS n FROM birds WHERE created >= ? GROUP BY day")
        .bind(Date.parse(since)),
    ]);
    return json({ reported: reported.results, bans: bans.results, stats, visits: visits.results, newBirds: newBirds.results });
  }
  if (method === 'POST' && path === '/admin/clear') {
    if (!ID.test(String(body.bird))) return fail(400, 'bad_bird');
    await env.DB.prepare('DELETE FROM flags WHERE bird_id = ?').bind(body.bird).run();
    return json({ ok: true });
  }
  if (method === 'GET' && path === '/admin/queue') {
    const { results } = await env.DB.prepare(`SELECT b.id, b.uid, b.name, b.created, u.name AS author,
        (SELECT COUNT(*) FROM birds x WHERE x.uid = b.uid AND x.status = 'live') AS liveCount
      FROM birds b LEFT JOIN users u ON u.uid = b.uid WHERE b.status = 'pending' ORDER BY b.created LIMIT 200`).all();
    for (const r of results) r.sig = await imgSig(env, r.id);
    return json({ queue: results });
  }
  if (method === 'POST' && path === '/admin/review') {
    const kind = ['ok', 'no', 'ban', 'clear'].includes(body.kind) ? body.kind : null;
    if (!kind) return fail(400, 'bad_kind');
    return json({ ok: true, result: await decide(env, kind, String(body.bird || ''), req.url) });
  }
  if (method === 'GET' && path === '/admin/telegram') return json(await telegramStatus(env));
  if (method === 'GET' && path === '/admin/messages') {
    const { results } = await env.DB.prepare('SELECT id, uid, topic, body, contact, created, done FROM messages ORDER BY done, created DESC LIMIT 200').all();
    return json({ messages: results });
  }
  if (method === 'POST' && path === '/admin/message') {
    const id = String(body.id || '');
    if (!ID.test(id)) return fail(400, 'bad_id');
    if (body.delete) await env.DB.prepare('DELETE FROM messages WHERE id = ?').bind(id).run();
    else await env.DB.prepare('UPDATE messages SET done = ? WHERE id = ?').bind(body.done ? 1 : 0, id).run();
    return json({ ok: true });
  }
  if (method === 'POST' && path === '/admin/readonly') {
    await env.DB.prepare("INSERT INTO settings (k, v) VALUES ('readonly', ?) ON CONFLICT(k) DO UPDATE SET v = excluded.v").bind(body.on ? '1' : '0').run();
    await notifyText(env, body.on ? '🔒 Bakım modu açıldı: site yalnız okunur.' : '🔓 Bakım modu kapatıldı.');
    return json({ ok: true });
  }
  if (method === 'POST' && path === '/admin/review-mode') {
    await env.DB.prepare("INSERT INTO settings (k, v) VALUES ('review', ?) ON CONFLICT(k) DO UPDATE SET v = excluded.v").bind(body.on ? '1' : '0').run();
    return json({ ok: true });
  }
  if (method === 'POST' && path === '/admin/telegram') return json(await connectTelegram(env, new URL(req.url).origin));
  if (method === 'POST' && path === '/admin/rename') {
    const uid = String(body.uid || '');
    if (!ID.test(uid)) return fail(400, 'bad_uid');
    await env.DB.prepare("UPDATE users SET name = '' WHERE uid = ?").bind(uid).run();
    return json({ ok: true });
  }
  if (method === 'POST' && path === '/admin/flock-delete') {
    const id = String(body.id || '');
    if (!ID.test(id)) return fail(400, 'bad_flock');
    await env.DB.prepare('DELETE FROM flocks WHERE id = ?').bind(id).run();
    return json({ ok: true });
  }
  if (method === 'POST' && path === '/admin/ban') {
    const uid = String(body.uid || '');
    if (!ID.test(uid)) return fail(400, 'bad_uid');
    await setBan(env, uid, !!body.on);
    return json({ ok: true });
  }
  return fail(404, 'not_found');
}

async function handleApi(req, env, url, ctx) {
  const path = url.pathname.slice(4); // strip "/api"
  const method = req.method;

  if (method === 'GET' && path === '/state') return state(req, env, url);
  if (method === 'GET' && path === '/sky') return sky(req, env, url);
  if (method === 'GET' && path === '/theme') {
    const lang = LANGS.includes(url.searchParams.get('lang')) ? url.searchParams.get('lang') : 'tr', U = WEEK_UI[lang];
    return json({ text: fill(U.theme_head, { title: U.themes[themeIndex(Date.now())][0] }), url: `${pre(lang)}/haftanin-kuslari` }, 200, { 'cache-control': 'public, max-age=600' });
  }
  if (method !== 'GET' && !path.startsWith('/admin/') && await limited(env.RL_WRITE, 'w:' + clientIp(req))) return fail(429, 'slow_down');
  if (method !== 'GET' && !path.startsWith('/admin/') && path !== '/telegram' && path !== '/hit' && (await setting(env, 'readonly')) === '1') return fail(503, 'readonly');
  if (method === 'POST' && path === '/hit') {
    // One count per browser session; nothing about the visitor is stored.
    await env.DB.prepare('INSERT INTO visits (day, n) VALUES (?, 1) ON CONFLICT(day) DO UPDATE SET n = n + 1')
      .bind(new Date().toISOString().slice(0, 10)).run();
    return json({ ok: true });
  }
  const img = /^\/img\/([a-z0-9]{16})$/.exec(path);
  if (method === 'GET' && img) return image(req, img[1], env);
  if (method === 'POST' && path === '/telegram') return handleTelegram(req, env, (kind, id) => decide(env, kind, id, req.url));

  let body = {};
  if (method === 'POST') { try { body = await readBody(req); } catch { return fail(413, 'too_large'); } }
  if (path.startsWith('/admin/')) return adminApi(req, env, path, method, body);
  if (method === 'GET') return fail(404, 'not_found');

  const me = await auth(req, env, true);
  if (!me) return fail(401, 'no_token');
  const admin = await isAdmin(req, env);

  if (method === 'DELETE' && path === '/me') {
    // Erase everything tied to this identity. Votes/flags others gave to these birds go with the birds.
    const { results } = await env.DB.prepare('SELECT id FROM birds WHERE uid = ?').bind(me.uid).all();
    const ids = results.map(r => r.id);
    const writes = [
      env.DB.prepare('DELETE FROM votes WHERE uid = ?').bind(me.uid),
      env.DB.prepare('DELETE FROM flags WHERE uid = ?').bind(me.uid),
      env.DB.prepare('DELETE FROM flocks WHERE uid = ?').bind(me.uid),
    ];
    for (const id of ids) writes.push(
      env.DB.prepare('DELETE FROM votes WHERE bird_id = ?').bind(id),
      env.DB.prepare('DELETE FROM flags WHERE bird_id = ?').bind(id),
      env.DB.prepare('DELETE FROM birds WHERE id = ?').bind(id));
    // birds.uid references users, so the user row goes last.
    writes.push(env.DB.prepare('DELETE FROM users WHERE uid = ?').bind(me.uid));
    await env.DB.batch(writes);
    for (const id of ids) await caches.default.delete(imgCacheKey(req.url, id));
    // A ban outlives the account on purpose (bans table), so erasing cannot be used to dodge one.
    return json({ ok: true, birds: ids.length });
  }

  if (method === 'POST' && path === '/contact') {
    // Rate-limited, stored in D1 and forwarded to the owner's Telegram. Contact details are optional.
    if (await overLimit(env, req, 'contact', 5, 3600)) return fail(429, 'slow_down');
    const topic = ['report', 'kvkk', 'bug', 'idea', 'other'].includes(body.topic) ? body.topic : 'other';
    const text = String(body.body ?? '').replace(/[\u0000-\u0008\u000b-\u001f\u007f\u200b-\u200f\u202a-\u202e\u2060-\u206f\ufeff]/g, '').trim().slice(0, 2000);
    if (text.length < 5) return fail(400, 'too_short');
    const contact = clean(body.contact, 120);
    const id = newId();
    await env.DB.prepare('INSERT INTO messages (id, uid, topic, body, contact, created) VALUES (?, ?, ?, ?, ?, ?)')
      .bind(id, me.uid, topic, text, contact, Date.now()).run();
    const label = { report: '🚩 Bildirim', kvkk: '🔐 KVKK talebi', bug: '🐞 Hata', idea: '💡 Öneri', other: '✉️ Mesaj' }[topic];
    ctx.waitUntil(notifyText(env, `${label}\n${text.slice(0, 900)}${contact ? `\nİletişim: ${contact}` : ''}`));
    return json({ ok: true });
  }

  if (method === 'POST' && path === '/me') {
    let name = clean(body.name, 24);
    const filtered = !!name && isBadName(name);
    if (filtered) name = '';
    await env.DB.prepare('UPDATE users SET name = ? WHERE uid = ?').bind(name, me.uid).run();
    return json({ ok: true, filtered });
  }

  if (method === 'POST' && path === '/birds') {
    if (await isBanned(env, me.uid) || await ipBanned(req, env)) return fail(403, 'banned');
    if (await limited(env.RL_BIRD, 'b:' + clientIp(req)) || await overLimit(env, req, 'bird', 40, 3600)) return fail(429, 'slow_down');
    const data = String(body.img || '');
    if (!/^data:image\/(png|webp);base64,[A-Za-z0-9+/=]+$/.test(data) || data.length > MAX_IMG || !looksLikeImage(data)) return fail(400, 'bad_image');
    const count = await env.DB.prepare('SELECT COUNT(*) AS n FROM birds WHERE uid = ?').bind(me.uid).first('n');
    if (count >= MAX_BIRDS) return fail(409, 'too_many_birds');
    const id = newId();
    let name = clean(body.name, 24) || 'İsimsiz kuş';
    const filtered = isBadName(name);
    if (filtered) name = 'İsimsiz kuş';
    // Pre-review of new artists is optional (admin setting 'review'); without it birds go live at once
    // and the community's reports plus the nightly Telegram digest are the safety net.
    const review = (await setting(env, 'review')) === '1';
    const trusted = review && await env.DB.prepare('SELECT trusted FROM users WHERE uid = ?').bind(me.uid).first('trusted');
    const status = !review || trusted ? 'live' : 'pending';
    await env.DB.batch([
      env.DB.prepare('INSERT INTO birds (id, uid, name, img, created, status) VALUES (?, ?, ?, ?, ?, ?)').bind(id, me.uid, name, data, Date.now(), status),
      env.DB.prepare('UPDATE users SET ip_hash = ? WHERE uid = ?').bind(await ipKey(req, env), me.uid),
    ]);
    if (status === 'pending') ctx.waitUntil(notifyBird(env, url.origin, { id, name, author: me.name, sig: await imgSig(env, id) }, 'pending'));
    return json({ id, pending: status === 'pending', filtered });
  }

  const del = /^\/birds\/([a-z0-9]{16})$/.exec(path);
  if (method === 'DELETE' && del) {
    const row = await env.DB.prepare('SELECT uid FROM birds WHERE id = ?').bind(del[1]).first();
    if (!row) return fail(404, 'not_found');
    if (row.uid !== me.uid && !admin) return fail(403, 'not_yours');
    await deleteBird(env, del[1], req.url);
    return json({ ok: true });
  }

  if (method === 'POST' && path === '/vote') {
    const bird = String(body.bird || ''), v = Number(body.v);
    if (!ID.test(bird) || ![-1, 0, 1].includes(v)) return fail(400, 'bad_vote');
    if (v === 0) await env.DB.prepare('DELETE FROM votes WHERE uid = ? AND bird_id = ?').bind(me.uid, bird).run();
    else await env.DB.prepare("INSERT INTO votes (uid, bird_id, v) SELECT ?, ?, ? WHERE EXISTS (SELECT 1 FROM birds WHERE id = ? AND status = 'live') ON CONFLICT(uid, bird_id) DO UPDATE SET v = excluded.v")
      .bind(me.uid, bird, v, bird).run();
    return json({ ok: true });
  }

  if (method === 'POST' && path === '/flag') {
    const bird = String(body.bird || '');
    if (!ID.test(bird)) return fail(400, 'bad_flag');
    if (body.on) {
      const added = await env.DB.prepare("INSERT OR IGNORE INTO flags (uid, bird_id) SELECT ?, ? WHERE EXISTS (SELECT 1 FROM birds WHERE id = ? AND uid != ? AND status = 'live')")
        .bind(me.uid, bird, bird, me.uid).run();
      if (added.meta.changes) {
        const b = await birdInfo(env, bird);
        const limit = b && Date.now() - b.created < 864e5 ? HIDE_FLAGS_NEW : HIDE_FLAGS;
        if (b && b.flags === limit) ctx.waitUntil(notifyBird(env, url.origin, b, 'flagged'));
      }
    } else await env.DB.prepare('DELETE FROM flags WHERE uid = ? AND bird_id = ?').bind(me.uid, bird).run();
    return json({ ok: true });
  }

  if (method === 'POST' && path === '/flocks') {
    const name = clean(body.name, 24);
    if (!name) return fail(400, 'no_name');
    if (isBadName(name)) return fail(400, 'bad_name');
    const n = await env.DB.prepare('SELECT COUNT(*) AS n FROM flocks WHERE uid = ?').bind(me.uid).first('n');
    if (n >= MAX_FLOCKS) return fail(409, 'too_many_flocks');
    const id = newId();
    await env.DB.prepare('INSERT INTO flocks (id, uid, name, birds, created, public) VALUES (?, ?, ?, ?, ?, ?)')
      .bind(id, me.uid, name, '[]', Date.now(), body.public === false ? 0 : 1).run();
    return json({ id });
  }
  const fl = /^\/flocks\/([a-z0-9]{16})(\/toggle)?$/.exec(path);
  if (fl) {
    const row = await env.DB.prepare('SELECT uid, birds FROM flocks WHERE id = ?').bind(fl[1]).first();
    if (!row) return fail(404, 'not_found');
    if (row.uid !== me.uid) return fail(403, 'not_yours');
    if (method === 'DELETE' && !fl[2]) {
      await env.DB.prepare('DELETE FROM flocks WHERE id = ?').bind(fl[1]).run();
      return json({ ok: true });
    }
    if (method === 'POST' && fl[2]) {
      const bird = String(body.bird || '');
      if (!ID.test(bird)) return fail(400, 'bad_bird');
      const list = JSON.parse(row.birds);
      const had = list.includes(bird);
      const next = had ? list.filter(b => b !== bird) : [...list, bird].slice(-100);
      await env.DB.prepare('UPDATE flocks SET birds = ? WHERE id = ?').bind(JSON.stringify(next), fl[1]).run();
      return json({ ok: true, added: !had });
    }
    if (method === 'POST') {
      let name = body.name == null ? null : clean(body.name, 24);
      if (name && isBadName(name)) return fail(400, 'bad_name');
      await env.DB.prepare('UPDATE flocks SET name = COALESCE(?, name), public = COALESCE(?, public) WHERE id = ?')
        .bind(name || null, typeof body.public === 'boolean' ? (body.public ? 1 : 0) : null, fl[1]).run();
      return json({ ok: true });
    }
  }
  return fail(404, 'not_found');
}

// Edge-cache a generated page for `ttl` seconds.
async function cached(req, build, ttl) {
  const cache = caches.default;
  const u = new URL(req.url); u.search = '';
  const key = new Request(u.toString());
  const hit = await cache.match(key);
  if (hit) return hit;
  const res = await build();
  res.headers.set('cache-control', `public, max-age=${ttl}`);
  await cache.put(key, res.clone());
  return res;
}

// ---- server-rendered week pages in every language: /haftanin-kuslari, /hafta/, /hafta/2026-W45 (others under /<lang>/) ----
const pre = lang => (lang === 'tr' ? '' : `/${lang}`);
const fill = (s, v) => String(s).replace(/\{(\w+)\}/g, (m, k) => (k in v ? v[k] : m));
const fmtDate = (U, ts) => { const d = new Date(ts); return fill(U.date_format, { d: d.getUTCDate(), month: U.months[d.getUTCMonth()], y: d.getUTCFullYear() }); };
// ISO 8601 week of a timestamp (UTC), and the Monday 00:00 UTC that starts a given ISO week.
function isoWeek(ts) {
  const d = new Date(ts); d.setUTCHours(0, 0, 0, 0);
  d.setUTCDate(d.getUTCDate() + 3 - ((d.getUTCDay() + 6) % 7));
  const y = d.getUTCFullYear(), jan4 = Date.UTC(y, 0, 4);
  return { year: y, week: 1 + Math.round(((d - jan4) / 864e5 - 3 + ((new Date(jan4).getUTCDay() + 6) % 7)) / 7) };
}
function weekStart(year, week) {
  const jan4 = new Date(Date.UTC(year, 0, 4));
  return jan4.getTime() - ((jan4.getUTCDay() + 6) % 7) * 864e5 + (week - 1) * 7 * 864e5;
}
const weekKey = ({ year, week }) => `${year}-W${String(week).padStart(2, '0')}`;
// Weekly drawing theme: WEEK_UI[lang].themes rotate one per ISO week, starting with 2026-W45. Same order as the themes.
const THEME_LESSONS = [['leylek', 'kirlangic'], ['guvercin', 'karga', 'serce'], ['baykus'], ['ordek', 'flamingo', 'marti'],
  ['papagan', 'tavuskusu', 'kolibri'], ['kartal', 'baykus'], ['agackakan', 'ibibik'], ['penguen']];
const THEME_EPOCH = weekStart(2026, 45);
const themeIndex = ts => { const n = THEME_LESSONS.length, k = Math.floor((ts - THEME_EPOCH) / (7 * 864e5)); return ((k % n) + n) % n; };
function themeBlock(U, lang) {
  const i = themeIndex(Date.now()), [title, text] = U.themes[i];
  const links = THEME_LESSONS[i].filter(s => U.lessons[s]).map(s => `<a href="${pre(lang)}/dersler/${s}">${esc(U.lessons[s])}</a>`).join(' · ');
  return `<div class="theme"><h2>${esc(fill(U.theme_head, { title }))}</h2><p>${esc(text)}</p>${links ? `<p>${esc(U.theme_lessons)} ${links}</p>` : ''}</div>`;
}
const NATIVE = { tr: 'Türkçe', en: 'English', es: 'Español', pt: 'Português', fr: 'Français', de: 'Deutsch', ru: 'Русский', ar: 'العربية', zh: '中文', ja: '日本語', id: 'Bahasa Indonesia' };

function shell({ lang, path, title, desc, image, body, origin }) {
  const U = WEEK_UI[lang], p = pre(lang);
  const nav = [[lang === 'tr' ? '/#ciz' : `/?lang=${lang}#ciz`, U.nav_draw], [`${p}/dersler/`, U.nav_lessons], [`${p}/kuslar/`, U.nav_birds],
    [`${p}/haftanin-kuslari`, U.nav_week, true], [`${p}/blog/`, U.nav_blog], [`${p}/sss`, U.nav_faq]]
    .map(([h, l, on]) => `<a${on ? ' class="on"' : ''} href="${h}">${esc(l)}</a>`).join('');
  const langs = LANGS.map(l => `<a href="${pre(l)}${path}" hreflang="${l}" lang="${l}"${l === lang ? ' aria-current="page"' : ''}>${NATIVE[l]}</a>`).join('');
  const alt = LANGS.map(l => `<link rel="alternate" hreflang="${l}" href="${origin}${pre(l)}${path}">`).join('\n');
  return new Response(`<!doctype html>
<html lang="${lang}" dir="${lang === 'ar' ? 'rtl' : 'ltr'}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>${esc(title)} · DrawBird</title>
<meta name="description" content="${esc(desc)}">
<meta property="og:title" content="${esc(title)} · DrawBird">
<meta property="og:description" content="${esc(desc)}">
<meta property="og:image" content="${image || `${origin}/og-card.png`}">
<link rel="canonical" href="${origin}${p}${path}">
<meta property="og:url" content="${origin}${p}${path}">
${alt}
<link rel="alternate" hreflang="x-default" href="${origin}${path}">
<link rel="icon" href="/icons/icon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="apple-touch-icon" href="/icons/apple-touch-icon.png">
<link rel="stylesheet" href="/fonts/fonts.css">
<link rel="stylesheet" href="/sayfa.css">
<style>.weeks { display: grid; gap: 8px; padding: 0; list-style: none; } .weeks a { display: flex; justify-content: space-between; gap: 10px; background: var(--chip); border-radius: 12px; padding: 10px 14px; text-decoration: none; } .pager { display: flex; justify-content: space-between; gap: 10px; flex-wrap: wrap; margin-top: 16px; } .langs { margin-top: 8px; display: flex; flex-wrap: wrap; justify-content: center; gap: 4px 10px; } .langs a[aria-current] { font-weight: 700; text-decoration: none; } .theme { background: var(--chip); border-radius: 14px; padding: 4px 16px; margin: 12px 0; }</style>
</head>
<body>
<main>
<nav class="top"><a class="brand" href="${lang === 'tr' ? '/' : `/?lang=${lang}`}" aria-label="DrawBird"><picture><source srcset="/logo/sembol-koyu.svg" media="(prefers-color-scheme: dark)"><img src="/logo/sembol.svg" alt="" width="40" height="40"></picture><picture><source srcset="/logo/yazi-koyu.svg" media="(prefers-color-scheme: dark)"><img src="/logo/yazi-acik.svg" alt="" width="99" height="30"></picture></a>${nav}</nav>
<article>
${body}
</article>
<footer>DrawBird · <a href="${p}/hakkinda">${esc(U.foot_about)}</a> · <a href="${p}/ogretmenler">${esc(U.foot_teachers)}</a> · <a href="${p}/kosullar">${esc(U.foot_terms)}</a> · <a href="${p}/gizlilik">${esc(U.foot_privacy)}</a> · <a href="${p}/kvkk">${esc(U.foot_kvkk)}</a> · <a href="${lang === 'tr' ? '/#iletisim' : `/?lang=${lang}#iletisim`}">${esc(U.foot_contact)}</a> · <a href="https://github.com/gunayboss/drawbird">${esc(U.foot_source)}</a><div class="langs">${langs}</div></footer>
</main>
</body>
</html>`, { headers: { 'content-type': 'text/html; charset=utf-8' } });
}

async function birdsBetween(env, from, to, limit = 24) {
  const { results } = await env.DB.prepare(`SELECT b.id, b.uid, b.name, b.created, u.name AS author,
      COALESCE(SUM(v.v), 0) AS score, COALESCE(SUM(v.v = 1), 0) AS up
    FROM birds b LEFT JOIN votes v ON v.bird_id = b.id LEFT JOIN users u ON u.uid = b.uid
    WHERE b.created >= ? AND b.created < ? AND b.status = 'live' AND b.uid NOT IN (SELECT uid FROM bans)
      AND NOT ${hiddenSql('b')}
    GROUP BY b.id ORDER BY score DESC, b.created DESC LIMIT ?`).bind(from, to, limit).all();
  return results;
}
async function weekStats(env, from, to) {
  return env.DB.prepare(`SELECT COUNT(*) AS birds, COUNT(DISTINCT uid) AS artists FROM birds
    WHERE created >= ? AND created < ? AND status = 'live' AND uid NOT IN (SELECT uid FROM bans)`).bind(from, to).first();
}
const birdCards = (U, birds) => `<div class="grid">${birds.map((b, i) => `
    <a class="bird" href="/k/${b.id}">
      <div class="art"><img src="/api/img/${b.id}" alt="${esc(b.name)}" loading="lazy" width="140" height="88"></div>
      <b>${esc(b.name)}</b>
      <span>${esc(fill(U.card_line, { rank: i + 1, author: b.author || U.an_artist, up: b.up }))}</span>
    </a>`).join('')}</div>`;

async function weeklyPage(env, url, lang) {
  const U = WEEK_UI[lang], now = Date.now(), from = now - 7 * 864e5;
  let birds = await birdsBetween(env, from, now + 1);
  const st = await weekStats(env, from, now + 1);
  const allTime = birds.length < 6;
  if (allTime) birds = await birdsBetween(env, 0, now + 1);
  const intro = allTime ? U.week_alltime : fill(U.week_intro, { from: fmtDate(U, from), birds: st.birds, artists: st.artists });
  return shell({
    lang, origin: url.origin, path: '/haftanin-kuslari', title: U.week_title, desc: U.week_desc,
    image: birds[0] && `${url.origin}/api/img/${birds[0].id}`,
    body: `  <h1>${esc(U.week_title)}</h1>
  ${themeBlock(U, lang)}
  <p>${esc(intro)} ${esc(U.week_tap)}</p>
  ${birds.length ? birdCards(U, birds) : `<p class="muted">${esc(U.week_empty)}</p>`}
  <p><a class="cta" href="${lang === 'tr' ? '/#ciz' : `/?lang=${lang}#ciz`}">${esc(U.week_cta)}</a></p>
  <p class="muted">${fill(U.week_note, { archive: `${pre(lang)}/hafta/` })}</p>`,
  });
}

async function weekArchive(env, url, lang) {
  const U = WEEK_UI[lang];
  const { results } = await env.DB.prepare(`SELECT created FROM birds WHERE status = 'live' AND uid NOT IN (SELECT uid FROM bans)`).all();
  const counts = new Map();
  for (const r of results) { const k = weekKey(isoWeek(r.created)); counts.set(k, (counts.get(k) || 0) + 1); }
  const rows = [...counts.entries()].sort((a, b) => b[0].localeCompare(a[0])).map(([k, n]) => {
    const [y, w] = k.split('-W').map(Number), s = weekStart(y, w);
    return `<li><a href="${pre(lang)}/hafta/${k}"><span><b>${esc(fill(U.archive_row, { y, w }))}</b> · ${esc(fmtDate(U, s))} – ${esc(fmtDate(U, s + 6 * 864e5))}</span><span>${esc(fill(U.archive_count, { n }))}</span></a></li>`;
  }).join('');
  return shell({
    lang, origin: url.origin, path: '/hafta/', title: U.archive_title, desc: U.archive_desc,
    body: `  <h1>${esc(U.archive_title)}</h1>
  <p>${esc(U.archive_intro)}</p>
  ${rows ? `<ul class="weeks">${rows}</ul>` : `<p class="muted">${esc(U.archive_empty)}</p>`}`,
  });
}

async function weekPage(env, url, lang, year, week) {
  if (week < 1 || week > 53 || year < 2026 || year > 2100) return null;
  const U = WEEK_UI[lang], from = weekStart(year, week), to = from + 7 * 864e5;
  if (from > Date.now()) return null;
  const [birds, st] = await Promise.all([birdsBetween(env, from, to), weekStats(env, from, to)]);
  const prev = weekKey(isoWeek(from - 864e5)), next = weekKey(isoWeek(to + 864e5)), best = birds[0];
  const range = { from: fmtDate(U, from), to: fmtDate(U, to - 864e5) };
  const summary = st.birds
    ? fill(U.weekpage_summary, { ...range, birds: st.birds, artists: st.artists }) + (best ? ' ' + fill(U.weekpage_best, { name: best.name, author: best.author || U.an_artist, up: best.up }) : '')
    : fill(U.weekpage_none, range);
  const p = pre(lang), key = weekKey({ year, week });
  return shell({
    lang, origin: url.origin, path: `/hafta/${key}`, title: fill(U.weekpage_title, { y: year, w: week }),
    desc: fill(U.weekpage_desc, { y: year, w: week, birds: st.birds, artists: st.artists }),
    image: best && `${url.origin}/api/img/${best.id}`,
    body: `  <h1>${esc(fill(U.weekpage_title, { y: year, w: week }))}</h1>
  <p>${esc(summary)}</p>
  ${birds.length ? birdCards(U, birds) : ''}
  <div class="pager"><a href="${p}/hafta/${prev}">${esc(U.prev_week)}</a><a href="${p}/hafta/">${esc(U.archive_link)}</a>${to < Date.now() ? `<a href="${p}/hafta/${next}">${esc(U.next_week)}</a>` : ''}</div>
  <p><a class="cta" href="${lang === 'tr' ? '/#ciz' : `/?lang=${lang}#ciz`}">${esc(U.week_cta)}</a></p>`,
  });
}

async function sitemap(env, url) {
  const { results } = await env.DB.prepare(`SELECT id, created FROM birds WHERE status = 'live' AND uid NOT IN (SELECT uid FROM bans)
    AND NOT ${hiddenSql('birds')} ORDER BY created DESC LIMIT 1000`).all();
  const day = ts => new Date(ts).toISOString().slice(0, 10);
  const today = day(Date.now());
  const weeks = [...new Set(results.map(b => weekKey(isoWeek(b.created))))];
  const pages = [
    ...STATIC_PAGES.map(([p, d]) => [p, d === 'today' ? today : d]),
    ...LANGS.flatMap(l => weeks.map(w => [`${pre(l)}/hafta/${w}`])),
    ...results.map(b => [`/k/${b.id}`, day(b.created)]),
  ];
  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${pages.map(([p, d]) => `  <url><loc>${url.origin}${p}</loc>${d ? `<lastmod>${d}</lastmod>` : ''}</url>`).join('\n')}
</urlset>`;
  return new Response(xml, { headers: { 'content-type': 'application/xml; charset=utf-8' } });
}

// Pick the visitor's language for pages that have no language in their address (share previews).
function acceptLang(req) {
  for (const part of (req.headers.get('accept-language') || '').split(',')) {
    const l = part.trim().slice(0, 2).toLowerCase();
    if (LANGS.includes(l)) return l;
  }
  return 'tr';
}

// Share links (/k/<bird>) get their own preview card for chat apps and social sites.
const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
async function sharePage(req, env, url, birdId) {
  const page = await env.ASSETS.fetch(new Request(new URL('/', url)));
  const bird = await env.DB.prepare("SELECT b.name, u.name AS author FROM birds b LEFT JOIN users u ON u.uid = b.uid WHERE b.id = ? AND b.status = 'live'").bind(birdId).first();
  if (!bird) return page;
  const title = `${bird.name} · DrawBird`;
  const U = WEEK_UI[acceptLang(req)];
  const desc = fill(U.share_desc, { author: bird.author || U.an_artist });
  const image = new URL('/api/img/' + birdId, url).toString();
  return new HTMLRewriter()
    .on('title', { element(e) { e.setInnerContent(title); } })
    .on('meta[property="og:title"]', { element(e) { e.setAttribute('content', title); } })
    .on('meta[property="og:description"]', { element(e) { e.setAttribute('content', desc); } })
    .on('meta[property="og:image"]', { element(e) { e.setAttribute('content', image); } })
    .on('meta[property="og:url"]', { element(e) { e.setAttribute('content', url.toString()); } })
    .on('meta[name="twitter:card"]', { element(e) { e.setAttribute('content', 'summary'); } })
    .on('head', { element(e) { e.append(`<meta name="drawbird:share" content="${esc(birdId)}">`, { html: true }); } })
    .transform(page);
}

// Mail sent to kvkk@drawbird.app (Cloudflare Email Routing -> this Worker) lands in the same inbox as "Bize yaz":
// stored in messages and forwarded to the owner's Telegram. Nothing is sent back; the owner replies from their own address.
async function receiveEmail(message, env) {
  if (message.rawSize > 512 * 1024) { message.setReject('Message too large'); return; }
  // At most 30 mails an hour in total, so a flood cannot fill the table or the Telegram chat.
  if (await overLimit(env, { headers: new Headers({ 'cf-connecting-ip': 'email' }) }, 'email', 30, 3600)) { message.setReject('Try again later'); return; }
  const mail = await PostalMime.parse(message.raw);
  const from = clean(mail.from?.address || message.from, 120);
  const subject = clean(mail.subject, 200);
  const text = String(mail.text || (mail.html || '').replace(/<[^>]*>/g, ' ') || '')
    .replace(/[\u0000-\u0008\u000b-\u001f\u007f\u200b-\u200f\u202a-\u202e\u2060-\u206f\ufeff]/g, '').replace(/\n{3,}/g, '\n\n').trim();
  const body = `${subject ? `Konu: ${subject}\n\n` : ''}${text}`.slice(0, 4000) || '(boş e-posta)';
  const topic = String(message.to).toLowerCase().startsWith('kvkk@') ? 'kvkk' : 'other';
  await env.DB.prepare('INSERT INTO messages (id, uid, topic, body, contact, created) VALUES (?, ?, ?, ?, ?, ?)')
    .bind(newId(), null, topic, body, from, Date.now()).run();
  await notifyText(env, `📧 ${message.to} adresine e-posta\nKimden: ${from}\n${body.slice(0, 900)}`);
}

export default {
  async email(message, env) {
    await receiveEmail(message, env);
  },
  async scheduled(event, env) {
    const now = Date.now();
    await env.DB.batch([
      env.DB.prepare('DELETE FROM messages WHERE created < ?').bind(now - 365 * 864e5),
      env.DB.prepare('DELETE FROM limits WHERE exp < ?').bind(now),
      env.DB.prepare('DELETE FROM new_ids WHERE day < ?').bind(new Date(now - 2 * 864e5).toISOString().slice(0, 10)),
      env.DB.prepare('DELETE FROM ip_bans WHERE exp < ?').bind(now),
    ]);
    const { results } = await env.DB.prepare(`SELECT b.id, b.name, u.name AS author FROM birds b LEFT JOIN users u ON u.uid = b.uid
      WHERE b.created >= ? AND b.status = 'live' AND b.uid NOT IN (SELECT uid FROM bans) ORDER BY b.created`).bind(now - 864e5).all();
    await sendDigest(env, results);
  },
  async fetch(req, env, ctx) {
    const url = new URL(req.url);
    // The site lives on drawbird.app. Pages asked for on the old workers.dev address or on www move there for good;
    // the API stays answering everywhere so already-open tabs keep working.
    if ((url.hostname === 'www.drawbird.app' || url.hostname.endsWith('.workers.dev')) && !url.pathname.startsWith('/api/')) {
      return Response.redirect(`https://drawbird.app${url.pathname}${url.search}`, 301);
    }
    if (url.pathname.startsWith('/api/')) {
      let res;
      try { res = await handleApi(req, env, url, ctx); }
      catch (e) {
        if (e?.status) res = fail(e.status, e.error);
        else {
          console.error(e);
          res = fail(500, 'server_error');
          ctx.waitUntil(overLimit(env, req, 'err-alert', 1, 600).then(over => over ? null : notifyText(env, `❗ Sunucu hatası: ${url.pathname} — ${String(e?.message || e).slice(0, 200)}`)).catch(() => {}));
        }
      }
      if (req.method !== 'GET' && res.ok && url.pathname !== '/api/hit') await caches.default.delete(publicKey(url));
      return secure(res);
    }
    if (/^\/[us]\/[a-z0-9]{16}$/.test(url.pathname)) return secure(await env.ASSETS.fetch(new Request(new URL('/', url), req)));
    const langRoot = /^\/([a-z]{2})\/?$/.exec(url.pathname);
    if (langRoot && LANGS.includes(langRoot[1]) && langRoot[1] !== 'tr') return Response.redirect(`${url.origin}/?lang=${langRoot[1]}`, 302);
    const share = /^\/k\/([a-z0-9]{16})$/.exec(url.pathname);
    if (share && req.method === 'GET') return secure(await sharePage(req, env, url, share[1]));
    // Week pages, with an optional language prefix: /haftanin-kuslari, /en/hafta/, /de/hafta/2026-W45
    const lm = /^(?:\/([a-z]{2}))?(\/haftanin-kuslari|\/hafta\/?|\/hafta\/(\d{4})-W(\d{2}))$/.exec(url.pathname);
    const wlang = lm && (lm[1] || 'tr');
    if (lm && LANGS.includes(wlang) && wlang !== (lm[1] ? 'tr' : '')) {
      if (lm[2] === '/haftanin-kuslari') return secure(await cached(req, () => weeklyPage(env, url, wlang), 300));
      if (!lm[3]) return secure(await cached(req, () => weekArchive(env, url, wlang), 3600));
      const res = await cached(req, async () => (await weekPage(env, url, wlang, +lm[3], +lm[4]))
        || new Response(WEEK_UI[wlang].week_not_found, { status: 404, headers: { 'content-type': 'text/plain; charset=utf-8' } }), 1800);
      return secure(res);
    }
    // English pages that moved when every language got the same pages.
    const moved = { '/en/how-to-play': '/en/nasil-oynanir', '/en/terms': '/en/kosullar', '/en/privacy': '/en/gizlilik' }[url.pathname.replace(/\.html$/, '')];
    if (moved) return Response.redirect(url.origin + moved, 301);
    // Google Search Console ownership file. Served here because static .html files are redirected to clean URLs.
    if (url.pathname === '/google83710215f7857799.html') {
      return secure(new Response('google-site-verification: google83710215f7857799.html', { headers: { 'content-type': 'text/html; charset=utf-8' } }));
    }
    if (url.pathname === '/sitemap.xml') return secure(await cached(req, () => sitemap(env, url), 3600));
    if (url.pathname === '/robots.txt') {
      return secure(new Response(`User-agent: *\nAllow: /\nDisallow: /api/\nSitemap: ${url.origin}/sitemap.xml\n`, { headers: { 'content-type': 'text/plain; charset=utf-8' } }));
    }
    return secure(await env.ASSETS.fetch(req));
  },
};
