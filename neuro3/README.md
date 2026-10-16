# Neuro 3: Cranial Nerves and Brainstem I

Open `index.html` for the lecture, `practice.html` for questions, and `coverage.html` for the slide-to-question map and references. The user confirmed that only the listed NNN 3 Cranial Nerves I PDF should be included. The static folder is ready for `/neuro3/`, with a link in the shared website menu. No build, account, or external service is required to use it.

## Included

- All 68 original slide images and the original PDF; every diagram, table, photograph, label, and source credit is retained. Click a slide to enlarge it; consult the PDF for original vector/detail access.
- Expanded bullet notes for all 57 instructional pages, including the image-only nuclei chart on slide 57. Eleven title, objective, divider, and closing pages are also retained.
- Complete named facial-muscle coverage, skull routes, functional components, nuclei, cranial motor/sensory/autonomic functions, reflexes, peripheral versus central lesions, long tracts, cross-sections, and arterial supply.
- Eight labeled board-review supplements: complete cranial overview; pupils/gaze; trigeminal/facial localization; hearing/vestibular tests; bulbar/laryngeal/neck/tongue localization; vascular syndromes; cross-sectional landmarks; systematic examination.
- 180 original single-best-answer, five-choice questions: 148 linked to lecture slides and 32 to supplements. All 900 choices have their own explanations. Stems include short recall and paragraph-style clinical vignettes.
- Search, image toggle, deck/topic/review filters, shuffle, retry, question deep links, and saved browser-local progress.

Submission scrolls to and focuses the choice-by-choice explanations. A persistent docked **Next question** button remains available while reading them. Next loads the following item and scrolls to its stem. At the end of the selected set it is disabled, with an end-of-set message. Reduced-motion preference is respected.

Document readings, videos, course directions, and contact details remain source material rather than instructions executed by the site. Explicit qualifications address ocular anatomical actions versus test positions, pupil-sparing III palsy, the two meanings of SCA, traditional cranial-XI terminology, sensory-classification conventions, and clinical-pattern exceptions. Questions are original NBME-style study material, not official NBME questions.

## Maintenance

Content sources are `notes.json`, `board-review.json`, `sources.json`, `slides.json`, and `questions.txt`. Each question source line has eight pipe-separated fields: section reference, topic, stem, correct choice, and four distractors. A choice uses `text~explanation`. `build.py` shuffles choice positions deterministically, validates content and coverage, and generates the HTML pages, question JSON, JavaScript data, and coverage report.

Run `python neuro3/build.py` from the repository root. It uses only Python's standard library. `extract.py` is the separate PDF rendering helper, configured for this task machine's source/runtime paths and using pdfplumber, Pillow, and Poppler. Extraction is not needed to use or rebuild the existing site.

## Verification

- Build checks passed for 68 image files, original PDF, all 57 instructional sections with questions, all eight supplements with questions, unique stems, five distinct answer choices, explanations, and valid section references.
- DOM tests passed for all 180 correct submissions and 900 rationales; wrong-answer feedback; retry; automatic explanation scrolling/focus; docked Next through the full bank; final-item state; filters; shuffle; deep links; saved-state reload; unavailable storage; lecture search; image toggle; and local files/anchors.
- All 68 original slide renders were visually checked in contact sheets, with selected pages inspected at full size.
- Browser visual testing was unavailable because no browser surface was connected. DOM tests verify behavior and requested scroll calls, not pixel layout or physical browser scrolling.
- Optional `verify.mjs` tests require happy-dom as a separate development dependency. Set `NEURO_DOM_MODULE` to its absolute `lib/index.js`, or make `happy-dom` resolvable to Node, then run `node neuro3/verify.mjs`. The website has no runtime dependency on it.
- Files are local repository changes; no commit, push, or deployment was performed.

Saved answers are separate from Neuro 1 and Neuro 2 and stay in the current browser/origin. If storage is blocked, practice remains usable for the page session and reports that persistence is unavailable.
