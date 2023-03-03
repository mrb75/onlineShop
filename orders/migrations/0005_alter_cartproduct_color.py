# Generated by Django 4.0.8 on 2023-02-09 17:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_product_properties'),
        ('orders', '0004_alter_cartproduct_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartproduct',
            name='color',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.color'),
        ),
    ]