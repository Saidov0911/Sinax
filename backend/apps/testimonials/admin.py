from django.contrib import admin
from django.core.cache import cache
from .models import Testimonial


def clear_testimonial_cache(modeladmin, request, queryset):
    cache.delete('testimonials_list')

clear_testimonial_cache.short_description = "Cache ni tozalash"

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'rating', 'is_active', 'order', 'created_at']
    list_filter = ['rating', 'is_active']
    list_editable = ['is_active', 'order']
    ordering = ['order']
    actions = [clear_testimonial_cache]
    readonly_fields = ['name', 'avatar', 'comment', 'rating', 'created_at']