def site_settings(request):
    """
    اطلاعات عمومی سایت که در تمام قالب‌ها در دسترس است
    (مثل نام سایت، اطلاعات تماس و...).
    """
    return {
        'SITE_NAME': 'Aerial Studio',
        'SITE_NAME_FA': 'آیریال استودیو',
        'SITE_PHONE': '021-12345678',
        'SITE_EMAIL': 'info@aerialstudio.com',
        'SITE_ADDRESS': 'تهران، خیابان ولیعصر',
    }
