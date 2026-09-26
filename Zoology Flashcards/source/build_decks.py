"""Build Anki packages for MAT Zoology chapters from the plain-text card sources.

Source format (chNN.txt):
    # <subdeck title>
    Q: <front>
    A: <back>
    T: <space-separated tags>      (optional)

Usage: python3 build_decks.py [chapter ...]   (default: every chNN.txt present)
Fronts must be unique within a chapter and across all chapters (checked on every run).
"""
import os, re, sys, hashlib, html
import genanki

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)

CHAPTERS = {
    1: ('প্রাণীর বিভিন্নতা ও শ্রেণিবিন্যাস', 'Prani_Bibhinnota_O_Shrenibinnash'),
    2: ('প্রাণীর পরিচিতি', 'Pranir_Porichiti'),
    5: ('মানব শারীরতত্ত্ব: শ্বসন ও শ্বাসক্রিয়া', 'Shoshon_O_Shashkriya'),
    6: ('মানব শারীরতত্ত্ব: বর্জ্য ও নিষ্কাশন', 'Borjo_O_Nishkashon'),
    7: ('মানব শারীরতত্ত্ব: চলন ও অঙ্গচালনা', 'Chalon_O_Ongochalona'),
    9: ('মানব জীবনের ধারাবাহিকতা', 'Manob_Jiboner_Dharabahikota'),
    10: ('মানবদেহের প্রতিরক্ষা (ইমিউনিটি)', 'Manobdeher_Protiroksha'),
    11: ('জিনতত্ত্ব ও বিবর্তন', 'Jinototto_O_Bibortan'),
    12: ('প্রাণীর আচরণ', 'Pranir_Achoron'),
}
BN_DIGITS = str.maketrans('0123456789', '০১২৩৪৫৬৭৮৯')
ROOT = 'MAT জীববিজ্ঞান ২৬-২৭'

# Same fields, templates and styling as the Chapter 8 example deck.
MODEL = genanki.Model(
    1740208802, 'MAT Zoology Basic',
    fields=[{'name': 'Question'}, {'name': 'Answer'}],
    templates=[{
        'name': 'Card 1',
        'qfmt': '<div class="question">{{Question}}</div>',
        'afmt': '{{FrontSide}}<hr id="answer"><div class="answer">{{Answer}}</div>',
    }],
    css=".card { font-family: 'Noto Sans Bengali', 'SolaimanLipi', Arial, sans-serif; font-size: 20px; "
        "text-align: left; line-height: 1.5; padding: 16px; }\n"
        "b { font-weight: 700; } hr#answer { margin: 14px 0; }",
)


def deck_id(name):
    return int(hashlib.sha1(name.encode()).hexdigest()[:8], 16) | (1 << 30)


def norm(s):
    return re.sub(r'[\s\?।,;:\-—–\'"‘’“”()]+', '', s).lower()


def parse(path):
    sections, cur, q, last = [], None, None, None
    for ln, line in enumerate(open(path, encoding='utf-8'), 1):
        line = line.strip()
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
            last = [q, line[3:].strip(), []]
            cur[1].append(last)
            q = None
        elif line.startswith('T: '):
            if last is None or q is not None:
                sys.exit(f'{path}:{ln}: T without card')
            last[2] = line[3:].split()
        else:
            sys.exit(f'{path}:{ln}: unrecognised line: {line[:60]}')
    if q is not None:
        sys.exit(f'{path}: dangling Q at end')
    return sections


def all_fronts():
    seen = {}
    for f in sorted(os.listdir(HERE)):
        m = re.match(r'ch(\d+)\.txt$', f)
        if not m:
            continue
        for sub, cards in parse(os.path.join(HERE, f)):
            for front, _, _ in cards:
                key = norm(front)
                if key in seen:
                    sys.exit(f'duplicate front "{front}" in ch{int(m.group(1))} "{sub}" (also {seen[key]})')
                seen[key] = f'ch{int(m.group(1))} "{sub}"'


def build(ch):
    title, slug = CHAPTERS[ch]
    sections = parse(os.path.join(HERE, f'ch{ch:02d}.txt'))
    parent = f'{ROOT}::অধ্যায় {str(ch).translate(BN_DIGITS)} - {title}'
    decks, total = [], 0
    for i, (sub, cards) in enumerate(sections, 1):
        name = f'{parent}::{i:02d} {sub}'.replace(f'::{i:02d} ', f'::{str(i).zfill(2).translate(BN_DIGITS)} ')
        deck = genanki.Deck(deck_id(name), name)
        for front, back, tags in cards:
            deck.add_note(genanki.Note(
                model=MODEL,
                fields=[html.escape(front, quote=False), html.escape(back, quote=False)],
                tags=tags, guid=genanki.guid_for('mat-zoology', f'ch{ch}', front)))
            total += 1
        decks.append(deck)
    out = os.path.join(OUT, f'MAT_Zoology_Ch{ch}_{slug}.apkg')
    genanki.Package(decks).write_to_file(out)
    print(f'Ch{ch}: {total} cards in {len(sections)} subdecks -> {os.path.basename(out)}')
    return total


if __name__ == '__main__':
    all_fronts()
    chs = [int(a) for a in sys.argv[1:]] or sorted(
        int(m.group(1)) for f in os.listdir(HERE) if (m := re.match(r'ch(\d+)\.txt$', f)))
    print('Total:', sum(build(c) for c in chs))
