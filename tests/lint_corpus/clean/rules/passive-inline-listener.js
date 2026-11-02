// Scroll and wheel listeners written inline, each passive: the options
// object follows a handler whose body holds its own parentheses.
window.addEventListener('scroll', function () {
  document.body.classList.toggle('scrolled', window.scrollY > Math.max(0, 8));
}, { passive: true });

const stage = document.querySelector('.stage');
stage.addEventListener('wheel', (event) => { stage.dataset.dir = String(Math.sign(event.deltaY)); }, { passive: true });
