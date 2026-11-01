"""Turn the ranked items (data/items.json) into the probable-question set.

Writes
  ../source/mp_<subject>.txt          card source, one file per subject
  ../lists/Most_Probable_<Subject>.md readable / printable list
  ../data/chapter_stats.json          per-chapter counts used in the README

Source format (read by build_decks.py here and by ../../webapp/build_data.py):
  # [p1_05] T1 | <topic>      chapter key, tier, topic
  Q: front  (" || " = line break)
  A: back
  Y: exam years (optional)
  R: probability score 0-100
  L: <chapter> | <question>   (optional) the existing repo card that already covers this past question;
     the web app ranks that card instead of adding the MCQ again
"""
import os, sys, re, json
from collections import defaultdict, Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

OUT = os.path.dirname(DATA)
SUBJ_FILE = {'Physics': 'physics', 'Chemistry': 'chemistry', 'Botany': 'botany', 'Zoology': 'zoology'}
SUBJ_BN = {'Physics': 'পদার্থবিজ্ঞান', 'Chemistry': 'রসায়ন', 'Botany': 'উদ্ভিদবিজ্ঞান', 'Zoology': 'প্রাণিবিজ্ঞান'}
TIER = {1: 'T1 | বারবার এসেছে (২ বা বেশি বার)',
        2: 'T2 | আগে এসেছে',
        3: 'T3 | সম্ভাব্য'}
SAME_PAPER = {'DAT 14-15': 'MAT 14-15', 'DAT 15-16': 'MAT 15-16'}
PAPER_ORDER = ['p1', 'p2', 'c1', 'c2', 'b1', 'z']
BN = str.maketrans('0123456789', '০১২৩৪৫৬৭৮৯')


def ch_sort(k):
    p, n = k.split('_')
    return (PAPER_ORDER.index(p), int(n))


def norm(s):
    return re.sub(r'[\s\?।,;:\-—–\'"‘’“”()|]+', '', s).lower()


def load_new():
    """Hand-written cards for gaps in the repo (Chem 1st paper Ch2 part 1)."""
    out, topic, q = [], None, None
    for line in open(os.path.join(OUT, 'source', 'new_c1_ch02_part1.txt'), encoding='utf-8'):
        line = line.strip()
        if line.startswith('# '):
            topic = line[2:]
        elif line.startswith('Q: '):
            q = line[3:]
        elif line.startswith('A: '):
            out.append(dict(src='new', ch='c1_02', tier=3, score=50, q=q, a=line[3:], y='', topic='নতুন: ' + topic))
        elif line.startswith('Y: '):
            out[-1]['y'] = line[3:]
            out[-1]['score'] = 58
    return out


