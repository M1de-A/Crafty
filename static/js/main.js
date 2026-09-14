// Crafty UI helpers. Kept dependency-free so the site works without a frontend build step.
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('[data-auto-slug]').forEach((input) => {
    const source = document.querySelector(input.dataset.autoSlug);
    if (!source) return;
    source.addEventListener('input', () => {
      if (input.dataset.touched === '1') return;
      input.value = source.value.toLowerCase().trim().replace(/[^a-zа-я0-9]+/gi, '-').replace(/^-+|-+$/g, '');
    });
    input.addEventListener('input', () => { input.dataset.touched = '1'; });
  });
});
