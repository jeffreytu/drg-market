# Generated by Django 3.0.6 on 2020-08-07 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0032_auto_20200802_0504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='listing_code',
            field=models.CharField(blank=True, default=0, max_length=8, null=True),
        ),
    ]
