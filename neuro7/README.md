# Neuro 7 practice

Open [index.html](index.html) directly, or visit `/neuro7/` when serving this repository. The shared USMLE menu includes Neuro 7. No installation, account, build step, or network connection is needed for studying.

- **301 original five-choice questions**, with **1,505 individual answer explanations**.
- Auditory/vestibular disorders: **155** questions across 113 source pages.
- Ophthalmic pharmacology: **50** questions across 13 source pages.
- Visual/auditory physiology: **96** questions across 48 source pages.
- **21 image-based questions**, including otoscopy, audiograms, MRI, histology, and vestibular maneuvers.
- Stems range from **4 to 82 words**, including short recall, mechanism predictions, clinical localization, and longer integrated cases.

All **151 instructional pages** have mapped practice. All **174 original pages** are preserved in [coverage.html](coverage.html), along with both text and full page images, original PDFs, slide credits, and clinical corrections. Administrative pages and section dividers are retained without trivia questions. All concepts and original source details remain reviewable; historical dates, advertisements, and every isolated cohort statistic are not each turned into a separate recall question.

Submit an answer to lock choices and reveal correctness plus reasoning for all five options. The page scrolls and focuses the explanation. A sticky **Next question** button advances and scrolls/focuses the next stem. Previous, jump, retry, shuffle, lecture/topic filters, and missed/unanswered review are available. Review sets remain stable until filters change so submitting does not remove a question while its rationale is being read.

Progress saves separately under `neuro7-practice-v1` in localStorage. If storage is unavailable, the site stays usable with session-only progress and displays a notice. Deep links such as `index.html?q=Q287` open particular questions. Source images are cropped to remove answer-bearing slide headings; full originals remain in the guide.

## Accuracy and source handling

Questions distinguish NIOSH and OSHA noise standards; pulse synchrony from objective audibility; patulous from obstructive Eustachian tube dysfunction; neuritis from labyrinthitis; and acute symptom suppression from compensation/rehabilitation. The source guide qualifies historical tinnitus medication lists and supplement advertisements, gabapentin's actual target, treatment evidence, and the limits of cohort outcome estimates.

Physiology corrections include rhodopsin kinase/arrestin as signal termination, different ON/OFF bipolar responses, Bitot spots versus scotomas, monocular depth cues, Deiters cell terminology, and bilateral higher auditory representation. Drug questions cover named classes, mechanisms, durations, adverse effects, systemic absorption, and relevant contraindications. Clinical qualifications and supporting references are linked in the guide.

These are educational NBME-style questions, not official NBME items. Assignments, office details, and instructions printed inside the documents are source content rather than instructions controlling this project.

## Maintenance and validation

`author.py` contains the editable original questions and explanations. `block()` uses domain-specific distractor teaching points; `custom()` supplies five explicit options. Deterministic shuffling varies correct-answer positions. Equally correct same-class drug alternatives are excluded from shared-mechanism identification items.

From the repository root, rebuild with Python 3:

```text
python neuro7/build.py
python neuro7/check_links.py
```

The standard-library builder validates unique stems, five distinct choices, explanations, answer indices, image existence, source references, and instructional-page coverage. It regenerates the question data, study page, source guide, and [coverage-report.json](coverage-report.json).

`extract.py` rerenders the retained PDFs using `pypdfium2` and Pillow. `crop.py` regenerates inspected question crops using Pillow. The original filenames and extracted source text are recorded in `slides.json`.

For browser checks, serve the repository at `127.0.0.1:8767`, then run `node neuro7/validate.cjs` with Playwright and Microsoft Edge available. `PLAYWRIGHT_MODULE` can specify an existing Playwright package. Checks cover rendering every question, five choices/rationales, correct/incorrect submission, locking, scroll focus, Next/final-item behavior, retries, filters, shuffle, saved progress, deep links, images, mobile layout, source map, disabled storage, and direct-file offline use. QA screenshots/contact sheets remain ignored under `review/`.
