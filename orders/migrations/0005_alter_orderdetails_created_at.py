# Generated by Django 5.0.7 on 2024-10-27 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_orderdetails_created_at_orderdetails_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdetails',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default='2023-01-01 00:00:00'),
            preserve_default=False,
        ),
    ]
