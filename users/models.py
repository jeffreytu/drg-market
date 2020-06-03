from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    first_name = models.CharField('First Name', max_length=255, null=True, blank=True)
    last_name = models.CharField('Last Name', max_length=255, null=True, blank=True)

    def __str__(self):
        return self.username