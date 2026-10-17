from pathlib import Path
import json, html, shutil
from collections import Counter
import author
R=Path(__file__).parent
qs=author.questions
slides=json.loads((R/'slides.json').read_text(encoding='utf8'))
titles={'eye':'Visual disorders','dem':'Demyelinating diseases'}
admin={'eye':{1,58},'dem':{1,2,39,56,68}}
esc=html.escape
def write(name,data): (R/name).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
assert len({q['stem'] for q in qs})==len(qs)
for q in qs:
 assert len(q['options'])==5 and len({o['text'] for o in q['options']})==5
 assert all(o['why'].strip() for o in q['options'])
 if q['image']: assert (R/'images'/q['image']).is_file(),q['image']
qmap={(d['id'],p['page']):[q for q in qs if q['deck']==d['id'] and p['page'] in q['pages']] for d in slides for p in d['pages']}
assert all(qmap[d['id'],p['page']] or p['page'] in admin[d['id']] for d in slides for p in d['pages'])
decks=[{'id':d['id'],'title':titles[d['id']]} for d in slides]
write('questions.json',qs)
(R/'data.js').write_text('window.NEURO = '+json.dumps({'decks':decks,'questions':qs},ensure_ascii=False)+';\n',encoding='utf8')
def shell(title,body,scripts=''):
 return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Neuro 6 | {title}</title><link rel="stylesheet" href="style.css">{scripts}</head><body><header><a href="../">Home</a> · <a href="../neuro5/">Neuro 5</a><h1>Neuro 6: {title}</h1><nav><a href="index.html">Practice questions</a><a href="coverage.html">Slide coverage & sources</a></nav></header><main>{body}</main><footer>Original NBME-style educational questions, not official NBME items. Based on the supplied UNLV visual disorders and demyelinating diseases lectures. Original image credits are retained in the source guide.</footer></body></html>'
