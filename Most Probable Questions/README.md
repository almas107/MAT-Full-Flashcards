# সবচেয়ে সম্ভাব্য প্রশ্ন — MAT / DAT (Physics, Chemistry, Botany, Zoology)

This is a ranked set of **7,112 questions**, most likely first. It was built from:
- **22 past papers** (MAT 2014-15 to 2025-26 and DAT 2014-15 to 2024-25): 2,193 questions, of which 1,631 are science.
- Every older year tag in this repo's decks (MAT/DAT from the early 2000s, AFMC and "মেডিকেল ভর্তি প্রশ্ন").
- The 25,107 cards in this repo.

Every question has a **probability score from 0 to 100** and a tier:

| Tier | What it means | Cards |
|---|---|---|
| **T1 — বারবার এসেছে** | Asked in 2 or more different exams (2014–26 papers plus the older tags in this repo) | 205 |
| **T2 — আগে এসেছে** | Asked once in a 2014–26 paper, or two or more times in older exams | 1,383 |
| **T3 — সম্ভাব্য** | Asked once in an older exam, or a card on a topic that past papers keep testing, or one of the 223 new cards for the missing Chem 1st paper Ch2 part 1 | 5,524 |

| বিষয় | মোট | T1 | T2 | T3 | 2014–26 MCQ | নতুন কার্ড |
|---|---|---|---|---|---|---|
| পদার্থবিজ্ঞান | 2,084 | 91 | 393 | 1,600 | 379 | 0 |
| রসায়ন | 2,422 | 59 | 395 | 1,968 | 435 | 223 |
| উদ্ভিদবিজ্ঞান | 1,022 | 17 | 230 | 775 | 247 | 0 |
| প্রাণিবিজ্ঞান | 1,584 | 38 | 365 | 1,181 | 338 | 0 |

Past-paper questions keep their **original four options** and the **answer letter**. Where it helps, they also carry a one-line explanation and the other years the question was asked.

## Does it work? (backtest)

The set was rebuilt as if one exam had not happened yet, and then checked against that exam. A question counts as covered when a card states the same fact (text similarity above 0.5).

| Held-out exam | Whole repo (25,107 cards) covers | This set (~6,900 cards, 28% of the repo) covers | T1 + T2 only (~1,550 cards) |
|---|---|---|---|
| MAT 25-26 | 57% | **49%** | 23% |
| MAT 24-25 | 69% | **41%** | 16% |
| DAT 24-25 | 60% | **44%** | 17% |

With about a quarter of the cards, the set catches roughly 70–85% of what the whole repo would catch. Raising the T3 budget from about 6,900 to 9,700 cards added only 2–4 more questions per paper. That is why the default stays focused.

## What the past papers show

- **Exact repeats are real but not the majority.** About 10% of 2014–26 science questions repeat an earlier MAT/DAT/AFMC question almost word for word. The rate is rising: 16% in the 2023-24 papers, 13% in 2024-25 and 21% in MAT 25-26. Topics repeat far more often than exact questions, which is why T3 exists.
- **Chemistry is the biggest science block, at about 23 questions per paper.** Recently, organic chemistry (রসায়ন ২য় পত্র অধ্যায় ২) and quantitative chemistry (অধ্যায় ৩) have grown: in 2022-23 to 2025-26 they averaged **6.6** and **5.7** questions per paper, against 4.4 and 3.5 across all years.
- **Biology (about 30 per paper):** the heaviest chapters are পরিপাক ও শোষণ (3.0 per paper), সমন্বয় ও নিয়ন্ত্রণ (2.9), অণুজীব (2.2), কোষ রসায়ন (2.0) and উদ্ভিদ শারীরতত্ত্ব (1.9). প্রাণীর আচরণ (0.14) and ব্রায়োফাইটা-টেরিডোফাইটা (0.27) are the lightest.
- **Physics (about 20 per paper):** questions are spread evenly. চল তড়িৎ, ভৌত জগৎ ও পরিমাপ, কাজ-শক্তি-ক্ষমতা and মহাকর্ষ each get about 1.4–1.6 per paper. তাপগতিবিদ্যা has risen recently (2.0 per paper since 2022-23).
- MAT/DAT 2014-15 was effectively one shared paper (90 of 100 questions are the same), and 2015-16 shares 44 questions. Each of these pairs is counted as **one** occurrence, so they don't inflate the repeat counts.

### Most repeated questions

