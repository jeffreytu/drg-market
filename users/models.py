from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    first_name = models.CharField('First Name', max_length=255, null=True, blank=True)
    last_name = models.CharField('Last Name', max_length=255, null=True, blank=True)

    def __str__(self):
        return self.username

class Product(models.Model):
    seller = models.ManyToManyField(CustomUser)
    sku = models.CharField('SKU', max_length=30, null=True, blank=False)
    title = models.CharField('Title', max_length=80, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    category_num = models.IntegerField('Category Number', default=-1)
    date_created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.sku
