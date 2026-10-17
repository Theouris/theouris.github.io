"""Build an offline question bank and complete lecture coverage guide."""
from pathlib import Path
from collections import Counter
import json,html
import author
R=Path(__file__).parent
qs=author.questions
slides=json.loads((R/'slides.json').read_text(encoding='utf8'))
admin={1,2,3,10,15};esc=html.escape
assert len(slides)==1 and len(slides[0]['pages'])==37
assert len({q['stem'] for q in qs})==len(qs),'Duplicate stem'
for q in qs:
 assert len(q['options'])==5 and len({o['text'] for o in q['options']})==5,q['id']
 assert all(o['why'].strip() for o in q['options']),q['id']
 assert 0<=q['answer']<5 and all(1<=p<=37 for p in q['pages'])
 if q['image']:assert (R/'images'/q['image']).is_file(),q['image']
pages=slides[0]['pages'];qmap={p['page']:[q for q in qs if p['page'] in q['pages']] for p in pages}
assert all(qmap[p['page']] or p['page'] in admin for p in pages),'Uncovered instructional slide'
assert all((R/p['image']).is_file() for p in pages)
assert (R/'lecture-inf.pdf').is_file()
def write(name,data):(R/name).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
write('questions.json',qs)
(R/'data.js').write_text('window.NEURO = '+json.dumps({'decks':[{'id':'inf','title':'CNS, eye & ear infections'}],'questions':qs},ensure_ascii=False)+';\n',encoding='utf8')
def shell(title,body,scripts=''):
 return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Neuro 8 | {title}</title><link rel="stylesheet" href="style.css">{scripts}</head><body><header><a href="../">Home</a> · <a href="../neuro7/">Neuro 7</a><h1>Neuro 8: {title}</h1><nav aria-label="Study pages"><a href="index.html">Practice questions</a><a href="coverage.html">Slide coverage & sources</a></nav></header><main>{body}</main><footer>Original NBME-style educational questions, not official NBME items. Based on the supplied CNS, Eye and Ear Infections lecture by Lloyd Jensen and Amy Stone. Original slide images, text, and credits are preserved in the source guide.</footer></body></html>'
