import os, sys, re, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter, defaultdict

P = load_papers()
R = repo_cards()

def sec_subj(s):
    s = (s or '').lower()
    if any(k in s for k in ['english', 'gk', 'সাধারণ', 'general', 'মানবিক']): return 'Other'
    if any(k in s for k in ['chem', 'রসায়ন']): return 'Chemistry'
    if any(k in s for k in ['phys', 'পদার্থ']): return 'Physics'
    if any(k in s for k in ['bio', 'জীব']): return 'Biology'
    return None

def qtext(q):
    a = q['opts'][q['ans'][0]] if q['ans'] else ''
    return q['q'] + ' ' + ' '.join(q['opts']) + ' ' + a + ' ' + q['expl'][:300]

docs = [r['q'] + ' ' + r['a'] for r in R]
labels = [r['ch'] for r in R]
# Other-class training: labelled English/GK questions
for q in P:
    if sec_subj(q['section']) == 'Other':
        docs.append(qtext(q)); labels.append('other')
vec = TfidfVectorizer(analyzer='char_wb', ngram_range=(2, 4), sublinear_tf=True, min_df=2, max_features=400000)
X = vec.fit_transform(docs)
Q = vec.transform([qtext(q) for q in P])
labels = np.array(labels)
S = (Q @ X.T).tocsr()
res = []
for i, q in enumerate(P):
    row = S.getrow(i).toarray().ravel()
    # exclude self (other-class training doc of same question)
    top = np.argsort(-row)[:25]
    sc = defaultdict(float)
    for j in top:
        sc[labels[j]] += row[j] ** 2
    ss = sec_subj(q['section'])
    def ok(lbl):
        if ss is None: return True
        if ss == 'Other': return lbl == 'other'
        if ss == 'Biology': return lbl.startswith(('b1', 'z'))
        if ss == 'Chemistry': return lbl.startswith('c')
        if ss == 'Physics': return lbl.startswith('p')
    cand = sorted(((v, k) for k, v in sc.items() if ok(k)), reverse=True)
    if not cand:
        cand = [(0, 'other' if ss == 'Other' else '?')]
    tot = sum(v for v, _ in cand) or 1
    best, conf = cand[0][1], cand[0][0] / tot
    second = cand[1][1] if len(cand) > 1 else ''
    res.append(dict(i=i, ch=best, conf=round(conf, 2), alt=second, top=round(float(row[top[0]]), 2), ss=ss,
                    ))
json.dump(res, open('cls.json', 'w'), ensure_ascii=False)
c = Counter(r['ch'] for r in res)
print(sorted(c.items()))
print('lowconf', sum(1 for r in res if r['conf'] < 0.5))
