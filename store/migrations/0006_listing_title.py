# Generated by Django 3.0.6 on 2020-06-05 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_listing_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='title',
            field=models.CharField(blank=True, max_length=80, null=True, verbose_name='Title'),
        ),
    ]