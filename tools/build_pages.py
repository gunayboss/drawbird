"""Builds the drawing lessons (/dersler) and bird pages (/kuslar) into public/.

Run from the project root:  python tools/build_pages.py
Edit the LESSONS / BIRDS data below, then run again; the HTML files are generated, do not edit them by hand.
"""
import html, io, os

ROOT = os.path.join(os.path.dirname(__file__), '..', 'public')
INK, ACCENT, GHOST = '#1b2740', '#f2b705', '#c9d3e0'

# Each step adds shapes; earlier steps are redrawn in a pale colour so the new part stands out.
# Shapes: ('e', cx, cy, rx, ry, fill) ellipse · ('c', cx, cy, r, fill) circle · ('p', d, fill) path · ('l', d) line only
def svg(steps, upto, full=False):
    out = [f'<svg viewBox="0 0 240 180" role="img" aria-label="Adım {upto + 1}" xmlns="http://www.w3.org/2000/svg">',
           '<line x1="10" y1="80" x2="230" y2="80" stroke="#9fb3c8" stroke-width="1.5" stroke-dasharray="6 6"/>']
    for i, step in enumerate(steps[:upto + 1]):
        current = full or i == upto
        stroke = INK if current else GHOST
        for sh in step:
            fill = (sh[-1] if current else '#eef2f7') if sh[0] != 'l' else 'none'
            common = f'stroke="{stroke}" stroke-width="3" stroke-linejoin="round" stroke-linecap="round" fill="{fill}"'
            if sh[0] == 'e': out.append(f'<ellipse cx="{sh[1]}" cy="{sh[2]}" rx="{sh[3]}" ry="{sh[4]}" {common}/>')
            elif sh[0] == 'c': out.append(f'<circle cx="{sh[1]}" cy="{sh[2]}" r="{sh[3]}" {common}/>')
            elif sh[0] in 'pl': out.append(f'<path d="{sh[1]}" {common}/>')
    out.append('</svg>')
    return ''.join(out)

