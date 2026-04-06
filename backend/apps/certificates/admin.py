from django.contrib import admin
from django.core.cache import cache
from .models import Certificate


def clear_certificate_cache(modeladmin, request, queryset):
    for lang in ['uz', 'ru', 'en']:
        cache.delete(f'certificates_list_{lang}')

clear_certificate_cache.short_description = "Cache ni tozalash"


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'is_active', 'order']
    list_editable = ['is_active', 'order']
    ordering = ['order']
    actions = [clear_certificate_cache]
    fieldsets = (
        ('Umumiy', {
            'fields': ('image', 'is_active', 'order')
        }),
        ("O'zbek", {
            'fields': ('title_uz',)
        }),
        ('Русский', {
            'fields': ('title_ru',)
        }),
        ('English', {
            'fields': ('title_en',)
        }),
    )