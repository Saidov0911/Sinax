from rest_framework import serializers
from apps.core.utils import get_lang
from .models import Specialist


class SpecialistSerializer(serializers.ModelSerializer):
    position = serializers.SerializerMethodField()

    class Meta:
        model = Specialist
        fields = [
            'id', 'image', 'name',
            'position', 'experience_years',
            'order', 'is_active',
        ]

    def get_position(self, obj):
        return obj.get_position(get_lang(self.context.get('request')))