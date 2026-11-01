import os, sys, json, re, math, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
from collections import defaultdict, Counter
from sklearn.feature_extraction.text import TfidfVectorizer

P = load_papers(); C = {r['i']: r for r in json.load(open('cls_final.json'))}
R = repo_cards(); M = {int(k): v for k, v in json.load(open('match.json')).items()}
G = json.load(open('groups.json')); FIX = {int(k): v for k, v in json.load(open('fixes.json')).items()}
LET = 'কখগঘ'
# backtest: HOLDOUT='MAT 25-26' builds the set as if that exam had not happened yet
HOLD = os.environ.get('HOLDOUT')
if HOLD:
    for i in C:
        if P[i]['exam'] == HOLD: C[i]['ch'] = 'other'
    for r in R:
        r['y'] = ', '.join(t for t in r['y'].split(', ') if t != HOLD)
def bn(s): return s
def clean1(s): return re.sub(r'\s+', ' ', s.replace('||', '|')).strip()
def ans_text(i):
    q = P[i]
    if i in FIX: return FIX[i][0]
    return q['opts'][q['ans'][0]] if q['ans'] else ''
def ans_letter(i):
    q = P[i]
    if i in FIX:
        a = FIX[i][0]
        for k, o in enumerate(q['opts']):
            if o and a.startswith(o): return LET[k]
        return ''
    return LET[q['ans'][0]] if q['ans'] else ''

def exam_tags(y):
    out = []
    for t in y.split(','):
        t = t.strip()
        if re.match(r'^(MAT|DAT|AFMC) \d{1,2}-\d{1,2}$', t) or t == 'মেডিকেল ভর্তি প্রশ্ন': out.append(t)
    return out
def ylabel_key(t):
    m = re.match(r'(MAT|DAT|AFMC) (\d{1,2})-(\d{1,2})', t)
    if not m: return (0, t)
    y = int(m.group(2)); y = 2000 + y if y < 50 else 1900 + y
    return (y, m.group(1))
def exam_year(t):
    m = re.match(r'(MAT|DAT|AFMC) (\d{1,2})-(\d{1,2})', t)
    if not m: return 0
    y = int(m.group(3)); return 2000 + y if y < 50 else 1900 + y

# DAT/MAT 14-15 were one combined paper and 15-16 shares many questions; count each pair once
SAME_PAPER = {'DAT 14-15': 'MAT 14-15', 'DAT 15-16': 'MAT 15-16'}
def canon(e): return SAME_PAPER.get(e, e)

def short_expl(i):
    e = P[i]['expl']
    if not e or e.lower().startswith(('উত্তরঃ blank', 'ans: blank')): return ''
    lines = [l for l in e.split('\n') if l.strip() and not re.search(r'begin|frac|overset|xrightarrow|~~', l)]
    s = ' '.join(lines[:2])
    s = clean1(s)
    if len(s) > 170: s = s[:167].rsplit(' ', 1)[0] + ' …'
    return s

# merge groups whose questions map to the same repo card with the same answer
# (same question worded differently, e.g. "জেলিফিশ যে পর্বের..." / "জেলিফিশ কোন পর্বের...")
import unicodedata
def _nk(t): t = unicodedata.normalize('NFC', t); return re.sub(r'[\s\-–—:;,.?।()\'"‘’“”~]+', '', t).lower()
_by_card = {}
_merged = []
for g in G:
    g = [i for i in g if C[i]['ch'] != 'other']
    if not g: continue
    keys = {(M[i]['card'], _nk(ans_text(i))) for i in g if i in M and (M[i]['same'] or M[i]['sim'] > 0.6)}
    target = next((_by_card[k] for k in keys if k in _by_card), None)
    if target is None:
        target = len(_merged); _merged.append([])
    _merged[target].extend(g)
    for k in keys: _by_card.setdefault(k, target)
G = [g for g in _merged if g]

