// DrawBird end-to-end smoke test (Node 20+, no dependencies).
// Run:  npx wrangler dev          (terminal 1, serves http://localhost:8787 with a local D1)
//       ADMIN_KEY=localtestkey node tests/smoke.mjs [baseUrl]   (terminal 2)
// ADMIN_KEY must match the dev server's ADMIN_KEY (default 'localtestkey').
// Only run this against a LOCAL server: it creates, bans and deletes data.
// Local rate-limit reset if you see 429s:
//   npx wrangler d1 execute drawbird --local --command "DELETE FROM new_ids; DELETE FROM limits; DELETE FROM ip_bans;"

const BASE = (process.argv[2] || 'http://localhost:8787').replace(/\/$/, '');
const ADMIN_KEY = process.env.ADMIN_KEY || 'localtestkey';
if (!/^https?:\/\/(localhost|127\.0\.0\.1|\[::1\])(:\d+)?$/.test(BASE)) {
  console.error('Refusing to run against a non-local URL: ' + BASE);
  process.exit(2);
}

const PNG = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==';
const FAKE = 'data:image/png;base64,' + Buffer.from('<html><script>alert(1)</script></html>').toString('base64');

let failed = 0;
const check = (name, ok, extra = '') => {
  if (!ok) failed++;
  console.log(`${ok ? '✓' : '✗'} ${name}${!ok && extra ? '  -> ' + extra : ''}`);
};

const newToken = () => {
  const a = new Uint8Array(24); crypto.getRandomValues(a);
  return Buffer.from(a).toString('base64url'); // 32 chars, [A-Za-z0-9_-]
};

// Tiny API helper: returns { status, body, headers }.
async function api(method, path, { token, admin, key, body } = {}) {
  const headers = {};
  if (token) headers.authorization = 'Bearer ' + token;
  if (admin) headers['x-admin-key'] = key ?? ADMIN_KEY;
  if (body !== undefined) headers['content-type'] = 'application/json';
  const res = await fetch(BASE + '/api' + path, { method, headers, body: body === undefined ? undefined : JSON.stringify(body) });
  let data = null;
  try { data = await res.json(); } catch { /* not JSON */ }
  return { status: res.status, body: data, headers: res.headers };
}
// The page reads the shared sky (/api/sky) and the viewer's own state (/api/state); merge them the same way.
const state = async token => {
  const [sky, st] = await Promise.all([api('GET', '/sky').then(r => r.body), api('GET', '/state', { token }).then(r => r.body)]);
  return { ...st, birds: [...(st.pending || []), ...sky.birds], flocks: [...sky.flocks, ...(st.flocks || [])], names: sky.names };
};
const admin = (method, path, body) => api(method, '/admin' + path, { admin: true, body });
const postBird = (token, name = 'Test kuşu', img = PNG) => api('POST', '/birds', { token, body: { name, img } });
const approve = id => admin('POST', '/review', { kind: 'ok', bird: id });

const tokens = [];
const mk = () => { const t = newToken(); tokens.push(t); return t; };
const created = []; // bird ids to delete at the end

async function pages() {
  const list = [
    ['/', 'tr'], ['/dersler/serce', 'tr'], ['/en/dersler/serce', 'en'], ['/ar/sss', 'ar'], ['/ja/kuslar/kumru', 'ja'],
    ['/haftanin-kuslari', 'tr'], ['/en/hafta/', 'en'], ['/sitemap.xml', null], ['/robots.txt', null],
  ];
  for (const [path, lang] of list) {
    const res = await fetch(BASE + path);
    const text = await res.text();
    const ok = res.status === 200 && (!lang || new RegExp(`<html[^>]*\\blang="${lang}"`).test(text));
    check(`GET ${path} 200${lang ? ` lang=${lang}` : ''}`, ok, `status ${res.status}`);
  }
  const h = (await fetch(BASE + '/')).headers;
  check('security headers on / (csp, x-frame-options)', !!h.get('content-security-policy') && !!h.get('x-frame-options'));
}

async function birdsFlow() {
  // Pre-review is off by default: a new artist's bird goes live at once.
  const quick = mk();
  const r0 = await postBird(quick, 'Hemen kus');
  if (r0.body?.id) created.push(r0.body.id);
  check('review off: new artist bird is live at once', r0.status === 200 && r0.body?.pending === false, JSON.stringify(r0.body));

  // The rest of the flow runs with pre-review on.
  const on = await api('POST', '/admin/review-mode', { admin: true, body: { on: true } });
  check('admin review-mode on -> 200', on.status === 200, `status ${on.status}`);
  const poster = mk();
  const r1 = await postBird(poster, 'Ilk kuş');
  check('POST /api/birds new token -> 200 pending', r1.status === 200 && r1.body?.pending === true, JSON.stringify(r1.body));
  const b1 = r1.body?.id; created.push(b1);

  const anon = await state();
  check('pending bird not in anonymous state', !anon.birds.some(b => b.id === b1));
  const mine = await state(poster);
  check('pending bird in poster state with pending flag', mine.birds.some(b => b.id === b1 && b.pending === true));

  const fake = await postBird(poster, 'Sahte', FAKE);
  check('fake image (html bytes as png) -> 400', fake.status === 400, `status ${fake.status}`);

  const bad = await postBird(poster, 's.i.k.t.i.r');
  if (bad.body?.id) created.push(bad.body.id);
  const badSeen = (await state(poster)).birds.find(b => b.id === bad.body?.id);
  check('bad name filtered and replaced', bad.body?.filtered === true && !!badSeen && badSeen.name !== 's.i.k.t.i.r', JSON.stringify(bad.body));

  const rev = await approve(b1);
  check('admin review ok -> 200', rev.status === 200, `status ${rev.status}`);
  check('approved bird visible in anonymous state', (await state()).birds.some(b => b.id === b1));

  const b2 = bad.body?.id;
  await approve(b2); // second approval makes the poster trusted
  const r3 = await postBird(poster, 'Uc kus');
  if (r3.body?.id) created.push(r3.body.id);
  check('third bird from trusted artist is not pending', r3.status === 200 && r3.body?.pending === false, JSON.stringify(r3.body));
  await api('POST', '/admin/review-mode', { admin: true, body: { on: false } });
  return { poster, bird: b1 };
}

