from django.contrib import admin
from django.core.cache import cache
from .models import Product, ProductCategory, ProductImage


def clear_product_cache(modeladmin, request, queryset):
    for lang in ['uz', 'ru', 'en']:
        cache.delete(f'product_categories_list_{lang}')
        for category in ProductCategory.objects.values_list('slug', flat=True):
            cache.delete(f'product_category_{category}_{lang}')
            cache.delete(f'products_list_{category}_{lang}')
    cache.delete('products_list_all_uz')
    cache.delete('products_list_all_ru')
    cache.delete('products_list_all_en')

clear_product_cache.short_description = "Cache ni tozalash"


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['title_uz', 'type', 'slug', 'is_active', 'order']
    list_editable = ['is_active', 'order']
    ordering = ['order']
    actions = [clear_product_cache]
    prepopulated_fields = {'slug': ('title_uz',)}
    fieldsets = (
        ("O'zbek", {
            'fields': ('title_uz', 'description_uz', 'meta_title_uz', 'meta_description_uz')
        }),
        ('Русский', {
            'fields': ('title_ru', 'description_ru', 'meta_title_ru', 'meta_description_ru')
        }),
        ('English', {
            'fields': ('title_en', 'description_en', 'meta_title_en', 'meta_description_en')
        }),
        ('Umumiy', {
            'fields': ('type', 'slug', 'hero_image', 'is_active', 'order')
        }),
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title_uz', 'category', 'price', 'is_active', 'order']
    list_filter = ['category', 'is_active']
    list_editable = ['is_active', 'order']
    ordering = ['category', 'order']
    actions = [clear_product_cache]
    fieldsets = (
        ("O'zbek", {
            'fields': ('title_uz', 'description_uz', 'price_label_uz')
        }),
        ('Русский', {
            'fields': ('title_ru', 'description_ru', 'price_label_ru')
        }),
        ('English', {
            'fields': ('title_en', 'description_en', 'price_label_en')
        }),
        ('Umumiy', {
            'fields': ('category', 'price', 'image', 'is_active', 'order')
        }),
    )

class ProductImageInline(admin.ModelAdmin):
    model = ProductImage
    extra = 5
    max_num = 5

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]