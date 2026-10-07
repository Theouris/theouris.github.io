# Neurovasculature lab

Open `index.html` directly, or visit `/neruovasculature/` on the static site. No dependencies or build step are required. `/neurovasculature/` redirects here, and the shared site menu links to the lab.

- Circle of Willis: 13 labels on the supplied inferior-view diagram.
- Cerebellar arteries: 9 labels on the supplied schematic.
- Territory matching: 8 vascular localizations, each with a normal-function card and an injury-pattern card (16 matches).

Drag labels onto numbered markers, or select a card and click/tap its destination. Keyboard users can select cards and destinations with Tab and Enter/Space. Functions and deficits have separate bank filters. Markers occupy the original printed label positions: follow the image's leader lines to identify the vessels. The supplied images are preserved; white SVG overlays conceal their answers during play.

The timer starts on the first attempted match. Accuracy is correct matches divided by all attempts. Best full-round results are stored locally, ordered by accuracy then time. Study mode stops the attempt and reveals the source labels or completed matching cards. Retry missed includes incorrectly attempted and unfinished targets; practice rounds cannot replace a full-round best.

References are linked in the page. PICA/vertebral and anterior-spinal/vertebral labels acknowledge overlapping medullary supply. The anterior spinal round concerns medial medulla, not the spinal cord. Clinical patterns are educational associations and vary with the precise lesion and anatomy.

Validation: JavaScript syntax and game-state checks covered all diagram/slot counts, correct and incorrect matches, scoring, completion, local bests, retry subsets, practice-score isolation, study/reset, and stable territory ordering. `git diff --check` passed. Browser visual verification was unavailable in the development session.
