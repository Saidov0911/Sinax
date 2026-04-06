from django.contrib import admin
from django.core.cache import cache
from .models import GalleryItem


def clear_gallery_cache(modeladmin, request, queryset):
    cache.delete('gallery_list')

clear_gallery_cache.short_description = "Cache ni tozalash"


@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'instagram_url', 'is_active', 'order']
    list_editable = ['is_active', 'order']
    ordering = ['order']
    actions = [clear_gallery_cache]