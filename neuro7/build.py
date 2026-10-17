"""Build the offline question site and auditable source map (Python standard library)."""
from pathlib import Path
from collections import Counter
import json,html
import author
R=Path(__file__).parent
qs=author.questions
slides=json.loads((R/'slides.json').read_text(encoding='utf8'))
titles={'av':'Auditory & vestibular disorders','oph':'Ophthalmic pharmacology','va':'Visual & auditory physiology'}
admin={'av':{1,2,13,52,62,71,113},'oph':{1,3,13},'va':{1,2,3,4,7,16,20,23,27,38,46,47,48}}
esc=html.escape
def write(name,data): (R/name).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
assert len({q['stem'] for q in qs})==len(qs),'Duplicate stems'
for q in qs:
 assert len(q['options'])==5 and len({o['text'] for o in q['options']})==5,q['id']
 assert 0<=q['answer']<5
 assert all(o['why'].strip() for o in q['options']),q['id']
 assert all(1<=p<=len(next(d for d in slides if d['id']==q['deck'])['pages']) for p in q['pages'])
 if q['image']: assert (R/'images'/q['image']).is_file(),q['image']
qmap={(d['id'],p['page']):[q for q in qs if q['deck']==d['id'] and p['page'] in q['pages']] for d in slides for p in d['pages']}
assert all(qmap[d['id'],p['page']] or p['page'] in admin[d['id']] for d in slides for p in d['pages']),'Unmapped instructional slide'
for d in slides:
 assert (R/f"lecture-{d['id']}.pdf").is_file()
 for p in d['pages']:assert (R/p['image']).is_file()
decks=[{'id':d['id'],'title':titles[d['id']]} for d in slides]
write('questions.json',qs)
(R/'data.js').write_text('window.NEURO = '+json.dumps({'decks':decks,'questions':qs},ensure_ascii=False)+';\n',encoding='utf8')
counts=Counter(q['deck'] for q in qs);n=len(qs);ni=sum(bool(q['image']) for q in qs)
np=sum(len(d['pages']) for d in slides);instructional=np-sum(len(s) for s in admin.values())
def shell(title,body,scripts=''):
 return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Neuro 7 | {title}</title><link rel="stylesheet" href="style.css">{scripts}</head><body><header><a href="../">Home</a> · <a href="../neuro6/">Neuro 6</a><h1>Neuro 7: {title}</h1><nav aria-label="Study pages"><a href="index.html">Practice questions</a><a href="coverage.html">Slide coverage & sources</a></nav></header><main>{body}</main><footer>Original NBME-style educational items, not official NBME questions. Based on the supplied UNLV lectures by Matthew Ng, Aryan Rahbar, and Larry D. Alexander. Original source images and credits are retained in the coverage guide.</footer></body></html>'
