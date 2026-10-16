"""Build the static Neuro 2 pages and validate slide/question coverage.
Only Python's standard library is required; no browser or build step is needed to use the output.
"""
from pathlib import Path
import json, html, random
root=Path(__file__).resolve().parent
def load(name):return json.loads((root/name).read_text(encoding='utf-8'))
esc=html.escape
decks=load('slides.json');notes=load('notes.json');boards=load('board-review.json');sources=load('sources.json')
questions=[]
for line_number,line in enumerate((root/'questions.txt').read_text(encoding='utf-8').splitlines(),1):
    if not line.strip():continue
    fields=line.split('|');assert len(fields)==8,(line_number,'Expected five choices',len(fields))
    ref,topic,stem,*choices=fields;opts=[]
    for i,choice in enumerate(choices):
        text,why=choice.split('~',1);assert text.strip() and why.strip()
        opts.append({'text':text,'why':why,'correct':i==0})
    random.Random(1826+line_number).shuffle(opts)
    answer=next(i for i,o in enumerate(opts) if o['correct'])
    for o in opts:del o['correct']
    questions.append({'id':f'Q{len(questions)+1:03}','ref':ref,'deck':ref.split('-')[0],'topic':topic,'stem':stem,'options':opts,'answer':answer})
valid={f"{d['id']}-{p['page']}" for d in decks for p in d['pages']}|{f"board-{b['id']}" for b in boards}
assert len(questions)==len({q['stem'] for q in questions}), 'Duplicate stem'
assert all(q['ref'] in valid for q in questions), 'Question has an invalid section'
assert set(notes)<=valid
assert all(any(q['ref']==ref for q in questions) for ref in notes), 'Instructional section missing a practice question'
assert all(any(q['ref']=='board-'+b['id'] for q in questions) for b in boards)
assert all(len(q['options'])==5 and len({o['text'] for o in q['options']})==5 and 0<=q['answer']<5 for q in questions)
assert sum(len(d['pages']) for d in decks)==76
assert all((root/p['image']).is_file() and (root/p['image']).stat().st_size>1000 for d in decks for p in d['pages'])
assert all((root/f'lecture-{d["id"]}.pdf').is_file() for d in decks)
assert all(k in sources for b in boards for k in b['refs'])
(root/'questions.json').write_text(json.dumps(questions,ensure_ascii=False,indent=2),encoding='utf-8')
(root/'data.js').write_text('window.NEURO = '+json.dumps({'questions':questions},ensure_ascii=False)+';\n',encoding='utf-8')
def shell(title,active,body,scripts=''):
    nav=''.join(f'<a href="{file}"'+(' aria-current="page"' if name==active else '')+f'>{name}</a>' for file,name in [('index.html','Lecture'),('practice.html','Practice questions'),('coverage.html','Coverage & sources')])
    return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Neuro 2 | {title}</title><link rel="stylesheet" href="style.css">{scripts}</head><body><header><a href="../">Home</a> · <a href="../neuro1/">Neuro 1</a><h1>Neuro 2: {title}</h1><nav aria-label="Study tabs">{nav}</nav></header><main>{body}</main><footer>Source lectures: Larry D. Alexander, Neural Signaling, and Aftab Merchant, Spinal Cord Anatomy & Clinical Correlates (post-class), UNLV, 2026. Original figures and credits are retained in the slide images and PDFs. Questions and board additions are original study material, not official NBME items.</footer></body></html>'
def bullets(items):return '<ul>'+''.join(f'<li>{esc(item)}</li>' for item in items)+'</ul>'
def links(keys):return '<p class="refs">References: '+''.join(f'<a href="{sources[k]["url"]}" target="_blank" rel="noopener">{esc(sources[k]["title"])}</a>' for k in keys)+'</p>'
def refs_for(deck,page):
    if deck=='sig':
        if page<=16:return ['ap','channels']
        if page in [22,32,35,36,37,42]:return ['photo']
        if page in [23,43]:return ['sour','sensory']
        if page==25:return ['dysreflexia']
        if page in [21,41,53]:return ['pain']
        return ['sensory','touch','mechanical']
    return {3:['brown','tracts'],4:['asa'],5:['asa'],6:['brown','tracts'],7:['b12'],8:['tracts'],9:['tabes'],10:['friedreich'],11:['tracts'],12:['sma'],13:['als'],14:['cauda'],15:['cauda'],16:['neurogenic','dysreflexia'],17:['tracts']}[page]
