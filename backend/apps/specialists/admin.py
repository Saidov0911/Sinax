from django.contrib import admin
from django.core.cache import cache
from .models import Specialist


def clear_specialist_cache(modeladmin, request, queryset):
    for lang in ['uz', 'ru', 'en']:
        cache.delete(f'specialists_list_{lang}')

clear_specialist_cache.short_description = "Cache ni tozalash"


@admin.register(Specialist)
class SpecialistAdmin(admin.ModelAdmin):
    list_display = ['name', 'position_uz', 'experience_years', 'is_active', 'order']
    list_editable = ['is_active', 'order']
    ordering = ['order']
    actions = [clear_specialist_cache]
    fieldsets = (
        ('Umumiy', {
            'fields': ('name', 'image', 'experience_years', 'is_active', 'order')
        }),
        ("O'zbek", {
            'fields': ('position_uz',)
        }),
        ('Русский', {
            'fields': ('position_ru',)
        }),
        ('English', {
            'fields': ('position_en',)
        }),
    )