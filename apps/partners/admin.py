from django.contrib import admin
from django.core.cache import cache
from .models import Partner


def clear_partner_cache(modeladmin, request, queryset):
    cache.delete('partners_list')

clear_partner_cache.short_description = "Cache ni tozalash"


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'order']
    list_editable = ['is_active', 'order']
    ordering = ['order']
    actions = [clear_partner_cache]