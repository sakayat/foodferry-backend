# Generated by Django 5.0.7 on 2024-08-30 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0004_alter_foodfeedback_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodfeedback',
            name='rating',
            field=models.CharField(choices=[('⭐', 1), ('⭐⭐', 2), ('⭐⭐⭐', 3), ('⭐⭐⭐⭐', 4), ('⭐⭐⭐⭐⭐', 5)], default=1, max_length=20),
        ),
    ]