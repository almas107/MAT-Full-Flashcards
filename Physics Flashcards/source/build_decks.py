"""Build Anki packages for MAT Physics (1st & 2nd paper) from plain-text card sources.

Source format (p1_chNN.txt / p2_chNN.txt):
    # <subdeck title>
    Q: <front>
    A: <back>            (use " || " for a line break inside the answer)
    Y: MAT 22-23, DAT 17-18   (optional: past-exam years; shown as a badge + Anki tags)

Usage: python3 build_decks.py [p1_06 p2_03 ...]   (default: every source file present)
"""
import os, re, sys, hashlib, html
import genanki

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)

PAPERS = {
    'p1': ('পদার্থবিজ্ঞান ১ম পত্র', 'Phy1', {
        1: ('ভৌত জগৎ ও পরিমাপ', 'Physical_World_Measurement'),
        2: ('ভেক্টর', 'Vector'),
        3: ('গতিবিদ্যা', 'Dynamics'),
        4: ('নিউটনিয়ান বলবিদ্যা', 'Newtonian_Mechanics'),
        5: ('কাজ, শক্তি ও ক্ষমতা', 'Work_Energy_Power'),
        6: ('মহাকর্ষ ও অভিকর্ষ', 'Gravitation'),
        7: ('পদার্থের গাঠনিক ধর্ম', 'Structural_Properties_of_Matter'),
        8: ('পর্যাবৃত্ত গতি', 'Periodic_Motion'),
        9: ('তরঙ্গ', 'Waves'),
        10: ('আদর্শ গ্যাস ও গ্যাসের গতিতত্ত্ব', 'Ideal_Gas_Kinetic_Theory'),
    }),
    'p2': ('পদার্থবিজ্ঞান ২য় পত্র', 'Phy2', {
        1: ('তাপগতিবিদ্যা', 'Thermodynamics'),
        2: ('স্থির তড়িৎ', 'Static_Electricity'),
        3: ('চল তড়িৎ', 'Current_Electricity'),
        4: ('তড়িৎ প্রবাহের চৌম্বক ক্রিয়া ও চুম্বকত্ব', 'Magnetic_Effect_Magnetism'),
        5: ('তড়িৎচৌম্বক আবেশ ও পরিবর্তী প্রবাহ', 'EM_Induction_AC'),
        6: ('জ্যামিতিক আলোকবিজ্ঞান', 'Geometrical_Optics'),
        7: ('ভৌত আলোকবিজ্ঞান', 'Physical_Optics'),
        8: ('আধুনিক পদার্থবিজ্ঞানের সূচনা', 'Intro_Modern_Physics'),
        9: ('পরমাণুর মডেল এবং নিউক্লিয়ার পদার্থবিজ্ঞান', 'Atomic_Model_Nuclear_Physics'),
        10: ('সেমিকন্ডাক্টর ও ইলেকট্রনিক্স', 'Semiconductor_Electronics'),
        11: ('জ্যোতির্বিজ্ঞান', 'Astronomy'),
    }),
}
BN_DIGITS = str.maketrans('0123456789', '০১২৩৪৫৬৭৮৯')

MODEL = genanki.Model(
    1607392711, 'MAT Physics Basic',
    fields=[{'name': 'Front'}, {'name': 'Back'}, {'name': 'Years'}],
    templates=[{
        'name': 'Card 1',
        'qfmt': '{{#Years}}<div class="yr">★ {{Years}}</div>{{/Years}}<div class="q">{{Front}}</div>',
        'afmt': '{{FrontSide}}<hr id="answer"><div class="a">{{Back}}</div>',
    }],
    css='.card{font-family:"Noto Sans Bengali","Kalpurush",sans-serif;\n'
        'font-size:21px;text-align:center;color:#1b1b1b;background:#fdfdfd;line-height:1.7;}\n'
        '.nightMode.card,.night_mode .card{color:#eee;background:#1e1e1e;}\n'
        '.q{font-weight:600;} .a{font-size:21px;color:#0b5394;font-weight:600;}\n'
        '.nightMode .a,.night_mode .a{color:#8fc1ff;}\n'
        '.yr{display:inline-block;font-size:13px;color:#b00020;border:1px solid #b00020;'
        'border-radius:10px;padding:0 8px;margin-bottom:8px;}\n'
        'hr#answer{margin:14px 0;}',
)


