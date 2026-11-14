import { MODES, MODE_INFO, CALCULATED_KEYS, MAX_COUNT, createProject, createReview, parseProject, boxesFor, calculate, countLabel, addGroupRow, removeGroupRow, validate } from './model.js';
import { buildScene, sceneToSVG, escapeXML } from './diagram.js';
import { downloadBlob, rasterize, canvasToPNG, canvasToPDF } from './export.js';

const $ = id => document.getElementById(id);
const STORAGE_KEY = 'theouris.prisma-flowchart.v1';
let project = createProject();
let undoStack = [], redoStack = [], lastEdit = '', lastEditTime = 0;
let saveTimer, toastTimer, scene, zoom = 1, fitMode = true, format = 'png', exporting = false;
let localStorageAvailable = true;
const measureContext = document.createElement('canvas').getContext('2d');
const measure = (text,size) => { measureContext.font = `${size}px Arial`; return measureContext.measureText(text).width; };
const current = () => project.reviews[project.activeMode];
const clone = value => JSON.parse(JSON.stringify(value));
const escaped = escapeXML;

try { const saved = localStorage.getItem(STORAGE_KEY); if (saved) project = parseProject(saved); }
catch { localStorageAvailable = false; }

function toast(message) {
  clearTimeout(toastTimer); $('toast').textContent = message; $('toast').hidden = false;
  toastTimer = setTimeout(()=>$('toast').hidden=true,4500);
}
function saveStatus(message) { $('save-status').replaceChildren(document.createElement('span'),document.createTextNode(message)); }
function persist(immediate = false) {
  clearTimeout(saveTimer);
  const save = () => {
    try { localStorage.setItem(STORAGE_KEY,JSON.stringify(project)); localStorageAvailable = true; saveStatus('Saved on this device'); }
    catch { localStorageAvailable = false; saveStatus('Use Save project to keep your work'); }
  };
  if (immediate) save(); else { saveStatus('Saving…'); saveTimer = setTimeout(save,350); }
}
function checkpoint(edit = '') {
  const now = Date.now();
  if (!edit || lastEdit !== edit || now-lastEditTime>900) { undoStack.push(clone(project)); if (undoStack.length>60) undoStack.shift(); }
  lastEdit = edit; lastEditTime = now; redoStack = [];
}

