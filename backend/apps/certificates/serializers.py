from rest_framework import serializers
from apps.core.utils import get_lang
from .models import Certificate


class CertificateSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    class Meta:
        model = Certificate
        fields = ['id', 'image', 'title', 'order']

    def get_title(self, obj):
        return obj.get_title(get_lang(self.context.get('request')))