from django.db import models
from users.models import CustomUser
from django.db.models.signals import post_save, pre_save
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.
class Product(models.Model):

    sku = models.CharField('SKU', max_length=30, null=True, blank=False)
    title = models.CharField('Title', max_length=80, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    category = TreeForeignKey('Category',null=True,blank=True, on_delete=models.CASCADE)

class Listing(models.Model):

    STATUS = (
        (0, 'Inactive'),
        (1, 'Active'),
        (2, 'Pending'),
        (3, 'Removed'),
        (4, 'Sold'),
    )

    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField('Title', max_length=80, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=False, null=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    category = TreeForeignKey('Category',null=True,blank=True, on_delete=models.CASCADE)
    status = models.IntegerField('Status', choices=STATUS, default=0)
    product = models.ForeignKey('Product', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Transaction(models.Model):

    STATUS = (
        (0, 'Incomplete'),
        (1, 'Complete'),
        (2, 'Pending'),
    )

    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='seller')
    buyer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='buyer')
    status = models.IntegerField('Status', choices=STATUS, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)


class Gallery(models.Model):

    def img_directory_path(instance, filename):
        return 'l_{0}/{1}'.format(instance.listing.id, filename)

    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    image = models.FileField(upload_to=img_directory_path, blank=True, null=True)

    def __str__(self):
        return self.image.name

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    body = models.TextField(blank=False, null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.author)

class Category(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(blank=True, null=True, default=None)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='product', blank=True, null=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name

# Signals
def update_listing(sender, instance, created, **kwargs):
    obj = Listing.objects.get(id=instance.listing.id)
    obj.status = 4
    obj.save()
post_save.connect(update_listing, sender=Transaction)

# def create_listing(sender, instance, *args, **kwargs):
# pre_save.connect(create_listing, sender=Listing)
