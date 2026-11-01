import sys, re, json, glob, os
from bs4 import BeautifulSoup, NavigableString

SUP = str.maketrans('0123456789+-−=()nxyabcdeikmoprst', '⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁻⁼⁽⁾ⁿˣʸᵃᵇᶜᵈᵉⁱᵏᵐᵒᵖʳˢᵗ')
SUB = str.maketrans('0123456789+-−=()aeoxhklmnpst', '₀₁₂₃₄₅₆₇₈₉₊₋₋₌₍₎ₐₑₒₓₕₖₗₘₙₚₛₜ')
GREEK = {'alpha':'α','beta':'β','gamma':'γ','delta':'δ','Delta':'Δ','theta':'θ','lambda':'λ','mu':'μ','pi':'π','rho':'ρ','sigma':'σ','Sigma':'Σ','omega':'ω','Omega':'Ω','epsilon':'ε','varepsilon':'ε','phi':'φ','eta':'η','tau':'τ','nu':'ν','times':'×','cdot':'·','circ':'°','degree':'°','rightarrow':'→','to':'→','longrightarrow':'→','leftarrow':'←','rightleftharpoons':'⇌','leftrightarrow':'↔','pm':'±','approx':'≈','neq':'≠','ne':'≠','leq':'≤','le':'≤','geq':'≥','ge':'≥','infty':'∞','propto':'∝','sqrt':'√','div':'÷','prime':'′','angle':'∠','Rightarrow':'⇒','uparrow':'↑','downarrow':'↓','hbar':'ħ','ldots':'…','cdots':'…','quad':' ','qquad':' ','partial':'∂','int':'∫','sum':'∑','triangle':'△','perp':'⊥','parallel':'∥','therefore':'∴','because':'∵','Omega':'Ω','AA':'Å','%':'%','rm':'','bf':'','mathrm':'','text':'','xrightarrow':'→','xleftarrow':'←','arrow':'→','longleftrightarrow':'⇌','begin':'','end':'','hspace':'','underline':'____','displaystyle':'','limits':'','circledR':'','overset':'','underset':'','mathbb':'','dfrac':'','tfrac':'','frac':'','sim':'~','ce':''}

def conv_script(s, table):
    s = s.strip()
    if table is SUP and s in ('০', 'o', 'circ', '°', '∘'): return '°'
    if table is SUP and s == 'H': return 'ᴴ'
    if s in ('′', "'"): return '′'
    t = s.translate(table)
    return t if all(c != o or c in ' ' for c, o in zip(t, s)) else ('^(' + s + ')' if table is SUP else '_(' + s + ')')

