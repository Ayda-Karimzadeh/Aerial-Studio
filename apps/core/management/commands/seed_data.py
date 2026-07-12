"""
دستور Seeder برای پر کردن دیتابیس با داده‌های نمونه (تست/دمو).
معادل php artisan db:seed در لاراول.

استفاده:
    python manage.py seed_data
    python manage.py seed_data --flush   (پاک کردن داده‌های قبلی قبل از ساخت داده‌ی جدید)
"""
from datetime import date, time, timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.bookings.models import Booking
from apps.classes.models import ClassSession, Discipline
from apps.coaches.models import CoachProfile, WeeklySchedule
from apps.evaluations.models import Evaluation
from apps.pages.models import Testimonial
from apps.payments.models import Payment
from apps.students.models import StudentProfile

User = get_user_model()


class Command(BaseCommand):
    help = 'پر کردن دیتابیس با داده‌های نمونه برای تست و دمو (مشابه Laravel Seeder)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--flush',
            action='store_true',
            help='قبل از ساخت داده‌ی جدید، داده‌های نمونه‌ی قبلی (بر اساس ایمیل) حذف شوند',
        )

    def handle(self, *args, **options):
        if options['flush']:
            self.stdout.write(self.style.WARNING('در حال حذف داده‌های نمونه‌ی قبلی...'))
            User.objects.filter(email__endswith='@example.com').delete()

        self.stdout.write('در حال ساخت داده‌های نمونه...')

        # ---------- ۱. کاربر ادمین ----------
        admin, created = User.objects.get_or_create(
            email='admin@example.com',
            defaults=dict(first_name='مدیر', last_name='سیستم', role='admin',
                          is_staff=True, is_superuser=True)
        )
        if created:
            admin.set_password('Admin@1234')
            admin.save()
            self.stdout.write(self.style.SUCCESS('  ادمین ساخته شد: admin@example.com / Admin@1234'))

        # ---------- ۲. رشته‌ها ----------
        disciplines_data = [
            ('silk', 'fa-ribbon'),
            ('hoop', 'fa-circle-notch'),
            ('sling', 'fa-link'),
            ('stretch', 'fa-arrows-left-right-to-line'),
            ('flexibility', 'fa-person-walking'),
        ]
        disciplines = {}
        for name, icon in disciplines_data:
            d, _ = Discipline.objects.get_or_create(name=name, defaults={'icon': icon})
            disciplines[name] = d
        self.stdout.write(self.style.SUCCESS(f'  {len(disciplines)} رشته آماده شد'))

        # ---------- ۳. مربیان ----------
        coaches_data = [
            ('سارا', 'احمدی', 'coach1@example.com', ['silk', 'hoop'], 5, 'مربی باتجربه در سیلک و هوپ هوایی.'),
            ('نیما', 'رضایی', 'coach2@example.com', ['sling', 'stretch'], 3, 'متخصص اسلینگ و تمرینات استرچ.'),
            ('پریسا', 'کریمی', 'coach3@example.com', ['flexibility', 'stretch'], 7, 'مربی انعطاف‌پذیری و آمادگی جسمانی.'),
        ]
        coach_users = []
        for first, last, email, specs, exp, bio in coaches_data:
            user, created = User.objects.get_or_create(
                email=email, defaults=dict(first_name=first, last_name=last,
                                            role='coach', phone_number='0912' + str(1000000 + len(coach_users)))
            )
            if created:
                user.set_password('Coach@1234')
                user.save()
            profile = user.coach_profile
            profile.bio = bio
            profile.years_of_experience = exp
            profile.save()
            profile.specialties.set([disciplines[s] for s in specs])
            coach_users.append(user)

            # برنامه‌ی هفتگی نمونه
            WeeklySchedule.objects.get_or_create(
                coach=profile, weekday=1, start_time=time(17, 0), end_time=time(20, 0)
            )
        self.stdout.write(self.style.SUCCESS(f'  {len(coach_users)} مربی ساخته شد (رمز همه: Coach@1234)'))

        # ---------- ۴. هنرجویان ----------
        students_data = [
            ('آیدا', 'کریم‌زاده', 'student1@example.com', 'beginner'),
            ('محمد', 'حسینی', 'student2@example.com', 'intermediate'),
            ('النا', 'موسوی', 'student3@example.com', 'beginner'),
            ('آرش', 'صادقی', 'student4@example.com', 'advanced'),
        ]
        student_users = []
        for first, last, email, level in students_data:
            user, created = User.objects.get_or_create(
                email=email, defaults=dict(first_name=first, last_name=last,
                                            role='student', phone_number='0913' + str(2000000 + len(student_users)))
            )
            if created:
                user.set_password('Student@1234')
                user.save()
            profile = user.student_profile
            profile.level = level
            profile.save()
            student_users.append(user)
        self.stdout.write(self.style.SUCCESS(f'  {len(student_users)} هنرجو ساخته شد (رمز همه: Student@1234)'))

        # ---------- ۵. کلاس‌ها ----------
        classes_data = [
            ('کلاس سیلک مبتدی', 'silk', 'beginner', coach_users[0], 8, 350000, 2),
            ('کلاس هوپ متوسط', 'hoop', 'intermediate', coach_users[0], 6, 400000, 3),
            ('کلاس اسلینگ پیشرفته', 'sling', 'advanced', coach_users[1], 5, 450000, 4),
            ('کلاس استرچ عمومی', 'stretch', 'beginner', coach_users[1], 10, 250000, 1),
            ('کلاس انعطاف‌پذیری', 'flexibility', 'intermediate', coach_users[2], 8, 300000, 5),
        ]
        classes = []
        for title, disc, level, coach, cap, price, days_ahead in classes_data:
            c, _ = ClassSession.objects.get_or_create(
                title=title, discipline=disciplines[disc], level=level, coach=coach,
                defaults=dict(
                    capacity=cap, equipment_count=cap, price=price,
                    session_date=date.today() + timedelta(days=days_ahead),
                    start_time=time(18, 0), end_time=time(19, 30),
                    description=f'کلاس {title} برای سطح {level}.'
                )
            )
            classes.append(c)
        self.stdout.write(self.style.SUCCESS(f'  {len(classes)} کلاس ساخته شد'))

        # ---------- ۶. رزرو + پرداخت نمونه ----------
        booking_count = 0
        for i, student in enumerate(student_users):
            class_session = classes[i % len(classes)]
            booking, created = Booking.objects.get_or_create(
                student=student, class_session=class_session,
                defaults={'status': Booking.Status.CONFIRMED}
            )
            if created:
                booking_count += 1
                Payment.objects.get_or_create(
                    student=student, booking=booking,
                    defaults={'amount': class_session.price, 'status': Payment.Status.PAID,
                              'paid_at': timezone.now()}
                )
        self.stdout.write(self.style.SUCCESS(f'  {booking_count} رزرو + پرداخت نمونه ساخته شد'))

        # ---------- ۷. ارزیابی نمونه ----------
        eval_count = 0
        for i, student in enumerate(student_users):
            coach = coach_users[i % len(coach_users)]
            _, created = Evaluation.objects.get_or_create(
                student=student, coach=coach,
                defaults=dict(skill_level='beginner', score=7 + (i % 3),
                              description='پیشرفت خوبی داشته و آماده‌ی سطح بعدی است.')
            )
            if created:
                eval_count += 1
        self.stdout.write(self.style.SUCCESS(f'  {eval_count} ارزیابی نمونه ساخته شد'))

        # ---------- ۸. نظرات هنرجویان (Testimonial) ----------
        testimonials_data = [
            ('آیدا کریم‌زاده', 'کلاس‌های این باشگاه واقعاً کیفیت بالایی دارن و مربی‌ها خیلی حرفه‌ای هستن.', 5),
            ('محمد حسینی', 'فضای دوستانه و آموزش اصولی، دقیقاً همون چیزی که دنبالش بودم.', 5),
            ('النا موسوی', 'پیشرفتم توی این چند ماه واقعا محسوس بوده.', 4),
        ]
        for name, content, rating in testimonials_data:
            Testimonial.objects.get_or_create(student_name=name, defaults={'content': content, 'rating': rating})

        self.stdout.write(self.style.SUCCESS('\nهمه‌ی داده‌های نمونه با موفقیت ساخته شدند! 🎉'))
        self.stdout.write('اطلاعات ورود:')
        self.stdout.write('  ادمین:   admin@example.com   / Admin@1234')
        self.stdout.write('  مربی:    coach1@example.com   / Coach@1234')
        self.stdout.write('  هنرجو:   student1@example.com / Student@1234')