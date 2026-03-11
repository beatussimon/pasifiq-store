/* PASIFIQ STORE — Dashboard JS */

// Notification dropdown
const notifBtn = document.getElementById('notifBtn');
const notifPanel = document.getElementById('notifPanel');
if (notifBtn && notifPanel) {
  notifBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    notifPanel.classList.toggle('open');
  });
  document.addEventListener('click', () => notifPanel.classList.remove('open'));
  notifPanel.addEventListener('click', (e) => e.stopPropagation());
}

// Sidebar toggle (mobile)
const sidebarToggle = document.getElementById('sidebarToggle');
const sidebar = document.querySelector('.dashboard-sidebar');
if (sidebarToggle && sidebar) {
  sidebarToggle.addEventListener('click', () => sidebar.classList.toggle('open'));
}

// Auto-dismiss alerts
document.querySelectorAll('.alert').forEach(el => {
  setTimeout(() => { el.style.opacity = '0'; setTimeout(() => el.remove(), 300); }, 4000);
});

// Mark all notifications read via AJAX
document.querySelectorAll('[href*="mark-all-read"]').forEach(el => {
  el.addEventListener('click', async (e) => {
    e.preventDefault();
    await fetch(el.href, { headers: { 'X-Requested-With': 'XMLHttpRequest' } });
    document.querySelectorAll('.notif-item.unread').forEach(n => n.classList.remove('unread'));
    document.querySelectorAll('.notif-badge, .sidebar-badge').forEach(b => b.remove());
    notifPanel.classList.remove('open');
  });
});
