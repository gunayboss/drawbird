// Name filter and Telegram moderation for DrawBird.
import { BADWORDS } from './badwords.js';

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
const FOLD = { 'ß': 'ss', 'ç': 'c', 'ğ': 'g', 'ı': 'i', 'İ': 'i', 'ö': 'o', 'ş': 's', 'ü': 'u', 'â': 'a', 'î': 'i', 'û': 'u' };

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
  if (SHORT.some(asWord)) return true;
  // The other site languages. Latin-script lists go through the same normalising as above.
  for (const lang of ['es', 'pt', 'fr', 'de', 'id']) {
    const L = BADWORDS[lang];
    if (L.long.some(w => inside(normalise(w).replace(/[^a-z]/g, ''))) || L.word.some(w => asWord(normalise(w).replace(/[^a-z]/g, '')))) return true;
  }
  // Cyrillic, Arabic, Chinese, Japanese: lowercase only (no NFKD, which would split Japanese kana), separators removed.
  const lower = String(text).toLowerCase();
  const parts = lower.split(/[\s\p{P}\p{S}\d_]+/u).filter(Boolean);
  const compact = parts.join('');
  for (const lang of ['ru', 'ar', 'zh', 'ja']) {
    const L = BADWORDS[lang];
    if (L.long.some(w => compact.includes(w)) || L.word.some(w => parts.includes(w))) return true;
  }
  return false;
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
  // The nightly digest runs without a request, so it needs to know the site address for photo links.
  await putSetting(env, 'origin', origin);
  const hook = await tg(env, 'setWebhook', { url: `${origin}/api/telegram`, secret_token: secret, allowed_updates: ['callback_query'] });
  if (!hook.ok) return { ok: false, error: 'webhook_failed' };
  await tg(env, 'sendMessage', { chat_id: last.chat.id, text: 'DrawBird bağlandı. Bildirilen kuşlar anında, günün yeni kuşları her sabah albüm olarak buraya gelecek; düğmelerle karar verebilirsin.' });
  return { ok: true, name: [last.chat.first_name, last.chat.last_name].filter(Boolean).join(' ') };
}

export async function telegramStatus(env) {
  return { token: !!env.TELEGRAM_TOKEN, connected: !!(await setting(env, 'tg_chat')), review: (await setting(env, 'review')) === '1' };
}

// Nightly album of the day's new birds, so the owner can glance at them once instead of approving each one.
// Ten photos per album (Telegram's limit), each followed by numbered delete buttons.
const DIGEST_MAX = 30;
export async function sendDigest(env, birds) {
  if (!env.TELEGRAM_TOKEN || !birds.length) return;
  const [chat, origin] = await Promise.all([setting(env, 'tg_chat'), setting(env, 'origin')]);
  if (!chat || !origin) return;
  const shown = birds.slice(0, DIGEST_MAX);
  const more = birds.length - shown.length;
  await tg(env, 'sendMessage', { chat_id: chat, text: `📸 Son 24 saatte ${birds.length} yeni kuş.${more ? ` İlk ${DIGEST_MAX} tanesi aşağıda, kalanı sitede.` : ''} Kötü olan varsa numarasına basıp sil.` });
  for (let i = 0; i < shown.length; i += 10) {
    const part = shown.slice(i, i + 10);
    await tg(env, 'sendMediaGroup', {
      chat_id: chat,
      media: part.map((b, j) => ({ type: 'photo', media: `${origin}/api/img/${b.id}`, caption: `${i + j + 1}. “${b.name}” · ${b.author || 'İsimsiz kuşçu'}` })),
    });
    const buttons = part.map((b, j) => ({ text: `🗑 ${i + j + 1}`, callback_data: `no:${b.id}` }));
    const rows = [];
    for (let k = 0; k < buttons.length; k += 5) rows.push(buttons.slice(k, k + 5));
    await tg(env, 'sendMessage', { chat_id: chat, text: `${i + 1}–${i + part.length} arası:`, reply_markup: { inline_keyboard: rows } });
  }
}

// Plain security or operations alert to the owner's chat.
export async function notifyText(env, text) {
  if (!env.TELEGRAM_TOKEN) return;
  const chat = await setting(env, 'tg_chat');
  if (chat) await tg(env, 'sendMessage', { chat_id: chat, text });
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
    photo: `${origin}/api/img/${bird.id}?${bird.sig ? `s=${bird.sig}&` : ''}v=${Date.now()}`,
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
  if (cb.message.photo) await tg(env, 'editMessageCaption', { chat_id: chat, message_id: cb.message.message_id, caption: `${cb.message.caption || ''}\n→ ${text}` });
  else {
    // Digest button rows: note which number was handled and keep the other buttons.
    const label = cb.message.reply_markup?.inline_keyboard.flat().find(x => x.callback_data === cb.data)?.text || '';
    await tg(env, 'editMessageText', { chat_id: chat, message_id: cb.message.message_id, text: `${cb.message.text || ''}\n${label} → ${text}`, reply_markup: cb.message.reply_markup });
  }
  return new Response('ok');
}
