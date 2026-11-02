// Name filter and Telegram moderation for DrawBird.

// ---- name filter ----
// Words are matched after normalising: Turkish lowercase, look-alike digits and symbols mapped to
// letters, separators removed, repeated letters squashed ("k.0.t.ü" -> "kotu", "siiiik" -> "sik").
// LONG roots are caught anywhere inside a name; SHORT ones only as whole words, so ordinary words
// that merely contain them ("ampul", "piknik", "fiziksel") pass.
const LONG = [
  // Türkçe
  'orospu', 'orspu', 'oruspu', 'siktir', 'sikerim', 'sikiyim', 'sikis', 'sikik', 'yarrak', 'yarak', 'amcik', 'amina', 'aminak',
  'amk', 'pezevenk', 'gavat', 'kahpe', 'kaltak', 'yavsak', 'serefsiz', 'gerizekali', 'ibne', 'puşt', 'pust', 'gotveren',
  'ananı', 'anani', 'bacini', 'got', 'mal', 'salak',
  // English
  'fuck', 'fuk', 'shit', 'bitch', 'cunt', 'dick', 'pussy', 'nigger', 'nigga', 'faggot', 'whore', 'slut', 'rape', 'porn',
  'nazi', 'hitler', 'penis', 'vagina', 'cock', 'asshole',
];
const SHORT = ['am', 'sik', 'pic', 'got', 'mal', 'ass', 'sex', 'seks', 'oc', 'aq', 'mk', 'sg', 'kkk'];
// Roots in LONG that also sit inside innocent words ("peacock", "grape", "nazik", "fukara"), so whole words only.
const LONG_AS_WORD = new Set(['got', 'mal', 'amk', 'salak', 'cock', 'dick', 'rape', 'nazi', 'fuk']);

const LEET = { '0': 'o', '1': 'i', '!': 'i', '|': 'i', '3': 'e', '4': 'a', '@': 'a', '5': 's', '$': 's', '7': 't', '8': 'b', '9': 'g', '+': 't' };
const FOLD = { 'ç': 'c', 'ğ': 'g', 'ı': 'i', 'İ': 'i', 'ö': 'o', 'ş': 's', 'ü': 'u', 'â': 'a', 'î': 'i', 'û': 'u' };

function normalise(text) {
  let s = String(text).toLocaleLowerCase('tr');
  s = [...s].map(c => LEET[c] ?? FOLD[c] ?? c).join('');
  return s.normalize('NFKD').replace(/[̀-ͯ]/g, '');
}
const squash = s => s.replace(/(.)\1+/g, '$1');

export function isBadName(text) {
  const norm = normalise(text);
  const wordsRaw = norm.split(/[^a-z]+/).filter(Boolean);
  const wordsSq = wordsRaw.map(squash);
  const joinedRaw = norm.replace(/[^a-z]/g, '');
  const joinedSq = squash(joinedRaw);
  // A squashed root is only trusted when it stays long enough to be specific ("ass" -> "as" is not).
  const asWord = root => { const rs = squash(root); return wordsRaw.includes(root) || (rs.length >= 3 && rs !== root && wordsSq.includes(rs)) || wordsSq.includes(root); };
  const inside = root => { const rs = squash(root); return joinedRaw.includes(root) || (rs.length >= 4 && joinedSq.includes(rs)); };
  for (const w of LONG) {
    const root = normalise(w).replace(/[^a-z]/g, '');
    if (LONG_AS_WORD.has(w) ? asWord(root) : inside(root)) return true;
  }
  return SHORT.some(asWord);
}

// ---- Telegram ----
// Needs the TELEGRAM_TOKEN secret. The chat id and webhook secret are stored in the settings table
// when the owner presses "Telegram'ı bağla" in the admin panel.
const tg = (env, method, payload) => fetch(`https://api.telegram.org/bot${env.TELEGRAM_TOKEN}/${method}`, {
  method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(payload),
}).then(r => r.json()).catch(() => ({ ok: false }));

