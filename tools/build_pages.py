"""Builds DrawBird's content pages into public/ and the static page list for the sitemap.

Run from the project root:  python tools/build_pages.py
Content lives in content_lessons.py, content_birds.py and content_pages.py; the HTML is generated, do not edit it by hand.
"""
import html, io, json, os, sys

sys.path.insert(0, os.path.dirname(__file__))
from content_lessons import LESSONS
from content_birds import BIRDS
from content_pages import TEACHERS, FAQ, ABOUT, POSTS

ROOT = os.path.join(os.path.dirname(__file__), '..')
PUBLIC = os.path.join(ROOT, 'public')
INK, GHOST = '#1b2740', '#c9d3e0'
esc = html.escape
written = []

def svg(steps, upto, full=False, label=None):
    out = [f'<svg viewBox="0 0 240 180" role="img" aria-label="{esc(label or f"Adım {upto + 1}")}" xmlns="http://www.w3.org/2000/svg">',
           '<line x1="10" y1="80" x2="230" y2="80" stroke="#9fb3c8" stroke-width="1.5" stroke-dasharray="6 6"/>']
    for i, step in enumerate(steps[:upto + 1]):
        current = full or i == upto
        stroke = INK if current else GHOST
        for sh in step:
            fill = (sh[-1] if current else '#eef2f7') if sh[0] != 'l' else 'none'
            common = f'stroke="{stroke}" stroke-width="3" stroke-linejoin="round" stroke-linecap="round" fill="{fill}"'
            if sh[0] == 'e': out.append(f'<ellipse cx="{sh[1]}" cy="{sh[2]}" rx="{sh[3]}" ry="{sh[4]}" {common}/>')
            elif sh[0] == 'c': out.append(f'<circle cx="{sh[1]}" cy="{sh[2]}" r="{sh[3]}" {common}/>')
            else: out.append(f'<path d="{sh[1]}" {common}/>')
    out.append('</svg>')
    return ''.join(out)

NAV_ITEMS = [('/#ciz', 'Çiz', None), ('/dersler/', 'Dersler', 'dersler'), ('/kuslar/', 'Kuşlar', 'kuslar'),
             ('/haftanin-kuslari', 'Haftanın kuşları', 'hafta'), ('/blog/', 'Blog', 'blog'), ('/sss', 'SSS', 'sss')]
FOOT = ('<footer>DrawBird · <a href="/hakkinda">Hakkında</a> · <a href="/ogretmenler">Öğretmenler</a> · <a href="/nasil-oynanir">Nasıl oynanır</a> · '
        '<a href="/kosullar">Koşullar</a> · <a href="/gizlilik">Gizlilik</a> · <a href="/kvkk">KVKK</a> · '
        '<a href="https://github.com/gunayboss/drawbird">Kaynak kod</a></footer>')
EXTRA_CSS = '''<style>
  .steps-grid { display: grid; gap: 18px; margin-top: 12px; }
  .step { display: grid; grid-template-columns: minmax(0, 240px) minmax(0, 1fr); gap: 16px; align-items: center; background: var(--chip); border-radius: 16px; padding: 12px; }
  .step svg, .list svg { width: 100%; height: auto; background: #ffffff; border-radius: 12px; }
  .list svg { margin-top: 8px; }
  .step h3 { margin: 0 0 4px; font-size: 18px; }
  .step p { margin: 0; }
  @media (max-width: 560px) { .step { grid-template-columns: 1fr; } }
  .facts { background: var(--chip); border-radius: 16px; padding: 4px 18px 4px 34px; }
  table.card { border-collapse: collapse; width: 100%; margin: 10px 0; }
  table.card th, table.card td { text-align: left; padding: 7px 10px; border-bottom: 1px solid var(--line); vertical-align: top; }
  table.card th { width: 40%; color: var(--muted); font-weight: 500; }
  .list { display: grid; gap: 10px; padding: 0; list-style: none; grid-template-columns: repeat(auto-fill, minmax(min(100%, 240px), 1fr)); }
  .list a { display: block; background: var(--chip); border-radius: 14px; padding: 12px 16px; text-decoration: none; height: 100%; }
  .list b { font-size: 18px; }
  .badge { display: inline-block; font-size: 12px; padding: 2px 9px; border-radius: 99px; background: var(--beak); color: var(--beak-ink); font-weight: 700; }
  details { background: var(--chip); border-radius: 14px; padding: 10px 14px; margin-bottom: 8px; }
  summary { cursor: pointer; font-weight: 700; }
  details p { margin: 8px 0 2px; }
  .post-meta { color: var(--muted); font-size: 14px; }
</style>'''

