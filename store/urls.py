from django.urls import path
from .views import *

urlpatterns = [
    path('products/', productList, name='product-list'),
    path('products/detail/', productDetail, name='product-detail'),
]