titles={};overrides={'sig-14':'Classification of Nerve Fibers: full table','sig-24':'Sensory Receptors: full modality and location table','sig-29':'Threshold: receptor potential versus action potential','sig-36':'Rod phototransduction: channels, voltage, and transmitter release','sig-37':'Pacinian versus rod: full comparison','sig-56':'The End: original closing illustration','sig-57':'Questions: original closing illustration','sig-58':'Thank You: original closing illustration','cord-1':'Spinal Cord Anatomy & Clinical Correlates','cord-18':'Spinal Cord: closing credits'}
for d in decks:
    for p in d['pages']:
        ref=f"{d['id']}-{p['page']}";lines=[s.strip() for s in p['text'].splitlines() if s.strip()]
        title=overrides.get(ref,lines[0] if lines else 'Original visual reference')
        if ref in ['sig-4','sig-26','sig-38']:title=' '.join(lines[:3]).replace('  ',' ')
        titles[ref]=title
body=f'<p class="intro"><strong>76 of 76 original slides</strong>: 58 Neural Signaling and 18 Spinal Cord slides. Expanded bullet notes cover all {len(notes)} instructional/summary slides; every page image, diagram, table, cartoon, label, and credit is retained. Includes {len(boards)} related board-review sections and <strong>{len(questions)} five-choice practice questions</strong> with explanations for every choice. Click an image to enlarge it. Corrections of simplified or inaccurate slide statements are explicitly labeled in the notes.</p>'
body+='<p><a href="lecture-sig.pdf">Original Neural Signaling PDF</a> · <a href="lecture-cord.pdf">Original Spinal Cord PDF</a> · <a href="#board-review">Board-review additions</a></p>'
body+='<div class="tools"><label>Search notes and original slide text<input type="search" id="search" placeholder="e.g. transducin, Romberg, A-delta"></label><label>Lecture<select id="deck"><option value="">Everything</option><option value="sig">Neural Signaling</option><option value="cord">Spinal Cord</option><option value="board">Board-review additions</option></select></label><button id="images" aria-pressed="false">Hide slide images</button><button onclick="window.print()">Print lecture</button></div><p id="search-status" role="status" aria-live="polite"></p>'
body+='<details><summary>Contents: all slides and additions</summary><div class="toc">'
for d in decks:
    for p in d['pages']:
        ref=f"{d['id']}-{p['page']}";body+=f'<a href="#slide-{ref}">{esc(d["title"])} / {p["page"]}: {esc(titles[ref])}</a>'
for b in boards:body+=f'<a href="#board-{b["id"]}">Board: {esc(b["title"])}</a>'
body+='</div></details>'
for d in decks:
    body+=f'<h2>{esc(d["title"])}</h2>'
    for p in d['pages']:
        ref=f"{d['id']}-{p['page']}";title=esc(titles[ref])
        body+=f'<section class="slide" data-deck="{d["id"]}" id="slide-{ref}"><span class="badge">{esc(d["title"])} · Slide {p["page"]}/{len(d["pages"])}</span><h3>{title}</h3>'
        if ref in notes:body+=bullets(notes[ref])+links(refs_for(d['id'],p['page']))
        elif ref=='sig-2':body+=bullets(['Classify fibers by diameter, speed, and myelination and connect these properties to conduction.','Identify sensory receptor classes, explain receptor-potential generation in Pacinian endings and rods, and compare transduction mechanisms.','Explain sensory adaptation and relate it to normal perception and clinical sensory conditions.'])
        elif ref=='sig-3':body+=bullets(['Lecture sequence: nerve fiber types → sensory reception → transduction/receptor potentials → modality-specific mechanisms → sensory adaptation.'])
        elif p['page']==1:body+=bullets(['Original title, author, course information, and reading/contact details are retained in the source slide below. Reading directions are part of the original document, not website instructions.'])
        elif ref in ['sig-56','sig-57','sig-58','cord-18']:body+=bullets(['Original closing page retained, including its illustration or credits. No additional examinable clinical content is introduced on this page.'])
        else:body+=bullets(['Original section divider; the following slides develop this topic.'])
        body+=f'<figure><a href="{p["image"]}" target="_blank" rel="noopener" aria-label="Enlarge {esc(d["title"])} slide {p["page"]}"><img src="{p["image"]}" width="{p["width"]}" height="{p["height"]}" loading="lazy" alt="Complete original {esc(d["title"])} slide {p["page"]}: {title}; includes all original figures, labels, and credits."></a><figcaption>Original full slide. Click for full resolution; all figures and labels are preserved together.</figcaption></figure><details><summary>Original slide text (verbatim extraction)</summary><pre class="transcript">{esc(p["text"])}</pre></details></section>'
