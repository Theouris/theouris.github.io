"""Build the static Neuro 3 study site; Python standard library only."""
from pathlib import Path
import json, html, random
root=Path(__file__).resolve().parent
def load(name):return json.loads((root/name).read_text(encoding='utf8'))
esc=html.escape
decks=load('slides.json');notes=load('notes.json');boards=load('board-review.json');sources=load('sources.json')
questions=[]
for line_number,line in enumerate((root/'questions.txt').read_text(encoding='utf8').splitlines(),1):
    if not line.strip():continue
    fields=line.split('|');assert len(fields)==8,(line_number,'Five choices required')
    ref,topic,stem,*choices=fields;opts=[]
    for i,choice in enumerate(choices):
        text,why=choice.split('~',1);assert text.strip() and why.strip()
        opts.append({'text':text,'why':why,'correct':i==0})
    random.Random(3817+line_number).shuffle(opts)
    answer=next(i for i,o in enumerate(opts) if o['correct'])
    for o in opts:del o['correct']
    questions.append({'id':f'Q{len(questions)+1:03}','ref':ref,'deck':ref.split('-')[0],'topic':topic,'stem':stem,'options':opts,'answer':answer})
valid={f"{d['id']}-{p['page']}" for d in decks for p in d['pages']}|{'board-'+b['id'] for b in boards}
assert len(questions)==len({q['stem'] for q in questions})
assert all(q['ref'] in valid for q in questions)
assert set(notes)<=valid
assert all(any(q['ref']==ref for q in questions) for ref in notes), 'An instructional slide lacks questions'
assert all(any(q['ref']=='board-'+b['id'] for q in questions) for b in boards)
assert all(len(q['options'])==5 and len({o['text'] for o in q['options']})==5 for q in questions)
assert sum(len(d['pages']) for d in decks)==68
assert all((root/p['image']).is_file() and (root/p['image']).stat().st_size>1000 for d in decks for p in d['pages'])
assert (root/'lecture-cn.pdf').is_file()
assert all(ref in sources for b in boards for ref in b['refs'])
(root/'questions.json').write_text(json.dumps(questions,ensure_ascii=False,indent=2),encoding='utf8')
(root/'data.js').write_text('window.NEURO = '+json.dumps({'questions':questions},ensure_ascii=False)+';\n',encoding='utf8')
def shell(title,active,body,scripts=''):
    nav=''.join(f'<a href="{file}"'+(' aria-current="page"' if name==active else '')+f'>{name}</a>' for file,name in [('index.html','Lecture'),('practice.html','Practice questions'),('coverage.html','Coverage & sources')])
    return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Neuro 3 | {title}</title><link rel="stylesheet" href="style.css">{scripts}</head><body><header><a href="../">Home</a> · <a href="../neuro1/">Neuro 1</a> · <a href="../neuro2/">Neuro 2</a><h1>Neuro 3: {title}</h1><nav aria-label="Study tabs">{nav}</nav></header><main>{body}</main><footer>Source: Aftab Merchant, Cranial Nerves and Brainstem I, UNLV, 2026. Every source slide and original figure credit is retained. Board additions and questions are original study material, not official NBME items.</footer></body></html>'
def bullets(items):return '<ul>'+''.join(f'<li>{esc(item)}</li>' for item in items)+'</ul>'
def links(keys):return '<p class="refs">References: '+''.join(f'<a href="{sources[k]["url"]}" target="_blank" rel="noopener">{esc(sources[k]["title"])}</a>' for k in keys)+'</p>'
def refs_for(page):
    if page<=13:return ['cn','brainstem']
    if page<=23:return ['ocular','iii','ino']
    if page<=28:return ['v']
    if page<=33:return ['facial','chorda']
    if page==34:return ['corneal']
    if page<=39:return ['viii','meniere','schwannoma']
    if page<=46:return ['ixx','vagal','larynx']
    if page<=52:return ['cn','exam']
    return ['brainstem','lateralmed','medialmed','pons']
titles={};override={31:'Facial nerve: five terminal motor branches',32:'Every named facial muscle: groups and actions',57:'Cranial nerve nuclei: complete image-only chart',68:'Closing credits'}
for d in decks:
    for p in d['pages']:
        lines=[s.strip() for s in p['text'].splitlines() if s.strip()]
        titles[p['page']]=override.get(p['page'],lines[0] if lines else 'Original visual reference')
