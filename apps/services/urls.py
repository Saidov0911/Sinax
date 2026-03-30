from django.urls import path
from .views import ServiceListView, RepairPartListView

urlpatterns = [
    path('', ServiceListView.as_view(), name='service-list'),
    path('repair-parts/', RepairPartListView.as_view(), name='repair-part-list'),
]