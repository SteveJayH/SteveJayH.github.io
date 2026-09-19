(() => {
  'use strict';

  // Native details elements keep the menu and CV usable without JavaScript.
  const menu = document.querySelector('.navigation');
  const toggle = menu?.querySelector('summary');
  menu?.addEventListener('toggle', () => {
    toggle?.setAttribute('aria-expanded', String(menu.open));
  });
  toggle?.setAttribute('aria-expanded', String(Boolean(menu?.open)));

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && menu?.open) {
      menu.open = false;
      toggle?.focus();
    }
  });

  document.addEventListener('click', (event) => {
    if (!(event.target instanceof Element)) return;
    if (menu?.open && !menu.contains(event.target)) menu.open = false;
    const anchor = event.target.closest('a[href]');
    if (anchor && menu?.contains(anchor)) menu.open = false;
  });

  function revealSection() {
    const hash = location.hash.slice(1);
    if (!hash) return;
    let id;
    try { id = decodeURIComponent(hash); } catch { return; }
    const target = document.getElementById(id);
    const section = target?.closest('details.resume-section');
    if (section) {
      section.open = true;
      requestAnimationFrame(() => section.scrollIntoView({ block: 'start' }));
    }
  }
  window.addEventListener('hashchange', revealSection);
  revealSection();

  let printState = [];
  window.addEventListener('beforeprint', () => {
    printState = [...document.querySelectorAll('.resume-section')].map(el => [el, el.open]);
    printState.forEach(([el]) => { el.open = true; });
  });
  window.addEventListener('afterprint', () => {
    printState.forEach(([el, open]) => { el.open = open; });
  });
})();
