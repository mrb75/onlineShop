# Generated by Django 4.0.8 on 2023-03-10 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestlog',
            name='url',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='requestlog',
            name='user_agent',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
