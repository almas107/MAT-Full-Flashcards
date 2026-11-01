import glob, os, re, json, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
DATA = os.path.join(os.path.dirname(HERE), 'data')
os.chdir(DATA)
sys.path.insert(0, os.path.join(ROOT, 'webapp'))
import importlib.util
spec = importlib.util.spec_from_file_location('bd', os.path.join(ROOT, 'webapp/build_data.py'))
bd = importlib.util.module_from_spec(spec); spec.loader.exec_module(bd)
CHAPTERS = bd.CHAPTERS

def repo_cards():
    out = []
    for pattern, rx in bd.SOURCES:
        for path in glob.glob(os.path.join(ROOT, pattern)):
            m = re.search(rx, os.path.basename(path))
            paper, num = m.group(1) or 'b1', int(m.group(2))
            for topic, q, a, y in bd.parse(path):
                out.append(dict(ch=f'{paper}_{num:02d}', topic=topic, q=q, a=a, y=y))
    return out

def chname(key):
    p, n = key.split('_'); n = int(n)
    return CHAPTERS[p][0], CHAPTERS[p][2][n]

def subj_of(key):
    p = key.split('_')[0]
    return {'p1':'Physics','p2':'Physics','c1':'Chemistry','c2':'Chemistry','b1':'Botany','z':'Zoology'}.get(p, 'Other')

def load_papers():
    d = json.load(open(os.path.join(DATA, 'past_papers.json')))
    seen = set(); out = []
    for p in d:
        sig = tuple(q['q'] for q in p['questions'][:10])
        if sig in seen: continue
        seen.add(sig)
        t = p['title'] or ''
        m = re.search(r'(\d{4})-(\d{2,4})', t) or re.search(r'(\d{4})-(\d{2,4})', p['file'])
        if not m:
            # url form
            m = re.search(r'(\d{4})-(\d{4})', t)
        y1 = int(m.group(1)); 
        kind = 'MAT' if ('edical' in t or 'EDICAL' in t or 'medical' in p['file']) else ('DAT' if ('ental' in t or 'ENTAL' in t) else 'MAT')
        label = f'{kind} {y1%100:02d}-{(y1+1)%100:02d}'
        for i, q in enumerate(p['questions']):
            q['exam'] = label; q['year'] = y1 + 1; q['kind'] = kind; q['idx'] = i
            out.append(q)
    return out
