# Generated by Django 4.0.8 on 2023-01-23 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='mobile',
            field=models.CharField(max_length=14),
        ),
    ]