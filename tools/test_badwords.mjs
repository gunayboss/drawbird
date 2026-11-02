import { readFileSync } from 'node:fs';
// src/ has no package.json "type":"module"; load the ES module through a data URL.
const src = readFileSync(new URL('../src/badwords.js', import.meta.url), 'utf8');
const { BADWORDS } = await import('data:text/javascript;base64,' + Buffer.from(src).toString('base64'));

const INNOCENT = {
  es: ['computadora', 'pájaro carpintero', 'disputa', 'reputación', 'círculo', 'cálculo', 'músculo', 'penetrar', 'vergara', 'colibrí', 'gorrión', 'águila', 'pelícano', 'cojín', 'mariposa', 'pelota', 'escuela', 'cono de helado', 'amigo'],
  pt: ['pássaro', 'computador', 'bom dia', 'passarinho', 'beija-flor', 'pardal', 'coruja', 'cornija', 'escola', 'amizade', 'caracol', 'papagaio', 'fodasse'.slice(0, 0) || 'cavalo', 'rolamento', 'paulista'],
  fr: ['conseil', 'oiseau', 'unique', 'ordinateur', 'moineau', 'mésange', 'hirondelle', 'bitume', 'cultiver', 'chatterie', 'bordeaux', 'pédalo', 'école', 'perroquet', 'sexagénaire'],
  de: ['Marsch', 'Meisenknödel', 'Vogel', 'Schwanzmeise', 'Specht', 'Fischer', 'Hurerei'.slice(0, 0) || 'Schule', 'Computer', 'Sauerkraut', 'Pinguin', 'Nachtigall', 'Rotkehlchen', 'Kuckuck', 'Mauersegler', 'Hitzewelle', 'Wichtel'],
  ru: ['оскорбление', 'воробей', 'синица', 'ласточка', 'попугай', 'хлеб', 'хлебать', 'педикюр', 'небанальный', 'сукно', 'мудрость', 'хуже', 'дятел', 'скворец', 'пингвин', 'компьютер', 'спасибо', 'привет'],
  ar: ['عصفور', 'حمامة', 'نسر', 'صقر', 'بومة', 'ببغاء', 'طاووس', 'كتاب', 'مدرسة', 'شمس', 'قمر', 'كسرة', 'كسول', 'زبدة', 'زبيب', 'منيرة'],
  zh: ['小鸟', '啄木鸟', '麻雀', '孔雀', '老鹰', '蜻蜓', '你好', '妈妈', '他们', '画画', '天空', '日本', '操场', '喜鹊', '企鹅', '谢谢', '我的妈妈的书'],
  ja: ['すずめ', 'つばめ', 'ことり', 'ふくろう', 'きつつき', 'ハト', 'ペンギン', 'ありがとう', 'こんにちは', 'マンゴー', 'ホモサピエンス', 'エロイカ', 'フェラーリ', 'ばかり', 'しねま', 'インコ'],
  id: ['burung', 'elang', 'merpati', 'pantai', 'anjungan', 'bangsawan', 'kontrol', 'asuransi', 'tolong', 'pepaya', 'bencana', 'cuka', 'selamat pagi', 'terima kasih', 'gajah', 'kenari'],
};

const LATIN = new Set(['es', 'pt', 'fr', 'de', 'id']);
let strip = true;
const norm = s => { const l = String(s).toLowerCase(); return strip ? l.normalize('NFKD').replace(/[̀-ͯ]/g, '') : l; };
const joined = s => norm(s).replace(/[\s\-_.]+/g, '');
let fail = 0;
const bad = m => { console.error('FAIL', m); fail++; };

for (const [lang, { long, word }] of Object.entries(BADWORDS)) {
  strip = LATIN.has(lang);
  const inn = INNOCENT[lang] || [];
  if (inn.length < 10) bad(`${lang}: need >=10 innocent words`);
  const all = [...long, ...word];
  if (all.length < 15 || all.length > 80) bad(`${lang}: entry count ${all.length}`);
  if (new Set(all).size !== all.length) bad(`${lang}: duplicate entries`);
  for (const e of all) if (!e || /[\s\-]/.test(e) || e !== e.toLowerCase() || (strip && e !== norm(e))) bad(`${lang}: malformed entry "${e}"`);
  for (const w of inn) {
    const j = joined(w);
    for (const r of long) if (j.includes(norm(r))) bad(`${lang}: "${w}" contains long root "${r}"`);
    for (const part of norm(w).split(/[^\p{L}\p{N}]+/u).filter(Boolean).concat(j))
      if (word.map(norm).includes(part)) bad(`${lang}: "${w}" equals word entry "${part}"`);
  }
  console.log(`${lang}: long=${long.length} word=${word.length} innocents=${inn.length}`);
}
if (fail) { console.error(`${fail} failure(s)`); process.exit(1); }
console.log('OK');