| প্রশ্ন | উত্তর | যে পরীক্ষাগুলোতে এসেছে |
|---|---|---|
| কানের কোন অংশ ভারসাম্য রক্ষায় কাজ করে? | ভেস্টিবুলার যন্ত্র | MAT 7-8, DAT 11-12, MAT 11-12, MAT 17-18, AFMC 19-20, MAT 24-25 |
| পৃথিবীর মুক্তিবেগ | 11.2 km s⁻¹ | AFMC 19-20, 20-21, 22-23, 23-24, MAT 25-26 |
| মাতৃদুগ্ধে কোন Immunoglobulin থাকে? | IgA | MAT 16-17, DAT 19-20, MAT 21-22, DAT 22-23, MAT 22-23 |
| ভরবেগ দ্বিগুণ হলে গতিশক্তি | চারগুণ | MAT/DAT 14-15, MAT/DAT 15-16, AFMC 21-22, MAT 23-24 |
| মৃদু এসিড ও তীব্র ক্ষারকের টাইট্রেশনে নির্দেশক | ফেনলফথ্যালিন | MAT/DAT 14-15, MAT 17-18, MAT 21-22 |
| STP তে গ্যাসের মোলার আয়তন | 22.4 L | MAT 06-07, MAT 22-23, DAT 23-24, DAT 24-25 |
| রান্নার সিলিন্ডারে কী থাকে? | বিউটেন ও প্রোপেন | MAT 17-18, DAT 19-20, DAT 24-25 |
| এক আলোকবর্ষ | 9.4 × 10¹² km | DAT 2-3, DAT 17-18, DAT 20-21, MAT 24-25 |
| 1 kWh = ? J | 3.6 × 10⁶ J | MAT 2-3, AFMC 18-19, AFMC 20-21, MAT 21-22 |
| অপটিক্যাল ফাইবার কোন নীতিতে কাজ করে? | পূর্ণ অভ্যন্তরীণ প্রতিফলন | MAT 22-23, DAT 23-24, DAT 24-25 |
| এরিথ্রোপয়েটিন উৎপন্ন হয় | বৃক্কে | DAT 16-17, MAT 19-20, MAT 25-26 |
| অগ্ন্যাশয়ের আলফা কোষ থেকে নিঃসৃত হয় | গ্লুকাগন | MAT 13-14, MAT/DAT 14-15, MAT 25-26 |
| ভরসংখ্যা সমান, পারমাণবিক সংখ্যা ভিন্ন | আইসোবার | MAT 17-18, DAT 20-21, MAT 25-26 |
| অপটিক্যাল ফাইবারের প্রধান উপাদান | SiO₂ | MAT 18-19, MAT 25-26 (+ মেডিকেল ভর্তি প্রশ্ন) |
| 4.9 m s⁻¹ বেগে খাড়া উপরে ছুড়লে শূন্যে থাকে | 1 s | MAT/DAT 15-16, MAT 24-25, DAT 24-25 |
| যকৃতে ইউরিয়া তৈরি হয় কোন চক্রে? | অরনিথিন চক্র | MAT 15-16, DAT 19-20, MAT 24-25 |
| কার্নো চক্রের চতুর্থ ধাপ | রুদ্ধতাপীয় সংকোচন | DAT 16-17, DAT 21-22, DAT 22-23 |
| ওজন অর্ধেক হবে কত উচ্চতায়? | ≈ 2650 km (√2 − 1)R | MAT 14-15, DAT 22-23, AFMC 23-24 |
| তীব্র অ্যাসিড ও মৃদু ক্ষারকের টাইট্রেশনে নির্দেশক | মিথাইল অরেঞ্জ | DAT 10-11, MAT 21-22, MAT 23-24 |
| ক্ষারীয় বাফার | NH₄Cl + NH₄OH | DAT 21-22, MAT 21-22, MAT 23-24 |

All T1 questions are in `lists/` and in the T1 decks.

## Chapter weights (2014-15 to 2025-26, 22 papers)

"প্রতি পরীক্ষায়" is the average number of questions per paper. "সাম্প্রতিক" is the same average over the 7 papers from 2022-23 to 2025-26. "পুনরাবৃত্তি" counts the question-topics in that chapter that were asked in more than one exam.