def page(rel_url, title, desc, body, active=None, jsonld=None):
    links = ''.join(f'<a{" class=\"on\"" if key == active else ""} href="{href}">{esc(label)}</a>' for href, label, key in NAV_ITEMS)
    ld = f'\n<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>' if jsonld else ''
    return f'''<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{esc(title)} · DrawBird</title>
<meta name="description" content="{esc(desc)}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="/og-card.png">
<link rel="canonical" href="{rel_url}">
<link rel="icon" href="/icons/icon-192.png" type="image/png">
<link rel="stylesheet" href="/fonts/fonts.css">
<link rel="stylesheet" href="/sayfa.css">
{EXTRA_CSS}{ld}
</head>
<body>
<main>
<nav class="top">{links}</nav>
<article>
{body}
</article>
{FOOT}
</main>
</body>
</html>
'''

def write(rel_file, url, text, lastmod=None):
    path = os.path.join(PUBLIC, rel_file)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    io.open(path, 'w', encoding='utf-8', newline='\n').write(text)
    written.append((url, lastmod))

def finished(L):
    return svg([s[2] for s in L['steps']], len(L['steps']) - 1, full=True, label=L['bird'])

lesson_by_slug = {l['slug']: l for l in LESSONS}

# ---- lessons ----
for L in LESSONS:
    shapes = [s[2] for s in L['steps']]
    steps = ''.join(
        f'<div class="step">{svg(shapes, i)}<div><h3>{i + 1}. {esc(name)}</h3><p>{esc(text)}</p></div></div>'
        for i, (name, text, _) in enumerate(L['steps']))
    steps += (f'<div class="step">{finished(L)}<div><h3>Bitti!</h3>'
              f'<p>{esc(L["bird"])} hazır. Şimdi DrawBird’de çiz, adını koy ve gökyüzüne sal.</p></div></div>')
    mistakes = ''.join(f'<li>{esc(m)}</li>' for m in L['mistakes'])
    facts = ''.join(f'<li>{esc(f)}</li>' for f in L['facts'])
    related = [b for b in BIRDS if b['lesson'] == L['slug']]
    rel = ('<h2>Bu dersle çizebileceğin kuşlar</h2><ul class="list">' + ''.join(
        f'<li><a href="/kuslar/{b["slug"]}"><b>{esc(b["name"])}</b><br><span class="muted">{esc(b["lead"][:90])}…</span></a></li>' for b in related) + '</ul>') if related else ''
    body = f'''  <h1>{esc(L['title'])}</h1>
  <p><span class="badge">{esc(L['level'])}</span></p>
  <p>{esc(L['intro'])}</p>
  <p class="muted">Kesik çizgi, DrawBird çizim alanındaki kanat hattıdır: üstündekiler çırpar, altındakiler gövde olarak kalır.</p>
  <h2>Adım adım</h2>
  <div class="steps-grid">{steps}</div>
  <h2>Sık yapılan hatalar</h2>
  <ul>{mistakes}</ul>
  <h2>{esc(L['bird'])} hakkında bilmen gerekenler</h2>
  <ul class="facts">{facts}</ul>
  {rel}
  <p><a class="cta" href="/#ciz">Şimdi kendi {esc(L['acc'])} çiz</a></p>'''
    write(f"dersler/{L['slug']}.html", f"/dersler/{L['slug']}", page(f"/dersler/{L['slug']}", L['title'], L['intro'][:155], body, 'dersler'))

