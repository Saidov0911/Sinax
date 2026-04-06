from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from django.core.cache import cache
from drf_spectacular.utils import extend_schema
from apps.core.utils import get_lang
from .models import FAQ
from .serializers import FAQSerializer

CACHE_TTL = 60 * 15


@extend_schema(tags=['FAQ'], summary='FAQlar ro\'yxati')
class FAQListView(ListAPIView):
    serializer_class = FAQSerializer

    def get_queryset(self):
        return FAQ.objects.filter(is_active=True)

    def list(self, request, *args, **kwargs):
        lang = get_lang(request)
        cache_key = f'faq_list_{lang}'

        cached = cache.get(cache_key)
        if cached:
            return Response(cached)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, CACHE_TTL)
        return response