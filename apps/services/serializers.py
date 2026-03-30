from rest_framework import serializers
from apps.core.utils import get_lang
from .models import Service, RepairPart


class ServiceSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    price_label = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = [
            'id', 'image', 'name',
            'price', 'price_label',
            'order', 'is_active',
        ]

    def get_name(self, obj):
        return obj.get_name(get_lang(self.context.get('request')))

    def get_price_label(self, obj):
        return obj.get_price_label(get_lang(self.context.get('request')))


class RepairPartSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    price_label = serializers.SerializerMethodField()

    class Meta:
        model = RepairPart
        fields = ['id', 'name', 'price', 'price_label']

    def get_name(self, obj):
        return obj.get_name(get_lang(self.context.get('request')))

    def get_price_label(self, obj):
        return obj.get_price_label(get_lang(self.context.get('request')))