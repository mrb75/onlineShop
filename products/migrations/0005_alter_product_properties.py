# Generated by Django 4.0.8 on 2023-01-27 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_color_hex_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='properties',
            field=models.ManyToManyField(blank=True, to='products.value'),
        ),
    ]
