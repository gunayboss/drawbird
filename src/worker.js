// DrawBird API: anonymous device tokens, birds, votes, flags, flocks, moderation on D1.
const MAX_BIRDS = 8;
const MAX_FLOCKS = 12;
const MAX_IMG = 90_000; // data URL characters (~65 KB image)
const HIDE_FLAGS = 3;
const PUBLIC_TTL = 10; // seconds the shared part of /api/state is cached at the edge
const NEW_IDS_PER_IP_DAY = 40; // classrooms share one IP, so keep this generous

// Hardening headers for everything the Worker answers.
const CSP = [
  "default-src 'self'", "script-src 'self' 'unsafe-inline'", "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
  "font-src https://fonts.gstatic.com", "img-src 'self' data: blob:", "connect-src 'self'", "manifest-src 'self'",
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
    // Cap how many new identities one IP can mint per day (vote and flag stuffing). Only a salted hash of the IP is kept, for two days.
    const day = new Date().toISOString().slice(0, 10);
    const ipHash = (await sha256(`${clientIp(req)}|${day}|${env.ADMIN_KEY || ''}`)).slice(0, 32);
    const n = await env.DB.prepare('INSERT INTO new_ids (day, ip_hash, n) VALUES (?, ?, 1) ON CONFLICT(day, ip_hash) DO UPDATE SET n = n + 1 RETURNING n')
      .bind(day, ipHash).first('n');
    if (Math.random() < .02) await env.DB.prepare('DELETE FROM new_ids WHERE day < ?').bind(new Date(Date.now() - 864e5).toISOString().slice(0, 10)).run();
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
      WHERE b.uid NOT IN (SELECT uid FROM bans)
      GROUP BY b.id ORDER BY b.created DESC LIMIT 2000`),
    env.DB.prepare('SELECT uid, name FROM users WHERE uid IN (SELECT DISTINCT uid FROM birds UNION SELECT DISTINCT uid FROM flocks)'),
    env.DB.prepare('SELECT id, uid, name, birds, created, public FROM flocks WHERE public = 1 AND uid NOT IN (SELECT uid FROM bans) ORDER BY created'),
  ]);
  const data = {
    birds: birds.results,
    names: Object.fromEntries(users.results.map(u => [u.uid, u.name])),
    flocks: flocks.results.map(f => ({ ...f, public: true, birds: JSON.parse(f.birds) })),
  };
  await cache.put(key, new Response(JSON.stringify(data), { headers: { 'content-type': 'application/json', 'cache-control': `public, max-age=${PUBLIC_TTL}` } }));
  return data;
}

async function state(req, env, url) {
  const me = await auth(req, env, false);
  const pub = await publicState(env, url);
  const mine = { v: {}, f: {} };
  let flocks = pub.flocks;
  if (me) {
    const [mv, mf, priv] = await env.DB.batch([
      env.DB.prepare('SELECT bird_id, v FROM votes WHERE uid = ?').bind(me.uid),
      env.DB.prepare('SELECT bird_id FROM flags WHERE uid = ?').bind(me.uid),
      env.DB.prepare('SELECT id, uid, name, birds, created, public FROM flocks WHERE uid = ? AND public = 0').bind(me.uid),
    ]);
    mv.results.forEach(r => { mine.v[r.bird_id] = r.v; });
    mf.results.forEach(r => { mine.f[r.bird_id] = true; });
    flocks = [...flocks, ...priv.results.map(f => ({ ...f, public: false, birds: JSON.parse(f.birds) }))];
  }
  return json({
    me: me ? { uid: me.uid, name: me.name, banned: !!(await isBanned(env, me.uid)) } : null,
    admin: await isAdmin(req, env),
    hideFlags: HIDE_FLAGS, maxBirds: MAX_BIRDS,
    birds: pub.birds, names: pub.names, flocks, mine,
  });
}

async function image(req, id, env) {
  const cache = caches.default;
  const key = new Request(new URL(req.url).origin + '/api/img/' + id);
  const hit = await cache.match(key);
  if (hit) return hit;
  const row = await env.DB.prepare('SELECT img FROM birds WHERE id = ?').bind(id).first();
  if (!row) return new Response('not found', { status: 404 });
  const m = /^data:(image\/(?:png|webp));base64,([A-Za-z0-9+/=]+)$/.exec(row.img);
  if (!m) return new Response('bad image', { status: 500 });
  const bytes = Uint8Array.from(atob(m[2]), c => c.charCodeAt(0));
  const res = new Response(bytes, { headers: {
    'content-type': m[1], 'cache-control': 'public, max-age=31536000, immutable',
    'content-security-policy': "default-src 'none'; sandbox", 'content-disposition': 'inline',
  } });
  await cache.put(key, res.clone());
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

async function adminApi(req, env, path, method, body) {
  if (await limited(env.RL_ADMIN, 'admin:' + clientIp(req))) return fail(429, 'slow_down');
  if (!(await isAdmin(req, env))) return fail(403, 'not_admin');
  if (method === 'GET' && path === '/admin/reports') {
    const [reported, bans] = await env.DB.batch([
      env.DB.prepare(`SELECT b.id, b.uid, b.name, b.created, COUNT(f.uid) AS flags,
          (SELECT name FROM users u WHERE u.uid = b.uid) AS author
        FROM birds b JOIN flags f ON f.bird_id = b.id GROUP BY b.id ORDER BY flags DESC, b.created DESC LIMIT 200`),
      env.DB.prepare('SELECT bans.uid, bans.created, users.name FROM bans LEFT JOIN users ON users.uid = bans.uid ORDER BY bans.created DESC'),
    ]);
    const stats = await env.DB.prepare('SELECT (SELECT COUNT(*) FROM birds) AS birds, (SELECT COUNT(*) FROM users) AS users, (SELECT COUNT(*) FROM votes) AS votes').first();
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
    if (body.on) await env.DB.prepare('INSERT OR IGNORE INTO bans (uid, created) VALUES (?, ?)').bind(uid, Date.now()).run();
    else await env.DB.prepare('DELETE FROM bans WHERE uid = ?').bind(uid).run();
    return json({ ok: true });
  }
  return fail(404, 'not_found');
}

async function handleApi(req, env, url) {
  const path = url.pathname.slice(4); // strip "/api"
  const method = req.method;

  if (method === 'GET' && path === '/state') return state(req, env, url);
  if (method !== 'GET' && !path.startsWith('/admin/') && await limited(env.RL_WRITE, 'w:' + clientIp(req))) return fail(429, 'slow_down');
  if (method === 'POST' && path === '/hit') {
    // One count per browser session; nothing about the visitor is stored.
    await env.DB.prepare('INSERT INTO visits (day, n) VALUES (?, 1) ON CONFLICT(day) DO UPDATE SET n = n + 1')
      .bind(new Date().toISOString().slice(0, 10)).run();
    return json({ ok: true });
  }
  const img = /^\/img\/([a-z0-9]{16})$/.exec(path);
  if (method === 'GET' && img) return image(req, img[1], env);

  let body = {};
  if (method === 'POST') { try { body = await readBody(req); } catch { return fail(413, 'too_large'); } }
  if (path.startsWith('/admin/')) return adminApi(req, env, path, method, body);
  if (method === 'GET') return fail(404, 'not_found');

  const me = await auth(req, env, true);
  if (!me) return fail(401, 'no_token');
  const admin = await isAdmin(req, env);

  if (method === 'POST' && path === '/me') {
    await env.DB.prepare('UPDATE users SET name = ? WHERE uid = ?').bind(clean(body.name, 24), me.uid).run();
    return json({ ok: true });
  }

  if (method === 'POST' && path === '/birds') {
    if (await isBanned(env, me.uid)) return fail(403, 'banned');
    if (await limited(env.RL_BIRD, 'b:' + clientIp(req))) return fail(429, 'slow_down');
    const data = String(body.img || '');
    if (!/^data:image\/(png|webp);base64,[A-Za-z0-9+/=]+$/.test(data) || data.length > MAX_IMG || !looksLikeImage(data)) return fail(400, 'bad_image');
    const count = await env.DB.prepare('SELECT COUNT(*) AS n FROM birds WHERE uid = ?').bind(me.uid).first('n');
    if (count >= MAX_BIRDS) return fail(409, 'too_many_birds');
    const id = newId();
    await env.DB.prepare('INSERT INTO birds (id, uid, name, img, created) VALUES (?, ?, ?, ?, ?)')
      .bind(id, me.uid, clean(body.name, 24) || 'İsimsiz kuş', data, Date.now()).run();
    return json({ id });
  }

  const del = /^\/birds\/([a-z0-9]{16})$/.exec(path);
  if (method === 'DELETE' && del) {
    const row = await env.DB.prepare('SELECT uid FROM birds WHERE id = ?').bind(del[1]).first();
    if (!row) return fail(404, 'not_found');
    if (row.uid !== me.uid && !admin) return fail(403, 'not_yours');
    await env.DB.batch([
      env.DB.prepare('DELETE FROM birds WHERE id = ?').bind(del[1]),
      env.DB.prepare('DELETE FROM votes WHERE bird_id = ?').bind(del[1]),
      env.DB.prepare('DELETE FROM flags WHERE bird_id = ?').bind(del[1]),
    ]);
    return json({ ok: true });
  }

  if (method === 'POST' && path === '/vote') {
    const bird = String(body.bird || ''), v = Number(body.v);
    if (!ID.test(bird) || ![-1, 0, 1].includes(v)) return fail(400, 'bad_vote');
    if (v === 0) await env.DB.prepare('DELETE FROM votes WHERE uid = ? AND bird_id = ?').bind(me.uid, bird).run();
    else await env.DB.prepare('INSERT INTO votes (uid, bird_id, v) SELECT ?, ?, ? WHERE EXISTS (SELECT 1 FROM birds WHERE id = ?) ON CONFLICT(uid, bird_id) DO UPDATE SET v = excluded.v')
      .bind(me.uid, bird, v, bird).run();
    return json({ ok: true });
  }

  if (method === 'POST' && path === '/flag') {
    const bird = String(body.bird || '');
    if (!ID.test(bird)) return fail(400, 'bad_flag');
    if (body.on) await env.DB.prepare('INSERT OR IGNORE INTO flags (uid, bird_id) SELECT ?, ? WHERE EXISTS (SELECT 1 FROM birds WHERE id = ? AND uid != ?)')
      .bind(me.uid, bird, bird, me.uid).run();
    else await env.DB.prepare('DELETE FROM flags WHERE uid = ? AND bird_id = ?').bind(me.uid, bird).run();
    return json({ ok: true });
  }

  if (method === 'POST' && path === '/flocks') {
    const name = clean(body.name, 24);
    if (!name) return fail(400, 'no_name');
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
      const name = body.name == null ? null : clean(body.name, 24);
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

// Server-rendered "birds of the week": real text and images for visitors and search engines.
async function weeklyPage(env, url) {
  const weekAgo = Date.now() - 7 * 864e5;
  const query = cutoff => env.DB.prepare(`SELECT b.id, b.name, b.created, u.name AS author,
      COALESCE(SUM(v.v), 0) AS score, COALESCE(SUM(v.v = 1), 0) AS up
    FROM birds b LEFT JOIN votes v ON v.bird_id = b.id LEFT JOIN users u ON u.uid = b.uid
    WHERE b.created >= ? AND b.uid NOT IN (SELECT uid FROM bans)
      AND (SELECT COUNT(*) FROM flags f WHERE f.bird_id = b.id) < ${HIDE_FLAGS}
    GROUP BY b.id ORDER BY score DESC, b.created DESC LIMIT 24`).bind(cutoff).all();
  let { results: birds } = await query(weekAgo);
  const allTime = birds.length < 6;
  if (allTime) ({ results: birds } = await query(0));
  const fmt = ts => new Date(ts).toLocaleDateString('tr-TR', { day: 'numeric', month: 'long', year: 'numeric' });
  const cards = birds.map((b, i) => `
    <a class="bird" href="/k/${b.id}">
      <div class="art"><img src="/api/img/${b.id}" alt="${esc(b.name)}" loading="lazy" width="140" height="88"></div>
      <b>${esc(b.name)}</b>
      <span>#${i + 1} · ${esc(b.author || 'Bir kuşçu')} · ${b.up} beğeni</span>
    </a>`).join('');
  const intro = allTime
    ? 'Bu hafta henüz yeterince kuş uçmadı; şimdilik tüm zamanların en sevilen kuşları burada.'
    : `${fmt(weekAgo)} ile bugün arasında gökyüzüne katılan ve en çok beğeni alan kuşlar.`;
  const first = birds[0];
  const html = `<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Haftanın Kuşları · DrawBird</title>
<meta name="description" content="DrawBird'de bu hafta en çok beğenilen kuş çizimleri.">
<meta property="og:title" content="Haftanın kuşları · DrawBird">
<meta property="og:description" content="Bu hafta ortak gökyüzünde en çok beğenilen kuş çizimleri.">
<meta property="og:image" content="${first ? `${url.origin}/api/img/${first.id}` : `${url.origin}/og-card.png`}">
<link rel="icon" href="/icons/icon-192.png" type="image/png">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Caveat:wght@700&family=Rubik:wght@400;500;700&display=swap">
<link rel="stylesheet" href="/sayfa.css">
</head>
<body>
<main>
<nav class="top">
  <a href="/#ciz">Çiz</a><a href="/nasil-oynanir.html">Nasıl oynanır</a><a class="on" href="/haftanin-kuslari">Haftanın kuşları</a><a href="/kosullar.html">Koşullar</a><a href="/gizlilik.html">Gizlilik</a>
</nav>
<article>
  <h1>Haftanın kuşları</h1>
  <p>${intro} Bir kuşa dokunursan gökyüzünde onu bulur, oy verebilirsin.</p>
  ${birds.length ? `<div class="grid">${cards}</div>` : '<p class="muted">Gökyüzü henüz boş. İlk kuşu sen çiz!</p>'}
  <p><a class="cta" href="/#ciz">Sen de bir kuş çiz</a></p>
  <p class="muted">Liste beş dakikada bir yenilenir. Sıralama, kuşların aldığı ▲ ve ▼ oyların farkına göre yapılır.</p>
</article>
<footer>DrawBird · <a href="https://github.com/gunayboss/drawbird">Kaynak kod</a></footer>
</main>
</body>
</html>`;
  return new Response(html, { headers: { 'content-type': 'text/html; charset=utf-8' } });
}

async function sitemap(env, url) {
  const { results } = await env.DB.prepare(`SELECT id, created FROM birds WHERE uid NOT IN (SELECT uid FROM bans)
    AND (SELECT COUNT(*) FROM flags f WHERE f.bird_id = birds.id) < ${HIDE_FLAGS} ORDER BY created DESC LIMIT 1000`).all();
  const day = ts => new Date(ts).toISOString().slice(0, 10);
  const today = day(Date.now());
  const pages = [['/', today], ['/haftanin-kuslari', today], ['/nasil-oynanir.html'], ['/kosullar.html'], ['/gizlilik.html'],
    ...results.map(b => [`/k/${b.id}`, day(b.created)])];
  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${pages.map(([p, d]) => `  <url><loc>${url.origin}${p}</loc>${d ? `<lastmod>${d}</lastmod>` : ''}</url>`).join('\n')}
</urlset>`;
  return new Response(xml, { headers: { 'content-type': 'application/xml; charset=utf-8' } });
}

