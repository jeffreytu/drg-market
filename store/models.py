from django.db import models
from users.models import CustomUser

# Create your models here.
class Product(models.Model):

    PROD_CATEGORY = (
        (-1, 'Unassigned'),
        (2, 'Apple iPhone 11'),
        (3, 'Samsung Galaxy S20'),
    )

    sku = models.CharField('SKU', max_length=30, null=True, blank=False)
    title = models.CharField('Title', max_length=80, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    category_num = models.IntegerField('Category Number', choices=PROD_CATEGORY, default=-1)

    def __str__(self):
        return self.get_category_num_display()

class Listing(models.Model):

    def img_directory_path(instance, filename):
        return 'l_{0}/{1}'.format(instance.id, filename)

    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField('Title', max_length=80, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    images = models.ImageField(null=True, blank=True, upload_to=img_directory_path)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    category = models.ForeignKey(Product, on_delete=models.CASCADE, default=-1)

    def __str__(self):
        return self.title


class Gallery(models.Model):

    def img_directory_path(instance, filename):
        return 'l_{0}/{1}'.format(instance.listing.id, filename)

    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    image = models.FileField(upload_to=img_directory_path, blank=True, null=True)

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    body = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.author)