from django.core.cache import cache
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from .models import Partner
from .serializers import PartnerSerializer

CACHE_TTL = 60 * 15


@extend_schema(
    tags=['Partners'],
    summary='Hamkorlar ro\'yxati',
)
class PartnerListView(ListAPIView):
    """
    GET /api/v1/partners/
    """
    serializer_class = PartnerSerializer

    def get_queryset(self):
        return Partner.objects.filter(is_active=True)

    def list(self, request, *args, **kwargs):
        cache_key = 'partners_list'

        cached = cache.get(cache_key)
        if cached:
            return Response(cached)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, CACHE_TTL)
        return response