groups = ''.join(
    f'<h2>{lv}</h2><ul class="list">' + ''.join(
        f'<li><a href="/dersler/{L["slug"]}"><b>{esc(L["title"])}</b>{finished(L)}</a></li>'
        for L in LESSONS if L['level'] == lv) + '</ul>'
    for lv in ['Kolay', 'Orta', 'Zor'] if any(L['level'] == lv for L in LESSONS))
write('dersler/index.html', '/dersler/', page('/dersler/', 'Kuş çizim dersleri',
      f'{len(LESSONS)} adım adım kuş çizim dersi: serçe, martı, baykuş, flamingo, papağan ve daha fazlası. DrawBird gökyüzünde kanat çırpan kuşlar çiz.',
      f'  <h1>Kuş çizim dersleri</h1>\n  <p>{len(LESSONS)} ders, her biri beş adım. Hepsi DrawBird\'ün kanat hattına göre hazırlandı, yani çizdiğin kuş gökyüzünde gerçekten kanat çırpar. Kolaydan zora sıralı; ilk kez çiziyorsan serçeyle başla.</p>\n  {groups}\n  <p><a class="cta" href="/#ciz">Çizmeye başla</a></p>', 'dersler'))

# ---- birds ----
for i, B in enumerate(BIRDS):
    rows = ''.join(f'<tr><th>{esc(k)}</th><td>{esc(v)}</td></tr>' for k, v in B['table'])
    paras = ''.join(f'<p>{esc(p)}</p>' for p in B['body'])
    L = lesson_by_slug.get(B['lesson'])
    others = [BIRDS[(i + k) % len(BIRDS)] for k in (1, 2, 3)]
    more = ''.join(f'<li><a href="/kuslar/{o["slug"]}"><b>{esc(o["name"])}</b><br><span class="muted">{esc(o["lead"][:90])}…</span></a></li>' for o in others)
    lesson_link = f'<p><a href="/dersler/{L["slug"]}">Çizim dersi: {esc(L["title"])} →</a></p>' if L else ''
    own_html = f'<h2>Benim notum</h2><p>{esc(B["own"])}</p>' if B.get('own') else ''
    body = f'''  <h1>{esc(B['name'])}</h1>
  <p class="muted"><i>{esc(B['latin'])}</i></p>
  <p>{esc(B['lead'])}</p>
  <table class="card">{rows}</table>
  {paras}
  {own_html}
  <h2>DrawBird'de çizmek için</h2>
  <p>{esc(B['draw'])}</p>
  {lesson_link}
  <p><a class="cta" href="/#ciz">Kendi {esc(B['acc'])} çiz</a></p>
  <h2>Diğer kuşlar</h2>
  <ul class="list">{more}</ul>'''
    write(f"kuslar/{B['slug']}.html", f"/kuslar/{B['slug']}", page(f"/kuslar/{B['slug']}", f"{B['name']}: tanı ve çiz", B['lead'][:155], body, 'kuslar'))

trkey = lambda s: s.translate(str.maketrans('çğıİöşüÇĞÖŞÜ', 'cgiIosuCGOSU'))
items = ''.join(f'<li><a href="/kuslar/{B["slug"]}"><b>{esc(B["name"])}</b> <i class="muted">{esc(B["latin"])}</i><br><span class="muted">{esc(B["lead"][:110])}…</span></a></li>'
                for B in sorted(BIRDS, key=lambda b: trkey(b['name'])))
