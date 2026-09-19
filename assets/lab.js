/* Event delegation also works when the single-file preview switches pages. */
(() => {
  'use strict';
  document.addEventListener('click', event => {
    if (!(event.target instanceof Element)) return;
    const button = event.target.closest('[data-press-filter]');
    if (button) {
      const filter = button.dataset.pressFilter;
      document.querySelectorAll('[data-press-filter]').forEach(el => {
        el.setAttribute('aria-pressed', String(el === button));
      });
      let visible = 0;
      document.querySelectorAll('.press-row[data-press-type]').forEach(el => {
        el.hidden = filter !== 'all' && el.dataset.pressType !== filter;
        if (!el.hidden) visible++;
      });
      const status = document.querySelector('.press-count');
      if (status) status.textContent = `${visible} coverage items`;
    }
    if (event.target.closest('[data-dismiss-font-warning]')) {
      document.getElementById('preview-font-warning')?.setAttribute('hidden', '');
    }
  });
})();
