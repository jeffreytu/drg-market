from django.urls import path
from .views import *
from users.views import *

urlpatterns = [
    
    path('', shopHome, name='home'),
    path('profile/', userProfileView, name='user-profile'),
    path('profile/<str:seller>/', userView, name='view-seller'),
    path('dash/', userHome, name='user-home'),
    path('sell/', createListing, name='create-listing'),
    path('shop/', shopHome, name='shop-home'),
    path('shop/phones/', shopPhones, name='shop-phones'),
    path('shop/<slug:the_slug>/', productCategoryView, name='product-category'),
    path('shop/listing/<int:listing_id>/', productListingDetail, name='product-listing'),
    path('shop/listing/<int:listing_id>/edit/', editListing, name='edit-listing'),
    path('shop/listing/<int:listing_id>/remove/', deleteListing, name='remove-listing'),
    path('shop/listing/<int:listing_id>/buy/', buyListing, name='buy-listing'),
    path('shop/listing/<int:listing_id>/buy/complete', transaction, name='buy-transaction'),
]