write('kuslar/index.html', '/kuslar/', page('/kuslar/', 'Türkiye\'nin kuşları',
      f'Türkiye\'de görebileceğin {len(BIRDS)} kuşu tanı, sonra DrawBird\'de çiz: kumru, leylek, flamingo, kelaynak ve daha fazlası.',
      f'  <h1>Türkiye\'nin kuşları</h1>\n  <p>Balkonundan, parktan, kıyıdan ve göllerden tanıyabileceğin {len(BIRDS)} kuş. Her sayfada kuşun boyu, ne yediği, nerede yaşadığı ve onu DrawBird\'de nasıl çizeceğin var.</p>\n  <ul class="list">{items}</ul>', 'kuslar'))

# ---- teachers, faq, about ----
write('ogretmenler.html', '/ogretmenler', page('/ogretmenler', TEACHERS['title'], TEACHERS['desc'],
      f'  <h1>{esc(TEACHERS["title"])}</h1>\n{TEACHERS["html"]}\n  <p><a class="cta" href="/#ciz">DrawBird\'ü aç</a></p>'))
faq_html = ''.join(f'<details><summary>{esc(q)}</summary><p>{a}</p></details>' for q, a in FAQ['items'])
faq_ld = {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
    {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in FAQ['items']]}
write('sss.html', '/sss', page('/sss', FAQ['title'], FAQ['desc'],
      f'  <h1>{esc(FAQ["title"])}</h1>\n  {faq_html}\n  <p>Cevabını bulamadın mı? <a href="https://github.com/gunayboss/drawbird/issues">GitHub üzerinden</a> sor.</p>', 'sss', faq_ld))
write('hakkinda.html', '/hakkinda', page('/hakkinda', ABOUT['title'], ABOUT['desc'], f'  <h1>{esc(ABOUT["title"])}</h1>\n{ABOUT["html"]}'))

# ---- blog ----
months = ['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran', 'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık']
fmt = lambda d: f'{int(d[8:10])} {months[int(d[5:7]) - 1]} {d[:4]}'
for P in POSTS:
    ld = {'@context': 'https://schema.org', '@type': 'BlogPosting', 'headline': P['title'], 'datePublished': P['date'], 'description': P['desc']}
    write(f"blog/{P['slug']}.html", f"/blog/{P['slug']}", page(f"/blog/{P['slug']}", P['title'], P['desc'],
          f'  <h1>{esc(P["title"])}</h1>\n  <p class="post-meta">{fmt(P["date"])}</p>\n{P["html"]}\n  <p><a href="/blog/">← Tüm yazılar</a></p>', 'blog', ld), P['date'])
posts = ''.join(f'<li><a href="/blog/{P["slug"]}"><b>{esc(P["title"])}</b><br><span class="post-meta">{fmt(P["date"])}</span><br><span class="muted">{esc(P["desc"])}</span></a></li>'
                for P in sorted(POSTS, key=lambda p: p['date'], reverse=True))
write('blog/index.html', '/blog/', page('/blog/', 'DrawBird blog', 'DrawBird\'den haberler, yeni özellikler, topluluğun öne çıkan kuşları ve aylık çizim meydan okumaları.',
      f'  <h1>Blog</h1>\n  <p>Yeni özellikler, topluluğun öne çıkan kuşları ve her ay bir çizim meydan okuması.</p>\n  <ul class="list">{posts}</ul>', 'blog'))

# ---- static page list for the Worker's sitemap ----
fixed = ['/', '/haftanin-kuslari', '/hafta/', '/nasil-oynanir', '/kosullar', '/gizlilik', '/kvkk', '/en/how-to-play', '/en/terms', '/en/privacy']
entries = [[u, None] for u in fixed] + [[u, m] for u, m in written]
io.open(os.path.join(ROOT, 'src', 'static_pages.js'), 'w', encoding='utf-8', newline='\n').write(
    '// Generated by tools/build_pages.py: static pages for sitemap.xml.\nexport const STATIC_PAGES = ' + json.dumps(entries, ensure_ascii=False) + ';\n')
print(len(written), 'sayfa')
