# Generated by Django 5.0.4 on 2024-05-25 16:39

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_core', '0011_alter_carrent_rental_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carrent',
            name='rental_start_date',
            field=models.DateField(blank=True, db_index=True, default=django.utils.timezone.now, null=True),
        ),
    ]