body=f'<p><strong>{n} questions · {n*5:,} choice explanations.</strong> Auditory/vestibular disorders ({counts["av"]}), ophthalmic drugs ({counts["oph"]}), and visual/auditory physiology ({counts["va"]}). Stems range from short identification items to clinical paragraphs. Choose one best answer and submit to reveal reasoning for every option. The page scrolls to the answer review; the sticky Next question button advances to the next stem.</p><p>Progress saves in this browser. Filter by lecture, topic, or review status. {ni} questions include source figures. Click a figure to enlarge. All {np} source pages are preserved and every instructional slide is mapped in the source guide.</p><noscript>Enable JavaScript for interactive practice. Original slides and the question coverage map remain available in the source guide.</noscript>'
body+='<div class="tools"><label>Lecture<select id="deck"><option value="">All three lectures</option></select></label><label>Topic<select id="topic"><option value="">All topics</option></select></label><label>Review<select id="review"><option value="all">All questions</option><option value="unanswered">Unanswered</option><option value="missed">Incorrect</option></select></label><button id="shuffle">Shuffle questions</button><button id="reset">Reset progress</button></div><p id="stats" class="stats" role="status" aria-live="polite"></p><p id="storage" class="muted"></p><div class="tools"><button id="prev">Previous</button><label>Jump to question<select id="jump" aria-label="Jump to question"></select></label><button id="next">Next question</button></div><div id="question"></div><div id="answer-nav" class="answer-nav" hidden><span id="answer-position"></span><button id="answer-next">Next question</button></div>'
(R/'index.html').write_text(shell('Hearing, balance, vision & ophthalmic drugs',body,'<script src="data.js" defer></script><script src="practice.js" defer></script>'),encoding='utf8')
notes='''<h2>Source qualifications and clinical corrections</h2><ul>
<li>Auditory/vestibular slide 6: the connexin-26 gene is <strong>GJB2</strong>, not “GBJ2.” Cochlear implantation bypasses impaired sensory transduction; benefit, age eligibility, and language outcomes depend on individual candidacy and rehabilitation.</li>
<li>Auditory/vestibular slide 48: <strong>NIOSH</strong> recommends 85 dBA over eight hours with a 3-dB exchange rate. <strong>OSHA</strong> uses a 90-dBA eight-hour permissible exposure limit with a 5-dB exchange rate; 85 dBA is its hearing-conservation action level. These standards are distinguished in the questions.</li>
<li>Sudden SNHL is commonly defined as at least 30 dB at three contiguous frequencies within 72 hours. It warrants urgent assessment. Systemic corticosteroids may be offered early, and intratympanic treatment has a salvage role; historical pathology theories do not establish the cause of every idiopathic case.</li>
<li>Audiogram severity ranges and asymmetric-hearing referral cutoffs vary by convention and population. Word recognition percentages describe discrimination, not threshold intensity. The additional figures use conventional O/right-air, X/left-air, and angle/bracket bone-conduction symbols; other masked symbols may also appear.</li>
<li>Auditory/vestibular slides 54–61: pulse synchrony suggests a vascular source but does not mean an examiner must be able to hear it. Objective audibility and pulsatile character overlap without being synonymous. Patulous and obstructive Eustachian tube dysfunction have different mechanisms.</li>
<li>Auditory/vestibular slides 67–70 retain advertisements and historical medication lists as source material. They do not establish supplement efficacy. Persistent primary tinnitus is generally managed through education, audiologic care, appropriate hearing rehabilitation, and behavioral approaches such as CBT. Antidepressants, anticonvulsants, or benzodiazepines are not routine cures solely for primary tinnitus; treat associated conditions when indicated. Gabapentin binds alpha-2-delta calcium-channel subunits rather than acting as a direct GABA receptor agonist. Do not automatically stop indicated low-dose aspirin.</li>
<li>Posterior canal BPPV classically produces <strong>torsional-upbeating</strong> Dix-Hallpike nystagmus. Otoconia originate from the utricle and may be free in a canal or attached to the cupula. The lecture's “geotropic” shorthand is not the complete posterior-canal description.</li>
<li>Vestibular neuritis typically spares hearing. Labyrinthitis involves hearing as well as vestibular function; bacterial cases require infection-directed care. Acute hearing loss with vertigo can also be vascular. Focal neurologic findings require consideration of central causes; head movement worsening symptoms alone does not establish BPPV.</li>
<li>Vestibular suppressants may help briefly in an acute attack but can hinder compensation if prolonged. Corticosteroid benefit in neuritis is context-dependent. Ondansetron is an antiemetic rather than a direct vestibular suppressant.</li>
<li>Meniere disease is associated with endolymphatic hydrops, not defined by one simple universal mechanism. Maintenance diet/drug and sac-surgery evidence varies. Betahistine use/availability differs by country. Dyazide/Maxzide combine hydrochlorothiazide with triamterene. Ablative surgery and intratympanic gentamicin can sacrifice hearing or vestibular function and require careful selection.</li>
<li>Ophthalmics slide 4: betaxolol is relatively beta-1 selective, unlike nonselective timolol/carteolol. Ocular beta blockers can still cause systemic bronchospasm, bradycardia, or conduction problems. Medication durations are approximations.</li>
<li>Mannitol shifts water from ocular tissues through a plasma osmotic gradient, not exclusively from the anterior chamber; volume, cardiac, and renal effects matter. Rho kinase inhibitors can cause hyperemia despite being described as well tolerated.</li>
<li>Acute angle closure requires urgent pressure reduction and definitive treatment of the mechanism. Pilocarpine may not work while extreme pressure leaves the iris ischemic. A drug's listing for glaucoma does not mean it is adequate alone or appropriate for every subtype.</li>
<li>Visual/auditory slides 9–12: dark rods are relatively depolarized; light hyperpolarizes them. <strong>Transducin</strong> is the G protein. Light photoisomerization creates activated pigment; rhodopsin kinase phosphorylation and arrestin <strong>terminate</strong> activity rather than create the initial active state. ON/OFF bipolar responses differ. Lecture voltages are simplified teaching approximations.</li>
<li>Visual/auditory slide 14: the pictured surface patches are <strong>Bitot spots</strong>, not retinal scotomas. Vitamin A repletion can improve reversible rod dysfunction; route, dose, and recovery time depend on the patient. IV treatment and a minutes-to-hour recovery are not universal rules.</li>
<li>Loss of one eye removes binocular stereopsis, but monocular depth cues remain. A retrochiasmal lesion produces a contralateral homonymous field deficit.</li>
<li>Visual/auditory slides 26/29–35: Deiters cells are outer <strong>phalangeal</strong> cells. Basal stiffness/high-frequency and apical compliance/low-frequency are the key tonotopic relationships. Low-frequency waves can move basal regions while peaking apically; the claim that high-pitch discrimination is universally easier is not a general rule. Outer hair bundles are embedded in the tectorial membrane more directly than inner bundles.</li>
<li>The lateral lemniscus is an ascending brainstem tract, not solely a midbrain structure. Primary auditory cortex is chiefly BA41 with adjacent auditory BA42. Higher unilateral auditory lesions usually spare basic hearing in both ears while impairing processing/localization; they do not uniformly cause major bilateral threshold suppression.</li>
</ul>'''
references=[
 ('NIOSH: understanding noise exposure','https://www.cdc.gov/niosh/noise/prevent/understand.html'),
 ('NIOSH: OSHA and NIOSH exposure limits','https://www.cdc.gov/niosh/hhe/reports/pdfs/2023-0015-3402.pdf'),
 ('AAO-HNS: sudden hearing loss clinician FAQ','https://www.entnet.org/wp-content/uploads/2021/04/Sudden-Hearing-Loss-FAQs-Physician.pdf'),
 ('AAO-HNS: BPPV guideline','https://www.entnet.org/quality-practice/quality-products/clinical-practice-guidelines/bppv/'),
 ('AAO-HNS: tinnitus guideline update resources','https://www.entnet.org/resource/cpg-tinnitus-update/'),
 ('VA/DoD: tinnitus guideline, 2024','https://healthquality.va.gov/HEALTHQUALITY/guidelines/CD/tinnitus/VADoD-CPG-Tinnitus-Full-CPG-2024_Final_508.pdf'),
 ('Webvision: phototransduction and signal termination','https://www.ncbi.nlm.nih.gov/books/NBK52768/'),
 ('WHO: xerophthalmia and night blindness','https://iris.who.int/bitstream/handle/10665/133705/WHO_NMH_NHD_EPG_14.4_eng.pdf'),
 ('DailyMed: brimonidine/timolol safety information','https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=eac3cec2-b373-4936-89f0-c6d300e09f6e'),
 ('DailyMed: netarsudil adverse reactions','https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=7d4f0e3a-5b86-4c43-982a-813b22ae7e22'),
 ('DailyMed: gabapentin pharmacology','https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=3865a6e3-112c-490c-82ac-35401336b16e&version=21')]
