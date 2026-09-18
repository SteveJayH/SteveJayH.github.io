/* Progressive enhancement: content remains readable without JavaScript. */
(() => {
  'use strict';
  document.documentElement.classList.add('js');
  const toggle = document.querySelector('.menu-toggle');
  const nav = document.querySelector('.site-nav');
  function closeMenu(returnFocus = false) {
    if (!toggle || !nav) return;
    toggle.setAttribute('aria-expanded', 'false');
    nav.classList.remove('is-open');
    if (returnFocus) toggle.focus();
  }
  if (toggle && nav) {
    toggle.addEventListener('click', () => {
      const open = toggle.getAttribute('aria-expanded') !== 'true';
      toggle.setAttribute('aria-expanded', String(open));
      nav.classList.toggle('is-open', open);
    });
    nav.querySelectorAll('a').forEach(a => a.addEventListener('click', () => closeMenu()));
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape' && nav.classList.contains('is-open')) closeMenu(true);
    });
    document.addEventListener('click', e => {
      if (!e.target.closest('.site-header')) closeMenu();
    });
    window.matchMedia('(min-width: 801px)').addEventListener('change', () => closeMenu());
  }
  // Preserve a usable layout when a portrait cannot be loaded.
  document.querySelectorAll('img[data-fallback]').forEach(img => {
    function fallback() {
      if (img.dataset.retried) { img.hidden = true; return; }
      img.dataset.retried = 'true';
      img.src = img.dataset.fallback;
    }
    img.addEventListener('error', fallback);
    if (img.complete && !img.naturalWidth) fallback();
  });
  const controls = document.querySelector('.pub-controls');
  if (controls) {
    const buttons = [...controls.querySelectorAll('[data-filter]')];
    const search = document.getElementById('paper-search');
    const year = document.getElementById('paper-year');
    const items = [...document.querySelectorAll('.publication')];
    const groups = [...document.querySelectorAll('.publication-group')];
    const count = document.getElementById('result-count');
    const empty = document.getElementById('no-results');
    let type = 'all';
    const normalize = s => s.toLowerCase().normalize('NFKD').replace(/[\u0300-\u036f]/g, '');
    const texts = new Map(items.map(item => [item, normalize(item.textContent)]));
    function filter() {
      const terms = normalize(search.value.trim()).split(/\s+/).filter(Boolean);
      let visible = 0;
      items.forEach(item => {
        const typeMatch = type === 'all' || (type === 'selected' ? item.dataset.selected === 'true' : item.dataset.type === type);
        const show = typeMatch && (!year.value || item.dataset.year === year.value) && terms.every(term => texts.get(item).includes(term));
        item.hidden = !show;
        if (show) visible++;
      });
      groups.forEach(group => {
        group.hidden = ![...group.querySelectorAll('.publication')].some(item => !item.hidden);
      });
      count.textContent = `${visible} of ${items.length} publications`;
      empty.hidden = visible > 0;
    }
    buttons.forEach(button => button.addEventListener('click', () => {
      type = button.dataset.filter;
      buttons.forEach(b => b.setAttribute('aria-pressed', String(b === button)));
      filter();
    }));
    search.addEventListener('input', filter);
    year.addEventListener('change', filter);
    document.querySelectorAll('[data-reset-filters]').forEach(button => button.addEventListener('click', () => {
      type = 'all'; search.value = ''; year.value = '';
      buttons.forEach(b => b.setAttribute('aria-pressed', String(b.dataset.filter === 'all')));
      filter(); search.focus();
    }));
    filter();
  }
  const links = [...document.querySelectorAll('.site-nav a[href^="#"]')];
  if (links.length) {
    const sections = links.map(link => document.querySelector(link.getAttribute('href'))).filter(Boolean).sort((a, b) => a.compareDocumentPosition(b) & Node.DOCUMENT_POSITION_FOLLOWING ? -1 : 1);
    let scheduled = false;
    function updateActive() {
      scheduled = false;
      let current = sections[0];
      sections.forEach(section => {
        if (section.getBoundingClientRect().top <= 160) current = section;
      });
      links.forEach(link => {
        if (current && link.getAttribute('href') === `#${current.id}`) link.setAttribute('aria-current', 'location');
        else link.removeAttribute('aria-current');
      });
    }
    window.addEventListener('scroll', () => {
      if (!scheduled) { scheduled = true; requestAnimationFrame(updateActive); }
    }, { passive: true });
    updateActive();
  }
})();