LESSONS = [
    {
        'slug': 'serce', 'title': 'Serçe nasıl çizilir?', 'bird': 'Serçe', 'acc': 'serçeni',
        'intro': 'Serçe, DrawBird gökyüzüne ilk kuşunu salmak için en iyi başlangıç: yuvarlak bir gövde, küçük bir baş, kısa bir gaga. Beş adımda, kanat çırpan bir serçe çizeceğiz.',
        'steps': [
            ('Gövde', 'Çizim alanının ortasındaki kesik çizginin hemen altına, yatay bir yumurta çiz. Gövde çizginin altında kalırsa uçarken sabit durur.', [('e', 105, 112, 50, 30, '#b07a4f')]),
            ('Baş', 'Gövdenin sağ üst köşesine, gövdeye biraz giren bir daire ekle. Serçenin boynu yok gibidir; baş doğrudan gövdeye oturur.', [('c', 155, 88, 24, '#b07a4f')]),
            ('Gaga ve göz', 'Başın sağına küçük, kalın bir üçgen gaga koy. Serçenin gagası tohum kırmak için kısa ve kalındır. Gözü gagaya yakın, dolu bir nokta olarak çiz.', [('p', 'M176 82 L196 88 L176 95 Z', '#f2b705'), ('c', 162, 82, 4, INK)]),
            ('Kanat ve kuyruk', 'Kesik çizginin ÜSTÜNE, gövdenin ortasından yukarı doğru bir yaprak gibi kanat çiz. Gökyüzünde bu kısım açılıp kapanır. Gövdenin soluna kısa, kare uçlu bir kuyruk ekle.', [('p', 'M80 100 Q95 40 135 48 Q120 78 118 100 Z', '#8a5a36'), ('p', 'M57 104 L22 92 L28 124 L60 118 Z', '#8a5a36')]),
            ('Renk ve ayrıntı', 'Erkek serçenin gerdanı siyah, yanakları gri olur. Gerdanına küçük siyah bir leke, kanadına iki açık çizgi ekle. Kalın kalemle (6 ve üstü) çizersen gökyüzünde daha net görünür.', [('p', 'M150 104 Q160 112 170 102 Q162 98 150 104 Z', INK), ('l', 'M98 66 L124 60'), ('l', 'M92 80 L122 74')]),
        ],
        'facts': [
            'Ev serçesi (Passer domesticus) 14–16 cm boyundadır ve insanların yaşadığı hemen her yerde görülür.',
            'Erkeğin tepesi gri, gerdanı siyahtır; dişi ise baştan aşağı kahverengi tonlardadır.',
            'Serçeler toz banyosu yapar: tüylerindeki parazitlerden kurtulmak için kuru toprağa yatıp kanat çırparlar.',
            'Çoğunlukla tohum yerler, ama yavrularını protein açısından zengin böceklerle beslerler.',
        ],
    },
    {
        'slug': 'marti', 'title': 'Martı nasıl çizilir?', 'bird': 'Martı', 'acc': 'martını',
        'intro': 'Martının sırrı uzun ve ince kanatlarıdır. DrawBird gökyüzünde martılar, kanatlarını yukarı kaldırınca en güzel görünür. Kıyı şehirlerinin bu tanıdık kuşunu beş adımda çizelim.',
        'steps': [
            ('Gövde', 'Kesik çizginin altına, serçeninkinden daha uzun ve ince bir gövde çiz. Martı gövdesi bir mermi gibi öne doğru incelir.', [('e', 112, 112, 62, 22, '#ffffff')]),
            ('Baş', 'Gövdenin sağ ucuna, yuvarlak ama gövdeye göre küçük bir baş ekle.', [('c', 174, 98, 18, '#ffffff')]),
            ('Gaga', 'Uzun, sarı bir gaga çiz; ucunu hafif aşağı kıvır. Alt gagaya kırmızı bir nokta koy: yavrular bu noktayı gagalayınca anne yiyecek verir.', [('p', 'M190 96 L218 100 L212 106 L190 104 Z', '#f2b705'), ('c', 210, 104, 2.5, '#e03131'), ('c', 180, 93, 3, INK)]),
            ('Kanatlar', 'Asıl iş burada: kesik çizginin ÜSTÜNE, gövdenin ortasından yukarı doğru uzun, ince, açık gri bir kanat çiz. Kanadın ucunu siyaha boya. Kanat ne kadar uzunsa, çırpınca o kadar martıya benzer.', [('p', 'M90 100 L120 30 L150 22 L128 60 L130 100 Z', '#c9d3e0'), ('p', 'M120 30 L150 22 L140 40 Z', INK)]),
            ('Kuyruk ve ayaklar', 'Gövdenin soluna kısa, beyaz bir yelpaze kuyruk ekle. Ayakları istersen sarı ve perdeli çizebilirsin; uçarken genelde gövdenin altına toplanırlar.', [('p', 'M52 108 L24 100 L26 122 L54 118 Z', '#ffffff'), ('l', 'M110 132 L104 146 M120 132 L118 146')]),
        ],
        'facts': [
            'İstanbul\'da en sık görülen martı, sarı bacaklı martıdır (Larus michahellis). Boyu 55–67 cm, kanat açıklığı 1,2–1,5 metreyi bulur.',
            'Martılar hem tatlı hem tuzlu su içebilir; gözlerinin üstündeki bezler fazla tuzu dışarı atar.',
            'Yavru martılar ilk yıllarında kahverengi beneklidir; yetişkin tüylerine kavuşmaları dört yıl sürebilir.',
            'Gagadaki kırmızı nokta bir "düğme" gibidir: yavru onu gagalayınca ebeveyn yiyeceği geri çıkarır.',
        ],
    },
    {
        'slug': 'baykus', 'title': 'Baykuş nasıl çizilir?', 'bird': 'Baykuş', 'acc': 'baykuşunu',
        'intro': 'Baykuşlar diğer kuşlardan farklıdır: kocaman başları ve öne bakan iri gözleri vardır. DrawBird\'de sevimli bir kukumav çizmek için yarı yandan bakan, kanatlarını açmış bir baykuş çizeceğiz.',
        'steps': [
            ('Gövde', 'Kesik çizginin altına, tombul ve hafif dik duran bir yumurta çiz. Baykuşun gövdesi serçeninkinden daha yuvarlaktır.', [('e', 110, 116, 44, 34, '#9c7b5b')]),
            ('Baş', 'Gövdenin üstüne, sağa doğru büyük bir daire ekle. Baykuşun başı gövdesine göre iridir; bu ona sevimli görüntüsünü verir.', [('c', 146, 86, 30, '#9c7b5b')]),
            ('Gözler ve gaga', 'İki büyük sarı daire içine siyah göz bebekleri çiz. Baykuşun gözleri yüzünün önündedir, bu yüzden ikisi de görünür. Aralarına aşağı bakan küçük bir gaga koy.', [('c', 136, 82, 10, '#f2b705'), ('c', 160, 82, 10, '#f2b705'), ('c', 137, 82, 4, INK), ('c', 161, 82, 4, INK), ('p', 'M146 90 L152 100 L156 90 Z', '#5c4632')]),
            ('Kanat', 'Kesik çizginin ÜSTÜNE, gövdenin solundan yukarı doğru geniş, yuvarlak uçlu bir kanat çiz. Baykuş kanatları geniştir ve uçları yumuşak tüylüdür, bu sayede neredeyse sessiz uçarlar.', [('p', 'M70 104 Q60 46 104 40 Q112 70 104 100 Z', '#7a5c42')]),
            ('Benekler ve pençeler', 'Gövdeye ve başa küçük beyaz benekler serpiştir; kukumavın tüyleri böyle beneklidir. Altına iki küçük pençe ekle.', [('c', 98, 118, 3, '#ffffff'), ('c', 116, 128, 3, '#ffffff'), ('c', 106, 104, 3, '#ffffff'), ('c', 132, 64, 2.5, '#ffffff'), ('l', 'M102 150 L98 160 M118 150 L120 160')]),
        ],
        'facts': [
            'Türkiye\'de en sık görülen baykuş kukumavdır (Athene noctua); boyu yalnız 21–23 cm\'dir.',
            'Baykuşlar gözlerini yuvalarında oynatamaz; bunun yerine başlarını yaklaşık 270 derece çevirebilirler.',
            'Kanat tüylerinin tarak gibi kenarları havayı böler, bu yüzden uçarken neredeyse ses çıkarmazlar.',
            'Kukumav, diğer baykuşların aksine gündüz de görülebilir; duvarlarda ve çatılarda tünediğini görebilirsin.',
        ],
    },
]

