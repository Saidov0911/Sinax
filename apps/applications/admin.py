from django.contrib import admin
from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'service_type', 'status', 'taken_by', 'created_at']
    list_filter = ['service_type', 'status']
    readonly_fields = ['name', 'phone', 'service_type', 'taken_by', 'created_at']
    ordering = ['-created_at']