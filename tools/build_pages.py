"""Builds DrawBird's content pages in every language into public/, plus the Worker's sitemap list and week-page strings.

Run from the project root:
  python tools/export_tr.py      # after editing Turkish content (content_*.py, ui_tr.py)
  python tools/build_pages.py
Turkish lives at the root (/dersler/serce), other languages under /<lang>/ (/en/dersler/serce).
A language is built only when tools/i18n_content/<lang>.py exists; run tools/check_i18n.py first.
"""
import html, importlib.util, io, json, os, re, sys

sys.path.insert(0, os.path.dirname(__file__))
from content_lessons import LESSONS as SHAPES
from content_birds import BIRDS as BIRD_META

HERE = os.path.dirname(__file__)
# Full site address for share cards and canonical links. Change it when the site moves to its own domain, then rebuild.
ORIGIN = 'https://drawbird.the-pit.workers.dev'
# AdSense. Empty = no ads anywhere (no script, no slots, no ads.txt, strict CSP). After approval fill in the
# publisher id ('ca-pub-…') and the two display ad unit ids, then rebuild and deploy.
# Keep Auto ads OFF in the AdSense account: these hand-placed slots are the only ad spots (none on the game).
ADSENSE_CLIENT = ''
AD_SLOTS = {'top': '', 'end': ''}
AD_LABEL = {'tr': 'Reklam', 'en': 'Advertisement', 'es': 'Publicidad', 'pt': 'Publicidade', 'fr': 'Publicité', 'de': 'Anzeige',
            'ru': 'Реклама', 'ar': 'إعلان', 'zh': '广告', 'ja': '広告', 'id': 'Iklan'}
# Text pages that carry ads (language-neutral path prefixes). Game, legal, profile and list pages never do.
AD_PATHS = ['/dersler/', '/kuslar/', '/blog/', '/sss', '/ogretmenler', '/hakkinda']
ROOT = os.path.join(HERE, '..')
PUBLIC = os.path.join(ROOT, 'public')
ALL_LANGS = ['tr', 'en', 'es', 'pt', 'fr', 'de', 'ru', 'ar', 'zh', 'ja', 'id']
NATIVE = {'tr': 'Türkçe', 'en': 'English', 'es': 'Español', 'pt': 'Português', 'fr': 'Français', 'de': 'Deutsch',
          'ru': 'Русский', 'ar': 'العربية', 'zh': '中文', 'ja': '日本語', 'id': 'Bahasa Indonesia'}
INK, GHOST = '#1b2740', '#c9d3e0'
esc = html.escape

def load(lang):
    spec = importlib.util.spec_from_file_location(f'i18n_{lang}', os.path.join(HERE, 'i18n_content', f'{lang}.py'))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m

def ready(lang):
    # Only languages whose file loads and passes tools/check_i18n.py are built (translations may be mid-write).
    if not os.path.exists(os.path.join(HERE, 'i18n_content', f'{lang}.py')): return False
    if lang == 'tr': return True
    import subprocess
    return subprocess.run([sys.executable, '-I', os.path.join(HERE, 'check_i18n.py'), lang], capture_output=True).returncode == 0
ONLY = [a for a in sys.argv[1:] if a in ALL_LANGS]
LANGS = [l for l in ALL_LANGS if (not ONLY or l in ONLY or l == 'tr') and ready(l)]
pre = lambda lang: '' if lang == 'tr' else f'/{lang}'

# Internal links inside translated HTML point at Turkish paths; move them into the page's language.
SECTIONS = 'dersler|kuslar|haftanin-kuslari|hafta|blog|sss|ogretmenler|hakkinda|nasil-oynanir|kosullar|gizlilik|kvkk'
def localize(text, lang):
    text = text.replace('.html"', '"')
    if lang == 'tr': return text
    text = re.sub(r'href="/(' + SECTIONS + r')([/"#])', lambda m: f'href="/{lang}/{m.group(1)}{m.group(2)}', text)
    text = text.replace('href="/#ciz"', f'href="/?lang={lang}#ciz"').replace('href="/#iletisim"', f'href="/?lang={lang}#iletisim"').replace('href="/"', f'href="/?lang={lang}"')
    return text

