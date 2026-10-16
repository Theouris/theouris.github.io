const bank=NEURO.questions;
const KEY='neuro4-practice-v1';
let state={answers:{},current:null},storageOK=true;
try{const saved=JSON.parse(localStorage.getItem(KEY));if(saved&&saved.answers&&typeof saved.answers==='object')state=saved;}catch{storageOK=false;}
// Ignore stale or malformed stored choices rather than letting them corrupt scores.
state.answers=Object.fromEntries(Object.entries(state.answers).filter(([id,a])=>bank.some(q=>q.id===id)&&Number.isInteger(a)&&a>=0&&a<5));
let queue=[],position=0;
const requested=new URLSearchParams(location.search).get('q');
if(bank.some(q=>q.id===requested))state.current=requested;
const $=id=>document.getElementById(id);
function save(){try{localStorage.setItem(KEY,JSON.stringify(state))}catch{storageOK=false;}$('storage').textContent=storageOK?'':'Browser storage is unavailable; progress lasts for this page session only.';}
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function option(label,value){const el=document.createElement('option');el.textContent=label;el.value=value;return el;}
for(const t of [...new Set(bank.map(q=>q.topic))].sort())$('topic').add(option(t,t));
$('topic').value='';
function rebuild(){
  queue=bank.filter(q=>(!$('topic').value||q.topic===$('topic').value)&&($('review').value==='all'||($('review').value==='unanswered'?!Object.hasOwn(state.answers,q.id):Object.hasOwn(state.answers,q.id)&&state.answers[q.id]!==q.answer)));
  position=Math.max(0,queue.findIndex(q=>q.id===state.current));render();
}
function render(){
  const answered=bank.filter(q=>Object.hasOwn(state.answers,q.id));const right=answered.filter(q=>state.answers[q.id]===q.answer).length;
  $('stats').textContent=`${bank.length} total · ${answered.length} answered · ${right} correct · ${answered.length?Math.round(100*right/answered.length):0}% accuracy · ${queue.length} in current set`;
  $('jump').replaceChildren(...queue.map((q,i)=>option(`${i+1}. ${q.id} — ${q.topic}`,String(i))));$('jump').value=String(position);
  $('prev').disabled=position<=0;$('next').disabled=position>=queue.length-1;
  $('answer-nav').hidden=true;
  if(!queue.length){$('question').innerHTML='<p>No questions match these filters. Choose another topic or review mode.</p>';return;}
  const q=queue[position],done=Object.hasOwn(state.answers,q.id);state.current=q.id;save();
  $('question').innerHTML=`<article class="question"><p class="muted">Question ${position+1} of ${queue.length} · ${esc(q.id)} · ${esc(q.topic)}</p><h2 id="question-heading" tabindex="-1">Choose the single best answer</h2><p class="stem">${esc(q.stem)}</p><form id="answer-form"><fieldset><legend>Answer choices</legend><ol class="choices">${q.options.map((o,i)=>`<li><label class="choice"><input type="radio" name="answer" value="${i}" ${done&&state.answers[q.id]===i?'checked':''} ${done?'disabled':''} required><span><strong>${'ABCDE'[i]}.</strong> ${esc(o.text)}</span></label></li>`).join('')}</ol></fieldset><div class="tools"><button type="submit" ${done?'disabled':''}>Submit answer</button><button type="button" id="retry" ${done?'':'hidden'}>Retry this question</button></div></form><div id="explanation" tabindex="-1" ${done?'':'hidden'}></div></article>`;
  $('answer-form').addEventListener('submit',e=>{e.preventDefault();const chosen=new FormData(e.currentTarget).get('answer');if(chosen===null)return;state.answers[q.id]=Number(chosen);save();render();$('explanation').focus({preventScroll:true});scrollSection($('explanation'));});
  $('retry').addEventListener('click',()=>{delete state.answers[q.id];save();render()});
  if(done){const isRight=state.answers[q.id]===q.answer;$('explanation').className='explanation';$('explanation').innerHTML=`<h3 class="${isRight?'correct':'incorrect'}">${isRight?'Correct':'Incorrect'} — best answer: ${'ABCDE'[q.answer]}</h3>${q.options.map((o,i)=>`<div class="rationale"><strong class="${i===q.answer?'correct':''}">${'ABCDE'[i]}. ${esc(o.text)} — ${i===q.answer?'Correct':'Incorrect'}${i===state.answers[q.id]?' (your choice)':''}</strong><p>${esc(o.why)}</p></div>`).join('')}<p><a href="coverage.html#${q.ref}">Review the source slide and coverage checklist</a></p>`;
    $('answer-nav').hidden=false;$('answer-next').disabled=position>=queue.length-1;
    $('answer-position').textContent=position>=queue.length-1?'End of current question set':`${q.id} reviewed · ${queue.length-position-1} remaining in this set`;
  }
}
function scrollSection(element){element.scrollIntoView({block:'start',behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});}
function advance(){if(position<queue.length-1){position++;render();$('question-heading').focus({preventScroll:true});scrollSection($('question'));}}
for(const id of ['topic','review'])$(id).addEventListener('change',rebuild);
$('prev').addEventListener('click',()=>{if(position>0){position--;render();scrollSection($('question'));}});$('next').addEventListener('click',advance);$('answer-next').addEventListener('click',advance);
$('jump').addEventListener('change',()=>{position=Number($('jump').value);render()});
$('shuffle').addEventListener('click',()=>{for(let i=queue.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[queue[i],queue[j]]=[queue[j],queue[i]];}position=0;render()});
$('reset').addEventListener('click',()=>{if(confirm('Clear all saved answers for these Neuro 4 questions?')){state={answers:{},current:null};save();rebuild()}});
rebuild();
