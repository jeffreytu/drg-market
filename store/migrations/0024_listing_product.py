# Generated by Django 3.0.6 on 2020-06-28 22:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0023_remove_product_category_num'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.Product'),
        ),
    ]
