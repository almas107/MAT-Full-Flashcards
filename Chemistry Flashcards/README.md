# Chemistry MAT Flashcards (Anki)

Anki decks for **রসায়ন ১ম ও ২য় পত্র**, one `.apkg` per chapter, written in the style of DGME MAT/DAT questions.

## Sources
1. **প্রশ্নব্যাংক (Unmesh Medical Master QB 26-27)**: every MCQ in each chapter's topic sections is a card. Year tags printed in the QB (e.g. `[MAT 22-23]`) are kept.
2. **Past medical-admission questions** from the uploaded `chemistry_mcq_qa.md`. Each was mapped to its chapter; ones not already covered were added. The file has no years, so these carry the tag `মেডিকেল ভর্তি প্রশ্ন`.
3. **Textbook pages marked in red or green**: only highlighted lines, bracketed paragraphs or sections, and marked math problems.

Where the QB answer key and the textbook disagree, or a key looks wrong, the card gives the exam answer and notes the correction.

## Card style
- Front: a direct recall question in Bengali. Back: a short answer. `বৈশিষ্ট্য`/list cards give terse items separated by line breaks.
- No definition cards and no "why" or explanation cards.
- **Negative stems** ("কোনটি নয়/সঠিক নয়") keep all four options on the front, so you see the whole set. The back gives `✗ wrong option — short reason`. This way you learn the trap and, implicitly, the three true facts.
- Math cards give the final value, plus at most one formula or step.
- Cards seen in past exams carry a **PYQ** tag and a year line. Each chapter deck has topic subdecks in textbook order.

## Decks

| পত্র | অধ্যায় | শিরোনাম | ফাইল | কার্ড | PYQ |
|---|---|---|---|---|---|
| রসায়ন ১ম পত্র | 1 | ল্যাবরেটরির নিরাপদ ব্যবহার | `MAT_Chem1_Ch1_Laboratory_Safety.apkg` | 495 | 61 |
| রসায়ন ১ম পত্র | 2 | গুণগত রসায়ন (part 2: 2.12–2.20) | `MAT_Chem1_Ch2_Qualitative_Chemistry_Part2.apkg` | 265 | 20 |
| রসায়ন ১ম পত্র | 3 | মৌলের পর্যায়বৃত্ত ধর্ম ও রাসায়নিক বন্ধন | `MAT_Chem1_Ch3_Periodic_Properties_Bonding.apkg` | 407 | 0 |
| রসায়ন ১ম পত্র | 4 | রাসায়নিক পরিবর্তন | `MAT_Chem1_Ch4_Chemical_Change.apkg` | 958 | 142 |
| রসায়ন ১ম পত্র | 5 | কর্মমুখী রসায়ন | `MAT_Chem1_Ch5_Vocational_Chemistry.apkg` | 517 | 78 |
| রসায়ন ২য় পত্র | 1 | পরিবেশ রসায়ন | `MAT_Chem2_Ch1_Environmental_Chemistry.apkg` | 503 | 0 |
| রসায়ন ২য় পত্র | 2 | জৈব রসায়ন | `MAT_Chem2_Ch2_Organic_Chemistry.apkg` | 2044 | 217 |
| রসায়ন ২য় পত্র | 3 | পরিমাণগত রসায়ন | `MAT_Chem2_Ch3_Quantitative_Chemistry.apkg` | 777 | 143 |
| রসায়ন ২য় পত্র | 4 | তড়িৎ রসায়ন | `MAT_Chem2_Ch4_Electrochemistry.apkg` | 749 | 39 |
| রসায়ন ২য় পত্র | 5 | অর্থনৈতিক রসায়ন | `MAT_Chem2_Ch5_Economic_Chemistry.apkg` | 620 | 60 |
| **মোট** | | | | **7335** | **760** |

The three decks for ১ম পত্র Ch2 (part 2 only), Ch3 and ২য় পত্র Ch1 were made outside this repo and uploaded as `.apkg`.
Their card text was extracted into `source/` with `../tools/extract_apkg.py`, so they don't follow every style rule above
(some answers are longer and include a short reason). Ch2 part 1 (2.1–2.11) is still missing.

## Reviewing fast
- Open the **PYQ** tag first (Browse → tag `PYQ` → create a filtered deck), then go through the topic subdecks.
- Answers are one line, so try **Again/Good only**: press Space then 1 or 3, with 1 s or less per card. Set *New cards/day* to 100–200 and *Learning steps* to `10m 1d`.
- Turn on *Show answer timer*, and keep *Bury related* off, since cards are independent.

## Rebuilding
Card text lives in `source/c1_chNN.txt` / `source/c2_chNN.txt`:

```
# subdeck name
Q: question
A: answer || line break inside answer
Y: MAT 22-23, DAT 17-18      (optional; adds PYQ tag)
```

```
cd "Chemistry Flashcards/source"
pip install genanki
python3 dedupe.py c2_ch03.txt     # merge identical fronts
python3 build_decks.py c2_03      # one chapter
```
