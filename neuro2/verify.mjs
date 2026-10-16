// Optional development test: set NEURO_DOM_MODULE to happy-dom's absolute lib/index.js.
// The static site itself has no dependency on happy-dom or Node.
import fs from 'node:fs';
import { pathToFileURL } from 'node:url';
import assert from 'node:assert/strict';
const { Window }=await import(process.env.NEURO_DOM_MODULE?pathToFileURL(process.env.NEURO_DOM_MODULE).href:'happy-dom');
const root=new URL('./',import.meta.url);
const read=name=>fs.readFileSync(new URL(name,root),'utf8');
const settings={enableJavaScriptEvaluation:true,disableJavaScriptFileLoading:true,disableCSSFileLoading:true,suppressInsecureJavaScriptEnvironmentWarning:true};
const win=new Window({url:'http://localhost/neuro2/practice.html',settings});
let lastScroll;
win.HTMLElement.prototype.scrollIntoView=function(options){lastScroll={id:this.id,options};};
win.document.write(read('practice.html'));win.eval(read('data.js'));win.eval(read('practice.js'));
const $=id=>win.document.getElementById(id),bank=win.NEURO.questions;
assert.equal(bank.length,158);assert.equal($('jump').options.length,158);
assert.ok($('answer-nav').hidden);
// Exercise the actual answer → scroll → docked Next path through every item.
for(let i=0;i<bank.length;i++){
  const q=bank[i];assert.ok($('question').textContent.includes(q.id));
  assert.equal(win.document.querySelectorAll('.choice').length,5);
  win.document.querySelector(`input[value="${q.answer}"]`).checked=true;
  $('answer-form').dispatchEvent(new win.Event('submit',{cancelable:true}));
  assert.match($('explanation').textContent,/Correct — best answer/);
  assert.equal(win.document.querySelectorAll('.rationale').length,5);
  for(const o of q.options)assert.ok($('explanation').textContent.includes(o.why));
  assert.ok(win.document.querySelector('#explanation a').href.includes(q.ref));
  assert.equal(lastScroll.id,'explanation');assert.equal(lastScroll.options.block,'start');
  assert.equal(win.document.activeElement.id,'explanation');assert.equal($('answer-nav').hidden,false);
  if(i<bank.length-1){
    assert.equal($('answer-next').disabled,false);$('answer-next').click();
    assert.equal(lastScroll.id,'question');assert.equal(win.document.activeElement.id,'question-heading');
    assert.ok($('answer-nav').hidden);
  }
}
assert.equal($('answer-next').disabled,true);assert.match($('answer-position').textContent,/End of current/);
assert.match($('stats').textContent,/158 answered · 158 correct · 100%/);
// Wrong-answer feedback, retry, saved state, and empty/filtered sets.
$('retry').click();win.document.querySelector(`input[value="${(bank.at(-1).answer+1)%5}"]`).checked=true;
$('answer-form').dispatchEvent(new win.Event('submit',{cancelable:true}));
assert.match($('explanation').textContent,/Incorrect — best answer/);assert.equal(lastScroll.id,'explanation');
const saved=win.localStorage.getItem('neuro2-practice-v1');assert.ok(saved);
$('review').value='missed';$('review').dispatchEvent(new win.Event('change'));assert.equal($('jump').options.length,1);
$('review').value='unanswered';$('review').dispatchEvent(new win.Event('change'));assert.match($('question').textContent,/No questions match/);assert.ok($('answer-nav').hidden);
$('review').value='all';$('deck').value='sig';$('deck').dispatchEvent(new win.Event('change'));assert.equal($('jump').options.length,78);
$('shuffle').click();assert.equal($('jump').options.length,78);
$('topic').value='Conduction';$('topic').dispatchEvent(new win.Event('change'));assert.equal($('jump').options.length,bank.filter(q=>q.deck==='sig'&&q.topic==='Conduction').length);
const reload=new Window({url:'http://localhost/neuro2/practice.html?q=Q012',settings});
reload.localStorage.setItem('neuro2-practice-v1',saved);reload.document.write(read('practice.html'));reload.eval(read('data.js'));reload.eval(read('practice.js'));
assert.match(reload.document.getElementById('question').textContent,/Q012/);assert.match(reload.document.getElementById('stats').textContent,/158 answered · 157 correct/);
assert.equal(reload.localStorage.getItem('neuro1-practice-v1'),null);
const blocked=new Window({url:'http://localhost/neuro2/practice.html',settings});Object.defineProperty(blocked,'localStorage',{get(){throw new Error('Storage disabled');}});
blocked.document.write(read('practice.html'));blocked.eval(read('data.js'));blocked.eval(read('practice.js'));assert.match(blocked.document.getElementById('storage').textContent,/unavailable/);
const lecture=new Window({url:'http://localhost/neuro2/index.html',settings});lecture.document.write(read('index.html'));lecture.eval(read('lecture.js'));
assert.equal(lecture.document.querySelectorAll('section.slide').length,76);assert.equal(lecture.document.querySelectorAll('figure img').length,76);
lecture.document.getElementById('search').value='transducin';lecture.document.getElementById('search').dispatchEvent(new lecture.Event('input'));
assert.ok(lecture.document.querySelectorAll('section.slide:not([hidden])').length>0);assert.ok(lecture.document.querySelectorAll('section.slide[hidden]').length>0);
lecture.document.getElementById('images').click();assert.equal(lecture.document.querySelectorAll('figure[hidden]').length,76);
lecture.document.getElementById('images').click();assert.equal(lecture.document.querySelectorAll('figure[hidden]').length,0);
// Every internal file and fragment must exist.
for(const file of ['index.html','practice.html','coverage.html']){
  const doc=new Window({url:'http://localhost/neuro2/'+file});doc.document.write(read(file));
  for(const el of doc.document.querySelectorAll('[href],[src]')){
    const value=el.getAttribute('href')||el.getAttribute('src');if(/^(https?:|\.\.\/)/.test(value))continue;
    const [target,hash]=value.split('?')[0].split('#');if(target)assert.ok(fs.existsSync(new URL(target,root)),`${file}: ${value}`);
    if(hash)assert.ok((target?read(target):read(file)).includes(`id="${hash}"`),`${file}: missing anchor ${value}`);
  }
  await doc.happyDOM.close();
}
console.log('PASS: all 158 answers, 790 rationales, automatic explanation scrolling/focus, docked Next through full bank, end state, wrong answers, retry, filters, shuffle, deep links, saved-state reload, storage failure, 76 slide images, search, image toggle, local links and anchors.');
await Promise.all([win.happyDOM.close(),reload.happyDOM.close(),blocked.happyDOM.close(),lecture.happyDOM.close()]);
