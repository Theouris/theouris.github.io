# PRISMA Flowchart

A browser-only editor for systematic, scoping, and narrative review flowcharts. Serve this repository with any static HTTP server, or visit `/PRISMA%20Flowchart/` when it is hosted on GitHub Pages. There is no build step, backend, package install, or third-party runtime dependency. JavaScript modules require HTTP(S); opening `index.html` directly with `file://` is not supported.

The desktop layout gives the editor one third of the page and the preview two thirds. On smaller screens the preview and editor stack vertically.

## Editing

- Choose a review type using the three-part sidebar toggle. Each type has its own draft.
- Enter identification, removal, and exclusion counts. Downstream totals update immediately. Empty deductions act as zero once an upstream count exists; an untouched template keeps its counts blank.
- Type directly into a calculated field to override it. Its button changes to **Manual**. Press that button to return to **Auto**; later stages use the effective value, including manual overrides.
- Use **Edit wording** under any box to edit its complete text. The initial systematic wording comes from the supplied Word document. Each `(n = )` marker inserts its corresponding count, in order. The editor reports missing or extra markers.
- Add or remove identification sources and exclusion reasons. Boxes grow with their text. Headings, phase labels, footnotes, attribution, and font size are editable under **Headings & footnotes**.
- Enter unique included studies separately in systematic mode. Reports and studies are not interchangeable, so the app does not invent a study count from the report total.
- Use the preview zoom controls or Control/Command + scroll. Scroll normally to pan. **Fit** shows the full diagram. Preview zoom does not affect export resolution.
- Each edit is saved to local browser storage. **Save project** downloads a JSON file containing all three drafts; **Open project** restores one. Undo/redo includes resets and review-type changes. If browser storage is unavailable, use the project download to keep work.

## Export

Download PNG, SVG, or PDF from the sidebar. Width and height are linked to the diagram's aspect ratio; editing either sets the other. Dimensions range from 100 to 12,000 pixels, with a 32-megapixel raster limit. DPI ranges from 36 to 1,200.

- **PNG:** the requested pixel dimensions, with the requested DPI written into the PNG `pHYs` density metadata.
- **SVG:** editable vector boxes, arrows, and text. Pixel dimensions define the canvas. SVG is resolution independent; DPI is recorded as metadata.
- **PDF:** a single page containing a lossless raster image at the selected pixel dimensions. Its physical page size is `pixels / DPI`. Choose SVG when you need editable vector artwork.

All exports include the chart and its footnotes, without the editor, zoom controls, or validation messages. Negative computed counts block exports; inconsistent manual overrides are reported and remain exportable.

## Template provenance

The reference is `PRISMA_2020_flow_diagram_new_SRs_v2.docx`. Systematic mode preserves its default wording, two identification routes, white boxes, black text and connectors, yellow `#FFC000` route headers with `#7F5F00` borders, and blue `#9CC2E5` phase labels. The app does not offer recoloring controls.

- [PRISMA 2020 flow diagram templates](https://www.prisma-statement.org/prisma-2020-flow-diagram). Page MJ, et al. *BMJ*. 2021;372:n71. [doi:10.1136/bmj.n71](https://doi.org/10.1136/bmj.n71). Template distributed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
- [PRISMA-ScR](https://www.prisma-statement.org/scoping). Tricco AC, et al. *Ann Intern Med*. 2018;169:467–473. [doi:10.7326/M18-0850](https://doi.org/10.7326/M18-0850). Item 14 calls for counts screened, assessed, and included, with exclusion reasons, ideally in a flow diagram. Scoping mode adapts the supplied 2020 structure to sources of evidence; it is not a separate official PRISMA-ScR diagram.
- [SANRA](https://doi.org/10.1186/s41073-019-0064-8). Baethge C, Goldbeck-Wood S, Mertens S. *Res Integr Peer Rev*. 2019;4:5. SANRA is a quality-appraisal scale that includes describing the literature search, not a flowchart standard. Narrative mode is an optional selection diagram adapted for this app and is labeled accordingly.

## Checks

With Node.js 22 or newer, run `node --test "PRISMA Flowchart/tests.mjs"` from the repository root. The tests cover arithmetic for all modes, overrides, route visibility, reasons, project validation, text escaping, layout growth, and PNG/PDF export metadata. They do not require a browser or installed packages. Browser layout and download interactions require a separate manual check.
