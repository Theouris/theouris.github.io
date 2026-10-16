# Neuro 4: Brainstem Localization Practice

Open `index.html` for the question bank and `coverage.html` for the slide-to-question map and source references. The static folder is ready for `/neuro4/` and is linked from the shared website menu. No build, account, network connection, or external service is required to use the site.

## Included

- 88 original NBME-style, single-best-answer questions with five choices and 440 choice-specific explanations.
- Short recall stems and paragraph-style clinical vignettes covering all 20 instructional slides in the 23-page NNN 4.1 deck.
- Arterial branches/territories, complete image-only nuclei chart, localization method, crossed findings, medial/lateral structures, Horner, medial/lateral medulla and pons, AICA/PICA comparison, Weber, and Parinaud.
- Original PDF and all 23 page renders, including title, objectives, image-only chart, and credits. Original figures and labels are retained in the reference tab.
- Coverage checklists, question links for every instructional slide, and supporting sources.
- Topic/review filters, shuffle, question jump/deep links, retry, reset, and saved browser-local progress.

Submitting an answer scrolls to and focuses the choice-by-choice reasoning. A persistent **Next question** button appears there and stays accessible while reading. Next loads the following item and scrolls to its stem. The last item in the selected set shows an end message and disables Next. Reduced-motion preference is respected.

The original deck's preparation instructions, readings, and author information remain source material, not website instructions. Clinical explanations qualify classic patterns where needed, including vascular variation, VI fascicle versus nucleus, central sympathetic laterality, and traditional cranial-XI terminology. Questions are original practice items, not official NBME questions.

## Maintenance

`questions.txt` contains eight pipe-separated fields per item: source slide number, topic, stem, correct choice, and four distractors. Each choice uses `text~explanation`. `topics.json` defines slide coverage; `slides.json` records source text and assets; `sources.json` contains supporting references.

Run `python neuro4/build.py` from the repository root. Only Python's standard library is needed. The build checks unique stems, five distinct choices, explanations, valid slide references, all 23 slide assets, the source PDF, and questions for every instructional slide. It shuffles choices deterministically and produces HTML, JSON/JavaScript question data, and a coverage report.

`extract.py` is a separate PDF rendering helper configured for this task machine's source/runtime paths; it uses pdfplumber, Pillow, and Poppler. It is not needed to use or rebuild the existing site.

## Verification

- Build/content coverage checks passed.
- DOM tests passed for all 88 correct submissions and 440 explanations; wrong answers, retry/reset, filters, shuffle, deep links, saved-state reload, disabled storage, automatic scroll/focus, persistent Next through the full bank, last-item state, reference images, and local links/anchors.
- All 23 slide renders were visually inspected in contact sheets.
- Browser visual testing was unavailable because no browser surface was connected. DOM tests verify behavior and scroll requests, not pixel layout or physical browser scrolling.
- Optional `verify.mjs` tests require happy-dom separately. Set `NEURO_DOM_MODULE` to its absolute `lib/index.js`, or make `happy-dom` resolvable to Node, then run `node neuro4/verify.mjs`. It is not a runtime dependency of the site.
- Changes are local repository files; no commit, push, or deployment was performed.

Progress is stored separately from Neuro 1-3 in the current browser/origin. If storage is unavailable, questions still work for the page session and the interface reports the persistence limitation.
