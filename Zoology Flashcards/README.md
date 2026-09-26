# Zoology Flashcards (জীববিজ্ঞান ২য় পত্র — প্রাণিবিজ্ঞান)

Anki packages for Zoology chapters 1, 2, 5, 6, 7, 9, 10, 11 and 12, one `.apkg` per chapter
(chapters 3, 4 and 8 were already done). The deck layout matches the Chapter 8 example deck:
`MAT জীববিজ্ঞান ২৬-২৭::অধ্যায় N - …::<subdeck>`. The fields are Question / Answer, with the same card style.

| অধ্যায় | Deck | Cards |
|---|---|---|
| ১ | প্রাণীর বিভিন্নতা ও শ্রেণিবিন্যাস | 494 |
| ২ | প্রাণীর পরিচিতি (হাইড্রা, ঘাসফড়িং, রুই মাছ) | 685 |
| ৫ | মানব শারীরতত্ত্ব: শ্বসন ও শ্বাসক্রিয়া | 228 |
| ৬ | মানব শারীরতত্ত্ব: বর্জ্য ও নিষ্কাশন | 274 |
| ৭ | মানব শারীরতত্ত্ব: চলন ও অঙ্গচালনা | 422 |
| ৯ | মানব জীবনের ধারাবাহিকতা | 464 |
| ১০ | মানবদেহের প্রতিরক্ষা (ইমিউনিটি) | 344 |
| ১১ | জিনতত্ত্ব ও বিবর্তন | 405 |
| ১২ | প্রাণীর আচরণ | 229 |
| | **Total** | **3545** |

## What is in the cards

- Sources:
  - The marked textbook chapters in `../Zoology/`. Only content marked in red, orange or green
    (bracketed or underlined) is used.
  - The Zoology question bank (Medical Master প্রশ্নব্যাংক), per-chapter sections.
  - The MAT/DAT past papers (2010+).
- The cards follow DGME MAT/DAT phrasing. They cover direct fact recall and characteristics of
  the marked text. There are no explanation ("কেন…"), definition-essay or theory-check cards.
  Past-paper "which one is not…" items are kept in that same MCQ-stem form.
- Answers are kept short.
- Duplicates were removed within each chapter, across chapters and against the Chapter 8 deck.
- Where the question bank and the textbook disagree, the answer notes both.
- Tags on each note:
  - `textbook::pNNN` gives the textbook page number.
  - `source::question_bank` marks a question-bank card.
  - `exam::MAT_xx-yy` / `exam::DAT_xx-yy` plus `past_question` mark a card that appeared in that exam.

## Rebuilding

Card text lives in `source/chNN.txt`. Each file uses `# subdeck`, then `Q:` / `A:` / optional `T:` tag lines.

```
cd source
pip install genanki
python3 build_decks.py        # all chapters, or e.g. `python3 build_decks.py 11`
```

The build fails if any question appears twice (checked across all chapters). Note GUIDs are derived
from the question text, so re-importing an edited package updates existing notes instead of duplicating them.
