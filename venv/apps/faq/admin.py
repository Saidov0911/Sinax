from django.contrib import admin
from .models import FAQ


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question_uz', 'is_active', 'order']
    list_editable = ['is_active', 'order']
    fieldsets = (
        ("O'zbek", {
            'fields': ('question_uz', 'answer_uz')
        }),
        ('Русский', {
            'fields': ('question_ru', 'answer_ru')
        }),
        ('English', {
            'fields': ('question_en', 'answer_en')
        }),
        ('Umumiy', {
            'fields': ('is_active', 'order')
        }),
    )