body+='<h2 id="board-review">Related high-yield board-review additions</h2><p>These sections connect the supplied lectures to board-style physiology and localization. They supplement the original slide content; they are not a claim about the frequency of particular NBME questions.</p>'
for b in boards:body+=f'<section class="board" data-deck="board" id="board-{b["id"]}"><span class="badge">Board-review addition</span><h3>{esc(b["title"])}</h3>{bullets(b["bullets"])}{links(b["refs"])}</section>'
(root/'index.html').write_text(shell('Lecture','Lecture',body,'<script src="lecture.js" defer></script>'),encoding='utf-8')
practice=f'<p class="intro"><strong>{len(questions)} original NBME-style questions</strong>, from short recall stems to paragraph-length clinical vignettes. Choose one best answer and submit to see reasoning for all five options. The page scrolls to the explanations and displays a Next question button there. Progress is saved in this browser when storage is available.</p><noscript>Enable JavaScript to use practice questions. Lecture and coverage pages remain readable without it.</noscript>'
practice+='<div class="tools"><label>Lecture<select id="deck"><option value="">All lectures and additions</option><option value="sig">Neural Signaling</option><option value="cord">Spinal Cord</option><option value="board">Board integration</option></select></label><label>Topic<select id="topic"><option value="">All topics</option></select></label><label>Review<select id="review"><option value="all">All questions</option><option value="unanswered">Unanswered</option><option value="missed">Incorrect</option></select></label><button id="shuffle">Shuffle questions</button><button id="reset">Reset progress</button></div><p class="stats" id="stats" role="status" aria-live="polite"></p><p class="muted" id="storage"></p><div class="tools"><button id="prev">← Previous</button><label>Jump to question<select id="jump" aria-label="Jump to question"></select></label><button id="next">Next question →</button></div><div id="question"></div><div id="answer-nav" class="answer-nav" hidden><span id="answer-position"></span><button id="answer-next">Next question →</button></div>'
(root/'practice.html').write_text(shell('Practice questions','Practice questions',practice,'<script src="data.js" defer></script><script src="practice.js" defer></script>'),encoding='utf-8')
coverage=f'<p>Both user-supplied PDFs are included: <strong>58 Neural Signaling slides + 18 Spinal Cord slides = 76 pages</strong>. Every original page is rendered, including tables, illustrations, cartoons, and credits. All {len(notes)} instructional/summary pages have expanded bullet notes and practice references. The other 14 pages are objectives, outlines, titles, dividers, and closing pages. The question bank has {len(questions)} items and {5*len(questions)} individual choice explanations.</p><p>Original images preserve text embedded inside diagrams that may be missing from automatic text extraction. Slide instructions, readings, and contact details remain source content. Corrections distinguish CNS MS from peripheral fiber classes, rods from spiking retinal ganglion cells, modern sour transduction, and multifactorial clinical disorders from adaptation alone.</p><p>Use a question ID below to open that item directly. Administrative and divider pages do not require separate questions.</p><div class="table-wrap"><table><thead><tr><th>Source/page</th><th>Topic</th><th>Notes</th><th>Questions</th></tr></thead><tbody>'
for d in decks:
    for p in d['pages']:
        ref=f"{d['id']}-{p['page']}";qs=[q for q in questions if q['ref']==ref]
        coverage+=f'<tr><td><a href="index.html#slide-{ref}">{esc(d["title"])} / {p["page"]}</a></td><td>{esc(titles[ref])}</td><td>{"Expanded" if ref in notes else "Original retained; administrative/divider"}</td><td>'+(', '.join(f'<a href="practice.html?q={q["id"]}">{q["id"]}</a>' for q in qs) if qs else 'Related instructional sections cover the concepts')+'</td></tr>'
for b in boards:
    qs=[q for q in questions if q['ref']=='board-'+b['id']]
    coverage+=f'<tr><td>Board addition</td><td><a href="index.html#board-{b["id"]}">{esc(b["title"])}</a></td><td>Expanded</td><td>'+', '.join(f'<a href="practice.html?q={q["id"]}">{q["id"]}</a>' for q in qs)+'</td></tr>'
coverage+='</tbody></table></div><h2>Source PDFs and references</h2><p><a href="lecture-sig.pdf">Neural Signaling: original PDF</a> · <a href="lecture-cord.pdf">Spinal Cord: original PDF</a></p><p>The provided decks determine lecture coverage. These references support related physiology, clinical localization, and corrections. Consulted October 15, 2026. No external dependencies are needed to read the site or answer questions.</p><ul>'
for s in sources.values():coverage+=f'<li><a href="{s["url"]}" target="_blank" rel="noopener">{esc(s["title"])}</a></li>'
coverage+='</ul>'
(root/'coverage.html').write_text(shell('Coverage & sources','Coverage & sources',coverage),encoding='utf-8')
report={'slides':76,'expanded_sections':len(notes),'board_sections':len(boards),'questions':len(questions),'choice_explanations':5*len(questions),'stem_words_min':min(len(q['stem'].split()) for q in questions),'stem_words_max':max(len(q['stem'].split()) for q in questions),'answer_positions':{str(i):sum(q['answer']==i for q in questions) for i in range(5)}}
(root/'coverage-report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2))
