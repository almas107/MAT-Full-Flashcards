# Botany Flashcards (জীববিজ্ঞান ১ম পত্র — উদ্ভিদবিজ্ঞান)

Anki packages for Botany chapters 2–12, one `.apkg` per chapter. They use the same
note type (`MAT Botany Basic`) and deck layout as the Chapter 1 deck
(`জীববিজ্ঞান ১ম পত্র::অধ্যায় N - …::<subdeck>`), so importing them sits alongside Ch1.

| অধ্যায় | Deck | Cards |
|---|---|---|
| ২ | কোষ বিভাজন | 283 |
| ৩ | কোষ রসায়ন | 605 |
| ৪ | অণুজীব | 826 |
| ৫ | শৈবাল ও ছত্রাক | 526 |
| ৬ | ব্রায়োফাইটা ও টেরিডোফাইটা | 237 |
| ৭ | নগ্নবীজী ও আবৃতবীজী উদ্ভিদ | 428 |
| ৮ | টিস্যু ও টিস্যুতন্ত্র | 336 |
| ৯ | উদ্ভিদ শারীরতত্ত্ব | 693 |
| ১০ | উদ্ভিদ প্রজনন | 314 |
| ১১ | জীবপ্রযুক্তি | 361 |
| ১২ | জীবের পরিবেশ, বিস্তার ও সংরক্ষণ | 587 |
| | **Total** | **5196** |

## What is in the cards

- Sources: the marked textbook chapters in `../Botany/` (only red/orange/green bracketed or
  underlined content) and the Medical Master question bank chapter sections.
- Card style follows DGME MAT/DAT phrasing: direct fact recall and characteristics of the
  marked text only — no explanation ("কেন…"), definition-essay or theory-check cards.
- Answers are kept short. Duplicates were removed within each chapter, across chapters and
  against the Chapter 1 deck.
- Where the question bank and the textbook disagree, the answer notes both.

## Rebuilding

Card text lives in `source/chNN.txt` (`# subdeck`, then `Q:` / `A:` lines).
Rebuild a chapter with:

```
cd source
pip install genanki
python3 build_decks.py 12
```

Note GUIDs are derived from the question text, so re-importing an edited package updates
existing notes instead of duplicating them (unless the question itself was changed).
