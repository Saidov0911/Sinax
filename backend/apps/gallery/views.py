from django.core.cache import cache
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from .models import GalleryItem
from .serializers import GalleryItemSerializer

CACHE_TTL = 60 * 15


@extend_schema(
    tags=['Gallery'],
    summary='Gallery ro\'yxati',
)
class GalleryListView(ListAPIView):
    """
    GET /api/v1/gallery/
    """
    serializer_class = GalleryItemSerializer

    def get_queryset(self):
        return GalleryItem.objects.filter(is_active=True)

    def list(self, request, *args, **kwargs):
        cache_key = 'gallery_list'

        cached = cache.get(cache_key)
        if cached:
            return Response(cached)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, CACHE_TTL)
        return response