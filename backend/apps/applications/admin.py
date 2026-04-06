from django.contrib import admin
from .models import Application, AllowedUser


@admin.register(AllowedUser)
class AllowedUserAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'telegram_id', 'is_active']
    list_editable = ['is_active']


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'service_type', 'status', 'taken_by', 'created_at']
    list_filter = ['service_type', 'status']
    readonly_fields = ['name', 'phone', 'service_type', 'taken_by', 'created_at']
    ordering = ['-created_at']