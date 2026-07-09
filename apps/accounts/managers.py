from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """
    مدیر سفارشی برای مدل User که از ایمیل به‌جای username
    برای احراز هویت استفاده می‌کند.
    """

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('وارد کردن ایمیل الزامی است.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('کاربر ادمین باید is_staff=True داشته باشد.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('کاربر ادمین باید is_superuser=True داشته باشد.')

        return self.create_user(email, password, **extra_fields)
