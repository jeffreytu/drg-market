from django.urls import path
from .views import *

urlpatterns = [
    path('home/', userHome, name='user-home'),
    path('list/', productList, name='product-list'),
    path('sell/', createListing, name='create-listing'),
    path('<str:sku>/', productDetail, name='product-detail'),
    path('listing/<int:listing_id>/', productListingDetail, name='product-listing'),
    path('listing/<int:listing_id>/edit/', editListing, name='edit-listing'),
    path('listing/<int:listing_id>/remove/', deleteListing, name='remove-listing'),
    path('listing/<int:listing_id>/buy/', buyListing, name='buy-listing'),
]