def svg(steps, upto, full=False, label=''):
    out = [f'<svg viewBox="0 0 240 180" role="img" aria-label="{esc(label)}" xmlns="http://www.w3.org/2000/svg">',
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

EXTRA_CSS = '''<style>
  .ad { margin: 28px 0; padding-top: 6px; border-top: 1px solid var(--line); min-height: 100px; }
  .ad-label { display: block; font-size: 11px; letter-spacing: .06em; text-transform: uppercase; color: var(--muted); margin-bottom: 4px; }
  .steps-grid { display: grid; gap: 18px; margin-top: 12px; }
  .step { display: grid; grid-template-columns: minmax(0, 240px) minmax(0, 1fr); gap: 16px; align-items: center; background: var(--chip); border-radius: 16px; padding: 12px; }
  .step svg, .list svg { width: 100%; height: auto; background: #ffffff; border-radius: 12px; }
  .list svg { margin-top: 8px; }
  .step h3 { margin: 0 0 4px; font-size: 18px; }
  .step p { margin: 0; }
  @media (max-width: 560px) { .step { grid-template-columns: 1fr; } }
  .facts { background: var(--chip); border-radius: 16px; padding: 4px 18px 4px 34px; }
  [dir="rtl"] .facts { padding: 4px 34px 4px 18px; }
  table.card { border-collapse: collapse; width: 100%; margin: 10px 0; }
  table.card th, table.card td { text-align: start; padding: 7px 10px; border-bottom: 1px solid var(--line); vertical-align: top; }
  table.card th { width: 40%; color: var(--muted); font-weight: 500; }
  .list { display: grid; gap: 10px; padding: 0; list-style: none; grid-template-columns: repeat(auto-fill, minmax(min(100%, 240px), 1fr)); }
  .list a { display: block; background: var(--chip); border-radius: 14px; padding: 12px 16px; text-decoration: none; height: 100%; }
  .list b { font-size: 18px; }
  .badge { display: inline-block; font-size: 12px; padding: 2px 9px; border-radius: 99px; background: var(--beak); color: var(--beak-ink); font-weight: 700; }
  details { background: var(--chip); border-radius: 14px; padding: 10px 14px; margin-bottom: 8px; }
  summary { cursor: pointer; font-weight: 700; }
  details p { margin: 8px 0 2px; }
  .post-meta { color: var(--muted); font-size: 14px; }
  .langs { margin-top: 8px; display: flex; flex-wrap: wrap; justify-content: center; gap: 4px 10px; }
  .langs a[aria-current] { font-weight: 700; text-decoration: none; }
</style>'''

written = []  # (url, lastmod)

def ad(lang, kind):
    """One labelled display ad unit, or '' while AdSense is not set up."""
    if not ADSENSE_CLIENT or not AD_SLOTS.get(kind):
        return ''
    return (f'<aside class="ad" aria-label="{AD_LABEL[lang]}"><span class="ad-label">{AD_LABEL[lang]}</span>'
            f'<ins class="adsbygoogle" style="display:block" data-ad-client="{ADSENSE_CLIENT}" data-ad-slot="{AD_SLOTS[kind]}" '
            f'data-ad-format="auto" data-full-width-responsive="true"></ins>'
            f'<script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script></aside>')

def with_ads(lang, body):
    """Free-text pages: one unit before the second heading (if any), one at the end."""
    top, end = ad(lang, 'top'), ad(lang, 'end')
    if not top and not end:
        return body
    first = body.find('<h2')
    second = body.find('<h2', first + 1) if first >= 0 else -1
    if second >= 0 and top:
        body = body[:second] + top + '\n' + body[second:]
    return body + '\n' + end

def page(lang, U, path, title, desc, body, active=None, jsonld=None):
    """path is the language-neutral path, e.g. '/dersler/serce'."""
    p = pre(lang)
    ads = ''
    if ADSENSE_CLIENT and any(path.startswith(a) and path != a or path == a and not a.endswith('/') for a in AD_PATHS):
        # Children use DrawBird, so every ad request asks for non-personalised ads.
        ads = (f'\n<script>(adsbygoogle = window.adsbygoogle || []).requestNonPersonalizedAds = 1;</script>'
               f'\n<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_CLIENT}" crossorigin="anonymous"></script>')
    nav_items = [(f'/?lang={lang}#ciz' if lang != 'tr' else '/#ciz', U['nav_draw'], None), (f'{p}/dersler/', U['nav_lessons'], 'dersler'),
                 (f'{p}/kuslar/', U['nav_birds'], 'kuslar'), (f'{p}/haftanin-kuslari', U['nav_week'], 'hafta'),
                 (f'{p}/blog/', U['nav_blog'], 'blog'), (f'{p}/sss', U['nav_faq'], 'sss')]
    links = ''.join(f'<a{" class=\"on\"" if key == active else ""} href="{href}">{esc(label)}</a>' for href, label, key in nav_items)
    foot = (f'<footer>DrawBird · <a href="{p}/hakkinda">{esc(U["foot_about"])}</a> · <a href="{p}/ogretmenler">{esc(U["foot_teachers"])}</a> · '
            f'<a href="{p}/nasil-oynanir">{esc(U["foot_howto"])}</a> · <a href="{p}/kosullar">{esc(U["foot_terms"])}</a> · '
            f'<a href="{p}/gizlilik">{esc(U["foot_privacy"])}</a> · <a href="{p}/kvkk">{esc(U["foot_kvkk"])}</a> · '
            f'<a href="{"/#iletisim" if lang == "tr" else f"/?lang={lang}#iletisim"}">{esc(U["foot_contact"])}</a> · '
            f'<a href="https://github.com/gunayboss/drawbird">{esc(U["foot_source"])}</a>'
            f'<div class="langs" aria-label="{esc(U["language"])}">' +
            ''.join(f'<a href="{pre(l)}{path}" hreflang="{l}" lang="{l}"{" aria-current=\"page\"" if l == lang else ""}>{NATIVE[l]}</a>' for l in LANGS) +
            '</div></footer>')
    alt = ''.join(f'\n<link rel="alternate" hreflang="{l}" href="{ORIGIN}{pre(l)}{path}">' for l in LANGS) + f'\n<link rel="alternate" hreflang="x-default" href="{ORIGIN}{path}">'
    ld = f'\n<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>' if jsonld else ''
    full = f'''<!doctype html>
<html lang="{lang}" dir="{'rtl' if lang == 'ar' else 'ltr'}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{esc(title)} · DrawBird</title>
<meta name="description" content="{esc(desc)}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{ORIGIN}/og-card.png">
<meta property="og:url" content="{ORIGIN}{p}{path}">
<link rel="canonical" href="{ORIGIN}{p}{path}">{alt}
<link rel="icon" href="/icons/icon-192.png" type="image/png">
<link rel="stylesheet" href="/fonts/fonts.css">
<link rel="stylesheet" href="/sayfa.css">
{EXTRA_CSS}{ld}{ads}
</head>
<body>
<main>
<nav class="top">{links}</nav>
<article>
{localize(body, lang)}
</article>
{foot}
</main>
</body>
</html>
'''
    rel = (p.lstrip('/') + '/' if p else '') + (path.strip('/') + '/index.html' if path.endswith('/') else path.strip('/') + '.html')
    out = os.path.join(PUBLIC, rel)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    io.open(out, 'w', encoding='utf-8', newline='\n').write(full)

def fmt_date(U, d):
    return U['date_format'].format(d=int(d[8:10]), month=U['months'][int(d[5:7]) - 1], y=d[:4])

shape_by_slug = {L['slug']: L for L in SHAPES}
meta_by_slug = {B['slug']: B for B in BIRD_META}
POST_DATES = {}
from content_pages import POSTS as TR_POSTS
for P in TR_POSTS: POST_DATES[P['slug']] = P['date']

for lang in LANGS:
    m = load(lang)
    U, LES, BIR, PAG, LEG, POS = m.UI, m.LESSONS, m.BIRDS, m.PAGES, m.LEGAL, m.POSTS
    p = pre(lang)
    levels = {'Kolay': U['level_easy'], 'Orta': U['level_medium'], 'Zor': U['level_hard']}

    # lessons
    for L in SHAPES:
        t = LES[L['slug']]
        shapes = [s[2] for s in L['steps']]
        steps = ''.join(f'<div class="step">{svg(shapes, i, label=U["step_n"].format(n=i + 1))}<div><h3>{i + 1}. {esc(n)}</h3><p>{esc(x)}</p></div></div>'
                        for i, (n, x) in enumerate(t['steps']))
        steps += (f'<div class="step">{svg(shapes, len(shapes) - 1, full=True, label=U["finished_label"])}<div><h3>{esc(U["done"])}</h3>'
                  f'<p>{esc(U["done_text"].format(bird=t["bird"]))}</p></div></div>')
        related = [b for b in BIRD_META if b['lesson'] == L['slug']]
        rel = (f'<h2>{esc(U["related_birds"])}</h2><ul class="list">' + ''.join(
            f'<li><a href="/kuslar/{b["slug"]}"><b>{esc(BIR[b["slug"]]["name"])}</b><br><span class="muted">{esc(BIR[b["slug"]]["lead"][:90])}…</span></a></li>'
            for b in related) + '</ul>') if related else ''
        body = (f'  <h1>{esc(t["title"])}</h1>\n  <p><span class="badge">{esc(levels[L["level"]])}</span></p>\n  <p>{esc(t["intro"])}</p>\n'
                f'  <p class="muted">{esc(U["wing_note"])}</p>\n  {ad(lang, "top")}\n  <h2>{esc(U["step_by_step"])}</h2>\n  <div class="steps-grid">{steps}</div>\n'
                f'  <h2>{esc(U["mistakes"])}</h2>\n  <ul>{"".join(f"<li>{esc(x)}</li>" for x in t["mistakes"])}</ul>\n'
                f'  <h2>{esc(U["about_bird"].format(bird=t["bird"]))}</h2>\n  <ul class="facts">{"".join(f"<li>{esc(x)}</li>" for x in t["facts"])}</ul>\n'
                f'  {rel}\n  <p><a class="cta" href="/#ciz">{esc(t["cta"])}</a></p>\n  {ad(lang, "end")}')
        page(lang, U, f'/dersler/{L["slug"]}', t['title'], t['intro'][:155], body, 'dersler')
        written.append((f'{p}/dersler/{L["slug"]}', None))
    groups = ''.join(
        f'<h2>{esc(levels[lv])}</h2><ul class="list">' + ''.join(
            f'<li><a href="/dersler/{L["slug"]}"><b>{esc(LES[L["slug"]]["title"])}</b>{svg([s[2] for s in L["steps"]], len(L["steps"]) - 1, full=True, label=LES[L["slug"]]["bird"])}</a></li>'
            for L in SHAPES if L['level'] == lv) + '</ul>'
        for lv in ['Kolay', 'Orta', 'Zor'] if any(L['level'] == lv for L in SHAPES))
    n = len(SHAPES)
    page(lang, U, '/dersler/', U['lessons_title'], U['lessons_desc'].format(n=n),
         f'  <h1>{esc(U["lessons_title"])}</h1>\n  <p>{esc(U["lessons_intro"].format(n=n))}</p>\n  {groups}\n  <p><a class="cta" href="/#ciz">{esc(U["start_drawing"])}</a></p>', 'dersler')
    written.append((f'{p}/dersler/', None))

    # birds
    for i, B in enumerate(BIRD_META):
        t = BIR[B['slug']]
        rows = ''.join(f'<tr><th>{esc(k)}</th><td>{esc(v)}</td></tr>' for k, v in zip(U['tbl'], t['table']))
        own = f'<h2>{esc(U["my_note"])}</h2><p>{esc(t["own"])}</p>' if t.get('own') else ''
        lesson = LES.get(B['lesson'])
        others = [BIRD_META[(i + k) % len(BIRD_META)] for k in (1, 2, 3)]
        more = ''.join(f'<li><a href="/kuslar/{o["slug"]}"><b>{esc(BIR[o["slug"]]["name"])}</b><br><span class="muted">{esc(BIR[o["slug"]]["lead"][:90])}…</span></a></li>' for o in others)
        body = (f'  <h1>{esc(t["name"])}</h1>\n  <p class="muted"><i>{esc(B["latin"])}</i></p>\n  <p>{esc(t["lead"])}</p>\n  <table class="card">{rows}</table>\n  {ad(lang, "top")}\n'
                f'  {"".join(f"<p>{esc(x)}</p>" for x in t["body"])}\n  {own}\n  <h2>{esc(U["draw_it"])}</h2>\n  <p>{esc(t["draw"])}</p>\n'
                + (f'  <p><a href="/dersler/{B["lesson"]}">{esc(U["lesson_link"].format(title=lesson["title"]))}</a></p>\n' if lesson else '')
                + f'  <p><a class="cta" href="/#ciz">{esc(t["cta"])}</a></p>\n  <h2>{esc(U["other_birds"])}</h2>\n  <ul class="list">{more}</ul>\n  {ad(lang, "end")}')
        page(lang, U, f'/kuslar/{B["slug"]}', U['bird_title'].format(name=t['name']), t['lead'][:155], body, 'kuslar')
        written.append((f'{p}/kuslar/{B["slug"]}', None))
    items = ''.join(f'<li><a href="/kuslar/{B["slug"]}"><b>{esc(BIR[B["slug"]]["name"])}</b> <i class="muted">{esc(B["latin"])}</i><br><span class="muted">{esc(BIR[B["slug"]]["lead"][:110])}…</span></a></li>'
                    for B in sorted(BIRD_META, key=lambda b: BIR[b['slug']]['name'].casefold()))
    n = len(BIRD_META)
    page(lang, U, '/kuslar/', U['birds_title'], U['birds_desc'].format(n=n),
         f'  <h1>{esc(U["birds_title"])}</h1>\n  <p>{esc(U["birds_intro"].format(n=n))}</p>\n  <ul class="list">{items}</ul>', 'kuslar')
    written.append((f'{p}/kuslar/', None))

    # teachers, faq, about
    T = PAG['ogretmenler']
    page(lang, U, '/ogretmenler', T['title'], T['desc'], f'  <h1>{esc(T["title"])}</h1>\n{with_ads(lang, T["html"])}\n  <p><a class="cta" href="/#ciz">{esc(U["open_drawbird"])}</a></p>')
    F = PAG['sss']
    faq_ld = {'@context': 'https://schema.org', '@type': 'FAQPage', 'inLanguage': lang, 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': localize(a, lang)}} for q, a in F['items']]}
    page(lang, U, '/sss', F['title'], F['desc'],
         f'  <h1>{esc(F["title"])}</h1>\n  {"".join(f"<details><summary>{esc(q)}</summary><p>{a}</p></details>" for q, a in F["items"])}\n  <p>{U["faq_more"]}</p>\n  {ad(lang, "end")}', 'sss', faq_ld)
    A = PAG['hakkinda']
    page(lang, U, '/hakkinda', A['title'], A['desc'], f'  <h1>{esc(A["title"])}</h1>\n{with_ads(lang, A["html"])}')
    written += [(f'{p}/ogretmenler', None), (f'{p}/sss', None), (f'{p}/hakkinda', None)]

    # legal and how-to
    for slug, Lg in LEG.items():
        page(lang, U, f'/{slug}', Lg['title'], Lg['desc'], f'  <h1>{esc(Lg["title"])}</h1>\n  {Lg["html"]}')
        written.append((f'{p}/{slug}', None))

    # blog
    for slug, P in POS.items():
        d = POST_DATES[slug]
        ld = {'@context': 'https://schema.org', '@type': 'BlogPosting', 'headline': P['title'], 'datePublished': d, 'description': P['desc'], 'inLanguage': lang}
        page(lang, U, f'/blog/{slug}', P['title'], P['desc'],
             f'  <h1>{esc(P["title"])}</h1>\n  <p class="post-meta">{fmt_date(U, d)}</p>\n{with_ads(lang, P["html"])}\n  <p><a href="/blog/">{esc(U["all_posts"])}</a></p>', 'blog', ld)
        written.append((f'{p}/blog/{slug}', d))
    posts = ''.join(f'<li><a href="/blog/{s}"><b>{esc(P["title"])}</b><br><span class="post-meta">{fmt_date(U, POST_DATES[s])}</span><br><span class="muted">{esc(P["desc"])}</span></a></li>'
                    for s, P in sorted(POS.items(), key=lambda kv: POST_DATES[kv[0]], reverse=True))
    page(lang, U, '/blog/', U['blog_title'], U['blog_desc'],
         f'  <h1>{esc(U["blog_heading"])}</h1>\n  <p>{esc(U["blog_intro"])}</p>\n  <ul class="list">{posts}</ul>', 'blog')
    written.append((f'{p}/blog/', None))

# ---- for the Worker: sitemap list and week-page strings ----
WEEK_KEYS = ['nav_draw', 'nav_lessons', 'nav_birds', 'nav_week', 'nav_blog', 'nav_faq', 'foot_about', 'foot_teachers', 'foot_terms',
             'foot_privacy', 'foot_kvkk', 'foot_source', 'foot_contact', 'months', 'date_format'] + [k for k in load('tr').UI if k.startswith(('week', 'archive', 'weekpage', 'card_', 'prev_', 'next_', 'share_'))] + ['an_artist']
week_ui = {l: {k: load(l).UI[k] for k in WEEK_KEYS} for l in LANGS}
fixed = []
for l in LANGS:
    fixed += [[f'{pre(l)}/haftanin-kuslari', 'today'], [f'{pre(l)}/hafta/', None]]
entries = [['/', 'today']] + fixed + [[u, d] for u, d in written]
io.open(os.path.join(ROOT, 'src', 'static_pages.js'), 'w', encoding='utf-8', newline='\n').write(
    '// Generated by tools/build_pages.py.\n'
    f'export const LANGS = {json.dumps(LANGS)};\n'
    f'export const STATIC_PAGES = {json.dumps(entries, ensure_ascii=False)};\n'
    f'export const WEEK_UI = {json.dumps(week_ui, ensure_ascii=False)};\n')
g = os.path.join(PUBLIC, 'index.html')
gs = io.open(g, encoding='utf-8').read()
gs = re.sub(r'<meta property="og:image" content="[^"]*">', f'<meta property="og:image" content="{ORIGIN}/og-card.png">', gs)
gs = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{ORIGIN}/">', gs)
io.open(g, 'w', encoding='utf-8', newline='\n').write(gs)
ads_txt = os.path.join(PUBLIC, 'ads.txt')
if ADSENSE_CLIENT:
    io.open(ads_txt, 'w', encoding='utf-8', newline='\n').write(f'google.com, {ADSENSE_CLIENT.replace("ca-", "")}, DIRECT, f08c47fec0942fa0\n')
elif os.path.exists(ads_txt):
    os.remove(ads_txt)
# Ad pages need Google's ad hosts in their CSP; every other page keeps the strict policy from the top of _headers.
hp = os.path.join(PUBLIC, '_headers')
hs = re.sub(r'\n# ads:start.*?# ads:end\n', '\n', io.open(hp, encoding='utf-8').read(), flags=re.S)
if ADSENSE_CLIENT:
    csp = ("default-src 'self'; script-src 'self' 'unsafe-inline' https:; style-src 'self' 'unsafe-inline'; font-src 'self'; "
           "img-src 'self' data: blob: https:; connect-src 'self' https:; frame-src https:; object-src 'none'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'")
    # _headers allows 100 rules in all, so one rule per path covers every language prefix through :lang.
    rules = [f'{lp}{a}*' if a.endswith('/') else f'{lp}{a}' for a in AD_PATHS for lp in ('', '/:lang')]
    hs = hs.rstrip('\n') + '\n# ads:start\n' + ''.join(f'{r}\n  ! Content-Security-Policy\n  Content-Security-Policy: {csp}\n' for r in rules) + '# ads:end\n'
io.open(hp, 'w', encoding='utf-8', newline='\n').write(hs)
print(len(LANGS), 'dil,', len(written), 'sayfa:', ', '.join(LANGS))
