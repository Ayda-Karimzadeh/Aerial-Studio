# Aerial Studio 🪂

سیستم مدیریت باشگاه تخصصی ورزش‌های هوایی (سیلک، هوپ، اسلینگ، استرچ، انعطاف‌پذیری)
ساخته‌شده با Django 5، PostgreSQL و Bootstrap 5 (RTL).

## ویژگی‌ها

- سه نقش کاربری: مدیر، مربی، هنرجو (هرکدام با داشبورد اختصاصی)
- مدیریت کامل هنرجویان، مربیان و کلاس‌ها
- سیستم رزرو با کنترل ظرفیت لحظه‌ای
- مدل پرداخت (Pending / Paid / Failed / Refunded)
- ثبت ارزیابی هنرجو توسط مربی (سطح، امتیاز، توضیحات)
- گزارش‌گیری کامل با نمودار (Chart.js): درآمد، محبوب‌ترین رشته، کلاس‌های پر/خالی
- API کامل با Django REST Framework
- طراحی Glassmorphism مدرن، ریسپانسیو، حالت روشن/تاریک، فونت وزیرمتن

## نصب و راه‌اندازی

### ۱. ایجاد محیط مجازی و نصب پکیج‌ها

```bash
python -m venv venv
source venv/bin/activate    # ویندوز: venv\Scripts\activate
pip install -r requirements.txt
```

### ۲. تنظیم فایل `.env`

فایل `.env` را در ریشه پروژه بر اساس نمونه موجود ویرایش کنید (نام پایگاه داده، کاربر PostgreSQL و ...).

### ۳. ایجاد پایگاه داده PostgreSQL

```sql
CREATE DATABASE aerial_studio_db;
```

### ۴. اجرای Migration ها

```bash
python manage.py makemigrations
python manage.py migrate
```

### ۵. ساخت کاربر مدیر (Superuser)

```bash
python manage.py createsuperuser
```
> نکته: در فرم ثبت‌نام کاربر ادمین، فیلد `role` به‌صورت خودکار admin در نظر گرفته می‌شود.

### ۶. اجرای سرور توسعه

```bash
python manage.py runserver
```

سپس به آدرس `http://127.0.0.1:8000` مراجعه کنید. پنل مدیریت جنگو در `/admin/` در دسترس است.

## ساختار پروژه

```
config/             تنظیمات پروژه (settings/base, development, production)
apps/
  core/              مدل‌ها و ابزارهای پایه مشترک
  accounts/          احراز هویت و User Model سفارشی
  students/          مدیریت هنرجویان
  coaches/           مدیریت مربیان
  classes/           مدیریت کلاس‌ها و رشته‌ها
  bookings/          سیستم رزرو
  payments/          مدل و مدیریت پرداخت
  evaluations/       ارزیابی هنرجو توسط مربی
  reports/           گزارش‌گیری و آمار
  dashboard/         سه داشبورد اختصاصی (ادمین/مربی/هنرجو)
  pages/             صفحات عمومی سایت
  api/               DRF API نسخه ۱
templates/           قالب‌های HTML (RTL + Bootstrap 5)
static/              CSS، JS و فایل‌های استاتیک
media/               فایل‌های آپلودی (آواتار، تصاویر کلاس و گالری)
```

## کاربران پیش‌فرض برای تست (پس از اجرای seed دستی)

می‌توانید از طریق پنل مدیریت (`/admin/`) یا شل جنگو (`python manage.py shell`) کاربرهای
مربی و هنرجو با نقش‌های مشخص بسازید. مثال:

```python
from apps.accounts.models import User
User.objects.create_user(email='coach@example.com', password='pass1234', first_name='نام', last_name='خانوادگی', role='coach')
```

## تکنولوژی‌ها

Python 3.13 · Django 5 · PostgreSQL · Django REST Framework · django-crispy-forms
· django-filter · Bootstrap 5 (RTL) · Chart.js · Font Awesome · فونت Vazirmatn

---
ساخته‌شده با ❤️ برای Aerial Studio
