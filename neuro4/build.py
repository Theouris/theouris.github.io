"""Build the static Neuro 4 practice site and validate source coverage."""
from pathlib import Path
import json, html, random
root=Path(__file__).resolve().parent
def load(name):return json.loads((root/name).read_text(encoding='utf8'))
esc=html.escape
slides=load('slides.json');topics=load('topics.json');sources=load('sources.json')
lines=[l for l in (root/'questions.txt').read_text(encoding='utf8').splitlines() if l.strip()]
lines.sort(key=lambda l:int(l.split('|')[0]))
questions=[]
for line_number,line in enumerate(lines,1):
    fields=line.split('|');assert len(fields)==8,(line_number,'Five answer choices required')
    page,topic,stem,*choices=fields;page=int(page);opts=[]
    for i,choice in enumerate(choices):
        text,why=choice.split('~',1);assert text.strip() and why.strip()
        opts.append({'text':text,'why':why,'correct':i==0})
    random.Random(4826+line_number).shuffle(opts);answer=next(i for i,o in enumerate(opts) if o['correct'])
    for o in opts:del o['correct']
    questions.append({'id':f'Q{line_number:03}','ref':f'slide-{page}','page':page,'topic':topic,'stem':stem,'options':opts,'answer':answer})
assert len(slides)==23 and [s['page'] for s in slides]==list(range(1,24))
assert [t['page'] for t in topics]==list(range(1,24))
assert len(questions)==len({q['stem'] for q in questions}), 'Duplicate stems'
assert all(q['page'] in range(1,24) and len(q['options'])==5 and len({o['text'] for o in q['options']})==5 for q in questions)
assert all(any(q['page']==t['page'] for q in questions) for t in topics if t['instructional']), 'Instructional slide not covered'
assert all((root/s['image']).is_file() and (root/s['image']).stat().st_size>1000 for s in slides)
assert (root/'lecture.pdf').is_file()
(root/'questions.json').write_text(json.dumps(questions,ensure_ascii=False,indent=2),encoding='utf8')
(root/'data.js').write_text('window.NEURO = '+json.dumps({'questions':questions},ensure_ascii=False)+';\n',encoding='utf8')
def shell(title,active,body,scripts=''):
    nav=''.join(f'<a href="{file}"'+(' aria-current="page"' if name==active else '')+f'>{name}</a>' for file,name in [('index.html','Practice questions'),('coverage.html','Slide coverage & source')])
    return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Neuro 4 | {title}</title><link rel="stylesheet" href="style.css">{scripts}</head><body><header><a href="../">Home</a> · <a href="../neuro3/">Neuro 3</a><h1>Neuro 4: {title}</h1><nav aria-label="Study tabs">{nav}</nav></header><main>{body}</main><footer>Based on Aftab Merchant, Brainstem and Cranial Nerves II (NNN 4.1), UNLV, 2026. Questions are original NBME-style practice, not official NBME items. Source diagrams and credits are preserved in the reference tab.</footer></body></html>'
