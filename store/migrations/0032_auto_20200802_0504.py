# Generated by Django 3.0.6 on 2020-08-02 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0031_auto_20200802_0503'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='listing_code',
            field=models.CharField(blank=True, max_length=8, null=True),
        ),
    ]
