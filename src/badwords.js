// Offensive-word lists for non-Turkish/English languages, used by the name filter.
// long: distinctive roots, safe to match anywhere inside a word.
// word: short or ambiguous terms, match only as whole words.
// Latin entries are lowercase without diacritics; no spaces inside entries (names are joined before matching).
export const BADWORDS = {
  es: {
    long: ['mierda', 'cabron', 'pendejo', 'gilipollas', 'carajo', 'cojones', 'boludo', 'pelotudo', 'chingad', 'chingar',
      'follar', 'follada', 'hijueputa', 'hijoputa', 'hijodeputa', 'hijadeputa', 'maricon', 'culero', 'sudaca', 'negrata',
      'malparid', 'hitler', 'mamaverga', 'chupapollas', 'comemierda', 'putamadre'],
    word: ['puta', 'puto', 'putas', 'putos', 'verga', 'polla', 'pene', 'culo', 'tetas', 'zorra', 'joder', 'marica',
      'puton', 'mamada', 'pajero', 'idiota', 'estupido', 'hostia', 'pinche', 'nazi', 'cabrona', 'mierdas', 'imbecil', 'sexo'],
  },
  pt: {
    long: ['caralho', 'buceta', 'fodase', 'merda', 'cuzao', 'filhodaputa', 'otario', 'arrombado', 'babaca', 'piroca', 'punheta',
      'nazista', 'hitler', 'cacete', 'siririca', 'viadinho', 'vagabundo', 'desgracado', 'putaria', 'bostalhao'],
    word: ['porra', 'foda', 'foder', 'puta', 'viado', 'bicha', 'vadia', 'rola', 'corno', 'boquete', 'tarado', 'safado', 'idiota', 'nazi',
      'cu', 'xota', 'sexo', 'pau', 'crl', 'fdp'],
  },
  fr: {
    long: ['putain', 'merde', 'salope', 'connard', 'connasse', 'enculer', 'encule', 'niquer', 'couille', 'bougnoule', 'youpin',
      'petasse', 'gouine', 'pouffiasse', 'trouduc', 'branler', 'hitler', 'sacdemerde'],
    word: ['pute', 'bite', 'chatte', 'foutre', 'pd', 'pede', 'tapette', 'negre', 'batard', 'nazi', 'ducon', 'ntm', 'fdp', 'cul',
      'sexe', 'nique', 'bordel', 'salaud', 'vagin', 'zob'],
  },
  de: {
    long: ['scheisse', 'scheiss', 'ficken', 'fotze', 'votze', 'hurensohn', 'wichser', 'arschloch', 'arschgeige', 'schwuchtel',
      'schlampe', 'pimmel', 'kanake', 'judensau', 'hitler', 'siegheil', 'drecksau', 'verpiss', 'miststueck', 'vollpfosten', 'wixer'],
    word: ['arsch', 'fick', 'nutte', 'schwanz', 'kacke', 'neger', 'nazi', 'spast', 'mongo', 'penner', 'bumsen', 'titten', 'muschi',
      'hure', 'vollidiot', 'sex', 'pisser', 'fotzen', 'schwul', 'sau'],
  },
  ru: {
    long: ['хуй', 'хуев', 'хуес', 'хуил', 'пизд', 'ебанат', 'ебанут', 'ебучи', 'заеб', 'выеб', 'долбоеб', 'долбаеб', 'пидор', 'пидар',
      'пидрил', 'блядь', 'бляд', 'блять', 'мудак', 'мудил', 'залуп', 'гандон', 'шлюх', 'дрочить', 'говно', 'ниггер', 'нацист',
      'гитлер', 'шалава', 'проститутк', 'порно', 'отсоси', 'ублюд', 'выблядок'],
    word: ['сука', 'жопа', 'хер', 'чмо', 'жид', 'хач', 'чурка', 'член', 'сиськи', 'секс', 'педик', 'гомик', 'мразь', 'тварь',
      'ебать', 'ебал', 'ебан', 'нахуй', 'мудо', 'срать', 'ссать'],
  },
  ar: {
    long: ['شرموط', 'عاهرة', 'قحبة', 'قحبه', 'منيوك', 'كسمك', 'كسامك', 'كساختك', 'ابنالكلب', 'ابنالحرام', 'ولدالزنا', 'ولادالزنا',
      'متناك', 'خنيث', 'لوطي', 'ديوث', 'هتلر', 'ابنالعاهرة', 'ابنالشرموطة', 'نيكامك', 'متناكة'],
    word: ['نيك', 'زب', 'زبي', 'طيز', 'عرص', 'خول', 'قواد', 'سكس', 'كس', 'شاذ', 'بزاز', 'نازي', 'زنجي', 'عاهر'],
  },
  zh: {
    long: ['傻逼', '操你', '他妈的', '去你妈', '草泥马', '艹你', '婊子', '贱人', '贱货', '骚货', '狗屎', '王八蛋', '混蛋', '鸡巴',
      '屁眼', '强奸', '做爱', '色情', '妓女', '妓院', '淫荡', '日你', '杂种', '畜生', '黑鬼', '日本鬼子', '支那', '小日本', '纳粹',
      '希特勒', '屌丝', '妈逼', '你妈逼', '尼玛', '卧槽', '口交', '肛交', '手淫', '性交', '死基佬', '阴茎', '阴道'],
    word: [],
  },
  ja: {
    long: ['ちんこ', 'ちんぽ', 'チンポ', 'チンコ', 'まんこ', 'マンコ', 'ファック', 'セックス', 'レイプ', 'ポルノ', 'ヤリマン', 'ヤリチン',
      'ビッチ', 'きちがい', 'キチガイ', '気違い', 'めくら', 'つんぼ', '支那', 'ジャップ', 'ニガー', 'ナチス', 'ヒトラー', '淫乱',
      '痴女', '売春', '中出し', '強姦', '死ね', '殺すぞ', 'パイパン'],
    word: ['くそ', 'クソ', 'しね', 'ばか', 'バカ', 'ブス', 'おっぱい', 'エロ', 'チョン', 'ホモ', 'オカマ', 'おかま', 'ガイジ', '変態',
      'セフレ', 'フェラ', 'うんこ', 'ウンコ'],
  },
  id: {
    long: ['anjing', 'bangsat', 'bajingan', 'kontol', 'memek', 'pepek', 'ngentot', 'jancuk', 'jancok', 'dancok', 'goblok', 'tolol',
      'brengsek', 'sialan', 'keparat', 'kampret', 'bokep', 'jablay', 'lonte', 'pelacur', 'sundal', 'bencong', 'colmek', 'ngewe',
      'jembut', 'kimak', 'pukimak', 'bispak', 'hitler'],
    word: ['cuk', 'asu', 'tai', 'babi', 'bego', 'pantat', 'perek', 'banci', 'homo', 'peli', 'coli', 'entot', 'tetek', 'toket', 'puki',
      'nazi', 'bacot', 'sex'],
  },
};
