/* Static game: no account, service, or build step required. */
'use strict';
const diagrams = {
  willis: { title: 'Circle of Willis & brainstem', image: 'assets/circle-of-willis.png', w:1792, h:1388,
    masks:[[15,388,431,45],[15,445,328,42],[15,493,304,44],[15,581,447,47],[15,635,345,44],[1443,585,349,575]],
    points:[
      ['Anterior communicating artery',390,410],['Anterior cerebral artery',295,465],['Internal carotid artery',267,516],
      ['Posterior communicating artery',407,606],['Posterior cerebral artery',310,656],['Middle cerebral artery',1480,612],
      ['Superior cerebellar artery',1480,675],['Pontine arteries',1480,736],['Basilar artery',1480,799],
      ['Anterior inferior cerebellar artery',1480,860],['Vertebral artery',1480,960],
      ['Posterior inferior cerebellar artery',1480,1022],['Anterior spinal artery',1480,1122]] },
  cerebellar: { title:'Cerebellar & vertebrobasilar arteries', image:'assets/cerebellar-arteries.png', w:430,h:379,
    masks:[[0,14,70,43],[0,70,70,42],[0,128,55,32],[0,184,72,35],[0,227,85,20],[0,258,103,34],[65,320,59,32],[331,267,99,34],[301,315,129,36]],
    points:[['Posterior cerebral arteries',44,36],['Superior cerebellar artery',38,91],['Pontine arteries',28,144],
      ['Labyrinthine artery',40,203],['Basilar artery',46,237],['Anterior inferior cerebellar artery',50,278],
      ['Vertebral arteries',94,339],['Posterior inferior cerebellar artery',383,284],['Posterior meningeal branch',367,335]] }
};
const territories = [
  {id:'aca',artery:'Anterior cerebral artery (ACA)',region:'Medial frontal and parietal cortex, including the paracentral lobule.',function:'Movement and sensation of the opposite leg; medial frontal circuits support initiation and bladder control.',deficit:'Opposite leg weakness and sensory loss greater than face/arm involvement; abulia or urinary incontinence may occur.'},
  {id:'mca',artery:'Middle cerebral artery (MCA)',region:'Lateral frontal, parietal, and temporal cortex.',function:'Movement and sensation of the opposite face and arm; dominant-side language and nondominant-side spatial attention.',deficit:'Opposite face/arm weakness and sensory loss greater than leg involvement; aphasia on the dominant side or neglect on the nondominant side.'},
  {id:'pca',artery:'Posterior cerebral artery (PCA)',region:'Occipital cortex and inferomedial temporal regions; deep branches also supply thalamus and midbrain.',function:'Visual processing in the opposite visual field; medial temporal structures contribute to memory.',deficit:'Opposite homonymous visual-field loss, sometimes with macular sparing; a dominant occipital-plus-splenial lesion can cause alexia without agraphia.'},
  {id:'pica',artery:'PICA / vertebral artery',region:'Lateral medulla and inferior cerebellum (classic lateral medullary localization).',function:'Swallowing and voice through nucleus ambiguus; balance, facial pain/temperature, and body pain/temperature pathways.',deficit:'Dysphagia and hoarseness with vertigo/ataxia; same-side facial and opposite-body pain/temperature loss, often with same-side Horner syndrome.'},
  {id:'aica',artery:'Anterior inferior cerebellar artery (AICA)',region:'Lateral caudal pons and anterior inferior cerebellum; inner ear usually via the labyrinthine branch.',function:'Facial movement, hearing, balance, and coordination through lateral pontine and inner-ear structures.',deficit:'Same-side peripheral facial weakness, vertigo and ataxia, often hearing loss; crossed facial/body pain-temperature deficits may occur.'},
  {id:'sca',artery:'Superior cerebellar artery (SCA)',region:'Superior cerebellum and much of the superior cerebellar peduncle.',function:'Coordination of limb movements, gait, and motor output from the cerebellum.',deficit:'Prominent same-side limb and gait ataxia with dysmetria and possible dysarthria; classic swallowing/voice or facial-paralysis signs are less typical.'},
  {id:'basilar',artery:'Basilar artery / pontine branches',region:'Pons; bilateral ventral pontine injury is the classic locked-in localization.',function:'Descending motor commands to limbs and cranial muscles pass through the ventral pons.',deficit:'Severe bilateral ventral pontine infarction can cause quadriplegia and anarthria with preserved consciousness and vertical eye movements (locked-in syndrome).'},
  {id:'asa',artery:'Anterior spinal artery / vertebral paramedian branches',region:'Medial medulla (this round tests medullary rather than spinal cord localization).',function:'Corticospinal motor output, medial-lemniscus vibration/position sensation, and hypoglossal tongue movement.',deficit:'Opposite-body weakness and vibration/position loss with same-side tongue weakness; the tongue deviates toward the lesion on protrusion.'}
];
const $ = selector => document.querySelector(selector);
let mode='willis', items=[], solved=new Set(), missed=new Set(), attempts=0, selected=null, started=null, elapsed=0, review=false, filter='function', activeSubset=null, territoryOrder=[];
const shuffle = array => { const result=[...array]; for(let i=result.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[result[i],result[j]]=[result[j],result[i]];}return result; };
const formatTime = seconds => `${String(Math.floor(seconds/60)).padStart(2,'0')}:${String(seconds%60).padStart(2,'0')}`;
function seconds(){return elapsed+(started===null?0:Math.floor((Date.now()-started)/1000));}
function stopTimer(){elapsed=seconds();started=null;}
function say(message,kind=''){ $('#feedback').textContent=message;$('#feedback').dataset.kind=kind; }
function getBest(){try{return JSON.parse(localStorage.getItem(`neuro-best-${mode}`));}catch{return null;}}
function stats(){
  $('#progress').textContent=`${solved.size} / ${items.length}`;
  $('#accuracy').textContent=attempts?`${Math.round(solved.size/attempts*100)}%`:'—';
  $('#time').textContent=formatTime(seconds());
  const best=getBest();$('#best').textContent=best?`Best: ${best.accuracy}% · ${formatTime(best.time)}`:'Your best round is saved on this device.';
}
function setup(subset=null){
  started=null;elapsed=0;attempts=0;solved=new Set();missed=new Set();selected=null;review=false;activeSubset=subset;
  items=mode==='territories'?territories.flatMap(t=>['function','deficit'].map(type=>({id:`${t.id}-${type}`,label:t[type],type,territory:t.id}))):diagrams[mode].points.map(([label,x,y],i)=>({id:`point-${i}`,label,x,y,number:i+1}));
  if(subset)items=items.filter(item=>subset.includes(item.id));
  items=shuffle(items);filter='function';territoryOrder=shuffle(territories);
  $('#game-title').textContent=mode==='territories'?'Territory → function → deficit':diagrams[mode].title;
  $('#game-type').textContent=mode==='territories'?'CLINICAL MATCHING':'DIAGRAM CHALLENGE';
  $('#instructions').textContent=mode==='territories'?'Match each artery’s territory with its normal function and characteristic injury pattern. Drag a card into a slot, or select a card and tap a slot. Switch between Functions and Deficits in the card bank.':'Drag an artery label onto its numbered marker. Each marker replaces a printed label; follow its original leader line to the vessel. You can also select a label, then tap a marker.';
  $('#reveal').textContent='Study answers';$('#retry').hidden=true;$('#summary').hidden=true;
  render();stats();say(subset?'Practice round: only your missed or unfinished matches.':'Ready when you are. The timer starts with your first match.');
}
function element(tag,className,text){const e=document.createElement(tag);if(className)e.className=className;if(text)e.textContent=text;return e;}
function render(){
  const area=$('#play-area');area.replaceChildren();
  const layout=element('div',mode==='territories'?'territory-layout':'diagram-layout');area.append(layout);
  if(mode==='territories')renderTerritories(layout);else renderDiagram(layout);
  renderBank(layout);
}
function renderDiagram(layout){
  const d=diagrams[mode], scroll=element('div','diagram-scroll'), stage=element('div',`diagram ${mode}`);scroll.append(stage);layout.append(scroll);
  const ns='http://www.w3.org/2000/svg',svg=document.createElementNS(ns,'svg');svg.setAttribute('viewBox',`0 0 ${d.w} ${d.h}`);svg.setAttribute('role','img');svg.setAttribute('aria-label',d.title+'; numbered markers correspond to original label leader lines.');
  const image=document.createElementNS(ns,'image');image.setAttribute('href',d.image);image.setAttribute('width',d.w);image.setAttribute('height',d.h);svg.append(image);
  if(!review)d.masks.forEach(([x,y,w,h])=>{const rect=document.createElementNS(ns,'rect');Object.entries({x,y,width:w,height:h,fill:'white'}).forEach(([key,val])=>rect.setAttribute(key,val));svg.append(rect);});
  stage.append(svg);
  if(!review)items.forEach(item=>{const button=element('button',`target${solved.has(item.id)?' solved':''}`,solved.has(item.id)?'✓':String(item.number));button.style.left=`${item.x/d.w*100}%`;button.style.top=`${item.y/d.h*100}%`;button.dataset.target=item.id;button.setAttribute('aria-label',solved.has(item.id)?`Marker ${item.number}: ${item.label}, matched`:`Marker ${item.number}`);button.title=solved.has(item.id)?item.label:`Marker ${item.number}`;button.disabled=solved.has(item.id);bindTarget(button,item.id);stage.append(button);});
}
function renderTerritories(layout){
  const grid=element('div','territory-grid');layout.append(grid);
  territoryOrder.filter(t=>items.some(i=>i.territory===t.id)).forEach(t=>{
    const block=element('article','territory');block.append(element('h3','',t.artery),element('p','',t.region));const slots=element('div','slots');block.append(slots);
    ['function','deficit'].forEach(type=>{const id=`${t.id}-${type}`,item=items.find(i=>i.id===id);if(!item)return;
      const button=element('button',`slot${solved.has(id)||review?' solved':''}`);button.dataset.target=id;button.append(element('small','',type==='function'?'NORMAL FUNCTION':'INJURY PATTERN'),document.createTextNode(solved.has(id)||review?item.label:`Drop a ${type==='function'?'function':'deficit'} card here`));button.disabled=solved.has(id)||review;button.setAttribute('aria-label',`${t.artery}: ${type}. ${solved.has(id)||review?item.label:'Unmatched'}`);bindTarget(button,id);slots.append(button);
    });grid.append(block);
  });
}
function renderBank(layout){
  const wrap=element('aside','bank-wrap');layout.append(wrap);wrap.append(element('h3','',review?'Answer key':'Your label bank'),element('p','',review?'Start a new round to test your recall.':'Select a card, then choose its destination.'));
  if(review){const list=element('ol','answer-list');if(mode!=='territories')diagrams[mode].points.forEach(([label])=>list.append(element('li','',label)));else list.append(element('li','','Read the completed territory cards for each association.'));wrap.append(list);return;}
  if(mode==='territories'){const filters=element('div','filter');['function','deficit'].forEach(type=>{const b=element('button','',type==='function'?'Functions':'Deficits');b.setAttribute('aria-pressed',String(filter===type));b.addEventListener('click',()=>{filter=type;selected=null;render();});filters.append(b);});wrap.append(filters);}
  const bank=element('div','bank');wrap.append(bank);
  const available=items.filter(i=>!solved.has(i.id)&&(mode!=='territories'||i.type===filter));
  if(!available.length)bank.append(element('p','empty',mode==='territories'?'All cards in this category matched. Try the other category.':'All labels matched.'));
  available.forEach(item=>{const card=element('button',`card${selected===item.id?' selected':''}`,item.label);card.dataset.card=item.id;card.draggable=true;card.setAttribute('aria-pressed',String(selected===item.id));
    card.addEventListener('click',()=>select(item.id));card.addEventListener('dragstart',event=>{selected=item.id;event.dataTransfer.setData('text/plain',item.id);event.dataTransfer.effectAllowed='move';});bindTouch(card,item);bank.append(card);
  });
}
function select(id){selected=selected===id?null:id;document.querySelectorAll('[data-card]').forEach(card=>{card.classList.toggle('selected',card.dataset.card===selected);card.setAttribute('aria-pressed',String(card.dataset.card===selected));});if(selected)say('Card selected. Choose a numbered marker or a matching slot.');}
function bindTarget(target,id){target.addEventListener('click',()=>{if(selected)match(selected,id);else say('Select a card from the label bank first.');});target.addEventListener('dragover',event=>{if(!target.disabled){event.preventDefault();target.classList.add('over');event.dataTransfer.dropEffect='move';}});target.addEventListener('dragleave',()=>target.classList.remove('over'));target.addEventListener('drop',event=>{event.preventDefault();target.classList.remove('over');match(event.dataTransfer.getData('text/plain'),id);});}
function bindTouch(card,item){
  let origin=null,ghost=null;
  card.addEventListener('pointerdown',event=>{if(event.pointerType==='mouse')return;origin={x:event.clientX,y:event.clientY,pointer:event.pointerId};});
  card.addEventListener('pointermove',event=>{if(!origin)return;if(!ghost&&Math.hypot(event.clientX-origin.x,event.clientY-origin.y)>12){ghost=element('div','drag-ghost',item.label);document.body.append(ghost);card.setPointerCapture(event.pointerId);}if(ghost){ghost.style.left=`${event.clientX+12}px`;ghost.style.top=`${event.clientY+12}px`;}});
  const finish=event=>{if(ghost){ghost.remove();ghost=null;if(event.type==='pointerup'){const target=document.elementFromPoint(event.clientX,event.clientY)?.closest('[data-target]');if(target)match(item.id,target.dataset.target);}}origin=null;};
  card.addEventListener('pointerup',finish);card.addEventListener('pointercancel',finish);
}
function match(cardId,targetId){
  if(review||solved.has(targetId)||solved.has(cardId)||!items.some(i=>i.id===cardId)||!items.some(i=>i.id===targetId))return;
  if(started===null)started=Date.now();attempts++;
  if(cardId!==targetId){missed.add(targetId);stats();say('Not quite. Follow the leader line or reconsider the territory and try again.','wrong');return;}
  solved.add(targetId);selected=null;const item=items.find(i=>i.id===targetId);render();stats();say(`Correct! ${mode==='territories'?'Association matched.':item.label}`, 'correct');
  if(solved.size===items.length)complete();
}
function complete(){
  stopTimer();stats();const accuracy=Math.round(solved.size/attempts*100),best=getBest();
  if(!activeSubset&&(!best||accuracy>best.accuracy||(accuracy===best.accuracy&&seconds()<best.time))){try{localStorage.setItem(`neuro-best-${mode}`,JSON.stringify({accuracy,time:seconds()}));}catch{ /* Storage may be disabled. Gameplay still works. */ }}
  stats();say(`Round complete! ${accuracy}% accuracy in ${formatTime(seconds())}.`,'correct');
  const summary=$('#summary');summary.hidden=false;summary.replaceChildren(element('h3','','Nice work. Follow the flow again.'),element('p','',`${items.length} matches · ${attempts-items.length} incorrect attempts · ${missed.size} targets to revisit.`));$('#retry').hidden=!missed.size;
  if(missed.size){const list=element('ul','answer-list');items.filter(i=>missed.has(i.id)).forEach(i=>list.append(element('li','',mode==='territories'?`${territories.find(t=>t.id===i.territory).artery}: ${i.label}`:`Marker ${i.number}: ${i.label}`)));summary.append(list);}
}
document.querySelectorAll('[data-mode]').forEach(button=>button.addEventListener('click',()=>{mode=button.dataset.mode;document.querySelectorAll('[data-mode]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));setup();}));
$('#restart').addEventListener('click',()=>setup());
$('#retry').addEventListener('click',()=>{const ids=items.filter(i=>missed.has(i.id)||!solved.has(i.id)).map(i=>i.id);if(ids.length)setup(ids);});
$('#reveal').addEventListener('click',()=>{if(review){setup();return;}stopTimer();review=true;selected=null;$('#reveal').textContent='Back to quiz';$('#retry').hidden=!items.some(i=>missed.has(i.id)||!solved.has(i.id));$('#summary').hidden=true;render();say('Study mode: answers revealed. This round will not be saved as a best score. Start again or retry your unfinished matches.');});
setInterval(()=>{$('#time').textContent=formatTime(seconds());},500);
setup();
