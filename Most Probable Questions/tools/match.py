import os, sys, json, re, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
from sklearn.feature_extraction.text import TfidfVectorizer
P = load_papers(); C = json.load(open('cls_final.json')); R = repo_cards()
def ans(q): return q['opts'][q['ans'][0]] if q['ans'] else ''
sci = [r for r in C if r['ch'] != 'other']
docsR = [r['q'] + ' ' + r['a'] for r in R]
docsP = [P[r['i']]['q'] + ' ' + ans(P[r['i']]) for r in sci]
v = TfidfVectorizer(analyzer='char_wb', ngram_range=(2, 4), sublinear_tf=True, min_df=2).fit(docsR + docsP)
XR = v.transform(docsR); XP = v.transform(docsP)
S = (XP @ XR.T).tocsr()
out = {}
for k, r in enumerate(sci):
    row = S.getrow(k).toarray().ravel()
    top = np.argsort(-row)[:5]
    q = P[r['i']]
    best = None
    for j in top:
        ys = R[j]['y']
        same_exam = q['exam'] in ys or q['exam'].replace('DAT', 'MAT') in ys
        if row[j] > 0.45 and same_exam:
            best = (int(j), float(row[j]), True); break
    if best is None:
        j = int(top[0]); best = (j, float(row[j]), False)
    out[r['i']] = dict(card=best[0], sim=round(best[1], 3), same=best[2])
json.dump(out, open('match.json', 'w'))
sims = np.array([o['sim'] for o in out.values()]); same = sum(o['same'] for o in out.values())
print('same-exam matches', same, 'of', len(out))
for t in (0.4, 0.5, 0.6, 0.7): print(t, (sims > t).sum())
import random; random.seed(5)
ks = [k for k, o in out.items() if not o['same'] and 0.5 < o['sim'] < 0.7]
for k in random.sample(ks, 15):
    o = out[k]; q = P[k]; c = R[o['card']]
    print(o['sim'], '|', q['q'][:55], '=>', ans(q)[:20], '||', c['q'][:55], '=>', c['a'][:25], c['y'][:20])
