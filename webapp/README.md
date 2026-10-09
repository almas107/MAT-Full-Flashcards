# MAT Brain Gym (study web app)

A web app for studying every flashcard in this repo (Physics, Chemistry, Botany, Zoology: 23,814 cards). It runs on spaced repetition and active recall, with a daily goal that counts down to the exam.

## What it does
- **Daily mission**: (cards you haven't seen ÷ days left before revision starts) + reviews due today. Revision-only days default to 10 before an exam on 5 Dec 2026; you can change both in Settings. The goal is fixed for the day, then re-balanced the next day from what you actually did. A skipped day never counts as progress.
- **Rounds of 20 cards** (~3 min): flip cards (think first, then flip and grade ❌ / ✅ / ⚡) mixed with MCQ cards built from answers in the same topic. A missed card comes back 4–6 cards later in the same round, then again tomorrow.
- **Spaced repetition**: boxes 1 → 3 → 7 → 14 → 30 days. A card counts as **mastered** at box 3, which means you recalled it at both a 1-day and a 3-day gap. Every card is shown once more the day before the exam.
- **Memory trick on every card**, made automatically from the card itself: first-letter chains for lists, number-shape pictures for numbers and years, trap warnings for "✗" cards, sound-alikes for scientific names, two-part reminders, and keyword bridges. You can also write your own trick for any card.
- **Error log**: every miss, with search, a subject filter, and a "drill these" button. A card counts as fixed after 2 correct answers in a row and reaching box 3.
- **Progress**: seen %, mastered %, 7-day accuracy against the 90% target, pace and projected finish date, a study calendar, and a "chapter monster" for each chapter. Tap a monster to start a focus round on that chapter.
- **Fun**: wiggly hand-drawn lines, synthesized sounds, combos, XP and levels, confetti, a mascot, and a 2-minute brain break. Keys: Space = flip / got it, 1/2/3 = grade, H = hint, Esc = end round.

## Files
- `app.html`: the app (page body as published to claude.ai).
- `index.html`: standalone copy, generated from `app.html`.
- `cards.json`: all cards, generated from the `source/*.txt` files.
- `build_data.py`: regenerates `cards.json` and `index.html`. Run `python3 build_data.py` after editing any card source or `app.html`.

Card ids hash the question text, so fixing an answer keeps your progress on that card.

## Running locally
```
cd webapp
python3 -m http.server 8000
# open http://localhost:8000
```
Progress is saved in the browser. Inside claude.ai it is also synced to your account. Settings → Backup copies everything as text.