function editWording(id) {
  return `<details class="label-editor"><summary>Edit wording</summary><label class="sr-only" for="wording-${id}">${escaped(boxesFor(current())[id]?.title || id)} wording</label><textarea id="wording-${id}" data-text="${id}" maxlength="12000" rows="${Math.min(7,current().texts[id].split('\n').length+1)}" spellcheck="true">${escaped(current().texts[id])}</textarea><p class="field-hint">Keep one <b>(n = )</b> marker per count, in the same order.</p></details>`;
}
function card(id) {
  const review = current(), box = boxesFor(review)[id], result = calculate(review);
  const rows = box.keys.map((key,index)=>{
    const auto = CALCULATED_KEYS.includes(key), isAuto = auto && !(key in review.values), value = result.values[key] ?? '';
    const label = escaped(countLabel(review.texts[id],index));
    return `<div class="count-row"><label class="count-label" for="count-${key}" data-count-label="${key}" data-box="${id}" data-index="${index}">${label}</label><input id="count-${key}" class="count-input${isAuto?' is-auto':''}" data-count="${key}" type="number" min="0" max="${MAX_COUNT}" step="1" inputmode="numeric" value="${value}" placeholder="${auto?'—':'0'}" aria-label="${label} count"${auto?' aria-describedby="auto-help-'+key+'"':''}>${auto?`<button type="button" class="auto-toggle" data-auto="${key}" aria-pressed="${isAuto}" title="${isAuto?'Calculated automatically. Type a value to override.':'Restore the upstream calculation'}">${isAuto?'Auto':'Manual'}</button><span class="sr-only" id="auto-help-${key}">Calculated automatically unless you enter an override. Use Auto to restore the calculation.</span>`:''}${box.add&&box.keys.length>1?`<button type="button" class="remove-reason" data-remove="${id}" data-index="${index}" aria-label="Remove ${label}" title="Remove this ${box.add}">×</button>`:''}</div>`;
  }).join('');
  return `<div class="parameter-card" data-card="${id}"><h3 class="card-title">${escaped(box.title)}</h3>${rows}${box.add?`<button type="button" class="add-reason" data-add="${id}">+ Add ${box.add}</button>`:''}${id==='included'&&review.mode==='systematic'?'<p class="field-hint">Enter unique studies separately: multiple reports may describe one study. The report total is calculated from both routes.</p>':''}${editWording(id)}</div>`;
}
function section(id,number,title,content,open=true) {
  return `<details class="parameter-section" data-section="${id}"${open?' open':''}><summary><span class="section-number">${number}</span><h2>${title}</h2><span class="summary-chevron" aria-hidden="true">⌄</span></summary><div class="section-body">${content}</div></details>`;
}
function textControl(id,label,rows=2) {
  return `<label class="standalone-text">${label}<textarea data-text="${id}" maxlength="12000" rows="${rows}">${escaped(current().texts[id])}</textarea></label>`;
}
function renderSidebar() {
  const previousOpen = new Map([...$('parameters').querySelectorAll('[data-section]')].map(el=>[el.dataset.section,el.open]));
  const review = current(), mode=project.activeMode;
  for (const button of document.querySelectorAll('[data-mode]')) { const active=button.dataset.mode===mode; button.setAttribute('aria-selected',String(active));button.tabIndex=active?0:-1; }
  $('review-panel').setAttribute('aria-labelledby',`tab-${mode}`);
  $('mode-note').textContent=MODE_INFO[mode].note; $('preview-template').textContent=MODE_INFO[mode].short;
  let identification = mode!=='narrative'?`<label class="toggle-row"><input id="show-other" type="checkbox"${review.showOther?' checked':''}> Include the other-methods identification route</label>`:'';
  identification += `<div class="route-heading">${mode==='narrative'?'Literature search':'Databases & registers'}</div>${card('dbSources')}${card('removed')}`;
  if(review.showOther)identification+=`<div class="route-heading other-route">Other methods</div>${card('otherSources')}`;
  let eligibility = `${review.showOther?'<div class="route-heading">Databases & registers</div>':''}${card('sought')}${card('notRetrieved')}${card('assessed')}${card('dbReasons')}`;
  if(review.showOther)eligibility+=`<div class="route-heading other-route">Other methods</div>${card('otherSought')}${card('otherNotRetrieved')}${card('otherAssessed')}${card('otherReasons')}`;
  let labels = textControl('dbHeader','Main route heading');
  if(review.showOther)labels+=textControl('otherHeader','Other-methods heading');
  labels+=textControl('phaseIdentification','Identification phase label',1)+textControl('phaseScreening','Screening phase label',1)+textControl('phaseIncluded','Included phase label',1)+textControl('footnotes','Footnotes & source attribution',7);
  labels+='<label class="font-control">Flowchart text size <input id="font-size" type="number" min="12" max="26" step="1" value="'+review.fontSize+'" aria-label="Flowchart text size in diagram units"></label><p class="field-hint">Boxes expand to fit your wording. The reference colors are preserved.</p>';
  $('parameters').innerHTML = section('identification','01','Identification',identification)+section('screening','02','Screening',card('screened')+card('excluded'))+section('eligibility','03',mode==='narrative'?'Retrieval & relevance':'Retrieval & eligibility',eligibility)+section('included','04','Included',card('included'))+section('labels','Aa','Headings & footnotes',labels,false);
  for(const el of $('parameters').querySelectorAll('[data-section]'))if(previousOpen.has(el.dataset.section))el.open=previousOpen.get(el.dataset.section);
}
function renderPreview() {
  const review=current(),result=calculate(review); scene=buildScene(review,measure);
  $('chart-paper').innerHTML=sceneToSVG(scene,{accessible:true});
  $('canvas-size').textContent=`${scene.width} × ${scene.height} · Original template colors`;
  for(const input of document.querySelectorAll('[data-count]')) {
    const key=input.dataset.count; if(document.activeElement!==input)input.value=result.values[key]??'';
    input.classList.toggle('is-auto',CALCULATED_KEYS.includes(key)&&!(key in review.values));
  }
  for(const button of document.querySelectorAll('[data-auto]')) {
    const auto=!(button.dataset.auto in review.values);button.setAttribute('aria-pressed',String(auto));button.textContent=auto?'Auto':'Manual';
    button.title=auto?'Calculated automatically. Type a value to override.':'Restore the upstream calculation';
  }
  for(const label of document.querySelectorAll('[data-count-label]')) { const text=countLabel(review.texts[label.dataset.box],Number(label.dataset.index));label.textContent=text;$(label.htmlFor).setAttribute('aria-label',`${text} count`); }
  const notices=validate(review,result);$('validation').hidden=!notices.length;
  $('validation-summary').textContent=`${notices.length} ${notices.length===1?'count or wording note':'count & wording notes'} to review`;
  $('validation-list').replaceChildren(...notices.map(notice=>{const li=document.createElement('li');li.textContent=notice.text;return li;}));
  $('undo').disabled=!undoStack.length;$('redo').disabled=!redoStack.length;resizePaper();updateDimensions();
}
function changed(rebuild=false) { if(rebuild)renderSidebar();renderPreview();persist(); }
function resizePaper() {
  if(!scene)return;
  const viewport=$('preview-viewport'),padding=window.innerWidth<=760?20:38;
  if(fitMode)zoom=Math.max(.08,Math.min(1,(viewport.clientWidth-padding*2)/scene.width,(viewport.clientHeight-padding*2)/scene.height));
  const width=Math.round(scene.width*zoom),height=Math.round(scene.height*zoom);
  $('chart-paper').style.width=width+'px';$('chart-paper').style.height=height+'px';
  $('chart-paper').firstElementChild.style.width='100%';$('chart-paper').firstElementChild.style.height='100%';
  $('chart-stage').style.width=Math.max(width,viewport.clientWidth-padding*2)+'px';$('chart-stage').style.height=Math.max(height,viewport.clientHeight-padding*2)+'px';
  $('zoom-label').value=`${Math.round(zoom*100)}%`;$('zoom-out').disabled=zoom<=.1001;$('zoom-in').disabled=zoom>=3;
}
function setZoom(next,anchor) {
  const viewport=$('preview-viewport'),rect=$('chart-paper').getBoundingClientRect(),previous=zoom;
  const center=anchor||{x:viewport.getBoundingClientRect().left+viewport.clientWidth/2,y:viewport.getBoundingClientRect().top+viewport.clientHeight/2};
  zoom=Math.max(.1,Math.min(3,next));fitMode=false;resizePaper();const newRect=$('chart-paper').getBoundingClientRect();
  viewport.scrollLeft+=newRect.left+(center.x-rect.left)*zoom/previous-center.x;viewport.scrollTop+=newRect.top+(center.y-rect.top)*zoom/previous-center.y;
}
function updateDimensions(from='width') {
  if(!scene)return;const ratio=scene.width/scene.height;
  if(from==='height') { if($('export-height').value)$('export-width').value=Math.round(Number($('export-height').value)*ratio); }
  else if($('export-width').value)$('export-height').value=Math.round(Number($('export-width').value)/ratio);
  const width=Number($('export-width').value),height=Number($('export-height').value),dpi=Number($('export-dpi').value);
  $('export-info').textContent=format==='svg'?'Resolution-independent vector. Canvas size is in pixels; DPI is recorded in metadata.':`${dpi>0?(width/dpi).toFixed(2):'—'} × ${dpi>0?(height/dpi).toFixed(2):'—'} inches at ${dpi||'—'} DPI. Aspect ratio is preserved.${format==='pdf'?' PDF embeds a lossless image.':''}`;
}
function undoRedo(redo=false) {
  const source=redo?redoStack:undoStack,target=redo?undoStack:redoStack;if(!source.length)return;
  target.push(clone(project));project=source.pop();lastEdit='';renderSidebar();renderPreview();persist();
}

