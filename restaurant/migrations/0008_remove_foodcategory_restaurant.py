# Generated by Django 5.0.7 on 2024-08-22 10:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0007_foodcategory_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='foodcategory',
            name='restaurant',
        ),
    ]