items = []
covered_cards = set()
# ---------- past-paper clusters ----------
for g in G:
    g = [i for i in g if C[i]['ch'] != 'other']
    if not g: continue
    exams = sorted({P[i]['exam'] for i in g}, key=ylabel_key)
    older = set()
    best_card = None
    for i in g:
        m = M.get(i)
        if not m: continue
        if m['same'] or m['sim'] > 0.6:
            covered_cards.add(m['card'])
            if best_card is None or m['sim'] > best_card[1]: best_card = (m['card'], m['sim'])
        if m['same'] or m['sim'] > 0.55:
            older.update(exam_tags(R[m['card']]['y']))
    allex = sorted(set(exams) | older, key=ylabel_key)
    n_recent = len(exams); n_all = len({canon(e) for e in allex})
    latest = max(P[i]['year'] for i in g)
    # representative: latest occurrence with a valid key
    rep = sorted(g, key=lambda i: (bool(P[i]['ans']) or i in FIX, P[i]['year']))[-1]
    ch = Counter(C[i]['ch'] for i in g).most_common(1)[0][0]
    score = 60 + 10 * (n_all - 1) + (6 if latest >= 2025 else 3 if latest >= 2022 else 0)
    score = min(100, score)
    tier = 1 if n_all >= 2 else 2
    q = P[rep]
    front = clean1(q['q']) + ' || ' + ' || '.join(f'{LET[k]}) {clean1(o)}' for k, o in enumerate(q['opts']))
    a = ans_text(rep); L = ans_letter(rep)
    back = (f'{L}) ' if L else '') + clean1(a)
    if rep in FIX and FIX[rep][1]: back += ' || নোট: ' + FIX[rep][1]
    else:
        import difflib
        def nk(t): return re.sub(r'[\s\-–—:;,.?।()\'"‘’“”~]+|হবে|হয়|টি$', '', t).lower()
        def same(a, b): 
            a, b = nk(a), nk(b)
            return bool(a) and bool(b) and (a in b or b in a or difflib.SequenceMatcher(None, a, b).ratio() > 0.6)
        ra = ans_text(rep); ropts = sorted(nk(o) for o in P[rep]['opts'])
        conflict, variants = set(), []
        for i in g:
            if i == rep or not ans_text(i): continue
            oo = sorted(nk(o) for o in P[i]['opts'])
            same_q = sum(1 for o in oo if any(same(o, p) for p in ropts)) >= 4
            if same_q and not same(ans_text(i), ra): conflict.add(f"{P[i]['exam']}: {clean1(ans_text(i))}")
            if not same_q and not same(ans_text(i), ra):
                v = f"{P[i]['exam']}: {clean1(P[i]['q'])[:90]} → {clean1(ans_text(i))}"
                if not any(same(v.split(': ', 1)[1], w.split(': ', 1)[1]) for w in variants): variants.append(v)
        if conflict: back += ' || নোট: অন্য বছরের key — ' + '; '.join(sorted(conflict))
        for v in variants[:2]: back += ' || অন্য রূপে এসেছে — ' + v
        ex = short_expl(rep)
        if ex: back += ' || ' + ex
    items.append(dict(src='past', ch=ch, tier=tier, score=score, q=front, a=back,
                      y=', '.join(allex), n=n_all, members=g, repo=best_card[0] if best_card else None,
                      covered=best_card is not None))
print('past items', len(items), 'tier1', sum(1 for x in items if x['tier'] == 1))

# ---------- repo PYQ cards not covered ----------
for j, r in enumerate(R):
    if j in covered_cards: continue
    ex = exam_tags(r['y'])
    if not ex: continue
    n = len({canon(e) for e in ex}); latest = max(exam_year(e) for e in ex)
    score = (66 if n >= 2 else 52) + 4 * min(n - 1, 3) + (4 if latest >= 2022 else 0)
    items.append(dict(src='repo', ch=r['ch'], tier=2 if n >= 2 else 3, score=min(score, 79), q=r['q'], a=r['a'],
                      y=', '.join(sorted(ex, key=ylabel_key)), n=n, repo=j, topic=r['topic']))
print('repo pyq items', sum(1 for x in items if x['src'] == 'repo'))

# ---------- hot non-PYQ repo cards ----------
sci = [i for i in C if C[i]['ch'] != 'other']
docsR = [r['q'] + ' ' + r['a'] for r in R]
docsP = [P[i]['q'] + ' ' + ans_text(i) for i in sci]
v = TfidfVectorizer(analyzer='char_wb', ngram_range=(2, 4), sublinear_tf=True, min_df=2).fit(docsR + docsP)
S = (v.transform(docsR) @ v.transform(docsP).T).tocsr()
fact = np.asarray(S.max(axis=1).todense()).ravel()
# topic hotness
tsize = Counter((r['ch'], r['topic']) for r in R)
thits = Counter()
for i in sci:
    m = M[i]; c = R[m['card']]
    if m['sim'] > 0.35: thits[(c['ch'], c['topic'])] += 1
chw = Counter(C[i]['ch'] for i in sci)
tot_w = sum(chw[k] + 3 for k in {r['ch'] for r in R})
BUDGET = int(os.environ.get('MP_BUDGET', 4200))
by_ch = defaultdict(list)
used = {x['repo'] for x in items if x.get('repo') is not None}
for j, r in enumerate(R):
    if j in used or j in covered_cards or exam_tags(r['y']): continue
    key = (r['ch'], r['topic'])
    th = thits[key] / math.sqrt(tsize[key])
    hot = 0.65 * fact[j] + 0.35 * min(th / 1.5, 1.0)
    by_ch[r['ch']].append((hot, j))
hotn = 0
for ch, lst in by_ch.items():
    quota = round(BUDGET * (chw[ch] + 3) / tot_w)
    quota = min(quota, int(float(os.environ.get('MP_CAP', 0.4)) * len(lst)))
    lst.sort(reverse=True)
    for rank, (hot, j) in enumerate(lst[:quota]):
        r = R[j]
        items.append(dict(src='hot', ch=ch, tier=3, score=int(30 + 19 * (1 - rank / max(quota, 1))), q=r['q'], a=r['a'],
                          y='', n=0, repo=j, topic=r['topic'], hot=round(float(hot), 3)))
        hotn += 1
print('hot items', hotn)
json.dump(items, open('items_holdout.json' if HOLD else 'items.json', 'w'), ensure_ascii=False)
c = Counter((subj_of(x['ch']), x['tier']) for x in items)
print(sorted(c.items()), len(items))
