"""Builds the DrawBird logo family (concept A, "Kalem gaga") as clean SVG: no live text, no filters.

Run from the project root:  python brand/logo/make.py
Needs: pip install fonttools brotli  (wordmarks are outlined from the site's own OFL fonts in public/fonts).
"""
import io, os
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, '..', '..', 'public', 'fonts')
OUT = os.path.join(HERE, 'v2')
os.makedirs(OUT, exist_ok=True)

INK, SKY, SKY_DEEP, SKY_PALE, BEAK, WHITE, NIGHT = '#1b2740', '#7cc3ee', '#3f8fc9', '#e4f4ff', '#f2b705', '#ffffff', '#0d1630'
NEON_CYAN, NEON_PINK = '#38e1ff', '#ff4fa3'

# ---- the bird, on a 256 grid, centred optically (a hair above centre) ----
# Parts are drawn back to front: tail, pencil cone (its base hides under the body), body, wing, eye, graphite tip.
def bird(c, mono=False):
    """c: colours for tail, body, wing, beak, tip, eye, pupil. mono: one colour, details cut as gaps."""
    g = []
    if mono:
        k = c['body']
        g.append(f'<path fill="{k}" fill-rule="evenodd" d="M120 66a62 62 0 1 1 0 124a62 62 0 0 1 0-124Z'
                 ' M158 96a10 10 0 1 0 0 20a10 10 0 0 0 0-20Z M134 146Q108 110 70 120Q92 164 134 146Z"/>')
        g.append(f'<path fill="{k}" d="M168 102 202 117.1 202 134.9 168 150Z M207 119.3 222 126 207 132.7Z M70 110 30 90 46 142 74 148Z"/>')
        return ''.join(g)
    g.append(f'<path fill="{c["tail"]}" d="M70 110 30 90 46 142 74 148Z"/>')
    g.append(f'<path fill="{c["beak"]}" d="M166 101 207 119.3 207 132.7 166 151Z"/>')
    g.append(f'<path fill="{c["tip"]}" d="M207 119.3 222 126 207 132.7Z"/>')
    g.append(f'<circle cx="120" cy="128" r="62" fill="{c["body"]}"/>')
    g.append(f'<path fill="{c["wing"]}" d="M134 146Q108 110 70 120Q92 164 134 146Z"/>')
    g.append(f'<circle cx="158" cy="106" r="11" fill="{c["eye"]}"/><circle cx="161.5" cy="106" r="5.5" fill="{c["pupil"]}"/>')
    return ''.join(g)

def drawn_bird(stroke, beak, tip):
    """Line version: the bird looks just drawn, with the pencil's line still trailing from the tail."""
    w = 11
    return (f'<path fill="none" stroke="{stroke}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" '
            'd="M120 66a62 62 0 1 1 0 124a62 62 0 0 1 0-124Z M134 146Q108 110 74 121Q94 160 134 146Z M66 112C40 96 26 120 10 108"/>'
            f'<path fill="{beak}" d="M176 104 207 119.3 207 132.7 176 148Z"/><path fill="{tip}" d="M207 119.3 222 126 207 132.7Z"/>'
            f'<circle cx="160" cy="106" r="7" fill="{stroke}"/>')

# ---- outlined wordmarks ----
def font(name, wght):
    f = TTFont(os.path.join(FONTS, f'{name}-latin.woff2'))
    return instantiateVariableFont(f, {'wght': wght})

def text_path(f, s, size, x, y, track=0, kern=None):
    """Return (svg path d, advance width) for s set at baseline y."""
    gs, cmap, hmtx = f.getGlyphSet(), f.getBestCmap(), f['hmtx']
    scale = size / f['head'].unitsPerEm
    pen = SVGPathPen(gs)
    cx = 0
    for i, ch in enumerate(s):
        gname = cmap[ord(ch)]
        tp = TransformPen(pen, (scale, 0, 0, -scale, x + cx * scale, y))
        gs[gname].draw(tp)
        cx += hmtx[gname][0] + track + (kern or {}).get(s[i:i + 2], 0)
    return pen.getCommands(), cx * scale - track * scale

RUBIK = font('rubik', 700)
CAVEAT = font('caveat', 700)

def wordmark(style, x, y, size, ink, accent):
    """style 'solid': DrawBird in Rubik Bold. 'hand': 'Draw' handwritten (Caveat), 'Bird' solid (Rubik)."""
    if style == 'solid':
        d, w = text_path(RUBIK, 'DrawBird', size, x, y, track=-18, kern={'aw': -10, 'wB': 10})
        return f'<path fill="{ink}" d="{d}"/>', w
    d1, w1 = text_path(CAVEAT, 'Draw', size * 1.32, x, y + size * 0.02, track=-10)
    d2, w2 = text_path(RUBIK, 'Bird', size, x + w1 + size * 0.06, y, track=-16)
    return f'<path fill="{accent}" d="{d1}"/><path fill="{ink}" d="{d2}"/>', w1 + size * 0.06 + w2