### পদার্থবিজ্ঞান
| পত্র | অধ্যায় | প্রশ্ন | প্রতি পরীক্ষায় | বিষয়ের % | সাম্প্রতিক | পুনরাবৃত্তি |
|---|---|---|---|---|---|---|
| ১ম | 1. ভৌত জগৎ ও পরিমাপ | 32 | 1.45 | 7.1% | 1.29 | 1 |
| ১ম | 2. ভেক্টর | 11 | 0.50 | 2.5% | 0.57 | 0 |
| ১ম | 3. গতিবিদ্যা | 22 | 1.00 | 4.9% | 1.00 | 0 |
| ১ম | 4. নিউটনিয়ান বলবিদ্যা | 17 | 0.77 | 3.8% | 0.57 | 1 |
| ১ম | 5. কাজ, শক্তি ও ক্ষমতা | 31 | 1.41 | 6.9% | 1.00 | 1 |
| ১ম | 6. মহাকর্ষ ও অভিকর্ষ | 31 | 1.41 | 6.9% | 1.29 | 2 |
| ১ম | 7. পদার্থের গাঠনিক ধর্ম | 23 | 1.05 | 5.1% | 0.86 | 0 |
| ১ম | 8. পর্যাবৃত্ত গতি | 12 | 0.55 | 2.7% | 0.29 | 0 |
| ১ম | 9. তরঙ্গ | 22 | 1.00 | 4.9% | 1.43 | 2 |
| ১ম | 10. আদর্শ গ্যাস ও গ্যাসের গতিতত্ত্ব | 22 | 1.00 | 4.9% | 0.57 | 2 |
| ২য় | 1. তাপগতিবিদ্যা | 28 | 1.27 | 6.2% | 2.00 | 2 |
| ২য় | 2. স্থির তড়িৎ | 12 | 0.55 | 2.7% | 0.57 | 0 |
| ২য় | 3. চল তড়িৎ | 36 | 1.64 | 8.0% | 1.57 | 5 |
| ২য় | 4. তড়িৎ প্রবাহের চৌম্বক ক্রিয়া ও চুম্বকত্ব | 21 | 0.95 | 4.7% | 0.86 | 2 |
| ২য় | 5. তড়িৎচৌম্বক আবেশ ও পরিবর্তী প্রবাহ | 6 | 0.27 | 1.3% | 0.29 | 0 |
| ২য় | 6. জ্যামিতিক আলোকবিজ্ঞান | 28 | 1.27 | 6.2% | 1.43 | 4 |
| ২য় | 7. ভৌত আলোকবিজ্ঞান | 23 | 1.05 | 5.1% | 0.86 | 0 |
| ২য় | 8. আধুনিক পদার্থবিজ্ঞানের সূচনা | 22 | 1.00 | 4.9% | 1.14 | 2 |
| ২য় | 9. পরমাণুর মডেল ও নিউক্লিয়ার পদার্থবিজ্ঞান | 23 | 1.05 | 5.1% | 1.57 | 1 |
| ২য় | 10. সেমিকন্ডাক্টর ও ইলেকট্রনিক্স | 14 | 0.64 | 3.1% | 0.29 | 1 |
| ২য় | 11. জ্যোতির্বিজ্ঞান | 12 | 0.55 | 2.7% | 0.29 | 2 |

### রসায়ন
| পত্র | অধ্যায় | প্রশ্ন | প্রতি পরীক্ষায় | বিষয়ের % | সাম্প্রতিক | পুনরাবৃত্তি |
|---|---|---|---|---|---|---|
| ১ম | 1. ল্যাবরেটরির নিরাপদ ব্যবহার | 29 | 1.32 | 5.7% | 1.86 | 1 |
| ১ম | 2. গুণগত রসায়ন | 36 | 1.64 | 7.1% | 1.29 | 1 |
| ১ম | 3. মৌলের পর্যায়বৃত্ত ধর্ম ও রাসায়নিক বন্ধন | 54 | 2.45 | 10.6% | 1.43 | 3 |
| ১ম | 4. রাসায়নিক পরিবর্তন | 64 | 2.91 | 12.6% | 2.43 | 2 |
| ১ম | 5. কর্মমুখী রসায়ন | 31 | 1.41 | 6.1% | 1.00 | 2 |
| ২য় | 1. পরিবেশ রসায়ন | 55 | 2.50 | 10.8% | 2.29 | 3 |
| ২য় | 2. জৈব রসায়ন | 96 | 4.36 | 18.9% | **6.57** | 7 |
| ২য় | 3. পরিমাণগত রসায়ন | 77 | 3.50 | 15.1% | **5.71** | 6 |
| ২য় | 4. তড়িৎ রসায়ন | 25 | 1.14 | 4.9% | 0.71 | 0 |
| ২য় | 5. অর্থনৈতিক রসায়ন | 42 | 1.91 | 8.3% | 1.00 | 1 |

