from django.core.cache import cache
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from apps.core.utils import get_lang
from .models import Product, ProductCategory
from .serializers import (
    ProductSerializer,
    ProductCategoryListSerializer,
    ProductCategoryDetailSerializer,
)

CACHE_TTL = 60 * 15  # 15 daqiqa


LANG_PARAMETER = OpenApiParameter(
    name='lang',
    type=OpenApiTypes.STR,
    location=OpenApiParameter.QUERY,
    description='Til tanlash: uz, ru, en (default: uz)',
    enum=['uz', 'ru', 'en'],
    required=False,
)

CATEGORY_PARAMETER = OpenApiParameter(
    name='category',
    type=OpenApiTypes.STR,
    location=OpenApiParameter.QUERY,
    description='Kategoriya slugi: masketnitsa, jalyuzi, kabinka',
    enum=['masketnitsa', 'jalyuzi', 'kabinka'],
    required=False,
)


@extend_schema(
    tags=['Products'],
    summary='Barcha mahsulotlar ro\'yxati',
    parameters=[LANG_PARAMETER, CATEGORY_PARAMETER],
)
class ProductListView(ListAPIView):
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


@extend_schema(
    tags=['Products'],
    summary='Bitta mahsulot',
    parameters=[LANG_PARAMETER],
)
class ProductDetailView(RetrieveAPIView):
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


@extend_schema(
    tags=['Categories'],
    summary='Barcha kategoriyalar ro\'yxati',
    parameters=[LANG_PARAMETER],
)
class ProductCategoryListView(ListAPIView):
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


@extend_schema(
    tags=['Categories'],
    summary='Bitta kategoriya va uning mahsulotlari',
    parameters=[LANG_PARAMETER],
)
class ProductCategoryDetailView(RetrieveAPIView):
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


@extend_schema(
    tags=['Products'],
    summary='Kategoriya bo\'yicha mahsulotlar',
    parameters=[LANG_PARAMETER],
)
class ProductListByCategoryView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        return Product.objects.filter(
            is_active=True,
            category__slug=slug
        ).select_related('category')

    def list(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug')
        lang = get_lang(request)
        cache_key = f'products_{slug}_{lang}'

        cached = cache.get(cache_key)
        if cached:
            return Response(cached)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, CACHE_TTL)
        return response
