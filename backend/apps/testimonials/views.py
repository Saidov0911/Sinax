from django.core.cache import cache
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from .models import Testimonial
from .serializers import TestimonialSerializer

CACHE_TTL = 60 * 15


@extend_schema(
    tags=['Testimonials'],
    summary='Mijozlar izohlari ro\'yxati',
)
class TestimonialListView(ListAPIView):
    """
    GET /api/v1/testimonials/
    """
    serializer_class = TestimonialSerializer

    def get_queryset(self):
        return Testimonial.objects.filter(is_active=True)

    def list(self, request, *args, **kwargs):
        cache_key = 'testimonials_list'

        cached = cache.get(cache_key)
        if cached:
            return Response(cached)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, CACHE_TTL)
        return response