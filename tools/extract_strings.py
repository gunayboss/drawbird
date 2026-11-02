"""Lists the Turkish UI strings of public/index.html into public/i18n/_source.json.

Run from the project root:  python tools/extract_strings.py
The page translates at run time by looking each Turkish string up in public/i18n/<lang>.json;
`${...}` parts of template strings become {0}, {1}… placeholders.
"""
import io, json, re

s = io.open('public/index.html', encoding='utf-8').read()
body = s.split('<body>', 1)[1]
markup, script = body.split('<script>', 1)
LETTER = re.compile('[A-Za-zÇĞİÖŞÜçğıöşü]')
TURKISH = re.compile('[çğıöşüÇĞİÖŞÜ]|[a-z] [a-z]', re.I)
SKIP = re.compile(r'^[\w#./:@-]+$|=>|function|querySelector|\bpx\b|rgba|translate|^M\d|image/|data:|^\s|\s$|^[{}()\[\]]|https?:')

found = []
for m in re.finditer(r'>([^<>]+)<', markup):
    t = ' '.join(m.group(1).split())
    if t and LETTER.search(t): found.append(t)
for m in re.finditer(r'(?:placeholder|title|aria-label)="([^"]+)"', markup):
    found.append(m.group(1))

def literals(src):
    i, n = 0, len(src)
    while i < n:
        q = src[i]
        if q in '\'"`':
            j, buf = i + 1, []
            while j < n and src[j] != q:
                if src[j] == '\\': buf.append(src[j:j + 2]); j += 2; continue
                if q != '`' and src[j] == '\n': break
                buf.append(src[j]); j += 1
            yield q, ''.join(buf)
            i = j + 1
        elif src.startswith('//', i) and (i == 0 or src[i - 1] in ' \n;{'):
            i = src.find('\n', i)
            if i < 0: break
        else:
            i += 1

for q, t in literals(script):
    if q == '`':
        k = [0]
        def ph(_):
            k[0] += 1
            return '{%d}' % (k[0] - 1)
        t = re.sub(r'\$\{(?:[^{}]|\{[^{}]*\})*\}', ph, t)
    t = t.replace("\\'", "'").replace('\\n', '\n')
    if not t or not LETTER.search(t) or SKIP.search(t) or not TURKISH.search(t): continue
    found.append(t)

out = []
for f in found:
    if f not in out: out.append(f)
io.open('public/i18n/_source.json', 'w', encoding='utf-8', newline='\n').write(json.dumps(out, ensure_ascii=False, indent=1) + '\n')
print(len(out), 'metin')
