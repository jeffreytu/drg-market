# Generated by Django 3.0.6 on 2020-06-12 07:14

from django.db import migrations, models
import store.models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_listing_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