def latex2txt(s):
    s = s.replace('\\left', '').replace('\\right', '').replace('\\,', ' ').replace('\\;', ' ').replace('\\!', '').replace('\\ ', ' ')
    s = re.sub(r'\\(?:mathrm|mathbf|rm|bf|ce)\s*\{([^{}]*)\}', lambda m: m.group(1).replace(' ', '').replace('~', ' '), s)
    s = re.sub(r'\\(?:text|textbf|operatorname|mathit|textit|boldsymbol|vec|overrightarrow|hat|bar|overline)\s*\{([^{}]*)\}', r'\1', s)
    s = re.sub(r'\\hspace\s*\{[^{}]*\}', '', s)
    s = re.sub(r'\\(?:begin|end)\s*\{[^{}]*\}', ' ', s)
    s = re.sub(r'\\(?:mathrm|text|mathbf|textbf|rm)\s*\{([^{}]*)\}', r'\1', s)
    for _ in range(3):
        s = re.sub(r'\\[dt]?frac\s*\{([^{}]*)\}\s*\{([^{}]*)\}', r'(\1)/(\2)', s)
        s = re.sub(r'\\sqrt\s*\{([^{}]*)\}', r'√(\1)', s)
        s = re.sub(r'\\sqrt\s*\[([^\]]*)\]\s*\{([^{}]*)\}', r'\1√(\2)', s)
        s = re.sub(r'\\(?:mathrm|text|mathbf|textbf|operatorname|rm)\s*\{([^{}]*)\}', r'\1', s)
    s = re.sub(r'\\([A-Za-z]+)', lambda m: GREEK.get(m.group(1), m.group(1)), s)
    def sup(m):
        x = m.group(1) or m.group(2)
        return conv_script(x, SUP)
    def sub(m):
        x = m.group(1) or m.group(2)
        return conv_script(x, SUB)
    s = s.replace('^{°}', '°').replace('^°', '°').replace('^{∘}', '°').replace('^∘', '°').replace('∘', '°')
    s = re.sub(r'\^\s*\{([^{}]*)\}|\^\s*(\S)', sup, s)
    s = re.sub(r'_\s*\{([^{}]*)\}|_\s*(\S)', sub, s)
    s = s.replace('{', '').replace('}', '').replace('\\', '')
    s = s.replace('^(∘)', '°').replace('^∘', '°').replace('ᵒ', '°') if '∘' in s else s
    s = s.replace('~', ' ').replace('&', ' ')
    s = re.sub(r'p\^\(\s*H\s*\)|pᴴ', 'pH', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def clean(el):
    """Return text of a bs4 element with KaTeX converted and sub/sup handled."""
    if el is None: return ''
    el = BeautifulSoup(str(el), 'html.parser')
    for k in el.select('.katex-display, .katex'):
        ann = k.find('annotation')
        tex = ann.get_text() if ann else k.get_text()
        k.replace_with(NavigableString(' ' + latex2txt(tex) + ' '))
    for t in el.find_all('sup'):
        x = t.get_text(); t.replace_with(NavigableString(conv_script(x, SUP)))
    for t in el.find_all('sub'):
        x = t.get_text(); t.replace_with(NavigableString(conv_script(x, SUB)))
    for br in el.find_all(['br']):
        br.replace_with(NavigableString('\n'))
    for p in el.find_all(['p', 'li', 'div', 'tr', 'h1','h2','h3','h4']):
        p.insert_after(NavigableString('\n'))
    for img in el.find_all('img'):
        img.replace_with(NavigableString(' [চিত্র] '))
    txt = el.get_text()
    txt = txt.replace('\u200b', '').replace('\xa0', ' ')
    txt = re.sub(r'[pP]\s*\^?\(?ᴴ\)?|[pP]\^\(\s*H\s*\)', 'pH', txt)
    txt = txt.replace('ᶜirc', '°').replace('^(০)', '°').replace('^০', '°')
    lines = [re.sub(r'[ \t]+', ' ', l).strip() for l in txt.split('\n')]
    lines = [l for l in lines if l]
    return '\n'.join(lines)

def parse(path):
    soup = BeautifulSoup(open(path, encoding='utf-8', errors='ignore').read(), 'html.parser')
    # exam title
    title = None
    for d in soup.find_all(string=re.compile(r'(?i)(medical|dental).*(admission|test)?.*\d{4}-\d{2,4}')):
        title = d.strip(); break
    out = []
    section = None
    # iterate over h3 section headings and question cards in document order
    for el in soup.find_all(['h3', 'div']):
        if el.name == 'h3':
            t = el.get_text(strip=True)
            if re.search(r'\(\d+\)', t) or t.isupper():
                section = t
            continue
        cls = el.get('class') or []
        if not ('relative' in cls and 'rounded-xl' in cls and 'p-5' in cls):
            continue
        qdiv = el.find('div', class_=lambda c: c and 'mb-2' in c)
        if not qdiv: continue
        q = clean(qdiv)
        tags = [s.get_text(strip=True) for s in el.select('span.tag')]
        opts, ans = [], []
        for i, b in enumerate(el.find_all('button', class_=lambda c: c and 'items-center' in c and 'gap-3' in c)):
            span = b.find('span')
            body = b.find('div', class_=lambda c: c and 'flex-1' in c)
            text = clean(body)
            opts.append(text)
            if '017A47' in ' '.join(span.get('class') or []) or '017A47' in ' '.join(b.get('class') or []):
                ans.append(i)
        expl = ''
        sec = el.find('section')
        if sec:
            expl = clean(sec)
            expl = re.sub(r'^(\[চিত্র\]\s*)?ব্যাখ্যা\s*', '', expl).strip()
        q = re.sub(r'^\d+\.\s*', '', q)
        out.append(dict(section=section, q=q, opts=opts, ans=ans, tags=tags, expl=expl))
    return title, out

if __name__ == '__main__':
    res = []
    for f in sorted(glob.glob(os.path.join(sys.argv[1], '*.html'))):
        title, qs = parse(f)
        res.append(dict(file=os.path.basename(f), title=title, questions=qs))
        secs = {}
        for q in qs: secs[q['section']] = secs.get(q['section'], 0) + 1
        noans = sum(1 for q in qs if len(q['ans']) != 1)
        print(os.path.basename(f)[:25], title, len(qs), secs, 'noans', noans, file=sys.stderr)
    json.dump(res, open(sys.argv[2], 'w'), ensure_ascii=False, indent=1)
