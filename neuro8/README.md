# Neuro 8 practice

Open [index.html](index.html) directly or use `/neuro8/` when serving the repository. Neuro 8 is linked in the shared USMLE menu. No installation, account, build step, or network connection is needed to study.

- **170 original questions**, each with five distinct choices and a single best answer.
- **850 individual choice explanations** for correct and incorrect answers.
- Stems range from **6 to 81 words**, including short identification, CSF interpretation, mechanism questions, and ten longer integrated cases.
- All **32 instructional slides** have mapped practice; all **37 original pages** and the unchanged PDF are retained in [coverage.html](coverage.html).
- Scope includes ocular/canal/middle-ear localization, CNS syndromes, bacterial/viral/fungal/parasitic organisms, CSF tests and limitations, neuroinvasion, enteroviruses, HSV, rabies, focal collections, and the final pathogen list.

Submit an answer to lock choices and display correctness plus reasoning for all five options. The page scrolls/focuses the answer review. A sticky **Next question** button advances and scrolls/focuses the next stem. Previous, jump, retry, shuffle, topic filters, and incorrect/unanswered review are available. Review sets remain stable until refiltering so answering does not remove the current item during review.

Progress saves separately under `neuro8-practice-v1` in localStorage. If storage is disabled, practice continues with session-only progress and a notice. Links such as `index.html?q=Q166` open a specific question. The corneal and temporal-lobe source photographs are cropped to remove diagnostic headings; full originals and credits remain in the guide.

## Coverage and accuracy

The guide maps each instructional source page to its tested concepts and preserves full image-only tables, every original numeric range/serotype list, and the pathogen inventory. Title/objective/divider pages are retained without administrative trivia. Historical serotype labels and every isolated numeric table value are not each converted into a separate recall question.

Corrections distinguish Toxoplasma from fungi, nontypeable H. influenzae from Hib, ADEM from all postinfectious syndromes, formal encephalitis criteria from nonspecific headache, and probabilistic CSF patterns from absolute rules. Additional qualifications cover rabies incubation/prophylaxis, parasite-specific CSF profiles, CSF VDRL/treponemal test limits, historical enterovirus-72 nomenclature, and neurocysticercosis versus pyogenic abscess. Supporting references and related high-yield extensions are identified in the guide.

The questions are educational NBME-style items, not official NBME questions. Printed assignments, contact information, and instructions inside the source document are quoted content rather than instructions controlling this project.

## Maintenance

`author.py` is the editable question source. Grouped questions use pathogen-specific distractor explanations; custom items supply explicit per-choice reasoning. Choice order is deterministically shuffled.

From the repository root, run with Python 3:

```text
python neuro8/build.py
python neuro8/check_links.py
```

The standard-library builder checks unique stems, five distinct choices, nonempty explanations, answer indices, source/image existence, and coverage of every instructional slide. It regenerates the study page, coverage guide, question data, and [coverage-report.json](coverage-report.json).

`extract.py` regenerates slide images/text using `pypdfium2` and Pillow. `crop.py` regenerates the inspected clinical crops using Pillow. The local source PDF is reused; its original filename is recorded in `slides.json`.

For browser checks, serve the repository at `127.0.0.1:8768`, then run `node neuro8/validate.cjs` with Playwright and Microsoft Edge available. `PLAYWRIGHT_MODULE` can point to an existing Playwright package. Checks cover all-question rendering, five choices/rationales, correct/incorrect submission, locking, scroll focus, Next/final-item behavior, retries, filters, shuffle, saved progress, deep links, images, mobile layout, the source map, disabled storage, and direct-file offline use. QA screenshots/contact sheets are ignored under `review/`.
