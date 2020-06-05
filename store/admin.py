from django.contrib import admin
from .models import Product, Listing

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title']

admin.site.register(Product, ProductAdmin)

class ListingAdmin(admin.ModelAdmin):
    list_display = ['seller','category','title','price']
admin.site.register(Listing, ListingAdmin)