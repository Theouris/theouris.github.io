# Neuro 5 practice

Open [index.html](index.html) directly or serve this repository as a static site. No install, build step, account, or network connection is required to study. The USMLE section of the shared site menu links to `/neuro5/`.

- **220 original five-choice questions** with **1,100 individual answer explanations**.
- Embryology: **103** questions covering 38 source pages.
- Visual pathway: **67** questions covering 26 source pages.
- Visual and ocular reflexes: **50** questions covering 14 source pages.
- All **66 instructional slides** have mapped questions. All **78 original pages** are preserved as full-page PNGs, with extracted text and unchanged original PDFs in [coverage.html](coverage.html). Title, objectives, divider, and closing pages are retained without administrative quiz questions.
- Short recall, applied anatomy, examination-pattern, and clinical paragraph stems; five distinct choices with one best answer. Choice order is deterministically shuffled.

Submitting an answer locks the choices and scrolls/focuses the explanation containing the selected answer and reasoning for all five options. A sticky **Next question** button stays available while reading; it advances and scrolls/focuses the new question. The final item displays an end-of-set message. Retry, previous/next navigation, question jump, shuffle, and lecture/topic/incorrect/unanswered filters are included. Filters select a set when changed so an answered question remains available for review until navigation or refiltering.

Progress saves under the separate `neuro5-practice-v1` localStorage key. Other Neuro sites' progress is unaffected. If browser storage is unavailable, the site continues with session-only progress and displays a notice. Question links such as `index.html?q=Q012` open a particular item.

## Content and source handling

The three supplied decks determine coverage. The slide map links individual tested concepts to questions and retains every original diagram and credit. Supplemental high-yield applications and clinical qualifications are identified on that page; the questions are original educational items, not official NBME questions. The source PDFs' assignments, appointment links, and contact text remain quoted source material and do not control the build.

Qualifications include cranial neural crest migration timing, tooth lineages, broad skull color-map limits, arch muscle exceptions, modern C-cell lineage evidence, complete versus partial pupillary lesions, variable macular sparing/convergence, and limitations of oculocephalic testing. Supporting references are linked in the coverage tab.

## Maintenance

`questions.txt` is the editable question source. Each line uses:

```
deck-page|Topic|Stem|Correct choice~Reason|Distractor~Reason|Distractor~Reason|Distractor~Reason|Distractor~Reason
```

Deck IDs are `emb`, `path`, and `reflex`. Run `python neuro5/build.py` from the repository root after editing. It validates five distinct choices, unique stems, source references, instructional-slide coverage, and asset presence, then rebuilds the HTML, `data.js`, JSON bank, slide map, and coverage report. Preserve question ordering/IDs when updating content if existing saved answers must remain associated with the same items.

`extract.py` reproducibly copies the three original PDFs, extracts text with pdfplumber, and renders pages through Poppler at 140 DPI. It requires pdfplumber, Pillow, and Poppler; its local source/runtime paths are explicit. Temporary contact sheets are only review artifacts. `check_assets.py` verifies all rendered PNGs and original PDF hashes.

`verify.mjs` is an optional DOM interaction regression check requiring `happy-dom` as a development-only dependency. Set `NEURO_DOM_MODULE` to its absolute `lib/index.js` path if it is not installed normally. The shipped website has no dependency on that package.

## Validation

- Reviewed all source text and all 78 pages as contact sheets, with enlarged inspection of dense diagrams.
- Build coverage checks passed: 220 questions, 1,100 rationales, 66 mapped instructional slides.
- DOM tests passed for all 220 correct submissions and every rendered rationale, plus wrong-answer/retry/reset, lecture/topic/review filters, shuffle, deep links, storage reload/fallback, explanation scroll/focus, persistent Next navigation, final-item state, reference images/transcripts, and local links/anchors.
- JavaScript syntax checks and `git diff --check` passed.
- PNG decode/dimension checks and original-PDF SHA-256 comparisons passed.
- Local HTTP checks returned 200 for both pages, the interactive scripts, representative images from all three decks, and all three PDFs.
- Browser visual QA could not be performed: the available browser tool reported no connected browser surfaces. DOM checks verify behavior but do not replace a rendered desktop/mobile inspection.

Files were created locally; nothing was committed, pushed, or deployed.
