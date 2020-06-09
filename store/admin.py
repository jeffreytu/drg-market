from django.contrib import admin
from .models import Product, Listing, Comment

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title']

admin.site.register(Product, ProductAdmin)

class ListingAdmin(admin.ModelAdmin):
    list_display = ['seller','category','title','price']
admin.site.register(Listing, ListingAdmin)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'body', 'listing', 'created_on')
    list_filter = ['created_on']
    search_fields = ('author', 'body')