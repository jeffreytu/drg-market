# Generated by Django 3.0.6 on 2020-06-03 04:47

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20200603_0431'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='seller',
        ),
        migrations.AddField(
            model_name='product',
            name='seller',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