def svg(w, h, body, bg=None, r=0):
    back = f'<rect width="{w}" height="{h}" rx="{r}" fill="{bg}"/>' if bg else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">{back}{body}</svg>\n'

def save(name, text):
    io.open(os.path.join(OUT, name), 'w', encoding='utf-8', newline='\n').write(text)

COLORWAYS = {
    'gece':  dict(tail=INK, body=INK, wing=SKY, beak=BEAK, tip=INK, eye=WHITE, pupil=INK),
    'gok':   dict(tail=SKY_DEEP, body=SKY, wing=WHITE, beak=BEAK, tip=INK, eye=WHITE, pupil=INK),
    'kart':  dict(tail=WHITE, body=WHITE, wing=SKY_PALE, beak=BEAK, tip=INK, eye=INK, pupil=WHITE),
    'neon':  dict(tail=NEON_PINK, body=NEON_CYAN, wing=NEON_PINK, beak=BEAK, tip=NIGHT, eye=NIGHT, pupil=WHITE),
}
save('sembol-gece.svg', svg(256, 256, bird(COLORWAYS['gece'])))
save('sembol-gok.svg', svg(256, 256, bird(COLORWAYS['gok'])))
save('sembol-koyu.svg', svg(256, 256, bird(dict(COLORWAYS['gece'], tail=WHITE, body=WHITE, wing=SKY, eye=INK, pupil=WHITE))))
save('sembol-tek-renk.svg', svg(256, 256, bird({'body': INK}, mono=True)))
save('sembol-cizgi.svg', svg(256, 256, drawn_bird(INK, BEAK, INK)))
save('ikon-gok.svg', svg(256, 256, f'<g transform="translate(26 26) scale(.8)">{bird(COLORWAYS["kart"])}</g>', SKY, 56))
save('ikon-neon.svg', svg(256, 256, f'<g transform="translate(26 26) scale(.8)">{bird(COLORWAYS["neon"])}</g>', NIGHT, 56))

for style in ('solid', 'hand'):
    for theme, (sym, ink, accent, bg) in {
        'acik': (bird(COLORWAYS['gece']), INK, SKY_DEEP, None),
        'koyu': (bird(dict(COLORWAYS['gece'], tail=WHITE, body=WHITE, wing=SKY, eye=INK, pupil=WHITE)), WHITE, SKY, NIGHT),
    }.items():
        wm, w = wordmark(style, 262, 170, 112, ink, accent)
        W = int(262 + w + 40)
        save(f'yatay-{style}-{theme}.svg', svg(W, 256, f'<g>{sym}</g>{wm}', bg))
    wm, w = wordmark(style, 0, 0, 96, INK, SKY_DEEP)
    W = int(max(w, 256) + 40)
    save(f'dikey-{style}.svg', svg(W, 400, f'<g transform="translate({(W - 256) / 2} 0)">{bird(COLORWAYS["gece"])}</g>'
                                         f'<g transform="translate({(W - w) / 2} 350)">{wm}</g>'))
# ---- site assets ----
# Maskable app icon: full-bleed square, bird inside the central safe zone (Android crops to a circle).
save('ikon-maskable.svg', svg(256, 256, f'<g transform="translate(43.5 43.5) scale(.66)">{bird(COLORWAYS["kart"])}</g>', SKY))
# Wordmark alone, for headers where the symbol sits next to it as its own image.
for theme, (ink, accent) in {'acik': (INK, SKY_DEEP), 'koyu': (WHITE, SKY)}.items():
    wm, w = wordmark('hand', 0, 118, 112, ink, accent)
    save(f'yazi-{theme}.svg', svg(int(w + 8), 150, wm))
# Share card (1200×630): sky, a few small birds, the stacked logo.
wm, w = wordmark('hand', 0, 0, 150, INK, SKY_DEEP)
flock = ''.join(f'<g transform="translate({x} {y}) scale({s})"{" opacity=\".55\"" if s < .4 else ""}>{bird(COLORWAYS[c])}</g>'
                for x, y, s, c in [(90, 70, .38, 'gok'), (960, 110, .32, 'gece'), (1010, 420, .42, 'gok'), (150, 430, .3, 'gece')])
save('og-card.svg', '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630">'
     f'<defs><linearGradient id="s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{SKY}"/><stop offset="1" stop-color="{SKY_PALE}"/></linearGradient></defs>'
     f'<rect width="1200" height="630" fill="url(#s)"/>{flock}'
     f'<g transform="translate(472 125) scale(1)">{bird(COLORWAYS["gece"])}</g>'
     f'<g transform="translate({(1200 - w) / 2} 500)">{wm}</g></svg>\n')
print('ok', sorted(os.listdir(OUT)))
