"""Backtest: how much of a held-out exam does the probable set (built without it) cover?
Usage: HOLDOUT='MAT 25-26' python3 rank.py && HOLDOUT='MAT 25-26' python3 backtest.py
A held-out question counts as covered when some card's question+answer is close to it (TF-IDF cosine > 0.5).
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
from sklearn.feature_extraction.text import TfidfVectorizer
HOLD = os.environ['HOLDOUT']
P = load_papers(); C = {r['i']: r for r in json.load(open('cls_final.json'))}
R = repo_cards(); I = json.load(open('items_holdout.json'))
def ans(i): q = P[i]; return q['opts'][q['ans'][0]] if q['ans'] else ''
hold = [i for i in C if C[i]['ch'] != 'other' and P[i]['exam'] == HOLD]
# the hold-out exam's own past-paper items must not count, so drop past items made only from it
I = [x for x in I if not (x['src'] == 'past' and all(P[m]['exam'] == HOLD for m in x['members']))]
qd = [P[i]['q'] + ' ' + ans(i) for i in hold]
setd = [x['q'].split(' || ')[0] + ' ' + x['a'].split(' || ')[0] for x in I]
repod = [r['q'] + ' ' + r['a'] for r in R]
v = TfidfVectorizer(analyzer='char_wb', ngram_range=(2, 4), sublinear_tf=True, min_df=2).fit(repod + setd + qd)
Q = v.transform(qd)
def cov(docs, thr=0.5):
    S = (Q @ v.transform(docs).T).max(axis=1).toarray().ravel()
    return (S > thr).sum()
t123 = cov(setd); t12 = cov([d for d, x in zip(setd, I) if x['tier'] <= 2]); full = cov(repod)
print(f'{HOLD}: {len(hold)} science questions')
print(f'  whole repo ({len(repod)} cards) covers {full} ({100*full/len(hold):.0f}%)')
print(f'  probable set ({len(setd)} cards, {100*len(setd)/len(repod):.0f}% of repo size) covers {t123} ({100*t123/len(hold):.0f}%)')
print(f'  T1+T2 only ({sum(1 for x in I if x["tier"] <= 2)} cards) covers {t12} ({100*t12/len(hold):.0f}%)')
