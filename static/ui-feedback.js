/* Sonner-inspired, dependency-free toast stack and password visibility. */
document.addEventListener('DOMContentLoaded', () => {
  const input = document.getElementById('login-password');
  const toggle = document.getElementById('toggle-password');
  if (input && toggle) toggle.addEventListener('click', () => {
    const visible = input.type === 'password';
    input.type = visible ? 'text' : 'password';
    toggle.textContent = visible ? 'Hide' : 'Show';
    toggle.setAttribute('aria-label', visible ? 'Hide password' : 'Show password');
    toggle.setAttribute('aria-pressed', String(visible));
  });
  document.querySelectorAll('.app-toast').forEach(toast => {
    let timeout;
    const dismiss = () => { clearTimeout(timeout); toast.classList.add('toast-exit'); setTimeout(() => toast.remove(), 220); };
    toast.querySelector('.toast-close')?.addEventListener('click', dismiss);
    timeout = setTimeout(dismiss, toast.classList.contains('error') ? 8500 : 5000);
    toast.addEventListener('mouseenter', () => clearTimeout(timeout));
    toast.addEventListener('mouseleave', () => { timeout = setTimeout(dismiss, 3000); });
  });
});
