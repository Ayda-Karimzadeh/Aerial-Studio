from django.contrib import admin
from .models import GalleryImage, Testimonial, ContactMessage


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'discipline', 'is_featured', 'created_at')
    list_filter = ('discipline', 'is_featured')


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'rating', 'is_published', 'created_at')
    list_filter = ('is_published', 'rating')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'subject', 'is_read', 'created_at')
    list_filter = ('is_read',)
    search_fields = ('full_name', 'email', 'subject')
