"""تنظیمات محیط توسعه (Development)"""
from .base import *
from decouple import config

DEBUG = True

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')

# در محیط توسعه از SQLite هم می‌توان استفاده کرد در صورت نبود PostgreSQL
# در صورت نیاز خط زیر را از کامنت خارج کنید:
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

INTERNAL_IPS = ['127.0.0.1']
