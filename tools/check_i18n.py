"""Checks that a translation file has exactly the shape of the Turkish source.

python tools/check_i18n.py en      (or several languages, or none for all)
"""
import importlib.util, os, re, sys

HERE = os.path.dirname(__file__)
def load(lang):
    spec = importlib.util.spec_from_file_location(lang, os.path.join(HERE, 'i18n_content', f'{lang}.py'))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return {k: getattr(m, k) for k in ('UI', 'LESSONS', 'BIRDS', 'PAGES', 'LEGAL', 'POSTS')}

PH = re.compile(r'\{[a-z]+\}')
TAG = re.compile(r'<(/?[a-z0-9]+)[^>]*>')
HREF = re.compile(r'href="([^"]+)"')

def compare(a, b, path, errs):
    if type(a) != type(b):
        errs.append(f'{path}: tür farklı ({type(a).__name__} / {type(b).__name__})'); return
    if isinstance(a, dict):
        for k in a:
            if k not in b: errs.append(f'{path}.{k}: eksik')
            else: compare(a[k], b[k], f'{path}.{k}', errs)
        for k in b:
            if k not in a: errs.append(f'{path}.{k}: fazla')
    elif isinstance(a, list):
        if len(a) != len(b): errs.append(f'{path}: {len(a)} öğe olmalı, {len(b)} var'); return
        for i, (x, y) in enumerate(zip(a, b)): compare(x, y, f'{path}[{i}]', errs)
    elif isinstance(a, str):
        if sorted(PH.findall(a)) != sorted(PH.findall(b)): errs.append(f'{path}: yer tutucular farklı {PH.findall(a)} / {PH.findall(b)}')
        if [t for t in TAG.findall(a)] != [t for t in TAG.findall(b)]: errs.append(f'{path}: HTML etiketleri farklı')
        if HREF.findall(a) != HREF.findall(b): errs.append(f'{path}: linkler farklı')
        if a.strip() and not b.strip(): errs.append(f'{path}: boş')

src = load('tr')
langs = sys.argv[1:] or [f[:-3] for f in os.listdir(os.path.join(HERE, 'i18n_content')) if f.endswith('.py') and f != 'tr.py' and not f.startswith('_')]
bad = 0
for lang in langs:
    try: tr = load(lang)
    except Exception as e: print(f'{lang}: YÜKLENEMEDİ {e}'); bad += 1; continue
    errs = []
    compare(src, tr, lang, errs)
    print(f'{lang}: {"tamam" if not errs else str(len(errs)) + " sorun"}')
    for e in errs[:40]: print('  ', e)
    bad += bool(errs)
sys.exit(1 if bad else 0)
