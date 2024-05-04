# Copyright 2024

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, AllowAny

# Serializers
from control_core.serializers import CarSerializer

# DB Models
from control_core.models import Car

# User detection
User = get_user_model()

##################################### Car Rent #####################################

class AddCars(generics.CreateAPIView):
    # Queryset for model
    queryset = Car.objects.all()

    # Only Authenticated user allowed to access 
    permission_classes = [IsAuthenticated]

    # Seralizer
    serializer_class = CarSerializer



class ListSearchableCar(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Fetch all car instances from the database
        cars = Car.objects.all()
        
        # Serialize the car instances
        serializer = CarSerializer(cars, many=True)
        
        # Return the serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)

class RentAgent(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        # Not serializable data
        serializers = CarSerializer(data=request.data)

        if serializers.is_valid():
            serializers.save()

            response = {
                "success":"Thank for choosing our service, Please contact our customer service for more details"
            }

            return Response(data=response, status=status.HTTP_200_OK)
        else:
            return Response(data=serializers.errors, status=status.HTTP_400_BAD_REQUEST)