body=f'<p class="intro"><strong>{len(questions)} five-choice questions</strong> covering every instructional slide in NNN 4.1: nuclei, tracts, vascular supply, crossed findings, Horner, medial/lateral medulla and pons, Weber, and Parinaud. Stems range from brief recall to clinical paragraphs. Submit one best answer to see reasoning for all five choices; the page scrolls to explanations and displays a persistent Next question button.</p><noscript>Enable JavaScript for interactive practice. The coverage and source page remains readable without it.</noscript>'
body+='<div class="tools"><label>Topic<select id="topic"><option value="">All topics</option></select></label><label>Review<select id="review"><option value="all">All questions</option><option value="unanswered">Unanswered</option><option value="missed">Incorrect</option></select></label><button id="shuffle">Shuffle questions</button><button id="reset">Reset progress</button></div><p class="stats" id="stats" role="status" aria-live="polite"></p><p class="muted" id="storage"></p><div class="tools"><button id="prev">← Previous</button><label>Jump to question<select id="jump" aria-label="Jump to question"></select></label><button id="next">Next question →</button></div><div id="question"></div><div id="answer-nav" class="answer-nav" hidden><span id="answer-position"></span><button id="answer-next">Next question →</button></div>'
(root/'index.html').write_text(shell('Brainstem localization practice','Practice questions',body,'<script src="data.js" defer></script><script src="practice.js" defer></script>'),encoding='utf8')
coverage=f'<p><strong>23 original pages, 20 instructional slides, {len(questions)} questions, {5*len(questions)} choice explanations.</strong> All instructional slides—including the image-only nuclei chart on slide 5—have linked questions. Title, objectives, and credits are retained without separate administrative questions. Select a question ID to open that question, or expand a source image below.</p><p><a href="lecture.pdf">Open original lecture PDF</a></p><p>Coverage checklists below describe source concepts and necessary clinical qualifications; they are reference aids for the question bank. Document readings and pre-class instructions remain source content. Named syndrome patterns and arterial associations are classic models rather than absolute rules for every patient.</p><div class="table-wrap"><table><thead><tr><th>Slide</th><th>Content</th><th>Questions</th></tr></thead><tbody>'
for t in topics:
    qs=[q for q in questions if q['page']==t['page']]
    coverage+=f'<tr><td><a href="#slide-{t["page"]}">{t["page"]}</a></td><td>{esc(t["title"])}</td><td>'+(', '.join(f'<a href="index.html?q={q["id"]}">{q["id"]}</a>' for q in qs) if qs else 'Title/objectives/credits: original retained')+'</td></tr>'
coverage+='</tbody></table></div><h2>Source slide references and coverage checklists</h2>'
for t,s in zip(topics,slides):
    coverage+=f'<section class="slide" id="slide-{s["page"]}"><span class="badge">Original slide {s["page"]}/23</span><h3>{esc(t["title"])}</h3><ul>'+''.join(f'<li>{esc(item)}</li>' for item in t['items'])+'</ul>'
    coverage+=f'<details><summary>Show original slide image</summary><figure><a href="{s["image"]}" target="_blank" rel="noopener" aria-label="Enlarge original slide {s["page"]}"><img src="{s["image"]}" loading="lazy" width="{s["width"]}" height="{s["height"]}" alt="Full original NNN 4.1 slide {s["page"]}: {esc(t["title"])}; all diagram labels and credits retained."></a><figcaption>Click to enlarge. The original PDF retains original vector/detail access.</figcaption></figure></details>'
    coverage+=f'<details><summary>{"Original extracted slide text" if s["text"] else "Text extraction note: image-only chart"}</summary><pre class="transcript">{esc(s["text"]) if s["text"] else "No machine-readable text was present. The nuclei chart is preserved in the image and its content is included in the checklist/questions."}</pre></details></section>'
coverage+='<h2>Supporting references</h2><p>The supplied deck determines coverage. References below support the explanations and clinical qualifications; consulted October 15, 2026. External sites are optional reading and not required to run practice.</p><ul>'
for s in sources:coverage+=f'<li><a href="{s["url"]}" target="_blank" rel="noopener">{esc(s["title"])}</a></li>'
coverage+='</ul>'
(root/'coverage.html').write_text(shell('Slide coverage & source','Slide coverage & source',coverage),encoding='utf8')
report={'source_pages':23,'instructional_slides':sum(t['instructional'] for t in topics),'questions':len(questions),'choice_explanations':len(questions)*5,'stem_words_min':min(len(q['stem'].split()) for q in questions),'stem_words_max':max(len(q['stem'].split()) for q in questions),'questions_per_slide':{str(t['page']):sum(q['page']==t['page'] for q in questions) for t in topics},'answer_positions':{str(i):sum(q['answer']==i for q in questions) for i in range(5)}}
(root/'coverage-report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
print(json.dumps(report,indent=2))