### উদ্ভিদবিজ্ঞান
| অধ্যায় | প্রশ্ন | প্রতি পরীক্ষায় | বিষয়ের % | সাম্প্রতিক | পুনরাবৃত্তি |
|---|---|---|---|---|---|
| 1. কোষ ও এর গঠন | 26 | 1.18 | 8.8% | 1.14 | 2 |
| 2. কোষ বিভাজন | 14 | 0.64 | 4.7% | 0.71 | 1 |
| 3. কোষ রসায়ন | 44 | 2.00 | 14.9% | 2.29 | 3 |
| 4. অণুজীব | 48 | 2.18 | 16.2% | 2.57 | 2 |
| 5. শৈবাল ও ছত্রাক | 23 | 1.05 | 7.8% | 1.14 | 1 |
| 6. ব্রায়োফাইটা ও টেরিডোফাইটা | 6 | 0.27 | 2.0% | 0.00 | 0 |
| 7. নগ্নবীজী ও আবৃতবীজী উদ্ভিদ | 22 | 1.00 | 7.4% | 0.43 | 2 |
| 8. টিস্যু ও টিস্যুতন্ত্র | 10 | 0.45 | 3.4% | 0.57 | 1 |
| 9. উদ্ভিদ শারীরতত্ত্ব | 42 | 1.91 | 14.2% | 1.71 | 1 |
| 10. উদ্ভিদ প্রজনন | 17 | 0.77 | 5.7% | 0.29 | 0 |
| 11. জীবপ্রযুক্তি | 25 | 1.14 | 8.4% | 1.57 | 1 |
| 12. জীবের পরিবেশ, বিস্তার ও সংরক্ষণ | 19 | 0.86 | 6.4% | 1.57 | 0 |

### প্রাণিবিজ্ঞান
| অধ্যায় | প্রশ্ন | প্রতি পরীক্ষায় | বিষয়ের % | সাম্প্রতিক | পুনরাবৃত্তি |
|---|---|---|---|---|---|
| 1. প্রাণীর বিভিন্নতা ও শ্রেণিবিন্যাস | 23 | 1.05 | 6.1% | 1.29 | 0 |
| 2. প্রাণীর পরিচিতি | 38 | 1.73 | 10.1% | 1.29 | 0 |
| 3. পরিপাক ও শোষণ | 66 | 3.00 | 17.5% | 2.86 | 4 |
| 4. রক্ত ও সঞ্চালন | 41 | 1.86 | 10.8% | 1.57 | 3 |
| 5. শ্বসন ও শ্বাসক্রিয়া | 21 | 0.95 | 5.6% | 1.29 | 1 |
| 6. বর্জ্য ও নিষ্কাশন | 19 | 0.86 | 5.0% | 0.57 | 2 |
| 7. চলন ও অঙ্গচালনা | 29 | 1.32 | 7.7% | 1.00 | 0 |
| 8. সমন্বয় ও নিয়ন্ত্রণ | 63 | 2.86 | 16.7% | 1.86 | 6 |
| 9. মানব জীবনের ধারাবাহিকতা | 18 | 0.82 | 4.8% | 1.00 | 0 |
| 10. মানবদেহের প্রতিরক্ষা | 35 | 1.59 | 9.3% | 2.00 | 1 |
| 11. জিনতত্ত্ব ও বিবর্তন | 22 | 1.00 | 5.8% | 0.86 | 0 |
| 12. প্রাণীর আচরণ | 3 | 0.14 | 0.8% | 0.14 | 0 |

## How to study it

1. **T1 first, then T2.** These ~1,600 cards are what has actually been asked, so learn every one. Read the "নোট" lines, because some old answer keys were wrong (see below).
2. **Then T3 by score.** Inside each deck, cards are in score order, so stop wherever time runs out.
3. In the study web app, open Settings → New card order → **Most probable first (past-paper ranking)**. New cards then follow the score, highest first. Your existing progress is kept.
   - Past-paper MCQs show their real exam options, and MCQ mode uses those options.
   - Ranked cards show a `P 87`-style tag.
4. For printing or quick reading, use `lists/Most_Probable_<Subject>.md`. It is the same content, grouped by tier and chapter.

