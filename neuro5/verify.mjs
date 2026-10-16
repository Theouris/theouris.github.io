// Optional development dependency: happy-dom. The website itself has no packages.
import fs from 'node:fs';
import {pathToFileURL} from 'node:url';
import assert from 'node:assert/strict';
const {Window}=await import(process.env.NEURO_DOM_MODULE?pathToFileURL(process.env.NEURO_DOM_MODULE).href:'happy-dom');
const root=new URL('./',import.meta.url),read=name=>fs.readFileSync(new URL(name,root),'utf8');
const report=JSON.parse(read('coverage-report.json'));
const settings={enableJavaScriptEvaluation:true,disableJavaScriptFileLoading:true,disableCSSFileLoading:true,suppressInsecureJavaScriptEnvironmentWarning:true};
const win=new Window({url:'http://localhost/neuro5/',settings});let lastScroll;
win.HTMLElement.prototype.scrollIntoView=function(options){lastScroll={id:this.id,options};};
win.document.write(read('index.html'));win.eval(read('data.js'));win.eval(read('practice.js'));
const $=id=>win.document.getElementById(id),bank=win.NEURO.questions;
const change=(id,value)=>{$(id).value=value;$(id).dispatchEvent(new win.Event('change'));};
assert.equal(bank.length,report.questions);assert.equal(bank.length,220);
assert.equal($('jump').options.length,bank.length);assert.ok($('answer-nav').hidden);
assert.equal($('deck').options.length,4);
for(let i=0;i<bank.length;i++){
  const q=bank[i];assert.ok($('question').textContent.includes(q.id));assert.equal(win.document.querySelectorAll('.choice').length,5);
  win.document.querySelector(`input[value="${q.answer}"]`).checked=true;
  $('answer-form').dispatchEvent(new win.Event('submit',{cancelable:true}));
  assert.match($('explanation').textContent,/Correct — best answer/);assert.equal(win.document.querySelectorAll('.rationale').length,5);
  for(const o of q.options)assert.ok($('explanation').textContent.includes(o.why));
  assert.ok(win.document.querySelector('#explanation a').href.endsWith('coverage.html#'+q.ref));
  assert.equal(lastScroll.id,'explanation');assert.equal(lastScroll.options.block,'start');assert.equal(win.document.activeElement.id,'explanation');
  assert.equal($('answer-nav').hidden,false);assert.equal(win.document.querySelectorAll('input:disabled').length,5);
  if(i<bank.length-1){$('answer-next').click();assert.equal(lastScroll.id,'question');assert.equal(win.document.activeElement.id,'question-heading');assert.ok($('answer-nav').hidden);}
}
assert.equal($('answer-next').disabled,true);assert.match($('answer-position').textContent,/End of current/);
assert.ok($('stats').textContent.includes(`${bank.length} answered · ${bank.length} correct · 100%`));
$('retry').click();assert.ok($('explanation').hidden);assert.ok($('answer-nav').hidden);
win.document.querySelector(`input[value="${(bank.at(-1).answer+1)%5}"]`).checked=true;
$('answer-form').dispatchEvent(new win.Event('submit',{cancelable:true}));assert.match($('explanation').textContent,/Incorrect — best answer/);
const saved=win.localStorage.getItem('neuro5-practice-v1');assert.ok(saved);
change('review','missed');assert.equal($('jump').options.length,1);
change('review','unanswered');assert.match($('question').textContent,/No questions match/);assert.ok($('answer-nav').hidden);
change('review','all');
for(const d of win.NEURO.decks){change('deck',d.id);assert.equal($('jump').options.length,report.questions_by_deck[d.id]);}
change('deck','emb');change('topic','Neurulation');
const topicCount=bank.filter(q=>q.deck==='emb'&&q.topic==='Neurulation').length;
assert.equal($('jump').options.length,topicCount);$('shuffle').click();assert.equal($('jump').options.length,topicCount);
change('deck','path');assert.match($('question').textContent,/No questions match/);change('topic','');
assert.equal($('jump').options.length,report.questions_by_deck.path);
const reload=new Window({url:'http://localhost/neuro5/index.html?q=Q012',settings});reload.localStorage.setItem('neuro5-practice-v1',saved);
reload.document.write(read('index.html'));reload.eval(read('data.js'));reload.eval(read('practice.js'));
assert.match(reload.document.getElementById('question').textContent,/Q012/);
assert.ok(reload.document.getElementById('stats').textContent.includes(`${bank.length} answered · ${bank.length-1} correct`));
assert.equal(reload.localStorage.getItem('neuro4-practice-v1'),null);
const blocked=new Window({url:'http://localhost/neuro5/',settings});Object.defineProperty(blocked,'localStorage',{get(){throw new Error('Storage blocked');}});
blocked.document.write(read('index.html'));blocked.eval(read('data.js'));blocked.eval(read('practice.js'));
assert.match(blocked.document.getElementById('storage').textContent,/unavailable/);
// Reset affects only this isolated test state.
win.confirm=()=>true;$('reset').click();assert.match($('stats').textContent,/0 answered/);assert.ok($('answer-nav').hidden);
const topics=JSON.parse(read('topics.json'));
assert.equal(topics.filter(t=>t.instructional).length,66);
assert.equal(topics.length,78);
for(const t of topics.filter(t=>t.instructional))assert.ok(bank.some(q=>q.ref==='slide-'+t.key));
for(const file of ['index.html','coverage.html']){
  const doc=new Window({url:'http://localhost/neuro5/'+file});doc.document.write(read(file));
  if(file==='coverage.html'){
    assert.equal(doc.document.querySelectorAll('section.slide').length,78);
    assert.equal(doc.document.querySelectorAll('figure img').length,78);
    assert.equal(doc.document.querySelectorAll('pre.transcript').length,78);
  }
  for(const el of doc.document.querySelectorAll('[href],[src]')){
    const value=el.getAttribute('href')||el.getAttribute('src');if(/^(https?:|\.\.\/)/.test(value))continue;
    const [target,hash]=value.split('?')[0].split('#');if(target)assert.ok(fs.existsSync(new URL(target,root)),`${file}: ${value}`);
    if(hash)assert.ok((target?read(target):read(file)).includes(`id="${hash}"`),`${file}: missing ${value}`);
  }
  await doc.happyDOM.close();
}
assert.match(read('style.css'),/\.answer-nav\{position:sticky;bottom:0/);
console.log(`PASS: ${bank.length} submissions; ${bank.length*5} rendered rationales; wrong answer, retry, reset, lecture/topic/review filters, shuffle, deep links, storage reload/fallback, explanation scroll/focus, persistent Next across full bank, final-item state, 78 source images/transcripts, 66 mapped instructional slides, local links and anchors.`);
await Promise.all([win.happyDOM.close(),reload.happyDOM.close(),blocked.happyDOM.close()]);
