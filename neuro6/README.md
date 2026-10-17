# Neuro 6 practice

Open [index.html](index.html) directly, or use `/neuro6/` when serving this repository. The shared USMLE menu includes the new folder. No network, build step, or account is needed to study.

- 294 original five-choice questions: 79 visual disorders and 215 demyelinating disease/localization questions.
- 1,470 answer-choice explanations and 61 questions containing clinical images.
- Stems range from 4 to 77 words, including short identification and clinical paragraph questions.
- All 136 instructional pages have mapped questions. All 143 original pages and both original PDFs are retained in [coverage.html](coverage.html), including image-only tables, full image credits, and ocular review prompts.
- Fundus photographs, gross specimens, histology, slit-lamp photographs, and MRI panels are cropped from the supplied material. Diagnostic slide titles are excluded from question images. Full originals remain in the guide.

Select one answer and submit. Choices lock, correctness and all five rationales appear, and the page scrolls/focuses the explanation. A sticky **Next question** button advances and scrolls/focuses the next stem. The final question shows an end-of-set message. Previous, jump, retry, shuffle, lecture/topic filters, and missed/unanswered review are included. Review sets remain stable until refiltering, so submitting does not remove an item while its explanation is being read.

Progress saves to `neuro6-practice-v1` in browser localStorage, separately from earlier Neuro sites. Storage failure falls back to session-only progress with a notice. A URL such as `index.html?q=Q271` opens a particular question.

## Coverage and accuracy

Questions cover disease presentation, mechanisms, morphology, risk factors, differential diagnosis, treatment principles, CNS/PNS localization, roots/plexuses/named nerves, electrodiagnostics, MS/NMOSD/MOGAD, leukodystrophies, GBS/CIDP variants, and nodopathies. The guide maps source pages to questions, preserves every table and diagram, and identifies corrections and framework dates. Detailed trial percentages, dose schedules, and every numeric table cell are preserved as reference rather than all being turned into isolated recall questions.

The source guide distinguishes the lecture's 2017 MS diagnostic rules from published 2024 revisions. Corrections include aqueous versus vitreous humor, retinal capillary microangiopathy, cotton-wool spot ischemia, anterior chamber protein flare, MG low-frequency RNS decrement, hereditary versus familial retinoblastoma, and individualized vaccine guidance after GBS. References supporting these corrections are linked in the guide.

These are educational NBME-style items, not official NBME questions. Source document assignments, links, and contact information are treated as quoted source content rather than build instructions.

## Maintenance

`author.py` is the editable question source. `block()` groups original stems with disease-specific distractor teaching points; `custom()` supplies five explicit choices with separate explanations. The builder deterministically shuffles choices and validates five distinct options, explanations, image existence, unique stems, and instructional-slide coverage.

Run with Python 3:

```text
python neuro6/build.py
```

This regenerates `questions.json`, `data.js`, `index.html`, `coverage.html`, and `coverage-report.json` using only the standard library and retained `slides.json`/images. `extract.py` can rerender local PDFs using `pypdfium2` and Pillow; `crop.py` regenerates the inspected figure crops using Pillow. Run those from the repository root when changing image assets.

For browser checks, serve the repository on `127.0.0.1:8766`, then run `node neuro6/validate.cjs`. The script uses Playwright with installed Microsoft Edge; `PLAYWRIGHT_MODULE` can point to an existing Playwright package. It tests correct/incorrect submission, five explanations, locking, scroll focus, next/last-item behavior, retries, saved state, filters, shuffle, deep links, images, mobile overflow, and the full slide map. QA screenshots and render contact sheets are ignored under `review/`.