$('parameters').addEventListener('input',event=>{
  const input=event.target,review=current();
  if(input.matches('[data-count]')) {
    const key=input.dataset.count;input.setCustomValidity('');if(input.validity.badInput)return;
    if(input.value!==''&&(!Number.isSafeInteger(Number(input.value))||Number(input.value)<0||Number(input.value)>MAX_COUNT)) { input.setCustomValidity(`Enter a whole number from 0 to ${MAX_COUNT}.`);input.reportValidity();return; }
    checkpoint('count-'+key);if(input.value==='')delete review.values[key];else review.values[key]=Number(input.value);changed();
  } else if(input.matches('[data-text]')) { checkpoint('text-'+input.dataset.text);review.texts[input.dataset.text]=input.value;changed(); }
  else if(input.id==='font-size') { if(!input.checkValidity()||!input.value)return;checkpoint('font');review.fontSize=Number(input.value);changed(); }
});
$('parameters').addEventListener('focusout',event=>{ const input=event.target;if(input.matches('[data-count]')&&input.checkValidity())input.value=calculate(current()).values[input.dataset.count]??''; });
$('parameters').addEventListener('change',event=>{ if(event.target.id==='show-other') {checkpoint();current().showOther=event.target.checked;fitMode=true;changed(true);} });
$('parameters').addEventListener('click',event=>{
  const button=event.target.closest('button');if(!button)return;
  if(button.dataset.auto) {checkpoint();delete current().values[button.dataset.auto];changed();}
  if(button.dataset.add) {checkpoint();if(addGroupRow(current(),button.dataset.add))changed(true);else toast('A box can contain up to 40 rows.');}
  if(button.dataset.remove) {checkpoint();removeGroupRow(current(),button.dataset.remove,Number(button.dataset.index));changed(true);}
});
for(const button of document.querySelectorAll('[data-mode]'))button.addEventListener('click',()=>{ if(project.activeMode===button.dataset.mode)return;checkpoint();project.activeMode=button.dataset.mode;fitMode=true;changed(true); });
document.querySelector('.review-toggle').addEventListener('keydown',event=>{
  if(!['ArrowLeft','ArrowRight','Home','End'].includes(event.key))return;event.preventDefault();let index=MODES.indexOf(project.activeMode);
  index=event.key==='Home'?0:event.key==='End'?2:(index+(event.key==='ArrowRight'?1:2))%3;const tab=$('tab-'+MODES[index]);tab.click();tab.focus();
});
$('zoom-in').addEventListener('click',()=>setZoom(zoom*1.25));$('zoom-out').addEventListener('click',()=>setZoom(zoom/1.25));
$('zoom-fit').addEventListener('click',()=>{fitMode=true;resizePaper();$('preview-viewport').scrollTo(0,0);});
$('preview-viewport').addEventListener('wheel',event=>{ if(!event.ctrlKey&&!event.metaKey)return;event.preventDefault();setZoom(zoom*Math.exp(-event.deltaY*.003),{x:event.clientX,y:event.clientY}); },{passive:false});
new ResizeObserver(()=>resizePaper()).observe($('preview-viewport'));
$('undo').addEventListener('click',()=>undoRedo());$('redo').addEventListener('click',()=>undoRedo(true));
document.addEventListener('keydown',event=>{ if(event.target.matches('input,textarea')||!(event.ctrlKey||event.metaKey))return;if(event.key.toLowerCase()==='z') {event.preventDefault();undoRedo(event.shiftKey);} });
for(const button of document.querySelectorAll('[data-format]'))button.addEventListener('click',()=>{format=button.dataset.format;document.querySelectorAll('[data-format]').forEach(el=>el.setAttribute('aria-pressed',String(el===button)));$('export-button').querySelector('span').textContent=`Download ${format.toUpperCase()}`;updateDimensions();});
$('export-width').addEventListener('input',()=>updateDimensions('width'));$('export-height').addEventListener('input',()=>updateDimensions('height'));$('export-dpi').addEventListener('input',()=>updateDimensions());
function filename() { return ($('filename').value.trim().replace(/[<>:"/\\|?*\u0000-\u001f]/g,'-').replace(/\.(png|svg|pdf|json)$/i,'').replace(/[. ]+$/g,'')||'prisma-flowchart'); }
$('save-project').addEventListener('click',()=>{downloadBlob(new Blob([JSON.stringify(project,null,2)],{type:'application/json'}),filename()+'.json');persist(true);toast('Project saved with all three review drafts.');});
$('open-project').addEventListener('click',()=>$('project-file').click());
$('project-file').addEventListener('change',async()=>{
  const file=$('project-file').files[0];if(!file)return;
  try {if(file.size>2_000_000)throw new Error('Choose a project smaller than 2 MB.');const opened=parseProject(await file.text());checkpoint();project=opened;fitMode=true;changed(true);toast('Project opened.');}
  catch(error) {toast(error.message||'The project could not be opened.');}finally {$('project-file').value='';}
});
$('reset-project').addEventListener('click',()=>{$('reset-dialog').returnValue='cancel';$('reset-dialog').showModal();});
$('reset-dialog').addEventListener('close',()=>{if($('reset-dialog').returnValue!=='reset')return;checkpoint();project.reviews[project.activeMode]=createReview(project.activeMode);fitMode=true;changed(true);toast('Current review reset. Undo is available.');});
$('export-button').addEventListener('click',async()=>{
  if(exporting)return;$('export-error').textContent='';
  const invalidInput=document.querySelector('#parameters input:invalid');if(invalidInput) {invalidInput.reportValidity();invalidInput.focus();return;}
  for(const id of ['export-width','export-height','export-dpi'])if(!$(id).value||!$(id).checkValidity()) {$(id).reportValidity();$(id).focus();return;}
  const errors=validate(current()).filter(n=>n.level==='error');if(errors.length) {$('validation').open=true;$('export-error').textContent='Resolve the negative counts before exporting.';return;}
  const width=Number($('export-width').value),height=Number($('export-height').value),dpi=Number($('export-dpi').value);
  if(!Number.isInteger(width)||!Number.isInteger(height)||!Number.isInteger(dpi)) {$('export-error').textContent='Use whole numbers for pixel dimensions and DPI.';return;}
  const exportFormat=format,exportScene=scene,exportName=filename();exporting=true;$('export-button').disabled=true;$('export-button').querySelector('span').textContent='Preparing download…';
  try {
    const svg=sceneToSVG(exportScene,{width,height,dpi});let blob;
    if(exportFormat==='svg')blob=new Blob([svg],{type:'image/svg+xml;charset=utf-8'});
    else {await new Promise(resolve=>requestAnimationFrame(resolve));const canvas=await rasterize(svg,width,height);try {blob=exportFormat==='png'?await canvasToPNG(canvas,dpi):await canvasToPDF(canvas,dpi);}finally {canvas.width=1;canvas.height=1;}}
    downloadBlob(blob,exportName+'.'+exportFormat);toast(`${exportFormat.toUpperCase()} exported · ${width} × ${height} px${exportFormat==='svg'?'':` · ${dpi} DPI`}`);
  } catch(error) {$('export-error').textContent=error.message||'Export failed. Try a smaller image.';}
  finally {exporting=false;$('export-button').disabled=false;$('export-button').querySelector('span').textContent=`Download ${format.toUpperCase()}`;}
});
window.addEventListener('pagehide',()=>persist(true));renderSidebar();renderPreview();if(!localStorageAvailable)saveStatus('Use Save project to keep your work');
