from rest_framework import serializers
from apps.core.utils import resize_image, get_lang
from .models import Product, ProductCategory


class ProductSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    price_label = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'title', 'description',
            'price', 'price_label',
            'image', 'order', 'is_active',
        ]

    def get_title(self, obj):
        return obj.get_title(get_lang(self.context.get('request')))

    def get_description(self, obj):
        return obj.get_description(get_lang(self.context.get('request')))

    def get_price_label(self, obj):
        return obj.get_price_label(get_lang(self.context.get('request')))


class ProductCategoryListSerializer(serializers.ModelSerializer):
    """Ro'yxat uchun — ichida products yo'q"""
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = ProductCategory
        fields = [
            'id', 'slug', 'type', 'title', 'description',
            'hero_image', 'order', 'is_active',
        ]

    def get_title(self, obj):
        return obj.get_title(get_lang(self.context.get('request')))

    def get_description(self, obj):
        return obj.get_description(get_lang(self.context.get('request')))


class ProductCategoryDetailSerializer(serializers.ModelSerializer):
    """Detail uchun — ichida products bor"""
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    meta_title = serializers.SerializerMethodField()
    meta_description = serializers.SerializerMethodField()
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = ProductCategory
        fields = [
            'id', 'slug', 'type', 'title', 'description',
            'hero_image', 'meta_title', 'meta_description',
            'order', 'is_active', 'products',
        ]

    def get_title(self, obj):
        return obj.get_title(get_lang(self.context.get('request')))

    def get_description(self, obj):
        return obj.get_description(get_lang(self.context.get('request')))

    def get_meta_title(self, obj):
        return obj.get_meta_title(get_lang(self.context.get('request')))

    def get_meta_description(self, obj):
        return obj.get_meta_description(get_lang(self.context.get('request')))