def deck_id(name):
    return int(hashlib.sha1(name.encode()).hexdigest()[:8], 16) | (1 << 30)


def norm(s):
    return re.sub(r'[\s\?।,;:\-—–\'"‘’“”()]+', '', s).lower()


def year_tags(years):
    tags = {'PYQ'}
    for exam in ('MAT', 'DAT', 'AFMC'):
        if exam in years.upper():
            tags.add(exam)
    return sorted(tags)


def parse(path):
    sections, cur, q, last = [], None, None, None
    for ln, line in enumerate(open(path, encoding='utf-8'), 1):
        line = line.rstrip('\n').strip()
        if not line:
            continue
        if line.startswith('# '):
            title = line[2:].strip()
            cur = next((x for x in sections if x[0] == title), None)
            if cur is None:
                cur = (title, [])
                sections.append(cur)
            last = None
        elif line.startswith('Q: '):
            if q is not None:
                sys.exit(f'{path}:{ln}: Q without A before it')
            q = line[3:].strip()
        elif line.startswith('A: '):
            if q is None or cur is None:
                sys.exit(f'{path}:{ln}: A without Q/section')
            last = [q, line[3:].strip(), '']
            cur[1].append(last)
            q = None
        elif line.startswith('Y: '):
            if last is None or last[2]:
                sys.exit(f'{path}:{ln}: Y must follow an A line')
            last[2] = line[3:].strip()
        else:
            sys.exit(f'{path}:{ln}: unrecognised line: {line[:60]}')
    if q is not None:
        sys.exit(f'{path}: dangling Q at end')
    return sections


def fmt(s):
    return html.escape(s, quote=False).replace(' || ', '<br>')


def build(key):
    paper, ch = key.split('_')
    ch = int(ch)
    root, short, chapters = PAPERS[paper]
    title, slug = chapters[ch]
    sections = parse(os.path.join(HERE, f'{paper}_ch{ch:02d}.txt'))
    parent = f'{root}::অধ্যায় {str(ch).translate(BN_DIGITS)} - {title}'
    decks, seen, total, pyq = [genanki.Deck(deck_id(parent), parent)], {}, 0, 0
    for i, (sub, cards) in enumerate(sections, 1):
        name = f'{parent}::{str(i).translate(BN_DIGITS)}. {sub}'
        deck = genanki.Deck(deck_id(name), name)
        for front, back, years in cards:
            k = norm(front)
            if k in seen:
                sys.exit(f'{key}: duplicate front "{front}" (also in "{seen[k]}")')
            seen[k] = sub
            tags = [f'{short}_Ch{ch}'] + (year_tags(years) if years else [])
            deck.add_note(genanki.Note(model=MODEL, fields=[fmt(front), fmt(back), html.escape(years)],
                                       tags=tags, guid=genanki.guid_for(key, front)))
            total += 1
            pyq += bool(years)
        decks.append(deck)
    out = os.path.join(OUT, f'MAT_{short}_Ch{ch}_{slug}.apkg')
    genanki.Package(decks).write_to_file(out)
    print(f'{key}: {total} cards ({pyq} PYQ) in {len(sections)} subdecks -> {os.path.basename(out)}')
    return total, pyq


if __name__ == '__main__':
    keys = sys.argv[1:] or sorted(
        f'{m.group(1)}_{m.group(2)}' for f in os.listdir(HERE)
        if (m := re.match(r'(p[12])_ch(\d+)\.txt$', f)))
    for k in keys:
        build(k)
