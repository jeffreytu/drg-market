# Generated by Django 3.0.6 on 2020-08-02 04:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0028_listing_listing_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='listing_id',
        ),
    ]
