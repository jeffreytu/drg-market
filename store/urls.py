from django.urls import path
from .views import *

urlpatterns = [
    path('', productList, name='product-list'),
    path('sell/', createListing, name='create-listing'),
    path('<str:sku>/', productDetail, name='product-detail'),
    path('listing/<int:listing_id>/', productListingDetail, name='product-listing'),
]