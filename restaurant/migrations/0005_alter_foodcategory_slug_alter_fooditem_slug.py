# Generated by Django 5.0.7 on 2024-08-19 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0004_foodcategory_slug_fooditem_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodcategory',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='fooditem',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