export async function setting(env, k) {
  return env.DB.prepare('SELECT v FROM settings WHERE k = ?').bind(k).first('v');
}
async function putSetting(env, k, v) {
  await env.DB.prepare('INSERT INTO settings (k, v) VALUES (?, ?) ON CONFLICT(k) DO UPDATE SET v = excluded.v').bind(k, v).run();
}

// Pair the bot with the chat that last messaged it, then point Telegram's webhook at us.
export async function connectTelegram(env, origin) {
  if (!env.TELEGRAM_TOKEN) return { ok: false, error: 'no_token' };
  await tg(env, 'deleteWebhook', {});
  const upd = await tg(env, 'getUpdates', { limit: 50 });
  const msgs = (upd.result || []).map(u => u.message).filter(m => m?.chat?.type === 'private');
  const last = msgs[msgs.length - 1];
  if (!last) return { ok: false, error: 'no_message' };
  const secret = [...crypto.getRandomValues(new Uint8Array(24))].map(b => b.toString(16).padStart(2, '0')).join('');
  await putSetting(env, 'tg_chat', String(last.chat.id));
  await putSetting(env, 'tg_secret', secret);
  const hook = await tg(env, 'setWebhook', { url: `${origin}/api/telegram`, secret_token: secret, allowed_updates: ['callback_query'] });
  if (!hook.ok) return { ok: false, error: 'webhook_failed' };
  await tg(env, 'sendMessage', { chat_id: last.chat.id, text: 'DrawBird bağlandı. Onay bekleyen ve bildirilen kuşlar buraya gelecek; düğmelerle karar verebilirsin.' });
  return { ok: true, name: [last.chat.first_name, last.chat.last_name].filter(Boolean).join(' ') };
}

export async function telegramStatus(env) {
  return { token: !!env.TELEGRAM_TOKEN, connected: !!(await setting(env, 'tg_chat')) };
}

// Fire-and-forget notice about one bird, with decision buttons.
export async function notifyBird(env, origin, bird, kind) {
  if (!env.TELEGRAM_TOKEN) return;
  const chat = await setting(env, 'tg_chat');
  if (!chat) return;
  const head = kind === 'pending' ? '🕊 Onay bekleyen kuş' : `🚩 Bildirilen kuş (${bird.flags} bildirim)`;
  const buttons = kind === 'pending'
    ? [[{ text: '✅ Onayla', callback_data: `ok:${bird.id}` }, { text: '🗑 Reddet', callback_data: `no:${bird.id}` }], [{ text: '⛔ Reddet ve engelle', callback_data: `ban:${bird.id}` }]]
    : [[{ text: '👍 Sorun yok', callback_data: `clear:${bird.id}` }, { text: '🗑 Sil', callback_data: `no:${bird.id}` }], [{ text: '⛔ Sil ve engelle', callback_data: `ban:${bird.id}` }]];
  await tg(env, 'sendPhoto', {
    chat_id: chat,
    photo: `${origin}/api/img/${bird.id}?v=${Date.now()}`,
    caption: `${head}\n“${bird.name}” · ${bird.author || 'İsimsiz kuşçu'}`,
    reply_markup: { inline_keyboard: buttons },
  });
}

// Handle a button press coming back from Telegram. `act(kind, birdId)` performs the decision and returns a short result text.
export async function handleTelegram(req, env, act) {
  const secret = await setting(env, 'tg_secret');
  if (!secret || req.headers.get('x-telegram-bot-api-secret-token') !== secret) return new Response('forbidden', { status: 403 });
  const update = await req.json().catch(() => ({}));
  const cb = update.callback_query;
  const chat = await setting(env, 'tg_chat');
  if (!cb || String(cb.message?.chat?.id) !== chat) return new Response('ok');
  const [kind, id] = String(cb.data || '').split(':');
  const text = await act(kind, id);
  await tg(env, 'answerCallbackQuery', { callback_query_id: cb.id, text });
  await tg(env, 'editMessageCaption', { chat_id: chat, message_id: cb.message.message_id, caption: `${cb.message.caption || ''}\n→ ${text}` });
  return new Response('ok');
}
