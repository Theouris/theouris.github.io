# Neuro 1 study website

Open `index.html` for the lecture and `practice.html` for questions. Everything needed to read and practice is local; no build, account, or external service is required. The same folder can be served directly by GitHub Pages at `/neuro1/`. The shared website menu includes a link.

## Contents

- All 64 original slide images (25 from NNN 1.1; 39 from NNN 1.2), preserving every figure, label, and attribution.
- Both original PDFs and the original extracted slide text.
- Expanded bullet notes for all 51 instructional slides; remaining pages are titles, objectives, dividers, summaries, and credits.
- Eight related board-review supplements, with sources and explicit corrections/clarifications of slide simplifications.
- 145 original five-choice questions, including short stems and ten extended clinical vignettes; 725 individual choice rationales.
- Slide-to-question coverage map, lecture search, full-resolution image links, question filters, shuffle, retry, and browser-local progress.

Question bank items are original NBME-style study material, not official NBME questions. The additions focus on topics related to the two supplied lectures, rather than attempting to cover all of neurology.

## Editing

`notes.json`, `board-review.json`, `questions.txt`, `sources.json`, and `slides.json` are the content sources. Each question source line has eight pipe-separated fields: slide/board reference, topic, stem, correct choice with rationale, and four distractors with rationales. Choice text and rationale are separated by `~`. `build.py` shuffles answer positions deterministically and creates `index.html`, `coverage.html`, `data.js`, and `questions.json`.

Run `python build.py` from this directory or `python neuro1/build.py` from the repository root. Python's standard library is sufficient. The build validates 64 slide assets, five distinct choices per question, all answer rationales, valid section references, and practice coverage for every expanded instructional slide.

## Verification

- Build/content validations passed.
- DOM interaction checks passed for all 145 correct submissions and all 725 rendered rationales, an incorrect submission, retry, review/deck filters, shuffle, saved-state reload, question deep links, lecture search, image toggle, and all local links/anchors.
- All 64 original slide renders were visually inspected in contact sheets, with selected pages checked at full size.
- Live browser visual QA was unavailable: no browser surface was connected, and the available Playwright wrapper could not initialize. DOM checks do not verify pixel layout.
- Progress is stored only in the current browser/origin; private browsing or disabled storage may prevent persistence. The UI reports storage failure and remains usable for the session.
- Changes are local repository files; no commit, push, or public deployment was performed.
