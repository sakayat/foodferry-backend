# Generated by Django 5.0.7 on 2024-08-19 15:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0002_foodcategory_fooditem'),
    ]

    operations = [
        migrations.AddField(
            model_name='fooditem',
            name='restaurant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='foods', to='restaurant.restaurant'),
        ),
    ]