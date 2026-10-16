"""Build the self-contained Neuro 5 question site from three source decks."""
from pathlib import Path
from collections import Counter
import json, html, random
root=Path(__file__).resolve().parent
def load(name): return json.loads((root/name).read_text(encoding='utf-8-sig'))
def write(name,obj): (root/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
esc=html.escape
decks=load('slides.json')
deck_order={d['id']:i for i,d in enumerate(decks)}
pages={f"{d['id']}-{p['page']}":p for d in decks for p in d['pages']}
admin={'emb':{1,2,13,31,38},'path':{1,2,3,11,19,26},'reflex':{1}}
titles={'emb-9':'Cervical meningocele and myelomeningocele photographs','path-9':'Normal fundus landmarks','path-10':'Normal disc versus papilledema'}
qualifications={
 'emb-3':['SHH is the classic ventral patterning signal; dorsal BMP/TGF-beta and Wnt pathways also participate. Neural induction is not identical to subsequent dorsal–ventral patterning.'],
 'emb-6':['The original diagram is retained unchanged. Its dentin/head-mesoderm grouping is simplified: odontoblasts are cranial neural crest-derived. Cranial crest migration can start before full tube closure, so the timing bullet is not universal. Cranial sensory ganglia may have both placodal and crest contributions.'],
 'emb-8':['Occulta is a closed vertebral arch defect; open neural lesions differ in sac contents and neurologic risk. Cutaneous markers can accompany more complex occult dysraphism.'],
 'emb-19':['Separate fourth-arch superior laryngeal/cricothyroid relationships from sixth-arch recurrent laryngeal/other intrinsic laryngeal muscles. Stylopharyngeus and tensor veli palatini are important IX and V3 exceptions.'],
 'emb-20':['The source color map is a broad crest-versus-mesoderm teaching schematic. Not all mesodermal skull territory is derived specifically from occipital somites.'],
 'emb-25':['Pouch contributions refer principally to epithelial primordia, not every cell in the mature organ. C-cell contribution is through ultimobranchial bodies; modern mammalian lineage studies support endoderm rather than the older universal neural-crest assignment.'],
 'path-4':['Posterior aqueous chamber is distinct from the large vitreous/postremal chamber. Conventional aqueous outflow uses the trabecular meshwork and scleral venous sinus.'],
 'path-10':['Papilledema means optic disc edema specifically due to raised intracranial pressure; the term does not cover every cause of a swollen disc.'],
 'path-24':['Macular sparing is common in some occipital lesions, but is neither required nor perfectly specific. Sparing reflects preserved central-field representation, sometimes with collateral supply.'],
 'reflex-3':['The source table models complete isolated afferent lesions and complete parasympathetic efferent failure. Partial lesions and pupil-sparing III palsies do not necessarily follow the complete-lesion table.'],
 'reflex-4':['RAPD describes asymmetric afferent drive, often with equal resting pupil sizes and intact efferent pathways. Severe asymmetric retinal disease can also cause it.'],
 'reflex-7':['Adie near constriction may be impaired early and becomes tonic with reinnervation. Light-near dissociation denotes a relative advantage of near over light constriction.'],
 'reflex-11':['Absent doll’s-eye responses require context, including medication and peripheral pathway confounders; this single maneuver does not establish brain death. Avoid head rotation with suspected cervical instability.'],
 'reflex-13':['Convergence is often preserved in INO but is not guaranteed. Name the lesion for the side of the impaired adducting eye.']}
sources=load('sources.json')
raw=[l for l in (root/'questions.txt').read_text(encoding='utf-8-sig').splitlines() if l.strip()]
raw.sort(key=lambda l:(deck_order[l.split('|')[0].rsplit('-',1)[0]],int(l.split('|')[0].rsplit('-',1)[1])))
questions=[];learning={}
for i,line in enumerate(raw,1):
    fields=line.split('|');assert len(fields)==8,(i,'Require five choices',len(fields))
    key,topic,stem,*choices=fields;assert key in pages,key
    code,page=key.rsplit('-',1);opts=[]
    for j,c in enumerate(choices):
        text,why=c.split('~',1);assert text.strip() and why.strip()
        opts.append({'text':text,'why':why,'correct':j==0})
    learning.setdefault(key,[]).append({'id':f'Q{i:03}','text':opts[0]['why']})
    random.Random(5826+i).shuffle(opts);answer=next(j for j,o in enumerate(opts) if o.pop('correct'))
    # Remove every remaining internal marker after finding the answer.
    for o in opts:o.pop('correct',None)
    questions.append({'id':f'Q{i:03}','deck':code,'ref':f'slide-{key}','page':int(page),'topic':topic,'stem':stem,'options':opts,'answer':answer})
assert len(questions)==len({q['stem'] for q in questions}),'Duplicate stem'
assert all(len(q['options'])==5 and len({o['text'] for o in q['options']})==5 for q in questions)
topics=[]
for d in decks:
    assert [p['page'] for p in d['pages']]==list(range(1,len(d['pages'])+1))
    assert (root/f"lecture-{d['id']}.pdf").is_file()
    for p in d['pages']:
        key=f"{d['id']}-{p['page']}";instructional=p['page'] not in admin[d['id']]
        assert not instructional or key in learning,('Uncovered instructional slide',key)
        assert (root/p['image']).is_file() and (root/p['image']).stat().st_size>1000
        title=titles.get(key,p['text'].splitlines()[0] if p['text'] else 'Image reference')
        topics.append({'key':key,'deck':d['id'],'page':p['page'],'title':title,'instructional':instructional,'items':learning.get(key,[]),'qualifications':qualifications.get(key,[])})
write('topics.json',topics);write('questions.json',questions)
deck_data=[{'id':d['id'],'title':d['title']} for d in decks]
(root/'data.js').write_text('window.NEURO = '+json.dumps({'decks':deck_data,'questions':questions},ensure_ascii=False)+';\n',encoding='utf8')
counts=Counter(q['deck'] for q in questions);n=len(questions);n_pages=len(pages);n_instructional=sum(t['instructional'] for t in topics)
def shell(title,active,body,scripts=''):
    nav=''.join(f'<a href="{file}"'+(' aria-current="page"' if name==active else '')+f'>{name}</a>' for file,name in [('index.html','Practice questions'),('coverage.html','Slide coverage & sources')])
    return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Neuro 5 | {title}</title><link rel="stylesheet" href="style.css">{scripts}</head><body><header><a href="../">Home</a> · <a href="../neuro4/">Neuro 4</a><h1>Neuro 5: {title}</h1><nav aria-label="Study tabs">{nav}</nav></header><main>{body}</main><footer>Based on Aftab Merchant’s NNN 5.1, 5.2A, and 5.2B lecture decks, UNLV, 2026. Original NBME-style practice questions; not official NBME items. Original slide images, text, and source credits are retained in the reference tab.</footer></body></html>'
body=f'<p class="intro"><strong>{n} questions · {n*5:,} choice explanations.</strong> Embryology ({counts["emb"]}), visual pathways ({counts["path"]}), and visual/ocular reflexes ({counts["reflex"]}). Every instructional slide has mapped practice. Stems range from short recall to clinical paragraphs, with one best answer and reasoning for all five options. Submit an answer to scroll to the explanations; use the persistent Next question button to continue.</p><p>Progress saves in this browser. Filter by lecture, topic, or review status. Review filters select a set when changed; answering does not remove the current question before you finish reviewing it. Source and related high-yield concepts are identified in the coverage tab.</p><noscript>Enable JavaScript for interactive practice. The source coverage tab remains readable without it.</noscript>'
body+='<div class="tools"><label>Lecture<select id="deck"><option value="">All three lectures</option></select></label><label>Topic<select id="topic"><option value="">All topics</option></select></label><label>Review<select id="review"><option value="all">All questions</option><option value="unanswered">Unanswered</option><option value="missed">Incorrect</option></select></label><button id="shuffle">Shuffle questions</button><button id="reset">Reset progress</button></div><p class="stats" id="stats" role="status" aria-live="polite"></p><p class="muted" id="storage"></p><div class="tools"><button id="prev">← Previous</button><label>Jump to question<select id="jump" aria-label="Jump to question"></select></label><button id="next">Next question →</button></div><div id="question"></div><div id="answer-nav" class="answer-nav" hidden><span id="answer-position"></span><button id="answer-next">Next question →</button></div>'
(root/'index.html').write_text(shell('Embryology, vision & reflex practice','Practice questions',body,'<script src="data.js" defer></script><script src="practice.js" defer></script>'),encoding='utf8')
coverage=f'<p><strong>{n_pages} original pages · {n_instructional} instructional slides · {n} questions.</strong> This page maps each slide to practice, preserves every original page image and all extracted text, and records clinical qualifications. Titles, objectives, section dividers, and closing pages remain available without administrative quiz items.</p><p>The supplied PDFs determine lecture coverage. Their pre-session assignments and contact/appointment text are preserved source material, not instructions for this website. Additional questions apply related high-yield concepts; they are identified below. Every question is self-contained and includes reasoning for all five choices.</p><h2>Original PDFs</h2><ul>'
for d in decks:coverage+=f'<li><a href="lecture-{d["id"]}.pdf">{esc(d["source"])}</a> — {len(d["pages"])} pages, {counts[d["id"]]} questions · <a href="#deck-{d["id"]}">Jump to slide map</a></li>'
coverage+='</ul><h2>Related high-yield applications</h2><p>In addition to slide bullets and diagram labels, practice includes neural-tube plate patterning, Hirschsprung disease, Chiari II, prenatal NTD markers and folic acid amounts, arch arterial derivatives, tympanic membrane layers, tooth lineages, thyroid tract variants, refractive errors/presbyopia, aqueous outflow and angle closure, retinal detachment, rods/cones and phototransduction, Horner syndrome, compressive III palsy, and one-and-a-half syndrome. These additions are educational extensions rather than claims that every detail appears in the lecture text.</p>'
for d in decks:
    coverage+=f'<section id="deck-{d["id"]}"><h2>{esc(d["title"])}</h2><div class="table-wrap"><table><thead><tr><th>Slide</th><th>Source content</th><th>Practice</th></tr></thead><tbody>'
    dt=[t for t in topics if t['deck']==d['id']]
    for t in dt:
        links=', '.join(f'<a href="index.html?q={i["id"]}">{i["id"]}</a>' for i in t['items'])
        coverage+=f'<tr><td><a href="#slide-{t["key"]}">{t["page"]}</a></td><td>{esc(t["title"])}</td><td>{links or "Title, objectives, divider, or closing page retained"}</td></tr>'
    coverage+='</tbody></table></div></section>'
    for t,p in zip(dt,d['pages']):
        coverage+=f'<section class="slide" id="slide-{t["key"]}"><span class="badge">{esc(d["title"])} — original slide {p["page"]}/{len(d["pages"])}</span><h3>{esc(t["title"])}</h3>'
        if t['items']:coverage+='<h4>Tested concepts and clinical applications</h4><ul>'+''.join(f'<li><a href="index.html?q={i["id"]}">{i["id"]}</a> — {esc(i["text"])}</li>' for i in t['items'])+'</ul>'
        for note in t['qualifications']:coverage+=f'<p><strong>Qualification:</strong> {esc(note)}</p>'
        coverage+=f'<details><summary>Show full original slide image</summary><figure><a href="{p["image"]}" target="_blank" rel="noopener"><img src="{p["image"]}" loading="lazy" width="{p["width"]}" height="{p["height"]}" alt="Original {esc(d["title"])} slide {p["page"]}: {esc(t["title"])}. Full labels and credits retained."></a><figcaption>Click the image to enlarge; the original PDF above retains the original document detail.</figcaption></figure></details><details><summary>Original extracted slide text</summary><pre class="transcript">{esc(p["text"]) if p["text"] else "No machine-readable text on this page; see the full source image."}</pre></details></section>'
coverage+='<h2>Supporting references</h2><p>The supplied decks are the primary content source. The following references were consulted for anatomy, clinical qualifications, and related applications (October 15, 2026). No external service is needed to use the question bank.</p><ul>'
for s in sources:coverage+=f'<li><a href="{s["url"]}" target="_blank" rel="noopener">{esc(s["title"])}</a> — {esc(s["supports"])}</li>'
coverage+='</ul>'
(root/'coverage.html').write_text(shell('Slide coverage & sources','Slide coverage & sources',coverage),encoding='utf8')
report={'source_pages':n_pages,'instructional_slides':n_instructional,'questions':n,'choice_explanations':n*5,'stem_words_min':min(len(q['stem'].split()) for q in questions),'stem_words_max':max(len(q['stem'].split()) for q in questions),'questions_by_deck':dict(counts),'questions_per_slide':{t['key']:len(t['items']) for t in topics},'answer_positions':{letter:sum(q['answer']==i for q in questions) for i,letter in enumerate('ABCDE')}}
write('coverage-report.json',report)
print(json.dumps({k:v for k,v in report.items() if k!='questions_per_slide'},indent=2))
