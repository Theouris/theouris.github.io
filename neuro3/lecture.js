const search=document.getElementById('search');
const deck=document.getElementById('deck');
function filter(){
  const term=search.value.trim().toLowerCase();let shown=0;
  document.querySelectorAll('section.slide,section.board').forEach(s=>{
    const match=(!deck.value||s.dataset.deck===deck.value)&&(!term||s.textContent.toLowerCase().includes(term));
    s.hidden=!match;if(match)shown++;
  });
  document.getElementById('search-status').textContent=`${shown} sections shown`;
}
search.addEventListener('input',filter);deck.addEventListener('change',filter);
document.getElementById('images').addEventListener('click',e=>{
  const hide=e.currentTarget.getAttribute('aria-pressed')!=='true';
  document.querySelectorAll('figure').forEach(f=>f.hidden=hide);
  e.currentTarget.setAttribute('aria-pressed',String(hide));e.currentTarget.textContent=hide?'Show all slide images':'Hide slide images';
});
document.querySelectorAll('.toc a').forEach(a=>a.addEventListener('click',()=>{search.value='';deck.value='';filter()}));
filter();
