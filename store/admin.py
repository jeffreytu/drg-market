from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Product, Listing, Comment, Gallery, Category


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title']

admin.site.register(Product, ProductAdmin)

class GalleryAdmin(admin.StackedInline):
    model = Gallery

class ListingAdmin(admin.ModelAdmin):
    list_display = ['seller','category','title','price']
    inlines = [GalleryAdmin]
admin.site.register(Listing, ListingAdmin)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'body', 'listing', 'created_on')
    list_filter = ['created_on']
    search_fields = ('author', 'body')

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Category, MPTTModelAdmin)