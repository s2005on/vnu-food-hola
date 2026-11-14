// V6: Presentation-only cart drawer; existing cart and checkout handlers remain in app.js.
'use strict';
(() => {
  const drawer = document.getElementById('basket');
  const trigger = document.getElementById('cart-open');
  const closeButton = document.getElementById('cart-close');
  if (!drawer || !trigger || !closeButton || !drawer.showModal) return;

  function open() {
    if (drawer.open) return;
    drawer.showModal();
    trigger.setAttribute('aria-expanded', 'true');
    closeButton.focus();
  }

  function close() {
    if (!drawer.open) return;
    drawer.close();
  }

  trigger.addEventListener('click', open);
  closeButton.addEventListener('click', close);
  drawer.addEventListener('close', () => {
    trigger.setAttribute('aria-expanded', 'false');
    // Return focus after closing with Escape or the close button.
    if (!document.getElementById('history-dialog')?.open && document.activeElement !== trigger) {
      trigger.focus({preventScroll: true});
    }
  });
  // Clicking outside the slide-out panel closes the native modal.
  drawer.addEventListener('click', (event) => {
    if (event.target !== drawer) return;
    const bounds = drawer.getBoundingClientRect();
    if (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) close();
  });

  window.VJUCartDrawer = {open, close};
})();
