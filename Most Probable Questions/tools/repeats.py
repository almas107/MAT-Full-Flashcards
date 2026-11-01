import os, sys, json, re, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
from sklearn.feature_extraction.text import TfidfVectorizer
P = load_papers(); C = json.load(open('cls.json'))
ov = dict(l.split() for l in open('overrides.txt') if l.strip())
for r in C:
    r['ch'] = ov.get(str(r['i']), r['ch'])
json.dump(C, open('cls_final.json', 'w'), ensure_ascii=False)
def ans(q): return q['opts'][q['ans'][0]] if q['ans'] else ''
def norm(s): s = s.translate(str.maketrans('০১২৩৪৫৬৭৮৯', '0123456789')); return re.sub(r'[\s\-–—:;,.?।()\'"‘’“”]+', ' ', s).strip().lower()
idx = [r['i'] for r in C if r['ch'] != 'other']
qt = [norm(P[i]['q']) for i in idx]
at = [norm(ans(P[i])) for i in idx]
v = TfidfVectorizer(analyzer='char_wb', ngram_range=(2, 4), sublinear_tf=True).fit(qt + at)
Qm = v.transform(qt); Am = v.transform(at)
SQ = (Qm @ Qm.T).toarray(); SA = (Am @ Am.T).toarray()
n = len(idx)
# union-find
par = list(range(n))
def f(x):
    while par[x] != x: par[x] = par[par[x]]; x = par[x]
    return x
pairs = []
for a in range(n):
    for b in range(a + 1, n):
        short = min(len(qt[a]), len(qt[b])) < 28
        ok = SQ[a, b] > 0.55 and (SA[a, b] > 0.5 or SQ[a, b] > 0.85)
        if short: ok = SQ[a, b] > 0.8 and SA[a, b] > 0.7
        if ok:
            pairs.append((a, b, SQ[a, b], SA[a, b]))
            par[f(a)] = f(b)
from collections import defaultdict
groups = defaultdict(list)
for a in range(n): groups[f(a)].append(idx[a])
G = [g for g in groups.values() if len(g) > 1]
print('pairs', len(pairs), 'groups', len(G), 'multi-exam groups', sum(1 for g in G if len({P[i]['exam'] for i in g}) > 1))
json.dump([sorted(g) for g in groups.values()], open('groups.json', 'w'))
# print borderline pairs
import random; random.seed(1)
bl = [p for p in pairs if p[2] < 0.7]
for a, b, sq, sa in random.sample(bl, min(30, len(bl))):
    print(round(sq, 2), round(sa, 2), '|', P[idx[a]]['q'][:60], '=>', ans(P[idx[a]])[:20], '||', P[idx[b]]['q'][:60], '=>', ans(P[idx[b]])[:20])
