/* تعویض حالت روشن/تاریک و ذخیره ترجیح کاربر */
(function () {
  const root = document.documentElement;
  const toggleBtns = document.querySelectorAll('.theme-toggle');
  const stored = localStorage.getItem('aerial-theme');

  if (stored) {
    root.setAttribute('data-theme', stored);
  }

  function updateIcons() {
    const current = root.getAttribute('data-theme') || 'light';
    document.querySelectorAll('.theme-toggle i').forEach((icon) => {
      icon.className = current === 'dark' ? 'fa-solid fa-sun' : 'fa-solid fa-moon';
    });
  }

  updateIcons();

  toggleBtns.forEach((btn) => {
    btn.addEventListener('click', () => {
      const current = root.getAttribute('data-theme') || 'light';
      const next = current === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      localStorage.setItem('aerial-theme', next);
      updateIcons();
    });
  });
})();
