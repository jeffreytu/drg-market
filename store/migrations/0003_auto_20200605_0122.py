# Generated by Django 3.0.6 on 2020-06-05 01:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20200605_0040'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='date_created',
        ),
        migrations.RemoveField(
            model_name='product',
            name='seller',
        ),
        migrations.RemoveField(
            model_name='product',
            name='sku',
        ),
        migrations.RemoveField(
            model_name='product',
            name='updated_at',
        ),
    ]
