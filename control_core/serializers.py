from rest_framework import serializers
from control_core.models import Car, CarRent
from control_core.utiles import mail_sender, ready_car_for_rent
from django.db import transaction
#----------------------- Serilizers logic implementation ----------------------- #

class CarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Car
        fields = ("id", "image", "name", "speed", "color", "available_for_city", "available_from", "available_till", "rent_price")
        
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
    class Meta:
        model = CarRent
        fields = "__all__"

    def create(self, validated_data):
        """
        Create and return a new `CarRent` instance, given the validated data.
        """
        user = self.context['request'].user
        car = validated_data['car']
        
        with transaction.atomic():
            instance = CarRent.objects.create(
                customer=user,
                car=car,
                days=validated_data['days'],
                rent_start_from=validated_data['rent_start_from'],
                rent_end_from=validated_data['rent_end_from'],
                total_rent_price=validated_data['total_rent_price'],
                city_location=validated_data['city_location']
            )
            ready_car_for_rent(user, car.id)
            # mail_sender(user)
        
        return instance
    

class CarUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Car
        fields = ("id", "image", "name", "speed", "color", "available_for_city", "available_from", "available_till", "rent_price")
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

        instance.save()
        return instance