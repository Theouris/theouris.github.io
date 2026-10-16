# Neuro 2: Neural Signaling and Spinal Cord

Open `index.html` for the bullet-point lecture and `practice.html` for the question tab. The folder works as a static website at `/neuro2/` and requires no build, account, or external service to use. A link is included in the shared website menu.

## Included

- All 76 source slides: 58 Neural Signaling slides by Larry D. Alexander and 18 Spinal Cord post-class slides by Aftab Merchant.
- Complete page images retain every original figure, graph, table, label, cartoon, and attribution. Click an image to enlarge; both original PDFs are included for original vector/detail access.
- Expanded bullet notes for all 62 instructional/summary slides, plus original extracted text for every slide. Fourteen title/objective/outline/divider/closing pages are also retained.
- Nine related board-review supplements, including electrical signaling, receptor coding, special senses, pain mechanisms, spinal tracts, vascular/autonomic complications, metabolic/genetic disease, clinical localization, and cross-sectional landmarks.
- 158 original single-best-answer, five-choice questions, with 790 choice-specific explanations. Stems range from 4 to 74 words, including paragraph-length clinical vignettes.
- Slide-to-question coverage map and references.
- Lecture search, image toggle, practice topic/deck/review filters, shuffle, retry, deep links, and local saved progress.

After submission, practice scrolls and focuses the choice-by-choice reasoning. A docked **Next question** button appears and stays accessible while explanations are read. Next loads the next question and scrolls to its stem. At the last item in a filtered set, Next is disabled and the set's end is indicated. Reduced-motion preference is respected.

Original document instructions and contact details remain source content. The added notes explicitly correct or qualify CNS versus peripheral demyelination, graded retinal responses, sour taste transduction, multifactorial sensory disorders, and clinical pattern exceptions. Questions are original NBME-style study material, not official NBME items.

## Content and maintenance

Edit `notes.json`, `board-review.json`, `sources.json`, and `questions.txt`. A question line contains eight pipe-separated fields: source-section reference, topic, stem, correct choice, and four distractors. Each choice has `text~explanation`. `build.py` deterministically shuffles answer choices, validates coverage, and generates the HTML pages and question data.

Run `python neuro2/build.py` from the repository root. Only Python's standard library is needed for rebuilding. `extract.py` is the separate source-PDF rendering helper and uses pdfplumber, Pillow, and Poppler; its configured source/runtime paths match the task machine. Extraction is not needed to use or rebuild existing content.

## Verification

- Build checks pass for all 76 image files, both PDFs, 62 instructional sections with linked questions, all nine supplements with questions, unique stems, five distinct choices per item, rationales, and valid references.
- `verify.mjs` passed DOM interaction tests for all 158 correct submissions and 790 rationales; automatic explanation scrolling/focus; docked Next through the entire bank; last-item state; incorrect answer; retry; filters; shuffle; question deep links; saved-state reload; disabled storage; lecture search/image toggle; and local files/anchors.
- The optional DOM tests require happy-dom. Install that development dependency separately and set `NEURO_DOM_MODULE` to its absolute `lib/index.js` path, or make `happy-dom` resolvable to Node, then run `node neuro2/verify.mjs`. The website has no runtime dependency on it.
- All 76 slide renders were visually checked in contact sheets; selected figures were additionally inspected at full size.
- Browser visual QA was unavailable because no browser surface was connected. DOM tests verify behavior and requested scroll calls, not actual pixel layout or physical scrolling in a browser.
- Files are local repository changes. No commit, push, or deployment was performed.

Progress is stored only in the current browser/origin, separately from Neuro 1. When browser storage is unavailable, practice still works for the page session and displays that limitation.
