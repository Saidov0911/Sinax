from django.urls import path
from .views import SpecialistListView

urlpatterns = [
    path('', SpecialistListView.as_view(), name='specialist-list'),
]