BIRDS = [
    {
        'slug': 'kumru', 'name': 'Kumru', 'acc': 'kumrunu', 'latin': 'Streptopelia decaocto',
        'lead': 'Pencere kenarlarının, balkonların ve şehir parklarının en tanıdık seslerinden biri kumruya aittir: yumuşak, üç heceli bir "gu-guuu-gu".',
        'table': [('Boy', '31–33 cm'), ('Kanat açıklığı', '47–55 cm'), ('Ağırlık', '125–240 g'), ('Beslenme', 'Tohum, tahıl, filiz'), ('Yumurta', 'Genellikle 2'), ('Görüldüğü yer', 'Şehirler, köyler, bahçeler; yıl boyu')],
        'body': [
            'Kumru, açık kum renginde, ince yapılı bir güvercin akrabasıdır. Onu en kolay tanıtan özelliği ensesindeki siyah yarım halkadır; İngilizcede bu yüzden "tasmalı güvercin" diye anılır.',
            'Aslında Anadolu ve Balkanların kuşu olan kumru, 20. yüzyılda bütün Avrupa\'ya yayıldı. Bugün Britanya\'dan İskandinavya\'ya kadar pek çok ülkede yerleşik bir kuştur. Bu yayılma, kuş bilimcilerin en çok incelediği doğal yayılmalardan biridir.',
            'Kumrular yılda birkaç kez kuluçkaya yatabilir. Yuvaları dalların arasına gelişigüzel bırakılmış birkaç çubuktan ibarettir; bazen alttan yumurtalar görünür. Anne ve baba yavruları "kursak sütü" denen, kursaklarında ürettikleri besleyici bir sıvıyla besler.',
            'Türk kültüründe kumru barışın ve sevginin simgesidir. "Kumru gibi" deyimi, birbirine çok bağlı çiftler için kullanılır.',
        ],
        'draw': 'Kumru çizmek için serçe dersini izle, ama gövdeyi biraz daha uzun, rengi açık kahve-gri yap. Baş küçük ve yuvarlak olsun, ensesine ince siyah bir yarım çizgi ekle. Gaga ince ve koyu, gözler kırmızımsı.',
        'lesson': 'serce',
    },
    {
        'slug': 'leylek', 'name': 'Leylek', 'acc': 'leyleğini', 'latin': 'Ciconia ciconia',
        'lead': 'Baharın habercisi ak leylek, bacaların ve elektrik direklerinin tepesine kurduğu kocaman yuvalarıyla Anadolu köylerinin vazgeçilmez kuşudur.',
        'table': [('Boy', '100–115 cm'), ('Kanat açıklığı', '155–215 cm'), ('Ağırlık', '2,3–4,4 kg'), ('Beslenme', 'Kurbağa, böcek, solucan, küçük memeliler'), ('Yumurta', '3–5'), ('Görüldüğü yer', 'Mart–Ağustos arası Türkiye\'de, kışın Afrika\'da')],
        'body': [
            'Ak leylek beyaz gövdesi, siyah kanat uçları, uzun kırmızı gagası ve kırmızı bacaklarıyla kolayca tanınır. Uçarken boynunu ve bacaklarını dümdüz uzatır.',
            'Leylekler göçmendir. Ağustos sonunda on binlercesi bir araya gelir ve İstanbul Boğazı üzerinden Afrika\'ya doğru süzülür. Kanat çırpmak yerine sıcak hava akımlarını kullanarak yükselir, sonra kilometrelerce süzülürler; bu yüzden denizin üstünden uzun süre uçmaktan kaçınır, dar boğazları seçerler.',
            'Leylekler neredeyse hiç ses çıkarmaz. Bunun yerine gagalarını hızla takırdatarak "konuşurlar"; yuvaya dönen eşini karşılayan leylek, başını arkaya atıp uzun uzun takırdar.',
            'Aynı yuva yıllarca kullanılır ve her yıl yeni çubuklarla büyütülür. Bazı leylek yuvaları bir metreden geniş ve yüzlerce kilo ağırlığındadır.',
        ],
        'draw': 'Leylek çizmek için martı dersini izle: gövde uzun ve beyaz, kanatlar uzun ve uçları siyah. Ama gagayı çok uzun ve kırmızı yap, boynu uzat. Bacakları da uzun ve kırmızı çiz, gövdenin arkasından dışarı uzansın.',
        'lesson': 'marti',
    },
]

