# Generated by Django 3.0.6 on 2020-06-05 01:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_auto_20200605_0127'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='category',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, to='store.Product'),
        ),
    ]
