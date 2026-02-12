// Shared menu behavior: attaches to #menuBtn (must exist in page header)
(() => {
  function ready(fn){ if (document.readyState !== 'loading') fn(); else document.addEventListener('DOMContentLoaded', fn); }

  ready(() => {
    const menuBtn = document.getElementById('menuBtn');
    const overlay = document.getElementById('overlay');

    if (!menuBtn) return; // pages without a menu button won't activate

    function setSidebarOpen(isOpen) {
      document.body.classList.toggle('sidebar-open', isOpen);
      menuBtn.setAttribute('aria-expanded', String(isOpen));
      if (!isOpen) closeAllSubmenus();
    }

    function closeAllSubmenus() {
      document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('open');
        const btn = item.querySelector('.nav-main');
        if (btn) btn.setAttribute('aria-expanded', 'false');
      });
    }

    // Sidebar open/close
    menuBtn.addEventListener('click', () => {
      const isOpen = document.body.classList.contains('sidebar-open');
      setSidebarOpen(!isOpen);
    });

    if (overlay) overlay.addEventListener('click', () => setSidebarOpen(false));
    window.addEventListener('keydown', (e) => { if (e.key === 'Escape') setSidebarOpen(false); });

    // Click-to-toggle dropdowns (Step 1/2/...)
    document.addEventListener('click', (ev) => {
      const btn = ev.target.closest('.nav-main');
      if (!btn) return;
      const item = btn.closest('.nav-item');
      const wasOpen = item.classList.contains('open');
      closeAllSubmenus();
      if (!wasOpen) {
        item.classList.add('open');
        btn.setAttribute('aria-expanded', 'true');
      }
    });

    // Close sidebar when clicking a submenu link (nice UX)
    document.addEventListener('click', (ev) => {
      const a = ev.target.closest('.submenu a');
      if (!a) return;
      setSidebarOpen(false);
    });
  });
})();
