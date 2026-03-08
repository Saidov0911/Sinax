from django.urls import path
from .views import (
    ProductCategoryListView,
    ProductCategoryDetailView,
    ProductListView,
    ProductDetailView,
    ProductListByCategoryView,  # yangi
)


urlpatterns = [
    path('', ProductListView.as_view(), name='product-list'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('categories/', ProductCategoryListView.as_view(), name='category-list'),
    path('categories/<slug:slug>/', ProductCategoryDetailView.as_view(), name='category-detail'),

    # Har kategoriya uchun alohida URL
    path('masketnitiysetka/', ProductListByCategoryView.as_view(), {'slug': 'masketniysetka'}, name='masketniysetka-list'),
    path('jalyuzi/', ProductListByCategoryView.as_view(), {'slug': 'jalyuzi'}, name='jalyuzi-list'),
    path('kabinka/', ProductListByCategoryView.as_view(), {'slug': 'kabinka'}, name='kabinka-list'),
]