// Optional development test dependency: happy-dom (not required by the site).
import fs from 'node:fs';
import {pathToFileURL} from 'node:url';
import assert from 'node:assert/strict';
const {Window}=await import(process.env.NEURO_DOM_MODULE?pathToFileURL(process.env.NEURO_DOM_MODULE).href:'happy-dom');
const root=new URL('./',import.meta.url),read=name=>fs.readFileSync(new URL(name,root),'utf8');
const settings={enableJavaScriptEvaluation:true,disableJavaScriptFileLoading:true,disableCSSFileLoading:true,suppressInsecureJavaScriptEnvironmentWarning:true};
const win=new Window({url:'http://localhost/neuro4/',settings});let lastScroll;
win.HTMLElement.prototype.scrollIntoView=function(options){lastScroll={id:this.id,options};};
win.document.write(read('index.html'));win.eval(read('data.js'));win.eval(read('practice.js'));
const $=id=>win.document.getElementById(id),bank=win.NEURO.questions;
assert.equal(bank.length,88);assert.equal($('jump').options.length,88);assert.ok($('answer-nav').hidden);
for(let i=0;i<bank.length;i++){
  const q=bank[i];assert.ok($('question').textContent.includes(q.id));assert.equal(win.document.querySelectorAll('.choice').length,5);
  win.document.querySelector(`input[value="${q.answer}"]`).checked=true;
  $('answer-form').dispatchEvent(new win.Event('submit',{cancelable:true}));
  assert.match($('explanation').textContent,/Correct — best answer/);assert.equal(win.document.querySelectorAll('.rationale').length,5);
  for(const o of q.options)assert.ok($('explanation').textContent.includes(o.why));
  assert.ok(win.document.querySelector('#explanation a').href.endsWith('coverage.html#'+q.ref));
  assert.equal(lastScroll.id,'explanation');assert.equal(lastScroll.options.block,'start');assert.equal(win.document.activeElement.id,'explanation');
  assert.equal($('answer-nav').hidden,false);
  if(i<bank.length-1){$('answer-next').click();assert.equal(lastScroll.id,'question');assert.equal(win.document.activeElement.id,'question-heading');assert.ok($('answer-nav').hidden);}
}
assert.equal($('answer-next').disabled,true);assert.match($('answer-position').textContent,/End of current/);assert.match($('stats').textContent,/88 answered · 88 correct · 100%/);
$('retry').click();win.document.querySelector(`input[value="${(bank.at(-1).answer+1)%5}"]`).checked=true;
$('answer-form').dispatchEvent(new win.Event('submit',{cancelable:true}));assert.match($('explanation').textContent,/Incorrect — best answer/);
const saved=win.localStorage.getItem('neuro4-practice-v1');assert.ok(saved);
$('review').value='missed';$('review').dispatchEvent(new win.Event('change'));assert.equal($('jump').options.length,1);
$('review').value='unanswered';$('review').dispatchEvent(new win.Event('change'));assert.match($('question').textContent,/No questions match/);assert.ok($('answer-nav').hidden);
$('review').value='all';$('topic').value='Horner syndrome';$('topic').dispatchEvent(new win.Event('change'));assert.equal($('jump').options.length,5);
$('shuffle').click();assert.equal($('jump').options.length,5);
const reload=new Window({url:'http://localhost/neuro4/index.html?q=Q012',settings});reload.localStorage.setItem('neuro4-practice-v1',saved);
reload.document.write(read('index.html'));reload.eval(read('data.js'));reload.eval(read('practice.js'));
assert.match(reload.document.getElementById('question').textContent,/Q012/);assert.match(reload.document.getElementById('stats').textContent,/88 answered · 87 correct/);
assert.equal(reload.localStorage.getItem('neuro3-practice-v1'),null);
const blocked=new Window({url:'http://localhost/neuro4/',settings});Object.defineProperty(blocked,'localStorage',{get(){throw new Error('Storage blocked');}});
blocked.document.write(read('index.html'));blocked.eval(read('data.js'));blocked.eval(read('practice.js'));assert.match(blocked.document.getElementById('storage').textContent,/unavailable/);
// Reset applies only to this isolated test origin/state.
win.confirm=()=>true;$('reset').click();assert.match($('stats').textContent,/0 answered/);assert.ok($('answer-nav').hidden);
for(const file of ['index.html','coverage.html']){
  const doc=new Window({url:'http://localhost/neuro4/'+file});doc.document.write(read(file));
  if(file==='coverage.html'){assert.equal(doc.document.querySelectorAll('section.slide').length,23);assert.equal(doc.document.querySelectorAll('figure img').length,23);}
  for(const el of doc.document.querySelectorAll('[href],[src]')){
    const value=el.getAttribute('href')||el.getAttribute('src');if(/^(https?:|\.\.\/)/.test(value))continue;
    const [target,hash]=value.split('?')[0].split('#');if(target)assert.ok(fs.existsSync(new URL(target,root)),`${file}: ${value}`);
    if(hash)assert.ok((target?read(target):read(file)).includes(`id="${hash}"`),`${file}: missing ${value}`);
  }
  await doc.happyDOM.close();
}
console.log('PASS: 88 correct submissions, 440 explanations, wrong-answer/retry/reset, topic/review filters, shuffle, deep links, saved-state reload, storage fallback, automatic explanation scroll/focus, persistent Next through full bank, last-item state, 23 reference images, and local links/anchors.');
await Promise.all([win.happyDOM.close(),reload.happyDOM.close(),blocked.happyDOM.close()]);
