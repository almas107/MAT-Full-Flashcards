# Zoology Flashcards (জীববিজ্ঞান ২য় পত্র — প্রাণিবিজ্ঞান)

Anki packages for Zoology chapters 1–12, one `.apkg` per chapter (deck `MAT জীববিজ্ঞান ২৬-২৭::অধ্যায় N - …::<subdeck>`).
These decks were made outside this repo and uploaded as-is. Their card text was extracted into `source/z_chNN.txt`
so the study web app (`../webapp`) can use them.

| অধ্যায় | Deck | Cards | PYQ |
|---|---|---|---|
| ১ | প্রাণীর বিভিন্নতা ও শ্রেণিবিন্যাস | 494 | 28 |
| ২ | প্রাণীর পরিচিতি | 685 | 39 |
| ৩ | পরিপাক ও শোষণ | 425 | 33 |
| ৪ | রক্ত ও সঞ্চালন | 433 | 23 |
| ৫ | শ্বসন ও শ্বাসক্রিয়া | 228 | 26 |
| ৬ | বর্জ্য ও নিষ্কাশন | 274 | 24 |
| ৭ | চলন ও অঙ্গচালনা | 422 | 44 |
| ৮ | সমন্বয় ও নিয়ন্ত্রণ | 709 | 230 |
| ৯ | মানব জীবনের ধারাবাহিকতা | 464 | 27 |
| ১০ | মানবদেহের প্রতিরক্ষা (ইমিউনিটি) | 344 | 42 |
| ১১ | জিনতত্ত্ব ও বিবর্তন | 405 | 41 |
| ১২ | প্রাণীর আচরণ | 229 | 5 |
| | **Total** | **5112** | **562** |

Chapter 8 repeats 118 questions in a later subdeck; the web app shows each once and keeps the exam years from both copies. PYQ counts are cards tagged with a past MAT/DAT year (`exam::MAT_22-23` and similar tags), shown as the `Y:` line in the source.

## Re-extracting
`.apkg` files are the source of truth here. After replacing a deck, regenerate its text with:

```
python3 ../tools/extract_apkg.py MAT_Zoology_Ch4_Rokto_O_Songchalon.apkg source/z_ch04.txt
```
`<br>` becomes ` || `, other HTML is stripped, and the topic is the last subdeck name.