n=len(qs)
body=f'<p><strong>{n} questions · {n*5:,} choice explanations.</strong> Eye and ear infections, CNS syndromes, bacterial/viral/fungal/parasitic pathogens, CSF interpretation, neuroinvasion, rabies, abscesses, and empyema. Questions range from one-sentence items to clinical paragraphs. Select one best answer and submit to review reasoning for all five choices.</p><p>After submission, the page scrolls to the answer review. A sticky <strong>Next question</strong> button advances and scrolls to the next stem. Progress saves in this browser. The source guide maps all 32 instructional slides and preserves all 37 original pages, including image-only tables and the final pathogen list.</p><noscript>Enable JavaScript for interactive practice. The source guide remains available without JavaScript.</noscript>'
body+='<div class="tools"><label hidden>Lecture<select id="deck"><option value="">Complete lecture</option></select></label><label>Topic<select id="topic"><option value="">All topics</option></select></label><label>Review<select id="review"><option value="all">All questions</option><option value="unanswered">Unanswered</option><option value="missed">Incorrect</option></select></label><button id="shuffle">Shuffle questions</button><button id="reset">Reset progress</button></div><p id="stats" class="stats" role="status" aria-live="polite"></p><p id="storage" class="muted"></p><div class="tools"><button id="prev">Previous</button><label>Jump to question<select id="jump" aria-label="Jump to question"></select></label><button id="next">Next question</button></div><div id="question"></div><div id="answer-nav" class="answer-nav" hidden><span id="answer-position"></span><button id="answer-next">Next question</button></div>'
(R/'index.html').write_text(shell('CNS, eye & ear infection practice',body,'<script src="data.js" defer></script><script src="practice.js" defer></script>'),encoding='utf8')
notes='''<h2>Source qualifications and corrections</h2><ul>
<li><strong>Clinical patterns are probabilistic.</strong> Discharge/matting increases the likelihood of bacterial conjunctivitis but does not reliably separate all cases. Severe pain, photophobia, or reduced acuity needs consideration of keratitis or intraocular disease.</li>
<li>Uveitis has major infectious, immune-mediated, and idiopathic categories. <strong>Toxoplasma is a protozoan</strong>, not a fungus, and is an important cause of posterior retinochoroiditis rather than uniformly rare. CMV retinitis is especially relevant with profound cellular immune suppression.</li>
<li>Nontypeable H. influenzae is an important AOM pathogen, but “the leading cause” varies by population, vaccination, and sampling. Hib invasive disease and nontypeable middle-ear disease are distinguished. A red drum or fluid alone does not prove AOM; acute bulging and symptoms matter.</li>
<li>Postinfectious ADEM is immune-mediated demyelination, not a synonym for every postinfectious encephalopathy. Myelitis means spinal cord inflammation; peripheral nerve weakness is a different localization. Transverse myelitis can be asymmetric and initially flaccid during spinal shock.</li>
<li>The International Encephalitis Consortium definition requires altered mental status for at least 24 hours without another cause, with two minor criteria for possible and at least three for probable classification. Minor criteria are fever, new seizures, focal findings, pleocytosis, compatible MRI, and EEG; <strong>headache is not itself a formal minor criterion</strong>. Confirmed disease needs additional etiologic/pathologic evidence. These classification rules must not delay urgent treatment.</li>
<li>Bacterial/viral CSF cell counts, protein, and glucose ranges overlap. Early viral disease can have neutrophils; Listeria can have mixed/mononuclear cells. Some viral infections lower glucose, and severe immune suppression can blunt cells. Use concurrent serum glucose and organism-directed tests rather than a single closed-range rule.</li>
<li>Gram stain/culture can be negative after antibiotics. PCR panels cover selected pathogens only. AFB smear is insensitive; TB NAAT and culture remain important. CSF VDRL is specific but insensitive; treponemal tests are more sensitive but need contextual interpretation. Cryptococcal antigen is targeted to Cryptococcus, not a universal fungal screen.</li>
<li>CSF eosinophilia is particularly useful for selected <strong>helminthic</strong> diseases, not every parasite. Naegleria PAM often has neutrophils and can resemble bacterial meningitis; Toxoplasma is often primarily parenchymal.</li>
<li>The enterovirus serotype table retains historical nomenclature, including HAV as “enterovirus 72.” HAV is now classified as <strong>Hepatovirus</strong>. Exact source serotype lists and specimen-detection timelines are preserved for reference; clinical associations are overlapping rather than exclusive.</li>
<li>Nonblanching petechiae can accompany several illnesses, but fever with petechiae/purpura warrants urgent evaluation for invasive disease. A glass test does not identify a virus or exclude meningococcemia.</li>
<li>HSV encephalitis often involves temporal regions but is not restricted to exactly one lobe. CSF erythrocytes are neither required nor specific; traumatic taps can also introduce red cells.</li>
<li>Rabies incubation varies beyond the illustrative table limits. Neural transport can involve more than the dorsal-root route pictured. Natural antibody timing is variable, so waiting for antibody or symptoms is inappropriate after a concerning exposure. Clinical rabies is <strong>nearly always fatal</strong>, with rare exceptions. PEP details depend on prior vaccination, immune status, and exposure risk.</li>
<li>Fungal disease can involve meninges, vessels, and parenchyma. The table’s plus signs and common/occasional labels are qualitative, not universal incidence estimates. “Zygomycetes” is historical terminology; Mucorales is used for the relevant mucormycosis group.</li>
<li>Taenia solium causes <strong>neurocysticercosis</strong>, not an ordinary pyogenic abscess. Tissue infection follows human-carrier egg ingestion; pork cysticerci cause intestinal taeniasis. Echinococcus hydatid cysts and cerebral malaria also have mechanisms distinct from bacterial pus collections.</li>
<li>Prions cause protein-misfolding neurodegeneration rather than a conventional inflammatory viral infection. The final list includes several distinct organism classes, not one interchangeable “septic” category.</li>
<li>Related applications add classic organism-identification clues, urgent diagnostic principles, and clinical host/exposure settings to the lecture lists. These include necrotizing otitis externa, Group B streptococcal CAMP positivity and E. coli K1 neonatal clues, mold/yeast morphology, malaria sequestration, and rabies prophylaxis. They are educational extensions, not claims that all those details appear explicitly on the slides.</li>
</ul>'''
references=[
 ('CDC: clinical overview of conjunctivitis','https://www.cdc.gov/conjunctivitis/hcp/clinical-overview/'),
 ('CDC: Acanthamoeba keratitis','https://www.cdc.gov/acanthamoeba/about/about-acanthamoeba-keratitis.html'),
 ('NIH: CMV disease','https://clinicalinfo.hiv.gov/en/guidelines/hiv-clinical-guidelines-adult-and-adolescent-opportunistic-infections/cytomegalovirus'),
 ('NIH: Toxoplasma encephalitis','https://clinicalinfo.hiv.gov/en/guidelines/hiv-clinical-guidelines-adult-and-adolescent-opportunistic-infections/toxoplasmosis'),
 ('NIH: cryptococcosis','https://clinicalinfo.hiv.gov/en/guidelines/hiv-clinical-guidelines-adult-and-adolescent-opportunistic-infections/cryptococcosis'),
 ('International Encephalitis Consortium case definition','https://pmc.ncbi.nlm.nih.gov/articles/PMC3783060/'),
 ('CDC: rabies postexposure prophylaxis','https://www.cdc.gov/rabies/hcp/clinical-care/post-exposure-prophylaxis.html'),
 ('CDC: free-living amebic infections','https://www.cdc.gov/dpdx/freeLivingAmebic/'),
 ('CDC: cysticercosis transmission','https://www.cdc.gov/dpdx/cysticercosis/index.html'),
 ('WHO: meningitis diagnosis and treatment','https://www.who.int/news-room/fact-sheets/detail/meningitis'),
 ('WHO: meningitis guidelines, 2025','https://www.who.int/publications/i/item/9789240108042'),
 ('CDC: bacterial meningitis','https://www.cdc.gov/meningitis/about/bacterial-meningitis.html')]
