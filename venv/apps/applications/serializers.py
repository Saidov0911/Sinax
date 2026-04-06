from rest_framework import serializers
from .models import Application


class ApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['name', 'phone', 'service_type']