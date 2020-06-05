from django.contrib import admin
from .models import Product, Listing

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title']

admin.site.register(Product, ProductAdmin)

admin.site.register(Listing)