from django.core.cache import cache
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response

from apps.core.utils import get_lang
from .models import Product, ProductCategory
from .serializers import (
    ProductSerializer,
    ProductCategoryListSerializer,
    ProductCategoryDetailSerializer,
)

CACHE_TTL = 60 * 15  # 15 daqiqa


class ProductCategoryListView(ListAPIView):
    """
    GET /api/v1/products/categories/
    GET /api/v1/products/categories/?lang=ru
    """
    serializer_class = ProductCategoryListSerializer

    def get_queryset(self):
        return ProductCategory.objects.filter(is_active=True)

    def list(self, request, *args, **kwargs):
        lang = get_lang(request)
        cache_key = f'product_categories_list_{lang}'

        cached = cache.get(cache_key)
        if cached:
            return Response(cached)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, CACHE_TTL)
        return response


class ProductCategoryDetailView(RetrieveAPIView):
    """
    GET /api/v1/products/categories/masketnitsa/
    GET /api/v1/products/categories/masketnitsa/?lang=en
    """
    serializer_class = ProductCategoryDetailSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return ProductCategory.objects.filter(
            is_active=True
        ).prefetch_related('products')

    def retrieve(self, request, *args, **kwargs):
        lang = get_lang(request)
        slug = kwargs.get('slug')
        cache_key = f'product_category_{slug}_{lang}'

        cached = cache.get(cache_key)
        if cached:
            return Response(cached)

        response = super().retrieve(request, *args, **kwargs)
        cache.set(cache_key, response.data, CACHE_TTL)
        return response


class ProductListView(ListAPIView):
    """
    GET /api/v1/products/
    GET /api/v1/products/?category=masketnitsa
    GET /api/v1/products/?category=jalyuzi&lang=ru
    """
    serializer_class = ProductSerializer

    def get_queryset(self):
        qs = Product.objects.filter(
            is_active=True
        ).select_related('category')
        category = self.request.query_params.get('category')
        if category:
            qs = qs.filter(category__slug=category)
        return qs

    def list(self, request, *args, **kwargs):
        lang = get_lang(request)
        category = request.query_params.get('category', 'all')
        cache_key = f'products_list_{category}_{lang}'

        cached = cache.get(cache_key)
        if cached:
            return Response(cached)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, CACHE_TTL)
        return response


class ProductDetailView(RetrieveAPIView):
    """
    GET /api/v1/products/<id>/
    """
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(
            is_active=True
        ).select_related('category')

    def retrieve(self, request, *args, **kwargs):
        lang = get_lang(request)
        pk = kwargs.get('pk')
        cache_key = f'product_detail_{pk}_{lang}'

        cached = cache.get(cache_key)
        if cached:
            return Response(cached)

        response = super().retrieve(request, *args, **kwargs)
        cache.set(cache_key, response.data, CACHE_TTL)
        return response