def main():
    global REPO
    REPO = repo_cards()
    items = json.load(open('items.json')) + load_new()
    for it in items:
        it['q'] = it['q'].replace('\n', ' ')
        it['a'] = it['a'].replace('\n', ' ')
    # topic used in the source header
    for it in items:
        if it['src'] == 'past':
            it['topic'] = 'পূর্ববর্তী MAT/DAT প্রশ্ন (২০১৪–২০২৬)'
        elif it['src'] in ('repo', 'hot'):
            it['topic'] = 'রিপোর কার্ড'
    # dedupe identical fronts inside a chapter (keep highest score, merge years)
    seen = {}
    keep = []
    for it in sorted(items, key=lambda x: -x['score']):
        k = (it['ch'], norm(it['q']))
        if k in seen:
            o = seen[k]
            ys = [y for y in o['y'].split(', ') if y]
            o['y'] = ', '.join(ys + [y for y in it['y'].split(', ') if y and y not in ys])
            continue
        seen[k] = it
        keep.append(it)
    items = keep

    by_subj = defaultdict(list)
    for it in items:
        by_subj[subj_of(it['ch'])].append(it)
    os.makedirs(os.path.join(OUT, 'lists'), exist_ok=True)
    summary = {}
    for subj, lst in by_subj.items():
        lst.sort(key=lambda x: (x['tier'], ch_sort(x['ch']), x['src'] == 'new', -x['score']))
        lines, md = [], []
        last = None
        tier_counts = Counter(x['tier'] for x in lst)
        md.append(f'# সবচেয়ে সম্ভাব্য প্রশ্ন — {SUBJ_BN[subj]}\n')
        md.append(f'মোট {len(lst)}টি প্রশ্ন। T1 = {tier_counts[1]}, T2 = {tier_counts[2]}, T3 = {tier_counts[3]}। '
                  'প্রতিটি অংশের ভেতরে প্রশ্নগুলো সম্ভাবনার স্কোর অনুযায়ী সাজানো (বেশি থেকে কম)।\n')
        md_last_tier, md_last_ch, num = None, None, 0
        for it in lst:
            head = f"# [{it['ch']}] T{it['tier']} | {it['topic']}"
            if head != last:
                lines.append('')
                lines.append(head)
                last = head
            lines.append('Q: ' + it['q'])
            lines.append('A: ' + it['a'])
            if it['y']:
                lines.append('Y: ' + it['y'])
            lines.append(f"R: {it['score']}")
            if it['src'] == 'past' and it.get('covered') and it.get('repo') is not None:
                rc = REPO[it['repo']]
                lines.append(f"L: {rc['ch']} | {rc['q']}")
            # readable list
            if it['tier'] != md_last_tier:
                md.append(f"\n## {TIER[it['tier']]}\n")
                md_last_tier, md_last_ch = it['tier'], None
            if it['ch'] != md_last_ch:
                paper, chn = chname(it['ch'])
                md.append(f"\n### {paper} · অধ্যায় {str(int(it['ch'].split('_')[1])).translate(BN)} — {chn}\n")
                md_last_ch = it['ch']
                num = 0
            num += 1
            parts = it['q'].split(' || ')
            qtxt = parts[0]
            opts = '  \n'.join('&nbsp;&nbsp;' + p for p in parts[1:])
            ans = it['a'].replace(' || ', '  \n')
            yr = f" *({it['y']})*" if it['y'] else ''
            md.append(f"**{str(num).translate(BN)}.** {qtxt}{yr}  \n" + (opts + '  \n' if opts else '') +
                      f"**উত্তর:** {ans}\n")
        with open(os.path.join(OUT, 'source', f'mp_{SUBJ_FILE[subj]}.txt'), 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines).lstrip() + '\n')
        with open(os.path.join(OUT, 'lists', f'Most_Probable_{subj}.md'), 'w', encoding='utf-8') as f:
            f.write('\n'.join(md) + '\n')
        summary[subj] = dict(total=len(lst), t1=tier_counts[1], t2=tier_counts[2], t3=tier_counts[3],
                             new=sum(1 for x in lst if x['src'] == 'new'),
                             past=sum(1 for x in lst if x['src'] == 'past'))
        print(subj, summary[subj])

    # chapter statistics from the 2014-2026 papers
    P = load_papers()
    C = json.load(open('cls_final.json'))
    G = json.load(open('groups.json'))
    sci = [r for r in C if r['ch'] != 'other']
    exams = sorted({P[r['i']]['exam'] for r in C})
    cnt = Counter(r['ch'] for r in sci)
    recent = Counter(r['ch'] for r in sci if P[r['i']]['year'] >= 2023)
    n_recent_exams = len({P[r['i']]['exam'] for r in C if P[r['i']]['year'] >= 2023})
    rep = Counter()
    chof = {r['i']: r['ch'] for r in C}
    for g in G:
        if len({SAME_PAPER.get(P[i]['exam'], P[i]['exam']) for i in g}) > 1:
            rep[Counter(chof[i] for i in g).most_common(1)[0][0]] += 1
    subj_tot = Counter()
    for k, v in cnt.items():
        subj_tot[subj_of(k)] += v
    rows = []
    for k in sorted(cnt, key=ch_sort):
        paper, name = chname(k)
        rows.append(dict(ch=k, subject=subj_of(k), paper=paper, name=name, n=cnt[k],
                         per_exam=round(cnt[k] / len(exams), 2),
                         share=round(100 * cnt[k] / subj_tot[subj_of(k)], 1),
                         recent_per_exam=round(recent[k] / n_recent_exams, 2), repeats=rep[k]))
    json.dump(dict(exams=exams, n_exams=len(exams), science_questions=len(sci),
                   subject_totals=subj_tot, chapters=rows, summary=summary),
              open('chapter_stats.json', 'w'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
