(() => {
  'use strict';
  const menu = document.querySelector('.navigation');
  const toggle = menu?.querySelector('summary');
  function closeMenu(restoreFocus = false) {
    if (!menu) return;
    menu.open = false;
    if (restoreFocus) toggle?.focus();
  }
  menu?.addEventListener('toggle', () => toggle?.setAttribute('aria-expanded', String(menu.open)));
  toggle?.setAttribute('aria-expanded', 'false');
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menu?.open) closeMenu(true);
  });
  document.addEventListener('click', event => {
    if (!(event.target instanceof Element)) return;
    if (menu?.open && (!menu.contains(event.target) || event.target.closest('a'))) closeMenu();
  });
  function filterPublications(year = 'all') {
    const items = [...document.querySelectorAll('.publication[data-year]')];
    items.forEach(item => { item.hidden = year !== 'all' && item.dataset.year !== year; });
    const count = document.getElementById('publication-count');
    if (count) count.textContent = `${items.filter(item => !item.hidden).length} publications`;
  }
  document.addEventListener('change', event => {
    if (event.target instanceof HTMLSelectElement && event.target.id === 'paper-year') filterPublications(event.target.value);
  });
  function reveal(id) {
    if (!id) return;
    const target = document.getElementById(id);
    if (!target) return;
    const details = target.closest('details.resume-section');
    if (details) details.open = true;
    if (target.classList.contains('publication')) {
      filterPublications('all');
      const select = document.getElementById('paper-year');
      if (select) select.value = 'all';
    }
    requestAnimationFrame(() => target.scrollIntoView({block: 'start'}));
  }
  function nativeHash() {
    if (location.hash.startsWith('#/')) return;
    try { reveal(decodeURIComponent(location.hash.slice(1))); } catch { /* Invalid URL fragment. */ }
  }
  window.addEventListener('hashchange', nativeHash);
  nativeHash();
  window.siteReveal = reveal;
  async function checkFont() {
    try {
      const faces = await Promise.race([
        document.fonts.load('300 50px "Manrope"'),
        new Promise((_, reject) => setTimeout(() => reject(new Error('font timeout')), 12000))
      ]);
      document.documentElement.dataset.fontStatus = faces.some(face => face.status === 'loaded') ? 'loaded' : 'fallback';
    } catch { document.documentElement.dataset.fontStatus = 'fallback'; }
    const warning = document.getElementById('preview-font-warning');
    if (warning) warning.hidden = document.documentElement.dataset.fontStatus === 'loaded';
  }
  if (document.fonts) checkFont();
  let printState = [];
  window.addEventListener('beforeprint', () => {
    printState = [...document.querySelectorAll('.resume-section')].map(el => [el, el.open]);
    printState.forEach(([el]) => { el.open = true; });
  });
  window.addEventListener('afterprint', () => printState.forEach(([el, state]) => { el.open = state; }));
})();
