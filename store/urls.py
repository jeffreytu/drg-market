from django.urls import path
from .views import *

urlpatterns = [
    path('', productList, name='product-list'),
    path('<str:sku>/', productDetail, name='product-detail'),
]