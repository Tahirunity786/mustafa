# Generated by Django 5.0.4 on 2024-05-25 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_core', '0007_alter_car_reviews'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='reviews',
            field=models.DecimalField(db_index=True, decimal_places=1, max_digits=5, null=True),
        ),
    ]