// Share links (/k/<bird>) get their own preview card for chat apps and social sites.
const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
async function sharePage(req, env, url, birdId) {
  const page = await env.ASSETS.fetch(new Request(new URL('/', url)));
  const bird = await env.DB.prepare('SELECT b.name, u.name AS author FROM birds b LEFT JOIN users u ON u.uid = b.uid WHERE b.id = ?').bind(birdId).first();
  if (!bird) return page;
  const title = `${bird.name} · DrawBird`;
  const desc = `${bird.author || 'Bir kuşçu'} bu kuşu çizdi. Sen de bir kuş çiz, ortak gökyüzünde uçsun.`;
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

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    if (url.pathname.startsWith('/api/')) {
      let res;
      try { res = await handleApi(req, env, url); }
      catch (e) {
        if (e?.status) res = fail(e.status, e.error);
        else { console.error(e); res = fail(500, 'server_error'); }
      }
      if (req.method !== 'GET' && res.ok && url.pathname !== '/api/hit') await caches.default.delete(publicKey(url));
      return secure(res);
    }
    const share = /^\/k\/([a-z0-9]{16})$/.exec(url.pathname);
    if (share && req.method === 'GET') return secure(await sharePage(req, env, url, share[1]));
    if (url.pathname === '/haftanin-kuslari') return secure(await cached(req, () => weeklyPage(env, url), 300));
    if (url.pathname === '/sitemap.xml') return secure(await cached(req, () => sitemap(env, url), 3600));
    if (url.pathname === '/robots.txt') {
      return secure(new Response(`User-agent: *\nAllow: /\nDisallow: /api/\nSitemap: ${url.origin}/sitemap.xml\n`, { headers: { 'content-type': 'text/plain; charset=utf-8' } }));
    }
    return secure(await env.ASSETS.fetch(req));
  },
};
