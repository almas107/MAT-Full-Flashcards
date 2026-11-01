"""Build one Anki package per subject from ../source/mp_<subject>.txt.

Deck layout: MAT সবচেয়ে সম্ভাব্য প্রশ্ন::<বিষয়>::<tier>::<chapter>
Cards inside a deck are added in score order (highest first).
Usage: python3 build_decks.py            (needs: pip install genanki)
"""
import os, re, sys, hashlib, html
import genanki

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from common import chname

ROOT_DECK = 'MAT সবচেয়ে সম্ভাব্য প্রশ্ন'
SUBJECTS = [('physics', 'Physics', 'পদার্থবিজ্ঞান'), ('chemistry', 'Chemistry', 'রসায়ন'),
            ('botany', 'Botany', 'উদ্ভিদবিজ্ঞান'), ('zoology', 'Zoology', 'প্রাণিবিজ্ঞান')]
TIER_DECK = {'T1': 'T1 বারবার এসেছে', 'T2': 'T2 আগে এসেছে', 'T3': 'T3 সম্ভাব্য'}
BN = str.maketrans('0123456789', '০১২৩৪৫৬৭৮৯')

MODEL = genanki.Model(
    1739104511, 'MAT Most Probable',
    fields=[{'name': 'Front'}, {'name': 'Back'}, {'name': 'Years'}, {'name': 'Score'}],
    templates=[{
        'name': 'Card 1',
        'qfmt': '<div class="meta">{{#Years}}<span class="yr">{{Years}}</span>{{/Years}}'
                '<span class="sc">সম্ভাবনা {{Score}}</span></div><div class="q">{{Front}}</div>',
        'afmt': '{{FrontSide}}<hr id="answer"><div class="a">{{Back}}</div>',
    }],
    css='.card{font-family:"Noto Sans Bengali","Kalpurush",sans-serif;font-size:21px;text-align:left;'
        'color:#1b1b1b;background:#fdfdfd;line-height:1.7;max-width:760px;margin:0 auto;}\n'
        '.nightMode.card,.night_mode .card{color:#eee;background:#1e1e1e;}\n'
        '.q{font-weight:600;} .a{color:#0b5394;font-weight:600;}\n'
        '.nightMode .a,.night_mode .a{color:#8fc1ff;}\n'
        '.meta{font-size:13px;margin-bottom:8px;} .yr{color:#b00020;border:1px solid #b00020;border-radius:10px;'
        'padding:0 8px;margin-right:6px;} .sc{color:#666;border:1px solid #999;border-radius:10px;padding:0 8px;}\n'
        'hr#answer{margin:14px 0;}',
)


def deck_id(name):
    return int(hashlib.sha1(name.encode()).hexdigest()[:8], 16) | (1 << 30)


def fmt(s):
    return html.escape(s, quote=False).replace(' || ', '<br>')


def parse(path):
    cards, head = [], None
    for ln, line in enumerate(open(path, encoding='utf-8'), 1):
        line = line.strip()
        if not line:
            continue
        if line.startswith('# '):
            m = re.match(r'# \[(\w+)\] (T\d) \| (.*)', line)
            if not m:
                sys.exit(f'{path}:{ln}: bad header')
            head = m.groups()
        elif line.startswith('Q: '):
            cards.append(dict(ch=head[0], tier=head[1], q=line[3:], a=None, y='', r=0))
        elif line.startswith('A: '):
            cards[-1]['a'] = line[3:]
        elif line.startswith('Y: '):
            cards[-1]['y'] = line[3:]
        elif line.startswith('R: '):
            cards[-1]['r'] = int(line[3:])
        elif line.startswith('L: '):
            pass
        else:
            sys.exit(f'{path}:{ln}: unrecognised line: {line[:60]}')
    return cards


def build(slug, subj, bn):
    cards = parse(os.path.join(OUT, 'source', f'mp_{slug}.txt'))
    decks = {}
    seen = set()
    for c in sorted(cards, key=lambda c: -c['r']):
        paper, name = chname(c['ch'])
        n = str(int(c['ch'].split('_')[1])).translate(BN)
        chdeck = f'{paper} অধ্যায় {n} - {name}' if subj in ('Physics', 'Chemistry') else f'অধ্যায় {n} - {name}'
        dname = f'{ROOT_DECK}::{bn}::{TIER_DECK[c["tier"]]}::{chdeck}'
        if dname not in decks:
            decks[dname] = genanki.Deck(deck_id(dname), dname)
        key = (dname, c['q'])
        if key in seen:
            continue
        seen.add(key)
        tags = [f'MP_{c["tier"]}', f'MP_{subj}'] + (['PYQ'] if c['y'] else [])
        decks[dname].add_note(genanki.Note(model=MODEL, fields=[fmt(c['q']), fmt(c['a']), html.escape(c['y']), str(c['r'])],
                                           tags=tags, guid=genanki.guid_for('mp', c['ch'], c['q'])))
    # order decks: tier, then paper/chapter
    out = os.path.join(OUT, f'MAT_Most_Probable_{subj}.apkg')
    genanki.Package(sorted(decks.values(), key=lambda d: d.name)).write_to_file(out)
    print(f'{subj}: {len(seen)} cards in {len(decks)} decks -> {os.path.basename(out)}')
    return len(seen)


if __name__ == '__main__':
    total = sum(build(*s) for s in SUBJECTS)
    print('total', total)
