'use strict';
(() => {
  const header = document.querySelector('.customer-header');
  if (!header) return;

  // Account names, sign-in state and small screens can change the header height.
  const updateHeight = () => document.documentElement.style.setProperty(
    '--customer-header-height', `${Math.ceil(header.getBoundingClientRect().height)}px`
  );
  updateHeight();
  if ('ResizeObserver' in window) {
    new ResizeObserver(updateHeight).observe(header);
  } else {
    window.addEventListener('resize', updateHeight);
    window.addEventListener('load', updateHeight);
  }
})();
