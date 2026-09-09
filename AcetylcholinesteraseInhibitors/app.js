'use strict';
const modes = {
  normal: { label:'BASELINE', title:'Release. Bind. Clear.', copy:'ACh activates muscle nicotinic receptors, then AChE rapidly hydrolyzes it. The end plate can reset for the next impulse.', clearance:'Rapid', receptors:'Preserved', response:'Brief, effective contraction', detail:'AChE ends the signal by breaking ACh into choline and acetate.', count:8, enzymes:3, duration:2200 },
  mg: { label:'MYASTHENIA GRAVIS', title:'Fewer working receptors.', copy:'In AChR-antibody–positive MG, functional postsynaptic receptors are reduced. ACh clearance continues, but the end-plate signal may not reach the threshold for a muscle action potential.', clearance:'Rapid', receptors:'Reduced', response:'Impaired transmission · fatigable weakness', detail:'The problem is receptor availability, not a shortage of released ACh. The number shown is illustrative.', count:3, enzymes:3, duration:2200 },
  treated: { label:'MG + AChE INHIBITOR', title:'Give ACh more time.', copy:'An inhibitor such as pyridostigmine slows ACh breakdown. ACh persists in the cleft, improving the chance of activating the remaining muscle receptors.', clearance:'Slower', receptors:'Still reduced', response:'Improved neuromuscular transmission', detail:'Symptomatic treatment improves signaling; it does not replace receptors or remove pathogenic antibodies.', count:3, enzymes:1, duration:4300 },
  excess: { label:'EXCESSIVE INHIBITION', title:'The reset fails.', copy:'Marked ACh accumulation causes repetitive stimulation, followed by impaired transmission from sustained depolarization and receptor desensitization.', clearance:'Markedly impaired', receptors:'Present; function impaired', response:'Fasciculations → weakness / paralysis', detail:'This model shows the NMJ component of cholinergic toxicity. Muscarinic and CNS effects occur at other sites.', count:8, enzymes:0, duration:5800 }
};
const ns='http://www.w3.org/2000/svg';
let mode='normal', frame=0, running=false;
const reducedMotion=window.matchMedia('(prefers-reduced-motion: reduce)');
const $=id=>document.getElementById(id);
function svgEl(name, attributes, parent){const el=document.createElementNS(ns,name);for(const [key,value] of Object.entries(attributes))el.setAttribute(key,value);parent.appendChild(el);return el;}
function drawStructure(){
  const state=modes[mode]; $('receptors').replaceChildren(); $('enzymes').replaceChildren();
  for(let i=0;i<8;i++){
    const x=190+i*50, available=state.count===8 || [1,3,6].includes(i);
    svgEl('path',{d:`M${x-10} 325v24h20v-24`,fill:'none',stroke:available?'#286b5b':'#bdc5bb','stroke-width':8,'stroke-linejoin':'round'},$('receptors'));
    if(!available)svgEl('path',{d:`M${x-8} 321l16 20m0-20l-16 20`,stroke:'#ac6555','stroke-width':2},$('receptors'));
  }
  for(let i=0;i<3;i++){
    const x=260+i*155,y=263,active=i<state.enzymes;
    svgEl('path',{d:`M${x} ${y-18}l19 11v16l-19 11-19-11v-16Z`,fill:active?'#8bb59b':'#e1d8c8',stroke:active?'#507e63':'#b59883','stroke-width':1.5},$('enzymes'));
    if(!active)svgEl('path',{d:`M${x-11} ${y-11}l22 22m0-22l-22 22`,stroke:'#a7543c','stroke-width':3},$('enzymes'));
  }
}
function particlesAt(progress){
  $('particles').replaceChildren();
  for(let i=0;i<24;i++){
    const delay=(i%6)*.045;
    const t=Math.max(0,Math.min(1,(progress-delay)/(1-delay)));
    if(progress<delay)continue;
    const retained=mode==='excess'?22:mode==='treated'?17:7;
    const cleared=i>=retained && t>.47;
    if(cleared){
      if(t<.7){const x=260+(i%3)*155;const y=263;svgEl('circle',{cx:x-5,cy:y+10*(t-.47),r:3,fill:'#bdc5bb',opacity:1-(t-.47)/.23},$('particles'));svgEl('circle',{cx:x+5,cy:y+16*(t-.47),r:2,fill:'#bdc5bb',opacity:1-(t-.47)/.23},$('particles'));}
      continue;
    }
    let x=245+(i%3)*125+Math.sin(i*4)*13,y=145;
    if(t<.6){y+=t/.6*145;x+=Math.sin(i*3)*t*70;}
    else{const u=(t-.6)/.4;x=190+(i%8)*50+Math.sin(i+u*5)*8;y=290+u*29;}
    const opacity=mode==='normal'||mode==='mg'?Math.max(0,1-Math.max(0,t-.75)*4):1;
    svgEl('circle',{cx:x,cy:y,r:5,fill:'#d89930',stroke:'#a66f1c','stroke-width':.6,opacity},$('particles'));
  }
}
function setMode(next){
  cancelAnimationFrame(frame);running=false;mode=next;const state=modes[mode];
  document.querySelectorAll('[data-mode]').forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.mode===mode)));
  for(const [id,value] of Object.entries({'mode-label':state.label,'mode-title':state.title,'mode-copy':state.copy,clearance:state.clearance,availability:state.receptors,response:state.response,'mode-detail':state.detail}))$(id).textContent=value;
  $('svg-desc').textContent=state.copy+' Muscle response: '+state.response+'.';
  $('animation-status').textContent='Selected: '+state.label.toLowerCase()+'. Release ACh to follow the signal.';
  $('replay').innerHTML='Release ACh <span>↻</span>';
  drawStructure();particlesAt(.58);
}
function release(){
  if(running){cancelAnimationFrame(frame);running=false;$('replay').innerHTML='Release ACh <span>↻</span>';$('animation-status').textContent='Animation stopped. Release ACh to restart.';return;}
  if(reducedMotion.matches){particlesAt(.82);$('animation-status').textContent='Static result (reduced motion): '+modes[mode].response+'.';return;}
  running=true;const start=performance.now();$('replay').innerHTML='Stop animation <span>■</span>';$('animation-status').textContent='ACh released. Watch its persistence in the cleft.';
  function tick(now){const p=Math.min(1,(now-start)/modes[mode].duration);particlesAt(p);if(p<1){frame=requestAnimationFrame(tick);}else{running=false;$('replay').innerHTML='Release ACh <span>↻</span>';$('animation-status').textContent='Result: '+modes[mode].response+'.';}}
  frame=requestAnimationFrame(tick);
}
document.querySelectorAll('[data-mode]').forEach(button=>button.addEventListener('click',()=>setMode(button.dataset.mode)));
$('replay').addEventListener('click',release);
document.querySelector('[data-show-treated]').addEventListener('click',()=>{setMode('treated');document.querySelector('[data-mode="treated"]').focus({preventScroll:true});$('junction').scrollIntoView({behavior:reducedMotion.matches?'instant':'smooth'});});
document.querySelectorAll('[data-answer]').forEach(button=>button.addEventListener('click',()=>{
  document.querySelectorAll('[data-answer]').forEach(b=>{delete b.dataset.result;b.removeAttribute('aria-pressed');});
  button.dataset.result=button.dataset.answer;button.setAttribute('aria-pressed','true');
  $('quiz-feedback').textContent=button.dataset.answer==='correct'?'Correct. Atropine blocks muscarinic receptors; it does not reverse Nm-mediated weakness. Pralidoxime can reactivate organophosphate-inhibited AChE before aging. [3, 4]':'Try again. Atropine is a competitive muscarinic receptor antagonist. Which receptor is on skeletal muscle?';
}));
setMode('normal');
