const slides = [...document.querySelectorAll('.slide')];
const dots = document.getElementById('dots');
const counter = document.getElementById('counter');
const progressBar = document.getElementById('progressBar');
const prev = document.getElementById('prev');
const next = document.getElementById('next');
let current = 0;

slides.forEach((slide, index) => {
  const button = document.createElement('button');
  button.className = 'dot-button';
  button.setAttribute('aria-label', `Go to ${slide.dataset.title}`);
  button.addEventListener('click', () => goTo(index));
  dots.appendChild(button);
});

function goTo(index) {
  const target = Math.max(0, Math.min(slides.length - 1, index));
  slides.forEach((slide, i) => {
    slide.classList.toggle('is-active', i === target);
    slide.classList.toggle('was-active', i < target);
    slide.setAttribute('aria-hidden', i === target ? 'false' : 'true');
    slide.inert = i !== target;
    if (i === target) slide.scrollTop = 0;
  });
  current = target;
  [...dots.children].forEach((dot, i) => dot.classList.toggle('active', i === current));
  counter.textContent = `${String(current + 1).padStart(2, '0')} / ${String(slides.length).padStart(2, '0')}`;
  progressBar.style.width = `${((current + 1) / slides.length) * 100}%`;
  prev.disabled = current === 0;
  next.disabled = current === slides.length - 1;
  document.title = `${slides[current].dataset.title} · Lymphoma decoded`;
}

prev.addEventListener('click', () => goTo(current - 1));
next.addEventListener('click', () => goTo(current + 1));
document.querySelectorAll('[data-next]').forEach(button => button.addEventListener('click', () => goTo(current + 1)));
document.getElementById('restart').addEventListener('click', () => goTo(0));

document.addEventListener('keydown', event => {
  if (document.getElementById('sourcesDialog').open) return;
  const interactive = event.target.matches('select, input, textarea, button, a');
  if (interactive && [' ', 'ArrowLeft', 'ArrowRight'].includes(event.key)) return;
  if (event.key === 'ArrowRight' || event.key === 'PageDown' || event.key === ' ') goTo(current + 1);
  if (event.key === 'ArrowLeft' || event.key === 'PageUp') goTo(current - 1);
  if (event.key === 'Home') goTo(0);
  if (event.key === 'End') goTo(slides.length - 1);
});

let touchStart = 0;
let touchInControl = false;
document.addEventListener('touchstart', event => {
  touchStart = event.changedTouches[0].clientX;
  touchInControl = Boolean(event.target.closest('.table-wrap, select, button, a'));
}, {passive:true});
document.addEventListener('touchend', event => {
  if (touchInControl) return;
  const distance = event.changedTouches[0].clientX - touchStart;
  if (Math.abs(distance) > 70) goTo(current + (distance < 0 ? 1 : -1));
}, {passive:true});

document.querySelectorAll('.choice').forEach(button => {
  button.addEventListener('click', () => {
    const group = button.closest('.decision-card, .age-card');
    group.querySelectorAll('.choice').forEach(choice => choice.classList.remove('correct', 'incorrect'));
    const right = button.dataset.answer === 'right';
    button.classList.add(right ? 'correct' : 'incorrect');
    const feedback = group.querySelector('.feedback');
    feedback.textContent = right
      ? (group.classList.contains('age-card') ? 'Correct—the two incidence peaks are a classic clue.' : 'Correct. That finding redirects the differential toward a myeloid neoplasm.')
      : (group.classList.contains('age-card') ? 'Try again: think two peaks, decades apart.' : 'Important clue, but it does not specifically identify the malignant lineage.');
  });
});

function wireChallenge(tableSelector, scoreId, revealId) {
  const fields = [...document.querySelectorAll(`${tableSelector} select`)];
  const score = document.getElementById(scoreId);
  const update = () => {
    let correct = 0;
    fields.forEach(field => {
      field.classList.remove('correct', 'incorrect');
      if (!field.value) return;
      const right = field.value === field.dataset.correct;
      field.classList.add(right ? 'correct' : 'incorrect');
      if (right) correct++;
    });
    score.textContent = `${correct} / ${fields.length} correct`;
  };
  fields.forEach(field => field.addEventListener('change', update));
  document.getElementById(revealId).addEventListener('click', () => {
    fields.forEach(field => field.value = field.dataset.correct);
    update();
  });
}

wireChallenge('#hlTable', 'hlScore', 'revealHl');
wireChallenge('.nhl-table', 'nhlScore', 'revealNhl');

const dialog = document.getElementById('sourcesDialog');
const openSources = () => dialog.showModal();
document.getElementById('openSources').addEventListener('click', openSources);
document.getElementById('openSourcesFinal').addEventListener('click', openSources);
document.getElementById('closeSources').addEventListener('click', () => dialog.close());
dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });

goTo(0);
