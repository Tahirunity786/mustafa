from rest_framework import serializers
from control_core.models import Car, CarRent, CarReview, Orders
from control_core.utiles import per_info_save, ready_car_for_rent
from django.db import transaction
from datetime import timedelta
from django.utils import timezone
from django.core.exceptions import ValidationError
#----------------------- Serilizers logic implementation ----------------------- #

class CarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Car
        fields = ("id", "image", "name","reviews", "speed", "color","model", "seats", "bags_capcity" ,"available_for_city", "available_from", "available_till", "rent_price")
        
        extra_kwargs = {
            'id': {'required': True},
            'image': {'required': True},
            'name': {'required': True},
            'speed': {'required': True},
            'color': {'required': True},
            'available_for_city': {'required': True},
            'available_from': {'required': True},
            'available_till': {'required': True},
            'rent_price': {'required': True},
        }
        
class CarRentAgentSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(write_only=True)
    nationality = serializers.CharField(write_only=True)
    phoneno = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    rental_start_date = timezone.now().date()
    days = serializers.IntegerField(write_only=True)

    class Meta:
        model = CarRent
        fields = "__all__"

    def validate(self, data):
        """
        Check that the car is available for booking and that the rental period is valid.
        """
        car = data.get('car')
        rental_days = data.get('days')
        
        rental_end_date = self.rental_start_date + timedelta(days=rental_days)
        
        if CarRent.objects.filter(car=car, city_location=data.get('city_location')).exists():
            raise ValidationError("This car is already booked by another user.")
        
        if self.rental_start_date < car.available_from or rental_end_date > car.available_till:
            raise ValidationError(f"This car is only available from {car.available_from} to {car.available_till}.")

        return data

    def create(self, validated_data):
        """
        Create and return a new `CarRent` instance, given the validated data.
        """
        user = self.context['request'].user
        car = validated_data.pop('car')
        fullname = validated_data.pop('fullname')
        nationality = validated_data.pop('nationality')
        phoneno = validated_data.pop('phoneno')
        email = validated_data.pop('email')
        total_rent_price = validated_data.pop('total_rent_price')
       
        days = validated_data.pop('days')
        
        
        
        with transaction.atomic():
            instance = CarRent.objects.create(
                customer=user,
                car=car,
                days=days,
                total_rent_price=total_rent_price,
                rental_start_date=self.rental_start_date,
                city_location=validated_data['city_location']
            )
            ready_car_for_rent(user, car.id, req=self.context['request'])
            per_info_save(user, fullname, nationality, phoneno, email)

        return instance
    

class CarUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Car
        fields = ("id", "image", "name", "speed", "color", "available_for_city", "available_from", "available_till", "rent_price", 'reviews')
        read_only_fields = ("id",)  # ID should be read-only, as it's not updated

    def update(self, instance, validated_data):
        """
        Update and return an existing `Car` instance, given the validated data.
        """
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.speed = validated_data.get('speed', instance.speed)
        instance.color = validated_data.get('color', instance.color)
        instance.available_for_city = validated_data.get('available_for_city', instance.available_for_city)
        instance.available_from = validated_data.get('available_from', instance.available_from)
        instance.available_till = validated_data.get('available_till', instance.available_till)
        instance.rent_price = validated_data.get('rent_price', instance.rent_price)
        instance.reviews = validated_data.get('reviews', instance.reviews)

        instance.save()
        return instance

class CarReviews(serializers.ModelSerializer):
    class Meta:
        model = CarReview
        fields = ("id","rating")

class CarDetails(serializers.ModelSerializer):

    car_reviews = CarReviews(many = True, read_only= True)
    class Meta:
        model = Car
        fields = ("id", "image", "name", "speed", "color","model","seats","bags_capcity", "available_for_city","reviews", "available_from", "available_till", "rent_price", "car_reviews")
    

class OrderSerializer(serializers.ModelSerializer):
    car = CarSerializer(read_only=True)
    remaining_days = serializers.SerializerMethodField()

    class Meta:
        model = CarRent
        fields = ("id", "car", "days", "rental_start_date", "total_rent_price", "city_location", "remaining_days")

    def get_remaining_days(self, obj):
        return obj.remaining_days()