"""Convert Anki .apkg decks into the plain-text card format used across this repo.

Output format (same as the Physics/Chemistry/Botany sources):
    # <topic subdeck>
    Q: <front>
    A: <back>                  (" || " marks a line break)
    Y: MAT 22-23, DAT 19-20    (only when the note carries past-exam tags)

Usage: python3 tools/extract_apkg.py <deck.apkg> <out.txt>
"""
import html, json, os, re, sqlite3, sys, tempfile, zipfile

BN_DIGITS = str.maketrans('০১২৩৪৫৬৭৮৯', '0123456789')
EXAM_TAG = re.compile(r'(?:exam::)?(MAT|DAT|AFMC)[_-](\d{1,2}-\d{1,2})$', re.I)


def clean(s):
    s = re.sub(r'<br\s*/?>', ' || ', s, flags=re.I)
    s = re.sub(r'</?[A-Za-z][^<>]*>', '', s)   # real tags only; keep text like '< Ksp' or '<1'
    s = html.unescape(s).replace('\xa0', ' ')
    s = re.sub(r'[ \t\r\n]+', ' ', s)
    s = re.sub(r'(\s*\|\|\s*)+', ' || ', s)
    return s.strip(' |')


def years(tags):
    out = []
    for t in tags.split():
        m = EXAM_TAG.match(t)
        if m:
            y = f'{m.group(1).upper()} {m.group(2)}'
            if y not in out:
                out.append(y)
    return ', '.join(out)


def deck_order(name):
    """Natural sort, so subdeck '3.2' comes before '3.10'; unnumbered subdecks go last."""
    last = name.split('::')[-1].translate(BN_DIGITS)
    nums = [int(x) for x in re.match(r'[\d.\-]*', last).group(0).replace('-', '.').split('.') if x]
    return (name.rsplit('::', 1)[0], 0 if nums else 1, nums, last)


def extract(apkg, out):
    with tempfile.TemporaryDirectory() as tmp:
        with zipfile.ZipFile(apkg) as z:
            name = next(n for n in ('collection.anki21', 'collection.anki2') if n in z.namelist())
            z.extract(name, tmp)
        db = sqlite3.connect(os.path.join(tmp, name))
        decks = json.loads(db.execute('select decks from col').fetchone()[0])
        rows = db.execute('select n.id, n.flds, n.tags, min(c.did) from notes n join cards c on c.nid = n.id '
                          'group by n.id').fetchall()
        db.close()
    chapter = None
    lines, last_topic, n = [], None, 0
    for nid, flds, tags, did in sorted(rows, key=lambda r: (deck_order(decks[str(r[3])]['name']), r[0])):
        parts = decks[str(did)]['name'].split('::')
        chapter = chapter or next((p for p in parts if p.startswith('অধ্যায়')), None)
        topic = re.sub(r'^[০-৯\d]+[.)]?\s+', '', parts[-1]).strip()   # drop '০১ ' / '১. ', keep '২.১২ '
        q, a = (clean(f) for f in flds.split('\x1f')[:2])
        if not q or not a:
            continue
        if topic != last_topic:
            lines.append(f'# {topic}')
            last_topic = topic
        lines += [f'Q: {q}', f'A: {a}']
        y = years(tags)
        if y:
            lines.append(f'Y: {y}')
        n += 1
    with open(out, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')
    print(f'{os.path.basename(apkg)} -> {os.path.basename(out)}: {n} cards ({chapter})')


if __name__ == '__main__':
    extract(sys.argv[1], sys.argv[2])
