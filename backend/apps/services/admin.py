from django.contrib import admin
from django.core.cache import cache
from .models import Service, RepairPart


def clear_service_cache(modeladmin, request, queryset):
    for lang in ['uz', 'ru', 'en']:
        cache.delete(f'services_list_{lang}')

clear_service_cache.short_description = "Cache ni tozalash"


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name_uz', 'price', 'is_active', 'order']
    list_editable = ['is_active', 'order']
    ordering = ['order']
    actions = [clear_service_cache]
    fieldsets = (
        ("O'zbek", {
            'fields': ('name_uz', 'price_label_uz')
        }),
        ('Русский', {
            'fields': ('name_ru', 'price_label_ru')
        }),
        ('English', {
            'fields': ('name_en', 'price_label_en')
        }),
        ('Umumiy', {
            'fields': ('image', 'price', 'is_active', 'order')
        }),
    )

@admin.register(RepairPart)
class RepairPartAdmin(admin.ModelAdmin):
    list_display = ['name_uz', 'price', 'is_active', 'order']
    list_editable = ['is_active', 'order']