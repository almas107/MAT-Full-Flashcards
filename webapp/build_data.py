"""Collect every flashcard source file into webapp/cards.json for the study app.

Reads  ../Physics Flashcards/source/p{1,2}_chNN.txt,
       ../Chemistry Flashcards/source/c{1,2}_chNN.txt,
       ../Botany Flashcards/source/chNN.txt,
       ../Zoology Flashcards/source/z_chNN.txt
(`# topic`, `Q:`, `A:` with " || " as a line break, optional `Y:` exam years).

Card ids hash the question text, so editing an answer keeps your progress on that card.
Also wraps app.html (the page body, as published to claude.ai) into a standalone index.html.
Usage: python3 build_data.py
"""
import glob, hashlib, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

CHAPTERS = {
    'p1': ('পদার্থবিজ্ঞান ১ম পত্র', 'Physics', {
        1: 'ভৌত জগৎ ও পরিমাপ', 2: 'ভেক্টর', 3: 'গতিবিদ্যা', 4: 'নিউটনিয়ান বলবিদ্যা',
        5: 'কাজ, শক্তি ও ক্ষমতা', 6: 'মহাকর্ষ ও অভিকর্ষ', 7: 'পদার্থের গাঠনিক ধর্ম',
        8: 'পর্যাবৃত্ত গতি', 9: 'তরঙ্গ', 10: 'আদর্শ গ্যাস ও গ্যাসের গতিতত্ত্ব'}),
    'p2': ('পদার্থবিজ্ঞান ২য় পত্র', 'Physics', {
        1: 'তাপগতিবিদ্যা', 2: 'স্থির তড়িৎ', 3: 'চল তড়িৎ',
        4: 'তড়িৎ প্রবাহের চৌম্বক ক্রিয়া ও চুম্বকত্ব', 5: 'তড়িৎচৌম্বক আবেশ ও পরিবর্তী প্রবাহ',
        6: 'জ্যামিতিক আলোকবিজ্ঞান', 7: 'ভৌত আলোকবিজ্ঞান', 8: 'আধুনিক পদার্থবিজ্ঞানের সূচনা',
        9: 'পরমাণুর মডেল এবং নিউক্লিয়ার পদার্থবিজ্ঞান', 10: 'সেমিকন্ডাক্টর ও ইলেকট্রনিক্স',
        11: 'জ্যোতির্বিজ্ঞান'}),
    'c1': ('রসায়ন ১ম পত্র', 'Chemistry', {
        1: 'ল্যাবরেটরির নিরাপদ ব্যবহার', 2: 'গুণগত রসায়ন',
        3: 'মৌলের পর্যায়বৃত্ত ধর্ম ও রাসায়নিক বন্ধন', 4: 'রাসায়নিক পরিবর্তন', 5: 'কর্মমুখী রসায়ন'}),
    'c2': ('রসায়ন ২য় পত্র', 'Chemistry', {
        1: 'পরিবেশ রসায়ন', 2: 'জৈব রসায়ন', 3: 'পরিমাণগত রসায়ন', 4: 'তড়িৎ রসায়ন',
        5: 'অর্থনৈতিক রসায়ন'}),
    'b1': ('উদ্ভিদবিজ্ঞান', 'Botany', {
        1: 'কোষ ও এর গঠন', 2: 'কোষ বিভাজন', 3: 'কোষ রসায়ন', 4: 'অণুজীব', 5: 'শৈবাল ও ছত্রাক',
        6: 'ব্রায়োফাইটা ও টেরিডোফাইটা', 7: 'নগ্নবীজী ও আবৃতবীজী উদ্ভিদ', 8: 'টিস্যু ও টিস্যুতন্ত্র',
        9: 'উদ্ভিদ শারীরতত্ত্ব', 10: 'উদ্ভিদ প্রজনন', 11: 'জীবপ্রযুক্তি',
        12: 'জীবের পরিবেশ, বিস্তার ও সংরক্ষণ'}),
    'z': ('প্রাণিবিজ্ঞান', 'Zoology', {
        1: 'প্রাণীর বিভিন্নতা ও শ্রেণিবিন্যাস', 2: 'প্রাণীর পরিচিতি', 3: 'পরিপাক ও শোষণ',
        4: 'রক্ত ও সঞ্চালন', 5: 'শ্বসন ও শ্বাসক্রিয়া', 6: 'বর্জ্য ও নিষ্কাশন', 7: 'চলন ও অঙ্গচালনা',
        8: 'সমন্বয় ও নিয়ন্ত্রণ', 9: 'মানব জীবনের ধারাবাহিকতা', 10: 'মানবদেহের প্রতিরক্ষা (ইমিউনিটি)',
        11: 'জিনতত্ত্ব ও বিবর্তন', 12: 'প্রাণীর আচরণ'}),
}
SOURCES = [
    ('Physics Flashcards/source/p[12]_ch*.txt', r'(p[12])_ch(\d+)'),
    ('Chemistry Flashcards/source/c[12]_ch*.txt', r'(c[12])_ch(\d+)'),
    ('Botany Flashcards/source/ch*.txt', r'()ch(\d+)'),
    ('Zoology Flashcards/source/z_ch*.txt', r'(z)_ch(\d+)'),
]
BN_DIGITS = str.maketrans('0123456789', '০১২৩৪৫৬৭৮৯')


