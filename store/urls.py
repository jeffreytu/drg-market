from django.urls import path
from .views import *

urlpatterns = [
    path('', shopHome, name='home'),
    path('dash/', userHome, name='user-home'),
    path('sell/', createListing, name='create-listing'),
    path('shop/', shopHome, name='shop-home'),
    path('shop/<slug:the_slug>/', productCategoryView, name='product-category'),
    path('shop/listing/<int:listing_id>/', productListingDetail, name='product-listing'),
    path('shop/listing/<int:listing_id>/edit/', editListing, name='edit-listing'),
    path('shop/listing/<int:listing_id>/remove/', deleteListing, name='remove-listing'),
    path('shop/listing/<int:listing_id>/buy/', buyListing, name='buy-listing'),
    path('shop/listing/<int:listing_id>/buy/complete', transaction, name='buy-transaction'),
]