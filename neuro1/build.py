"""Rebuild the dependency-free study pages and validate content/asset coverage.
Run with Python 3. No third-party packages required.
"""
from pathlib import Path
import json, html, random, re
root=Path(__file__).resolve().parent
def load(name): return json.loads((root/name).read_text(encoding='utf-8'))
decks=load('slides.json'); notes=load('notes.json'); boards=load('board-review.json'); sources=load('sources.json')
esc=html.escape
questions=[]
for number,line in enumerate((root/'questions.txt').read_text(encoding='utf-8').splitlines(),1):
    if not line.strip(): continue
    fields=line.split('|'); assert len(fields)==8,(number,len(fields))
    ref,topic,stem,*choices=fields
    opts=[]
    for i,choice in enumerate(choices):
        text,why=choice.split('~',1); assert text and why
        opts.append({'text':text,'why':why,'correct':i==0})
    random.Random(947+number).shuffle(opts)
    answer=next(i for i,o in enumerate(opts) if o.pop('correct',False))
    # Pop all remaining internal markers as well.
    for o in opts:o.pop('correct',None)
    questions.append({'id':f'Q{number:03}','ref':ref,'deck':'board' if ref.startswith('board-') else ref[:3],'topic':topic,'stem':stem,'options':opts,'answer':answer})
assert len({q['stem'] for q in questions})==len(questions)
valid={f"{d['id']}-{p['page']}" for d in decks for p in d['pages']}|{f"board-{b['id']}" for b in boards}
assert all(q['ref'] in valid for q in questions)
assert set(notes)<=valid
assert all((root/p['image']).is_file() for d in decks for p in d['pages'])
assert sum(len(d['pages']) for d in decks)==64
assert all(len(q['options'])==5 and len({o['text'] for o in q['options']})==5 for q in questions)
assert all(any(q['ref']==ref for q in questions) for ref in notes), 'An instructional slide has no practice question'
(root/'data.js').write_text('window.NEURO = '+json.dumps({'questions':questions},ensure_ascii=False)+';\n',encoding='utf-8')
(root/'questions.json').write_text(json.dumps(questions,ensure_ascii=False,indent=2),encoding='utf-8')
def shell(title,tab,body,script=''):
    nav=''.join(f'<a href="{file}"'+(' aria-current="page"' if label==tab else '')+f'>{label}</a>' for file,label in [('index.html','Lecture'),('practice.html','Practice questions'),('coverage.html','Coverage & sources')])
    return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Neuro 1 | {title}</title><link rel="stylesheet" href="style.css">{script}</head><body><header><a href="../">Home</a><h1>Neuro 1: {title}</h1><nav aria-label="Study tabs">{nav}</nav></header><main>{body}</main><footer>Source lectures: Aftab Merchant, UNLV, 2026. Original figures and credits preserved in every slide image and the source PDFs. Board-review notes and questions are study additions and are not official NBME material.</footer></body></html>'
def bullets(items):return '<ul>'+''.join(f'<li>{esc(t)}</li>' for t in items)+'</ul>'
def links(keys):return '<p class="refs">Further reading: '+''.join(f'<a href="{sources[k]["url"]}" target="_blank" rel="noopener">{esc(sources[k]["title"])}</a>' for k in keys)+'</p>'
def refs_for(deck,page):
    if deck=='1.1':return ['ans','splanchnic','pelvic'] if 6<=page<=17 else ['cns','glia']
    return ['skull'] if page<=11 else ['herniation','meninges'] if page<=21 else ['csf','hydro','aqueduct','iih']
titles={}
for d in decks:
    for p in d['pages']:
        lines=[t.strip() for t in p['text'].splitlines() if t.strip()]
        title=lines[0] if lines else 'Visual reference'
        if title=='Self-Study': title=lines[1]
        if title in ['Somatic vs','Overview of the','Meninges and']:title=' '.join(lines[:2])
        titles[f"{d['id']}-{p['page']}"]=title
body=f'<p class="intro">Complete slide-by-slide study lecture for NNN 1.1 and 1.2: <strong>64 of 64 original slides</strong>, expanded bullet notes, original slide text, and <strong>{len(questions)} five-choice practice questions</strong>. Every original figure is preserved within its full slide. Select a slide image to open it at full resolution; both source PDFs are also available. Board-review additions are labeled separately. Slide assignments and contact details are preserved as source content, not instructions for this website.</p>'
body+='<p><a href="lecture-1.1.pdf">Original Lecture 1.1 PDF</a> · <a href="lecture-1.2.pdf">Original Lecture 1.2 PDF</a> · <a href="#board-review">Jump to board-review additions</a></p>'
body+='<div class="tools"><label>Search lecture notes and original text<input id="search" type="search" placeholder="e.g. aqueduct, gray ramus, pterion"></label><label>Section<select id="deck"><option value="">Everything</option><option value="1.1">Lecture 1.1</option><option value="1.2">Lecture 1.2</option><option value="board">Board-review additions</option></select></label><button id="images" aria-pressed="false">Hide slide images</button><button onclick="window.print()">Print lecture</button></div><p id="search-status" role="status" aria-live="polite"></p>'
body+='<details><summary>Contents: every slide and board-review section</summary><div class="toc">'
for d in decks:
    for p in d['pages']:
        ref=f"{d['id']}-{p['page']}";body+=f'<a href="#slide-{ref}">{d["id"]} · Slide {p["page"]}: {esc(titles[ref])}</a>'