def parse(path):
    topic, q, cards = None, None, []
    for ln, line in enumerate(open(path, encoding='utf-8'), 1):
        line = line.strip()
        if not line:
            continue
        if line.startswith('# '):
            topic = line[2:].strip()
        elif line.startswith('Q: '):
            q = line[3:].strip()
        elif line.startswith('A: '):
            if q is None:
                sys.exit(f'{path}:{ln}: A without Q')
            cards.append([topic or '', q, line[3:].strip(), ''])
            q = None
        elif line.startswith('Y: '):
            cards[-1][3] = line[3:].strip()
        else:
            sys.exit(f'{path}:{ln}: unrecognised line: {line[:60]}')
    return cards


def main():
    subjects, chapters, topics, cards, ids = [], [], [], [], {}
    for pattern, rx in SOURCES:
        for path in sorted(glob.glob(os.path.join(ROOT, pattern)),
                           key=lambda p: (re.search(rx, p).group(1), int(re.search(rx, p).group(2)))):
            m = re.search(rx, os.path.basename(path))
            paper, num = m.group(1) or 'b1', int(m.group(2))
            paper_name, subject, names = CHAPTERS[paper]
            if subject not in subjects:
                subjects.append(subject)
            ci = len(chapters)
            chapters.append({'s': subjects.index(subject), 'p': paper_name, 'n': num,
                             't': f'অধ্যায় {str(num).translate(BN_DIGITS)} · {names[num]}'})
            for topic, q, a, y in parse(path):
                key = (ci, topic)
                if not topics or topics[-1][0] != key:
                    topics.append((key, topic))
                cid = hashlib.sha1(f'{paper}|{num}|{q}'.encode()).hexdigest()[:10]
                if cid in ids:   # repeated question: keep the first card, but keep every exam year
                    if y:
                        kept = ids[cid]
                        old = [x for x in kept.get('y', '').split(', ') if x]
                        kept['y'] = ', '.join(old + [x for x in y.split(', ') if x not in old])
                    continue
                card = {'i': cid, 'c': ci, 't': len(topics) - 1, 'q': q, 'a': a}
                if y:
                    card['y'] = y
                ids[cid] = card
                cards.append(card)
    out = {'subjects': subjects, 'chapters': chapters, 'topics': [t for _, t in topics], 'cards': cards}
    with open(os.path.join(HERE, 'cards.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, separators=(',', ':'))
    print(f'{len(cards)} cards, {len(chapters)} chapters, {len(topics)} topics, '
          f'{sum(1 for c in cards if "y" in c)} PYQ')
    with open(os.path.join(HERE, 'app.html'), encoding='utf-8') as f:
        body = f.read()
    with open(os.path.join(HERE, 'index.html'), 'w', encoding='utf-8') as f:
        f.write('<!doctype html>\n<!-- Generated from app.html by build_data.py; edit app.html instead. -->\n'
                '<html lang="bn"><head><meta charset="utf-8">'
                '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
                '</head><body>\n' + body + '\n</body></html>\n')


if __name__ == '__main__':
    main()
