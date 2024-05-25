# Generated by Django 5.0.4 on 2024-05-25 06:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_core', '0004_orders_total_days_orders_total_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='rent_car_by_user',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='car_orders', to='control_core.car'),
        ),
    ]