for b in boards:body+=f'<a href="#board-{b["id"]}">Board: {esc(b["title"])}</a>'
body+='</div></details>'
for d in decks:
    body+=f'<h2>{d["id"]} — {esc(d["title"])}</h2>'
    for p in d['pages']:
        ref=f"{d['id']}-{p['page']}"
        body+=f'<section class="slide" id="slide-{ref}" data-deck="{d["id"]}"><span class="badge">Lecture {d["id"]} · Slide {p["page"]}</span><h3>{esc(titles[ref])}</h3>'
        if ref in notes:body+=bullets(notes[ref])+links(refs_for(d['id'],p['page']))
        else:
            defaults=['This opening/title slide identifies the lecture and its author; the original is preserved below.'] if p['page']==1 else ['This slide preserves the stated course objectives and pre-session resources. They describe the original course; all instructional content is presented in this study lecture.'] if p['page']==2 else ['Section divider: the following slides develop this topic.'] if p['text'].count('\n')<3 else ['This summary/closing slide is retained in full. Its original points and credits appear below; the corresponding concepts are expanded in the preceding slide sections.']
            body+=bullets(defaults)
        body+=f'<figure><a href="{p["image"]}" target="_blank" rel="noopener" aria-label="Open lecture {d["id"]} slide {p["page"]} at full resolution"><img src="{p["image"]}" loading="lazy" width="1734" height="975" alt="Lecture {d["id"]}, slide {p["page"]}: {esc(titles[ref])}. Complete original slide including all diagrams and labels."></a><figcaption>Original slide {p["page"]} of {len(d["pages"])}; all figures, labels, and source credits retained. Click to enlarge.</figcaption></figure><details><summary>Original slide text (verbatim extraction)</summary><pre class="transcript">{esc(p["text"])}</pre></details></section>'
body+='<h2 id="board-review">Related high-yield board-review additions</h2><p>These supplements connect the supplied lectures to common board-style mechanisms and clinical patterns. They are original study explanations, not a claim about NBME question frequency or exhaustive coverage of all neurology.</p>'
for b in boards:body+=f'<section class="board" data-deck="board" id="board-{b["id"]}"><span class="badge">Board-review addition</span><h3>{esc(b["title"])}</h3>{bullets(b["bullets"])}{links(b["refs"])}</section>'
(root/'index.html').write_text(shell('Lecture','Lecture',body,'<script src="lecture.js" defer></script>'),encoding='utf-8')
coverage=f'<p>Source inventory: Lecture 1.1 has 25 pages; Lecture 1.2 has 39 pages. <strong>All 64 page images and original extracted texts are included.</strong> Expanded notes cover {len(notes)} instructional slides, with {len(boards)} related board-review sections. The bank contains {len(questions)} original questions and {5*len(questions)} answer-choice explanations.</p><p>Title pages, objectives, section dividers, summaries, and closing credits are preserved; their repeated or administrative content does not require a separate question. The map below links every instructional slide to its questions. Image labels remain available at full resolution even where they are not machine-readable in the text extraction.</p><p>Clarifications in the notes address the endothelial BBB seal, specialized choroid epithelium, deep brain gray matter, sensory-neuron VZV latency, spinal epidural contents, and non-universal clinical patterns.</p><div class="table-wrap"><table><thead><tr><th>Slide</th><th>Content</th><th>Expanded notes</th><th>Practice references</th></tr></thead><tbody>'
for d in decks:
    for p in d['pages']:
        ref=f"{d['id']}-{p['page']}";qs=[q for q in questions if q['ref']==ref]
        coverage+=f'<tr><td><a href="index.html#slide-{ref}">{d["id"]} / {p["page"]}</a></td><td>{esc(titles[ref])}</td><td>{"Yes" if ref in notes else "Original retained; administrative/repeated/divider"}</td><td>'+(', '.join(f'<a href="practice.html?q={q["id"]}">{q["id"]}</a>' for q in qs) if qs else 'Covered through related instructional sections')+'</td></tr>'
for b in boards:
    qs=[q for q in questions if q['ref']=='board-'+b['id']]
    coverage+=f'<tr><td>Board</td><td><a href="index.html#board-{b["id"]}">{esc(b["title"])}</a></td><td>Yes</td><td>'+', '.join(f'<a href="practice.html?q={q["id"]}">{q["id"]}</a>' for q in qs)+'</td></tr>'
coverage+='</tbody></table></div><h2>Sources and further reading</h2><p>The supplied slides are the primary source for course coverage. Linked references support the related clinical additions. Links were checked during preparation on October 15, 2026; no external page content or web images are needed to run this site.</p><ul class="sources-list">'
for s in sources.values():coverage+=f'<li><a href="{s["url"]}" target="_blank" rel="noopener">{esc(s["title"])}</a></li>'
coverage+='</ul><p><a href="lecture-1.1.pdf">Original Lecture 1.1 PDF</a> · <a href="lecture-1.2.pdf">Original Lecture 1.2 PDF</a></p>'
(root/'coverage.html').write_text(shell('Coverage & sources','Coverage & sources',coverage),encoding='utf-8')
print(json.dumps({'slides':64,'expanded_slide_sections':len(notes),'board_sections':len(boards),'questions':len(questions),'choice_explanations':5*len(questions),'correct_answer_positions':{str(i):sum(q['answer']==i for q in questions) for i in range(5)}},indent=2))