body=f'<p class="intro"><strong>68 of 68 original slides</strong> from the supplied Cranial Nerves I PDF, with complete images, figures, diagrams, labels, and credits. Expanded bullet notes cover all {len(notes)} instructional slides, including the image-only nuclei chart. Includes {len(boards)} related board-review sections and <strong>{len(questions)} five-choice questions</strong> with explanations for every choice. Click any slide image to enlarge it.</p>'
body+='<p><a href="lecture-cn.pdf">Original lecture PDF</a> · <a href="#board-review">Related board-review additions</a> · <a href="coverage.html">Slide-to-question coverage</a></p><div class="tools"><label>Search notes and original slide text<input type="search" id="search" placeholder="e.g. trochlear, solitary, chorda tympani"></label><label>Section<select id="deck"><option value="">Everything</option><option value="cn">Cranial Nerves I lecture</option><option value="board">Board-review additions</option></select></label><button id="images" aria-pressed="false">Hide slide images</button><button onclick="window.print()">Print lecture</button></div><p id="search-status" role="status" aria-live="polite"></p>'
body+='<details><summary>Contents: every slide and board-review section</summary><div class="toc">'
for p in decks[0]['pages']:body+=f'<a href="#slide-cn-{p["page"]}">Slide {p["page"]}: {esc(titles[p["page"]])}</a>'
for b in boards:body+=f'<a href="#board-{b["id"]}">Board: {esc(b["title"])}</a>'
body+='</div></details>'
for p in decks[0]['pages']:
    ref=f'cn-{p["page"]}';title=esc(titles[p['page']])
    body+=f'<section class="slide" data-deck="cn" id="slide-{ref}"><span class="badge">Original lecture · Slide {p["page"]}/68</span><h3>{title}</h3>'
    if ref in notes:body+=bullets(notes[ref])+links(refs_for(p['page']))
    elif p['page']==2:body+=bullets(['Describe brainstem external anatomy, surface landmarks, cranial attachments, and arterial supply.','Explain the twelve cranial nerve pathways, components, functions, skull foramina, and peripheral lesion patterns.','Relate internal nuclei, fascicles, long tracts, and vascular territories to motor, sensory, and autonomic function.','Original pre-session readings/videos and directions are preserved below as source content; they are not instructions executed by this site.'])
    elif p['page'] in [1,68]:body+=bullets(['Original title/author or closing credits page retained in full. No additional clinical content is introduced on this page.'])
    else:body+=bullets(['Original section divider retained. The following slides develop the named topic.'])
    body+=f'<figure><a href="{p["image"]}" target="_blank" rel="noopener" aria-label="Enlarge slide {p["page"]}: {title}"><img src="{p["image"]}" width="{p["width"]}" height="{p["height"]}" loading="lazy" alt="Complete original cranial nerves slide {p["page"]}: {title}; all original figures, labels, and credits retained."></a><figcaption>Full original slide. Click to enlarge; use the source PDF for original vector/detail access.</figcaption></figure><details><summary>Original slide text (verbatim extraction)</summary><pre class="transcript">{esc(p["text"]) if p["text"] else "This slide is an image-only nuclei chart. Its content is explained in the bullet notes and retained in the full image above."}</pre></details></section>'
