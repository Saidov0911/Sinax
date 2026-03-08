from django.core.cache import cache
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from apps.core.utils import get_lang
from .models import Specialist
from .serializers import SpecialistSerializer

CACHE_TTL = 60 * 15

LANG_PARAMETER = OpenApiParameter(
    name='lang',
    type=OpenApiTypes.STR,
    location=OpenApiParameter.QUERY,
    description='Til tanlash: uz, ru, en (default: uz)',
    enum=['uz', 'ru', 'en'],
    required=False,
)


@extend_schema(
    tags=['Specialists'],
    summary='Mutaxassislar ro\'yxati',
    parameters=[LANG_PARAMETER],
)
class SpecialistListView(ListAPIView):
    """
    GET /api/v1/specialists/
    GET /api/v1/specialists/?lang=ru
    """
    serializer_class = SpecialistSerializer

    def get_queryset(self):
        return Specialist.objects.filter(is_active=True)

    def list(self, request, *args, **kwargs):
        lang = get_lang(request)
        cache_key = f'specialists_list_{lang}'

        cached = cache.get(cache_key)
        if cached:
            return Response(cached)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, CACHE_TTL)
        return response