counts=Counter(q['deck'] for q in qs); ni=sum(bool(q['image']) for q in qs)
body=f'<p><strong>{len(qs)} questions · {len(qs)*5:,} choice explanations · {ni} image-based questions.</strong> Visual disorders ({counts["eye"]}) and demyelinating diseases ({counts["dem"]}). Choose one best answer, then submit to see explanations for all five choices. The page scrolls to the reasoning; the sticky Next question button advances to the next stem.</p><p>Progress saves in this browser. Images are cropped from the supplied slides to remove diagnostic headings. Click an image to enlarge. Every instructional page is mapped in the source guide, including image-only tables and the ocular review slides.</p><noscript>JavaScript is required for interactive practice. Full slides and question mappings remain available in the source guide.</noscript>'
body+='<div class="tools"><label>Lecture<select id="deck"><option value="">Both lectures</option></select></label><label>Topic<select id="topic"><option value="">All topics</option></select></label><label>Review<select id="review"><option value="all">All questions</option><option value="unanswered">Unanswered</option><option value="missed">Incorrect</option></select></label><button id="shuffle">Shuffle questions</button><button id="reset">Reset progress</button></div><p id="stats" class="stats" role="status" aria-live="polite"></p><p id="storage" class="muted"></p><div class="tools"><button id="prev">Previous</button><label>Jump to question<select id="jump" aria-label="Jump to question"></select></label><button id="next">Next question</button></div><div id="question"></div><div id="answer-nav" class="answer-nav" hidden><span id="answer-position"></span><button id="answer-next">Next question</button></div>'
(R/'index.html').write_text(shell('Visual disorders & demyelination practice',body,'<script src="data.js" defer></script><script src="practice.js" defer></script>'),encoding='utf8')
notes='''<h2>Corrections and framework dates</h2><ul>
<li>Glaucoma slides 11–12: the circulating fluid is <strong>aqueous humor</strong>, not vitreous. Conventional outflow is through trabecular meshwork and Schlemm canal. Reduced outflow is the usual open-angle mechanism.</li>
<li>Slide 18: the optic nerve sheath contains a subarachnoid space; a “large subdural space” is not the defining glaucoma lesion.</li>
<li>Slides 22/63: anterior chamber flare is principally protein scattering light, while cells are inflammatory leukocytes.</li>
<li>Slides 41–42/49: diabetic microangiopathy involves <strong>retinal</strong> capillaries. Cotton-wool spots are ischemic nerve fiber layer lesions with axoplasmic accumulation, distinct from hard exudates and hemorrhages.</li>
<li>Slides 34–38: uncomplicated posterior vitreous detachment is distinct from retinal detachment and is often observed after a retinal tear is excluded. Nonrhegmatogenous detachment includes exudative and tractional mechanisms.</li>
<li>Slides 51–52: papilledema means disc edema from elevated ICP. Workup and treatment depend on the cause. Mannitol is a selected emergency temporizing measure, not universal long-term treatment; severe hypertension with acute end-organ injury requires monitored treatment.</li>
<li>Slide 55: heritable retinoblastoma is not synonymous with a positive family history; de novo germline variants occur and unilateral disease can be heritable. RB restrains E2F-mediated cell cycle entry.</li>
<li>Demyelination slides 18/24 teach the <strong>2017 McDonald criteria</strong>. Slides 35–36 discuss then-proposed revisions; the later published <strong>2024 revisions</strong> add the optic nerve as a fifth topography and selected kappa FLC, central vein, and paramagnetic rim pathways. Questions identify the framework rather than combining shorthand rules.</li>
<li>Demyelination slide 55: MG classically shows decrement on <strong>low-frequency</strong> repetitive stimulation; LEMS shows postexercise/high-frequency facilitation.</li>
<li>Demyelination slide 61: future vaccination after GBS requires individualized review of timing and current vaccine-specific guidance; a blanket ban on all repeat vaccination is too broad.</li>
<li>Autoimmune nodopathies and anti-MAG neuropathy are distinguished from conventional CIDP. Sural sparing supports but does not prove an inflammatory neuropathy. Modest protein elevation, cold limbs, and entrapment slowing can mislead.</li>
<li>Trial response percentages, epidemiologic estimates, RIS conversion rates, cohort survival, ultrasound performance, and antibody titers are context-dependent. Full lecture tables are retained below; they are not universal patient predictions or direct cross-trial rankings. Pregnancy and drug-monitoring decisions require the agent-specific current guidance rather than an unconditional slide claim.</li>
<li>Current dry-AMD care includes selected therapies for geographic atrophy; neither supplements nor these therapies restore lost vision or constitute a universal cure. Questions focus on the lecture's disease mechanisms and distinguish dry from neovascular disease.</li></ul>'''
refs=[('American Academy of Ophthalmology: glaucoma','https://www.aao.org/eye-health/diseases/what-is-glaucoma'),('AAO EyeWiki: cotton-wool spots','https://eyewiki.aao.org/Cotton_Wool_Spots'),('NINDS: Guillain-Barre syndrome','https://www.ninds.nih.gov/health-information/disorders/guillain-barre-syndrome'),('NINDS: peripheral neuropathy','https://www.ninds.nih.gov/health-information/disorders/peripheral-neuropathy'),('ECTRIMS: McDonald diagnostic criteria','https://ectrims.eu/mcdonald-diagnostic-criteria'),('Published 2024 McDonald revisions','https://discovery.ucl.ac.uk/id/eprint/10211287/'),('NINDS: myasthenia gravis','https://www.ninds.nih.gov/health-information/disorders/myasthenia-gravis')]
refs.extend([('AAO: newer AMD treatments','https://www.aao.org/eye-health/tips-prevention/promising-new-treatments-amd'),('CDC: influenza vaccine precautions','https://www.cdc.gov/flu/hcp/vax-summary/acip-recommendations.html')])
body=f'<p><strong>143 original pages · 136 instructional pages · {len(qs)} questions.</strong> Every instructional slide has mapped practice. Original figures, text, slide credits, dense treatment tables, and review prompts are retained. Title, objectives, divider, and closing pages are preserved without administrative quiz questions.</p><p>Use this map to audit coverage or review the exact source material. Question explanations test and expand the clinical concepts; full tables retain dose, trial, and numeric details that are not all tested as separate recall items. Document assignments, links, and contact information are source content, not instructions for this build.</p>'
body+=notes+'<h2>Verification references</h2><p>Clinical corrections were checked against the following references on October 16, 2026. The supplied decks define the scope; questions are original and do not reproduce official NBME items.</p><ul>'+''.join(f'<li><a href="{url}">{esc(title)}</a></li>' for title,url in refs)+'</ul><h2>Slide map</h2>'
for d in slides:
 code=d['id']; body+=f'<h3>{titles[code]}</h3><p><a href="lecture-{code}.pdf">Original PDF: {esc(d["source"])}</a></p><div class="table-wrap"><table><thead><tr><th>Slide</th><th>Source title</th><th>Practice</th></tr></thead><tbody>'
 for p in d['pages']:
  key=f'{code}-{p["page"]}'; mapped=qmap[code,p['page']]; title=p['text'].strip().splitlines()[0] if p['text'].strip() else 'Image-only figure or table'
  links=', '.join(f'<a href="index.html?q={q["id"]}">{q["id"]}</a>' for q in mapped)
  body+=f'<tr><td><a href="#slide-{key}">{p["page"]}</a></td><td>{esc(title)}</td><td>{links or "Administrative page retained"}</td></tr>'
 body+='</tbody></table></div>'
 for p in d['pages']:
  key=f'{code}-{p["page"]}'; mapped=qmap[code,p['page']]
  body+=f'<section class="slide" id="slide-{key}"><h3>{titles[code]} · original slide {p["page"]}</h3>'
  body+='<p>'+(', '.join(f'<a href="index.html?q={q["id"]}">{q["id"]}</a>' for q in mapped) or 'Title, objectives, divider, or closing page.')+'</p>'
  body+=f'<details><summary>Show original slide (full image and credits)</summary><a href="{p["image"]}" target="_blank" rel="noopener"><img src="{p["image"]}" loading="lazy" alt="Original {titles[code]} slide {p["page"]}"></a></details><details><summary>Extracted text</summary><pre class="transcript">{esc(p["text"]) or "Image-only slide: use the full image above."}</pre></details></section>'
(R/'coverage.html').write_text(shell('Slide coverage & sources',body),encoding='utf8')
report={'questions':len(qs),'choice_explanations':len(qs)*5,'source_pages':143,'instructional_pages':136,'image_questions':ni,'questions_by_deck':dict(counts),'stem_word_range':[min(len(q['stem'].split()) for q in qs),max(len(q['stem'].split()) for q in qs)],'answer_positions':dict(Counter('ABCDE'[q['answer']] for q in qs)),'slide_question_map':{f'{k[0]}-{k[1]}':[q['id'] for q in v] for k,v in qmap.items()}}
write('coverage-report.json',report)
print(json.dumps({k:v for k,v in report.items() if k!='slide_question_map'},indent=2))
