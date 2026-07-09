/* اسکریپت‌های عمومی سایت Aerial Studio */
document.addEventListener('DOMContentLoaded', function () {

  // نمایش/مخفی کردن سایدبار در داشبورد (موبایل)
  const sidebarToggle = document.querySelector('[data-sidebar-toggle]');
  const sidebar = document.querySelector('.sidebar');
  if (sidebarToggle && sidebar) {
    sidebarToggle.addEventListener('click', function () {
      sidebar.classList.toggle('show');
    });
  }

  // بستن خودکار پیام‌های Alert بعد از چند ثانیه
  document.querySelectorAll('.alert-auto-dismiss').forEach(function (alertEl) {
    setTimeout(function () {
      const bsAlert = new bootstrap.Alert(alertEl);
      bsAlert.close();
    }, 5000);
  });

  // فعال‌سازی Tooltip های بوت‌استرپ
  const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
  tooltipTriggerList.forEach(function (el) {
    new bootstrap.Tooltip(el);
  });

  // انیمیشن ساده fade-in برای عناصر هنگام اسکرول
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('fade-in-up');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.observe-fade').forEach((el) => observer.observe(el));

  // پر کردن نوار ظرفیت کلاس‌ها با انیمیشن
  document.querySelectorAll('.capacity-bar-fill').forEach((bar) => {
    const target = bar.getAttribute('data-fill') || '0';
    setTimeout(() => { bar.style.width = target + '%'; }, 200);
  });
});
