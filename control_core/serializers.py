from rest_framework import serializers
from control_core.models import Car, CarRent

#----------------------- Serilizers logic implementation ----------------------- #

class CarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Car
        fields = ("id", "image", "name", "speed", "color", "available_for_city", "rating", "available_from", "available_till", "rent_price")
        extra_kwargs = {
            'id': {'required': True},
            'image': {'required': True},
            'name': {'required': True},
            'speed': {'required': True},
            'color': {'required': True},
            'available_for_city': {'required': True},
            'rating': {'required': True},
            'available_from': {'required': True},
            'available_till': {'required': True},
            'rent_price': {'required': True},
        }


class CarAgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarRent
        fields = "__all__"

        def create(self, validated_data):

             """
                Create and return a new `Snippet` instance, given the validated data.
            """
             return self.model.objects.create(**validated_data)