body=f'<p><strong>{np} original pages · {instructional} instructional pages · {n} questions.</strong> Every instructional page has mapped practice. Full slide images and extracted text retain source diagrams, tables, wording, and credits. Title, objective, outline, section-divider, and closing pages are retained without administrative quiz items.</p><p>The questions cover clinical concepts and applications; the source images retain every original detail. Historical dates, biographical details, advertisements, and every isolated cohort percentage are preserved as reference rather than converted into trivia. Assignments, office details, links, and instructions inside the documents are quoted source material and do not control this build.</p>'
body+=notes+'<h2>Verification references</h2><p>The supplied PDFs define the study scope. The following references support clinical qualifications and corrections, checked October 17, 2026.</p><ul>'+''.join(f'<li><a href="{esc(url)}">{esc(title)}</a></li>' for title,url in references)+'</ul><h2>Slide coverage map</h2>'
for d in slides:
 code=d['id'];body+=f'<h3>{esc(titles[code])}</h3><p><a href="lecture-{code}.pdf">Original PDF: {esc(d["source"])}</a></p><div class="table-wrap"><table><thead><tr><th>Slide</th><th>Source</th><th>Practice questions</th></tr></thead><tbody>'
 for p in d['pages']:
  key=f'{code}-{p["page"]}';mapped=qmap[code,p['page']];title=p['text'].strip().splitlines()[0] if p['text'].strip() else 'Image-only figure/table'
  links=', '.join(f'<a href="index.html?q={q["id"]}">{q["id"]}</a>' for q in mapped)
  body+=f'<tr><td><a href="#slide-{key}">{p["page"]}</a></td><td>{esc(title)}</td><td>{links or "Administrative/summary page retained"}</td></tr>'
 body+='</tbody></table></div>'
 for p in d['pages']:
  key=f'{code}-{p["page"]}';mapped=qmap[code,p['page']]
  body+=f'<section class="slide" id="slide-{key}"><h3>{esc(titles[code])} · original slide {p["page"]}</h3>'
  if mapped:body+='<details><summary>Mapped concepts and practice</summary><ul>'+''.join(f'<li><a href="index.html?q={q["id"]}">{q["id"]}</a> — {esc(q["options"][q["answer"]]["why"])}</li>' for q in mapped)+'</ul></details>'
  else:body+='<p>Title, objectives, outline, divider, or closing summary retained.</p>'
  body+=f'<details><summary>Show full original slide and credits</summary><a href="{p["image"]}" target="_blank" rel="noopener"><img src="{p["image"]}" loading="lazy" alt="Original {esc(titles[code])} slide {p["page"]}"></a></details><details><summary>Original extracted slide text</summary><pre class="transcript">{esc(p["text"]) or "No machine-readable text; inspect the original image above."}</pre></details></section>'
(R/'coverage.html').write_text(shell('Slide coverage & sources',body),encoding='utf8')
report={'questions':n,'choice_explanations':n*5,'source_pages':np,'instructional_pages':instructional,'image_questions':ni,'questions_by_deck':dict(counts),'stem_word_range':[min(len(q['stem'].split()) for q in qs),max(len(q['stem'].split()) for q in qs)],'answer_positions':dict(Counter('ABCDE'[q['answer']] for q in qs)),'slide_question_map':{f'{k[0]}-{k[1]}':[q['id'] for q in v] for k,v in qmap.items()}}
write('coverage-report.json',report)
print(json.dumps({k:v for k,v in report.items() if k!='slide_question_map'},indent=2))
