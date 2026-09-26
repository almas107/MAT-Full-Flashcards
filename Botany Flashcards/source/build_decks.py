"""Build Anki packages for MAT Botany chapters from the plain-text card sources.

Source format (chNN.txt):
    # <subdeck title>
    Q: <front>
    A: <back>

Usage: python3 build_decks.py [chapter ...]   (default: every chNN.txt present)
"""
import os, re, sys, hashlib, html
import genanki

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)

CHAPTERS = {
    2: ('কোষ বিভাজন', 'Cell_Division'),
    3: ('কোষ রসায়ন', 'Cell_Chemistry'),
    4: ('অণুজীব', 'Microorganisms'),
    5: ('শৈবাল ও ছত্রাক', 'Algae_Fungi'),
    6: ('ব্রায়োফাইটা ও টেরিডোফাইটা', 'Bryophyta_Pteridophyta'),
    7: ('নগ্নবীজী ও আবৃতবীজী উদ্ভিদ', 'Gymnosperm_Angiosperm'),
    8: ('টিস্যু ও টিস্যুতন্ত্র', 'Tissue_Tissue_System'),
    9: ('উদ্ভিদ শারীরতত্ত্ব', 'Plant_Physiology'),
    10: ('উদ্ভিদ প্রজনন', 'Plant_Reproduction'),
    11: ('জীবপ্রযুক্তি', 'Biotechnology'),
    12: ('জীবের পরিবেশ, বিস্তার ও সংরক্ষণ', 'Environment_Distribution_Conservation'),
}
BN_DIGITS = str.maketrans('0123456789', '০১২৩৪৫৬৭৮৯')
ROOT = 'জীববিজ্ঞান ১ম পত্র'

# Same note type as the Chapter 1 example deck, so every chapter shares it on import.
MODEL = genanki.Model(
    3324442695, 'MAT Botany Basic',
    fields=[{'name': 'Front'}, {'name': 'Back'}],
    templates=[{
        'name': 'Card 1',
        'qfmt': '<div class="q">{{Front}}</div>',
        'afmt': '{{FrontSide}}<hr id="answer"><div class="a">{{Back}}</div>',
    }],
    css='.card{font-family:"Noto Sans Bengali","Kalpurush",sans-serif;\n'
        'font-size:21px;text-align:center;color:#1b1b1b;background:#fdfdfd;line-height:1.7;}\n'
        '.q{font-weight:600;} .a{font-size:20px;} hr#answer{margin:14px 0;}',
)


def deck_id(name):
    return int(hashlib.sha1(name.encode()).hexdigest()[:8], 16) | (1 << 30)


def norm(s):
    return re.sub(r'[\s\?\?।,;:\-—–\'"‘’“”()]+', '', s).lower()


def parse(path):
    sections, cur, q = [], None, None
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
        elif line.startswith('Q: '):
            if q is not None:
                sys.exit(f'{path}:{ln}: Q without A before it')
            q = line[3:].strip()
        elif line.startswith('A: '):
            if q is None or cur is None:
                sys.exit(f'{path}:{ln}: A without Q/section')
            cur[1].append((q, line[3:].strip()))
            q = None
        else:
            sys.exit(f'{path}:{ln}: unrecognised line: {line[:60]}')
    if q is not None:
        sys.exit(f'{path}: dangling Q at end')
    return sections


def build(ch):
    title, slug = CHAPTERS[ch]
    sections = parse(os.path.join(HERE, f'ch{ch:02d}.txt'))
    parent = f'{ROOT}::অধ্যায় {str(ch).translate(BN_DIGITS)} - {title}'
    decks, seen, total = [genanki.Deck(deck_id(parent), parent)], {}, 0
    for i, (sub, cards) in enumerate(sections, 1):
        name = f'{parent}::{str(i).translate(BN_DIGITS)}. {sub}'
        deck = genanki.Deck(deck_id(name), name)
        for front, back in cards:
            key = norm(front)
            if key in seen:
                sys.exit(f'ch{ch}: duplicate front "{front}" (also in "{seen[key]}")')
            seen[key] = sub
            deck.add_note(genanki.Note(model=MODEL, fields=[html.escape(front, quote=False), html.escape(back, quote=False)],
                                       guid=genanki.guid_for(f'ch{ch}', front)))
            total += 1
        decks.append(deck)
    out = os.path.join(OUT, f'MAT_Botany_Ch{ch}_{slug}_MARKED.apkg')
    genanki.Package(decks).write_to_file(out)
    print(f'Ch{ch}: {total} cards in {len(sections)} subdecks -> {os.path.basename(out)}')


if __name__ == '__main__':
    chs = [int(a) for a in sys.argv[1:]] or sorted(
        int(m.group(1)) for f in os.listdir(HERE) if (m := re.match(r'ch(\d+)\.txt$', f)))
    for c in chs:
        build(c)
