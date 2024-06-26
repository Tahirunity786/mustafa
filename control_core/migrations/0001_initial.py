# Generated by Django 5.0.4 on 2024-05-18 05:40

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(db_index=True, default='', upload_to='cars')),
                ('people_counter', models.PositiveIntegerField(db_index=True, default=0)),
                ('name', models.CharField(db_index=True, default='', max_length=100)),
                ('speed', models.CharField(db_index=True, default='', max_length=100)),
                ('color', models.CharField(db_index=True, default='', max_length=100)),
                ('model', models.CharField(db_index=True, default='', max_length=100)),
                ('seats', models.PositiveIntegerField(db_index=True, default=2)),
                ('bags_capcity', models.PositiveIntegerField(db_index=True, default=1)),
                ('available_for_city', models.CharField(db_index=True, default='', max_length=100)),
                ('available_from', models.DateField(db_index=True, default=django.utils.timezone.now)),
                ('available_till', models.DateField(db_index=True, default='')),
                ('rent_price', models.PositiveIntegerField(db_index=True, default=0)),
                ('people_rent_it', models.ManyToManyField(db_index=True, default='', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CarRent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('days', models.PositiveIntegerField(db_index=True, default=0)),
                ('rent_start_from', models.DateField(db_index=True, default='')),
                ('rent_end_from', models.DateField(db_index=True, default='')),
                ('total_rent_price', models.PositiveIntegerField(db_index=True, default=0)),
                ('city_location', models.CharField(db_index=True, default='', max_length=200)),
                ('car', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='control_core.car')),
                ('customer', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CarReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.DecimalField(db_index=True, decimal_places=1, max_digits=5)),
                ('experience', models.TextField(db_index=True, default='')),
                ('car', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='control_core.car')),
                ('user', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='car',
            name='car_reviews',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='control_core.carreview'),
        ),
    ]