NAV = ('<nav class="top"><a href="/#ciz">Çiz</a><a{d} href="/dersler/">Dersler</a><a{k} href="/kuslar/">Kuşlar</a>'
       '<a href="/haftanin-kuslari">Haftanın kuşları</a><a href="/nasil-oynanir.html">Nasıl oynanır</a></nav>')
FOOT = ('<footer>DrawBird · <a href="/kosullar.html">Koşullar</a> · <a href="/gizlilik.html">Gizlilik</a> · '
        '<a href="/kvkk.html">KVKK</a> · <a href="https://github.com/gunayboss/drawbird">Kaynak kod</a></footer>')
EXTRA_CSS = '''<style>
  .steps-grid { display: grid; gap: 18px; margin-top: 12px; }
  .step { display: grid; grid-template-columns: minmax(0, 240px) minmax(0, 1fr); gap: 16px; align-items: center; background: var(--chip); border-radius: 16px; padding: 12px; }
  .step svg { width: 100%; height: auto; background: #ffffff; border-radius: 12px; }
  .step h3 { margin: 0 0 4px; font-size: 18px; }
  .step p { margin: 0; }
  @media (max-width: 560px) { .step { grid-template-columns: 1fr; } }
  .facts { background: var(--chip); border-radius: 16px; padding: 4px 18px 4px 34px; }
  table.card { border-collapse: collapse; width: 100%; margin: 10px 0; }
  table.card th, table.card td { text-align: left; padding: 7px 10px; border-bottom: 1px solid var(--line); vertical-align: top; }
  table.card th { width: 40%; color: var(--muted); font-weight: 500; }
  .list { display: grid; gap: 10px; padding: 0; list-style: none; }
  .list a { display: block; background: var(--chip); border-radius: 14px; padding: 12px 16px; text-decoration: none; }
  .list b { font-size: 18px; }
</style>'''

def page(title, desc, body, active, path):
    nav = NAV.format(d=' class="on"' if active == 'd' else '', k=' class="on"' if active == 'k' else '')
    return f'''<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{html.escape(title)} · DrawBird</title>
<meta name="description" content="{html.escape(desc)}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:image" content="/og-card.png">
<link rel="canonical" href="{path}">
<link rel="icon" href="/icons/icon-192.png" type="image/png">
<link rel="stylesheet" href="/fonts/fonts.css">
<link rel="stylesheet" href="/sayfa.css">
{EXTRA_CSS}
</head>
<body>
<main>
{nav}
<article>
{body}
</article>
{FOOT}
</main>
</body>
</html>
'''

def write(rel, text):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    io.open(path, 'w', encoding='utf-8', newline='\n').write(text)
    print('yazıldı', rel)