body=f'<p><strong>37 original pages · 32 instructional slides · {n} questions.</strong> Every instructional slide has mapped practice. Full original images and text preserve diagrams, tables, captions, source credits, and the final pathogen inventory. Title, objectives, and section dividers are retained without administrative quiz questions.</p><p>The questions cover the lecture’s clinical concepts and add identified high-yield applications. Original tables retain every serotype, numeric range, and historical label; each isolated number or serotype is not turned into a separate trivia question. Instructions inside the document are quoted source material, not instructions controlling this project.</p><p><a href="lecture-inf.pdf">Original PDF: {esc(slides[0]["source"])}</a></p>'
body+=notes+'<h2>Verification references</h2><p>Clinical qualifications were checked against the following references on October 17, 2026. The supplied lecture defines the study scope.</p><ul>'+''.join(f'<li><a href="{esc(url)}">{esc(title)}</a></li>' for title,url in references)+'</ul><h2>Slide coverage map</h2><div class="table-wrap"><table><thead><tr><th>Slide</th><th>Source</th><th>Practice questions</th></tr></thead><tbody>'
for p in pages:
 title=p['text'].strip().splitlines()[0] if p['text'].strip() else 'Image-only table or figure'
 links=', '.join(f'<a href="index.html?q={q["id"]}">{q["id"]}</a>' for q in qmap[p['page']])
 body+=f'<tr><td><a href="#slide-inf-{p["page"]}">{p["page"]}</a></td><td>{esc(title)}</td><td>{links or "Title, objectives, or divider retained"}</td></tr>'
body+='</tbody></table></div>'
for p in pages:
 body+=f'<section class="slide" id="slide-inf-{p["page"]}"><h3>Original slide {p["page"]}</h3>'
 if qmap[p['page']]:body+='<details><summary>Mapped concepts and practice</summary><ul>'+''.join(f'<li><a href="index.html?q={q["id"]}">{q["id"]}</a> — {esc(q["options"][q["answer"]]["why"])}</li>' for q in qmap[p['page']])+'</ul></details>'
 else:body+='<p>Administrative page retained.</p>'
 body+=f'<details><summary>Show original slide image and credits</summary><a href="{p["image"]}" target="_blank" rel="noopener"><img src="{p["image"]}" loading="lazy" alt="Original CNS, eye and ear infections slide {p["page"]}"></a></details><details><summary>Original extracted text</summary><pre class="transcript">{esc(p["text"]) or "Image-only source: inspect the full original slide above."}</pre></details></section>'
(R/'coverage.html').write_text(shell('Slide coverage & sources',body),encoding='utf8')
report={'questions':n,'choice_explanations':n*5,'source_pages':37,'instructional_pages':32,'image_questions':sum(bool(q['image']) for q in qs),'questions_by_topic':dict(Counter(q['topic'] for q in qs)),'stem_word_range':[min(len(q['stem'].split()) for q in qs),max(len(q['stem'].split()) for q in qs)],'answer_positions':dict(Counter('ABCDE'[q['answer']] for q in qs)),'slide_question_map':{str(p):[q['id'] for q in mapped] for p,mapped in qmap.items()}}
write('coverage-report.json',report)
print(json.dumps({k:v for k,v in report.items() if k not in {'questions_by_topic','slide_question_map'}},indent=2))