async function socialFlow(bird) {
  const voter = mk();
  const v = await api('POST', '/vote', { token: voter, body: { bird, v: 1 } });
  let s = await state(voter);
  const row = s.birds.find(b => b.id === bird);
  check('vote up counted', v.status === 200 && s.mine.v[bird] === 1 && row?.up >= 1);
  await api('POST', '/vote', { token: voter, body: { bird, v: 0 } });
  check('vote removed', (await state(voter)).mine.v[bird] === undefined);

  await api('POST', '/flag', { token: voter, body: { bird, on: true } });
  check('flag on', (await state(voter)).mine.f[bird] === true);
  await api('POST', '/flag', { token: voter, body: { bird, on: false } });
  check('flag off', !(await state(voter)).mine.f[bird]);

  const f = await api('POST', '/flocks', { token: voter, body: { name: 'Suruyum' } });
  const fid = f.body?.id;
  check('flock create', f.status === 200 && !!fid, JSON.stringify(f.body));
  const t1 = await api('POST', `/flocks/${fid}/toggle`, { token: voter, body: { bird } });
  check('flock toggle add', t1.body?.added === true);
  const inState = async () => (await state(voter)).flocks.find(x => x.id === fid);
  check('flock holds bird', (await inState())?.birds.includes(bird));
  const t2 = await api('POST', `/flocks/${fid}/toggle`, { token: voter, body: { bird } });
  check('flock toggle remove', t2.body?.added === false);
  await api('POST', `/flocks/${fid}`, { token: voter, body: { public: false } });
  check('flock public off', (await inState())?.public === false);
  await api('POST', `/flocks/${fid}`, { token: voter, body: { public: true } });
  check('flock public on', (await inState())?.public === true);
  const d = await api('DELETE', `/flocks/${fid}`, { token: voter });
  check('flock delete', d.status === 200 && !(await inState()));
}

async function adminAndBan() {
  const wrong = await api('GET', '/admin/queue', { admin: true, key: 'definitely-wrong-key' });
  check('wrong admin key -> 403', wrong.status === 403, `status ${wrong.status}`);

  const bandit = mk();
  const pb = await postBird(bandit, 'Yasakli kus');
  if (pb.body?.id) created.push(pb.body.id);
  const uid = (await state(bandit)).me?.uid;
  const ban = await admin('POST', '/ban', { uid, on: true });
  check('admin ban -> 200', ban.status === 200 && !!uid, `status ${ban.status}`);
  const fresh = await api('POST', '/me', { token: mk(), body: { name: 'Yeni' } });
  check("ban: fresh identity from same IP -> 403 'banned'", fresh.status === 403 && fresh.body?.error === 'banned', JSON.stringify(fresh));
  const un = await admin('POST', '/ban', { uid, on: false });
  const ok = await api('POST', '/me', { token: mk(), body: { name: 'Yeni2' } });
  check('unban -> new identity allowed again', un.status === 200 && ok.status === 200, `status ${ok.status}`);
}

async function eraseFlow() {
  const t = mk();
  const r = await postBird(t, 'Silinecek');
  const id = r.body?.id; created.push(id);
  const del = await api('DELETE', '/me', { token: t });
  check('DELETE /api/me erases birds', del.status === 200 && del.body?.birds === 1, JSON.stringify(del.body));
  const img = await fetch(`${BASE}/api/img/${id}`);
  check('erased bird image gone (404)', img.status === 404, `status ${img.status}`);
}

async function cleanup() {
  for (const id of created.filter(Boolean)) await api('DELETE', `/birds/${id}`, { token: tokens[0], admin: true });
  for (const t of tokens) await api('DELETE', '/me', { token: t });
  const left = (await state()).birds.filter(b => created.includes(b.id));
  check('cleanup: no test birds left', left.length === 0);
}

try {
  console.log(`DrawBird smoke test -> ${BASE}`);
  await pages();
  const { bird } = await birdsFlow();
  await socialFlow(bird);
  await adminAndBan();
  await eraseFlow();
} catch (e) {
  check('unexpected error', false, e?.stack || String(e));
} finally {
  try { await cleanup(); } catch (e) { check('cleanup', false, String(e)); }
}
console.log(failed ? `\n${failed} check(s) FAILED` : '\nall checks passed');
process.exit(failed ? 1 : 0);
