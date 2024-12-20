# Generated by Django 5.0.7 on 2024-10-29 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_order_payment_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Completed', 'Completed'), ('Canceled', 'Canceled'), ('Paid', 'Paid')], default='Pending', max_length=30),
        ),
    ]
