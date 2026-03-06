from django.urls import path
from .views import (
    ProductCategoryListView,
    ProductCategoryDetailView,
    ProductListView,
    ProductDetailView,
)

urlpatterns = [
    path('', ProductListView.as_view(), name='product-list'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('categories/', ProductCategoryListView.as_view(), name='category-list'),
    path('categories/<slug:slug>/', ProductCategoryDetailView.as_view(), name='category-detail'),
]