from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    first_name = models.CharField('First Name', max_length=255, null=True, blank=True)
    last_name = models.CharField('Last Name', max_length=255, null=True, blank=True)

    def __str__(self):
        return self.username

class UserAddress(models.Model):

    ADDRESS_TYPE = (
        (0, 'Home'),
        (1, 'Work'),
        (2, 'Other'),
    )

    STATE_CHOICES = (
        (-1,'Unassigned'),
        ('AK','Alaska'),
        ('AL','Alabama'),
        ('AR','Arkansas'),
        ('AS','American Samoa'),
        ('AZ','Arizona'),
        ('CA','California'),
        ('CO','Colorado'),
        ('CT','Connecticut'),
        ('DC','District of Columbia'),
        ('DE','Delaware'),
        ('FL','Florida'),
        ('GA','Georgia'),
        ('GU','Guam'),
        ('HI','Hawaii'),
        ('IA','Iowa'),
        ('ID','Idaho'),
        ('IL','Illinois'),
        ('IN','Indiana'),
        ('KS','Kansas'),
        ('KY','Kentucky'),
        ('LA','Louisiana'),
        ('MA','Massachusetts'),
        ('MD','Maryland'),
        ('ME','Maine'),
        ('MI','Michigan'),
        ('MN','Minnesota'),
        ('MO','Missouri'),
        ('MS','Mississippi'),
        ('MT','Montana'),
        ('NC','North Carolina'),
        ('ND','North Dakota'),
        ('NE','Nebraska'),
        ('NH','New Hampshire'),
        ('NJ','New Jersey'),
        ('NM','New Mexico'),
        ('NV','Nevada'),
        ('NY','New York'),
        ('OH','Ohio'),
        ('OK','Oklahoma'),
        ('OR','Oregon'),
        ('PA','Pennsylvania'),
        ('PR','Puerto Rico'),
        ('RI','Rhode Island'),
        ('SC','South Carolina'),
        ('SD','South Dakota'),
        ('TN','Tennessee'),
        ('TX','Texas'),
        ('UT','Utah'),
        ('VA','Virginia'),
        ('VI','Virgin Islands'),
        ('VT','Vermont'),
        ('WA','Washington'),
        ('WI','Wisconsin'),
        ('WV','West Virginia'),
        ('WY','Wyoming'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    type = models.IntegerField('Address Type', choices=ADDRESS_TYPE, default=0)
    default = models.BooleanField('Default')
    street1 = models.CharField('Street 1', max_length=255, null=True, blank=True)
    street2 = models.CharField('Street 2', max_length=255, null=True, blank=True)
    city = models.CharField('City', max_length=255, null=True, blank=True)
    state = models.CharField('State', max_length=2, null=True, blank=True, choices=STATE_CHOICES, default=-1)
    zipcode = models.CharField('Zip Code', max_length=10, null=True, blank=True)