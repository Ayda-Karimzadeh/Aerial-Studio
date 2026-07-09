from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # صفحات عمومی سایت
    path('', include('apps.pages.urls')),

    # احراز هویت
    path('accounts/', include('apps.accounts.urls')),

    # داشبورد سه‌گانه
    path('dashboard/', include('apps.dashboard.urls')),

    # ماژول‌های مدیریتی
    path('students/', include('apps.students.urls')),
    path('coaches/', include('apps.coaches.urls')),
    path('classes/', include('apps.classes.urls')),
    path('bookings/', include('apps.bookings.urls')),
    path('payments/', include('apps.payments.urls')),
    path('evaluations/', include('apps.evaluations.urls')),
    path('reports/', include('apps.reports.urls')),

    # API
    path('api/v1/', include('apps.api.v1.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = 'پنل مدیریت Aerial Studio'
admin.site.site_title = 'Aerial Studio'
admin.site.index_title = 'خوش آمدید'
