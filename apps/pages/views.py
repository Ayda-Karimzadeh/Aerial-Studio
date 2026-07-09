from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView

from apps.classes.models import ClassSession, Discipline
from apps.coaches.models import CoachProfile
from .forms import ContactForm
from .models import GalleryImage, Testimonial


class HomeView(TemplateView):
    """صفحه اصلی (Landing Page) سایت."""
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['disciplines'] = Discipline.objects.all()
        context['featured_classes'] = ClassSession.objects.filter(is_active=True)[:6]
        context['coaches'] = CoachProfile.objects.filter(is_active=True)[:4]
        context['testimonials'] = Testimonial.objects.filter(is_published=True)[:6]
        context['gallery_preview'] = GalleryImage.objects.filter(is_featured=True)[:8]
        return context


class AboutView(TemplateView):
    """صفحه درباره ما."""
    template_name = 'pages/about.html'


class ScheduleView(TemplateView):
    """صفحه برنامه هفتگی کلاس‌ها."""
    template_name = 'pages/schedule.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['classes'] = ClassSession.objects.filter(is_active=True).select_related('discipline', 'coach')
        return context


class GalleryView(ListView):
    """صفحه گالری تصاویر."""
    model = GalleryImage
    template_name = 'pages/gallery.html'
    context_object_name = 'images'
    paginate_by = 16


class PricingView(TemplateView):
    """صفحه تعرفه‌ها و قیمت‌گذاری."""
    template_name = 'pages/pricing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['disciplines'] = Discipline.objects.all()
        return context


class ContactView(CreateView):
    """صفحه تماس با ما و ارسال پیام."""
    form_class = ContactForm
    template_name = 'pages/contact.html'
    success_url = reverse_lazy('pages:contact')

    def form_valid(self, form):
        messages.success(self.request, 'پیام شما با موفقیت ارسال شد. به‌زودی با شما تماس خواهیم گرفت.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'لطفاً خطاهای فرم را برطرف کنید.')
        return super().form_invalid(form)