body+='<h2 id="board-review">Related high-yield board-review additions</h2><p>These labeled supplements connect the supplied lecture to common board-style mechanisms, examinations, and localization patterns. They are not official NBME content or a claim about exact question frequency.</p>'
for b in boards:body+=f'<section class="board" data-deck="board" id="board-{b["id"]}"><span class="badge">Board-review addition</span><h3>{esc(b["title"])}</h3>{bullets(b["bullets"])}{links(b["refs"])}</section>'
(root/'index.html').write_text(shell('Lecture','Lecture',body,'<script src="lecture.js" defer></script>'),encoding='utf8')
practice=f'<p class="intro"><strong>{len(questions)} original NBME-style questions</strong>, from short recall stems to paragraph-length clinical vignettes. Each has one best answer and five choices. Submit to reveal choice-by-choice reasoning; the page scrolls to it and shows a persistent Next question button. Browser-local progress is saved when storage is available.</p><noscript>Enable JavaScript for practice. Lecture and coverage pages remain readable without it.</noscript>'
practice+='<div class="tools"><label>Section<select id="deck"><option value="">All lecture and board questions</option><option value="cn">Original lecture topics</option><option value="board">Board integration</option></select></label><label>Topic<select id="topic"><option value="">All topics</option></select></label><label>Review<select id="review"><option value="all">All questions</option><option value="unanswered">Unanswered</option><option value="missed">Incorrect</option></select></label><button id="shuffle">Shuffle questions</button><button id="reset">Reset progress</button></div><p class="stats" id="stats" role="status" aria-live="polite"></p><p class="muted" id="storage"></p><div class="tools"><button id="prev">← Previous</button><label>Jump to question<select id="jump" aria-label="Jump to question"></select></label><button id="next">Next question →</button></div><div id="question"></div><div id="answer-nav" class="answer-nav" hidden><span id="answer-position"></span><button id="answer-next">Next question →</button></div>'
(root/'practice.html').write_text(shell('Practice questions','Practice questions',practice,'<script src="data.js" defer></script><script src="practice.js" defer></script>'),encoding='utf8')
coverage=f'<p>The user confirmed that this section should use only <strong>NNN 3 – Cranial Nerves I.pdf</strong>. Its 68 pages are included in full. Expanded bullet notes cover all {len(notes)} instructional pages, including slide 57, whose nuclei chart has no machine-readable text. The other 11 pages are titles, objectives, dividers, and credits. There are {len(boards)} related board-review sections, {len(questions)} questions, and {len(questions)*5} individual choice explanations.</p><p>Original images preserve all diagram labels and figure credits. Course directions and contact details remain source content. Clarifications address ocular test position versus anatomical action, CN III pupil exceptions, the two meanings of SCA, traditional cranial-XI terminology, and variable sensory classifications.</p><div class="table-wrap"><table><thead><tr><th>Slide</th><th>Topic</th><th>Notes</th><th>Practice references</th></tr></thead><tbody>'
for p in decks[0]['pages']:
    ref=f'cn-{p["page"]}';qs=[q for q in questions if q['ref']==ref]
    coverage+=f'<tr><td><a href="index.html#slide-{ref}">{p["page"]}</a></td><td>{esc(titles[p["page"]])}</td><td>{"Expanded" if ref in notes else "Original retained; administrative/divider"}</td><td>'+(', '.join(f'<a href="practice.html?q={q["id"]}">{q["id"]}</a>' for q in qs) if qs else 'Related instructional sections cover the concepts')+'</td></tr>'
for b in boards:
    qs=[q for q in questions if q['ref']=='board-'+b['id']]
    coverage+=f'<tr><td>Board addition</td><td><a href="index.html#board-{b["id"]}">{esc(b["title"])}</a></td><td>Expanded</td><td>'+', '.join(f'<a href="practice.html?q={q["id"]}">{q["id"]}</a>' for q in qs)+'</td></tr>'
coverage+='</tbody></table></div><h2>Sources and references</h2><p><a href="lecture-cn.pdf">Original lecture PDF</a>. The supplied lecture determines slide coverage; these references support related explanations and clinical qualifications. Consulted October 15, 2026. External pages are optional reading, not dependencies of this site.</p><ul>'
for s in sources.values():coverage+=f'<li><a href="{s["url"]}" target="_blank" rel="noopener">{esc(s["title"])}</a></li>'
coverage+='</ul>'
(root/'coverage.html').write_text(shell('Coverage & sources','Coverage & sources',coverage),encoding='utf8')
report={'slides':68,'expanded_sections':len(notes),'board_sections':len(boards),'questions':len(questions),'choice_explanations':5*len(questions),'stem_words_min':min(len(q['stem'].split()) for q in questions),'stem_words_max':max(len(q['stem'].split()) for q in questions),'questions_by_deck':{key:sum(q['deck']==key for q in questions) for key in ['cn','board']},'answer_positions':{str(i):sum(q['answer']==i for q in questions) for i in range(5)}}
(root/'coverage-report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
print(json.dumps(report,indent=2))
