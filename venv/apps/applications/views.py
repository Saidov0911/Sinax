from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

from .models import Application
from .serializers import ApplicationCreateSerializer
from .services import send_telegram_notification


@extend_schema(
    tags=['Applications'],
    summary='Yangi ariza yuborish',
)
class ApplicationCreateView(CreateAPIView):
    """
    POST /api/v1/applications/
    """
    serializer_class = ApplicationCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        application = serializer.save()

        send_telegram_notification(application)

        return Response(
            {'detail': 'Arizangiz qabul qilindi!'},
            status=status.HTTP_201_CREATED
        )