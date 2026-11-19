for (const card of document.querySelectorAll('.card')) {
  const cover = card.querySelector('.card-front');
  const details = card.querySelector('.card-back');
  const revealButton = cover.querySelector('.reveal');
  const returnButton = details.querySelector('.return');
  const detailsHeading = details.querySelector('h2');

  function setFlipped(flipped) {
    cover.inert = flipped;
    details.inert = !flipped;
    revealButton.setAttribute('aria-expanded', String(flipped));
    card.classList.toggle('is-flipped', flipped);

    const focusTarget = flipped ? detailsHeading : revealButton;
    focusTarget.focus();
  }

  details.inert = true;
  revealButton.addEventListener('click', () => setFlipped(true));
  returnButton.addEventListener('click', () => setFlipped(false));
  details.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
      setFlipped(false);
    }
  });
}

document.documentElement.classList.add('flip-ready');
