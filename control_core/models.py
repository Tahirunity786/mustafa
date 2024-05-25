from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Car(models.Model):
    image = models.ImageField(upload_to="cars", default="", db_index=True)
    people_rent_it = models.ManyToManyField(User, default="", db_index=True)
    people_counter = models.PositiveIntegerField(db_index=True, default=0)
    name = models.CharField(max_length=100, db_index=True, default="")
    speed = models.CharField(max_length=100, db_index=True, default="")
    color = models.CharField(max_length=100, db_index=True, default="")
    model = models.CharField(max_length=100, db_index=True, default="")
    seats = models.PositiveIntegerField(db_index=True, default=2)
    bags_capcity = models.PositiveIntegerField(db_index=True, default=1)
    available_for_city = models.CharField(max_length=100, db_index=True, default="")
    available_from = models.DateField(db_index=True, default=timezone.now)
    available_till = models.DateField(db_index=True, default="")
    rent_price = models.PositiveIntegerField(db_index=True, default=0)
    reviews = models.DecimalField(max_digits=5, decimal_places=1, db_index=True, null=True)

class CarRent(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    car = models.ForeignKey(Car, on_delete=models.CASCADE, default="")
    days = models.PositiveIntegerField(default=0, db_index=True)
    total_rent_price = models.PositiveIntegerField(default=0, db_index=True)
    city_location = models.CharField(max_length=200, db_index=True, default="")
    rental_start_date = models.DateField(db_index=True, default=timezone.now)

class CarReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="", db_index=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, default="", db_index=True)
    rating = rating = models.DecimalField(max_digits=5, decimal_places=1, db_index=True)
    experience = models.TextField(db_index=True, default="")

class Orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    rent_car_by_user = models.ForeignKey('Car', related_name="car_orders", on_delete=models.CASCADE, default=0)
    date_ordered = models.DateField(auto_now_add=True, db_index=True)
    total_price = models.PositiveBigIntegerField(db_index=True, default=0)
    total_days = models.PositiveIntegerField(db_index=True, default=0)


    def __str__(self):
        return f"Order {self.id} by {self.user.username}"