## Files

| Path | What |
|---|---|
| `MAT_Most_Probable_<Subject>.apkg` | Anki decks: `MAT সবচেয়ে সম্ভাব্য প্রশ্ন::<বিষয়>::<T1/T2/T3>::<অধ্যায়>`; tags `MP_T1`, `MP_T2`, `MP_T3`, `PYQ` |
| `lists/Most_Probable_<Subject>.md` | Readable / printable lists |
| `source/mp_<subject>.txt` | Card source: `# [chapter] Tn \| topic`, then `Q:` `A:` `Y:` `R:` (score), and an optional `L:` that links to the existing card covering it |
| `source/new_c1_ch02_part1.txt` | 223 new cards for রসায়ন ১ম পত্র অধ্যায় ২ (2.1–2.11), which was missing from the repo: fundamental particles, isotopes and their uses, Rutherford/Bohr models, quantum numbers, orbitals, Aufbau/Pauli/Hund, configurations, the EM spectrum, hydrogen spectral series, UV/IR/MRI uses, solubility |
| `data/past_papers.json` | All 22 parsed papers (2,193 questions including English/GK): options, key, explanation, exam |
| `data/cls_final.json`, `groups.json`, `chapter_stats.json` | Chapter for every question, repeat groups, chapter statistics |
| `data/fixes.json`, `overrides.txt` | Hand corrections: answer keys and chapter assignments |
| `tools/` | The pipeline (see below) |

## How it was made

1. **Parse** (`parse_papers.py`): reads the saved chorcha.net pages. The correct option is the green one. LaTeX is turned into plain text with sub- and superscripts.
2. **Classify** (`classify.py`): assigns each question to a chapter, by character n-gram TF-IDF nearest neighbours against every card in this repo, limited to the paper's own subject section. All 312 low-confidence assignments were checked by hand (`data/overrides.txt`). English, GK and humanities questions are left out.
3. **Repeats** (`repeats.py`): groups the same question across exams, using question and answer similarity. Short generic stems such as "কোনটি সঠিক?" need a near-identical answer to match.
4. **Match** (`match.py`): links each past question to the repo card that covers it. That card's older year tags extend the history back to the 2000s.
5. **Rank** (`rank.py`):
   - Past questions score 60, plus 10 for every extra exam, plus a recency bonus.
   - Older-only PYQ cards score 52–79.
   - Every other repo card gets a "hotness" score: 65% how close it is to any past question, 35% how often past questions hit its topic. Each chapter gets a quota in proportion to its weight in the papers, filled with its hottest cards (scores 30–49).
6. **Output** (`make_sets.py`, `build_decks.py`). The web app reads `source/mp_*.txt` through `../webapp/build_data.py`.

### Answer-key corrections
chorcha.net's keys were used as given, except where a key was blank, self-contradictory, or wrong. In those cases the card gives the correct answer and a `নোট:` line. Examples:
- The half-weight height is 2650 km, not 1600 km.
- Planck's principle → Pauli's exclusion principle.
- Absolute alcohol is 100% ethanol, not methylated spirit.
- The safe food preservative is sodium benzoate.
- Water heated from 0 to 10 °C first contracts, then expands.
- Blank keys were filled where an option is correct; where none is, the card says so.

All 95 numerical Physics and Chemistry past questions were re-solved by hand. All 17 corrections are in `data/fixes.json`.

### Limits
- Chapter assignment is automatic, with the uncertain cases checked by hand. A few questions near chapter boundaries may sit in the neighbouring chapter.
- The Botany decks in this repo have no year tags, so Botany T1/T2 come only from the 2014–26 papers.
- "Probable" means the exam's own history says so. It cannot see this year's question setters, so treat T3 as a well-ordered revision list, not a prediction of exact questions.

### Rebuilding
```bash
pip install genanki scikit-learn beautifulsoup4
cd "Most Probable Questions/tools"
python3 parse_papers.py <folder with the saved chorcha .html pages> ../data/past_papers.json   # only if papers change
python3 classify.py && python3 repeats.py && python3 match.py && python3 rank.py
python3 make_sets.py && python3 build_decks.py
cd ../../webapp && python3 build_data.py
```
- **Bigger T3:** set `MP_BUDGET=7000 MP_CAP=0.6` before running `rank.py`.
- **Backtest:** run `HOLDOUT='MAT 25-26' python3 rank.py && HOLDOUT='MAT 25-26' python3 backtest.py`.
