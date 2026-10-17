const dialog = document.querySelector('#lookup');
document.querySelectorAll('[data-lookup]').forEach(button => button.addEventListener('click', () => {
  document.querySelector('#lookup-action').value = button.dataset.lookup;
  dialog.showModal();
}));
document.querySelector('[data-close]')?.addEventListener('click', () => dialog.close());
document.querySelectorAll('[data-confirm]').forEach(form => form.addEventListener('submit', event => {
  if (!window.confirm(form.dataset.confirm)) event.preventDefault();
}));