for L in LESSONS:
    shapes = [s[2] for s in L['steps']]
    steps = ''.join(
        f'<div class="step">{svg(shapes, i)}<div><h3>{i + 1}. {html.escape(name)}</h3><p>{html.escape(text)}</p></div></div>'
        for i, (name, text, _) in enumerate(L['steps']))
    steps += (f'<div class="step">{svg(shapes, len(shapes) - 1, full=True)}<div><h3>Bitti!</h3>'
              f'<p>{html.escape(L["bird"])} hazır. Şimdi DrawBird’de çiz, adını koy ve gökyüzüne sal.</p></div></div>')
    facts = ''.join(f'<li>{html.escape(f)}</li>' for f in L['facts'])
    body = f'''  <h1>{html.escape(L['title'])}</h1>
  <p>{html.escape(L['intro'])}</p>
  <p class="muted">Kesik çizgi, DrawBird çizim alanındaki kanat hattıdır: üstündekiler çırpar, altındakiler gövde olarak kalır.</p>
  <h2>Adım adım</h2>
  <div class="steps-grid">{steps}</div>
  <h2>{html.escape(L['bird'])} hakkında bilmen gerekenler</h2>
  <ul class="facts">{facts}</ul>
  <p><a class="cta" href="/#ciz">Şimdi kendi {html.escape(L['acc'])} çiz</a></p>'''
    write(f"dersler/{L['slug']}.html", page(L['title'], L['intro'][:155], body, 'd', f"/dersler/{L['slug']}"))

items = ''.join(f'<li><a href="/dersler/{L["slug"]}.html"><b>{html.escape(L["title"])}</b><br><span class="muted">{html.escape(L["intro"][:110])}…</span></a></li>' for L in LESSONS)
write('dersler/index.html', page('Kuş çizim dersleri', 'Adım adım kuş çizim dersleri: serçe, martı, baykuş. DrawBird gökyüzünde kanat çırpan kuşlar çiz.',
      f'  <h1>Kuş çizim dersleri</h1>\n  <p>Her ders beş adım. Hepsi DrawBird\'ün kanat hattına göre hazırlandı, yani çizdiğin kuş gökyüzünde gerçekten kanat çırpar. Kolaydan zora sıralı.</p>\n  <ul class="list">{items}</ul>\n  <p><a class="cta" href="/#ciz">Çizmeye başla</a></p>', 'd', '/dersler/'))

for B in BIRDS:
    rows = ''.join(f'<tr><th>{html.escape(k)}</th><td>{html.escape(v)}</td></tr>' for k, v in B['table'])
    paras = ''.join(f'<p>{html.escape(p)}</p>' for p in B['body'])
    body = f'''  <h1>{html.escape(B['name'])}</h1>
  <p class="muted"><i>{html.escape(B['latin'])}</i></p>
  <p>{html.escape(B['lead'])}</p>
  <table class="card">{rows}</table>
  {paras}
  <h2>DrawBird'de {html.escape(B['name'].lower())} çizmek</h2>
  <p>{html.escape(B['draw'])}</p>
  <p><a href="/dersler/{B['lesson']}.html">İlgili çizim dersine git →</a></p>
  <p><a class="cta" href="/#ciz">Kendi {html.escape(B['acc'])} çiz</a></p>'''
    write(f"kuslar/{B['slug']}.html", page(f"{B['name']}: tanı ve çiz", B['lead'][:155], body, 'k', f"/kuslar/{B['slug']}"))

items = ''.join(f'<li><a href="/kuslar/{B["slug"]}.html"><b>{html.escape(B["name"])}</b> <i class="muted">{html.escape(B["latin"])}</i><br><span class="muted">{html.escape(B["lead"][:110])}…</span></a></li>' for B in BIRDS)
write('kuslar/index.html', page('Türkiye\'nin kuşları', 'Türkiye\'de görebileceğin kuşları tanı, sonra DrawBird\'de çiz: kumru, leylek ve daha fazlası.',
      f'  <h1>Türkiye\'nin kuşları</h1>\n  <p>Balkonundan, parktan, kıyıdan tanıyabileceğin kuşlar. Her sayfada kuşun boyu, ne yediği, nerede yaşadığı ve onu DrawBird\'de nasıl çizeceğin var. Yeni kuşlar ekleniyor.</p>\n  <ul class="list">{items}</ul>', 'k', '/kuslar/'))
