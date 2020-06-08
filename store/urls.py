from django.urls import path
from .views import *

urlpatterns = [
    path('user/', userHome, name='user-home'),
    path('list/', productList, name='product-list'),
    path('sell/', createListing, name='create-listing'),
    path('<str:sku>/', productDetail, name='product-detail'),
    path('listing/<int:listing_id>/', productListingDetail, name='product-listing'),
]