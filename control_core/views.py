# Copyright 2024

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated

# Serializers
from control_core.serializers import CarSerializer, CarRentAgentSerializer, CarUpdateSerializer, CarDetails

# DB Models
from control_core.models import Car

# Django utiles 
from django.db.models import Q
from django.utils.dateparse import parse_date
from django.shortcuts import get_object_or_404
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

class FilterCars(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        city = request.data.get("city")
        date = request.data.get("date")
        parsed_date = parse_date(date)
      
        if not city and not parse_date:
            return Response({"Error":"City and date not given"}, status = status.HTTP_400_BAD_REQUEST)

        try:
            car_data = Car.objects.filter(available_for_city=city, available_from__lte=parsed_date, available_till__gte=parsed_date)
            serializers = CarDetails(car_data, many=True)  # Note `many=True` since car_data is a queryset
            return Response(serializers.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



class RentAgent(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Pass request object to serializer context
        serializers = CarRentAgentSerializer(data=request.data, context={'request': request})
        
        if serializers.is_valid():
            serializers.save()
            
            
            response = {
                "success": "Thank you for choosing our service. Please contact our customer service for more details."
            }
    
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            return Response(data=serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        

class CarUpdateView(APIView):
    def post(self, request, format=None):
        pk = request.data.get('car_id')
        try:
            car = Car.objects.get(pk=pk)
        except Car.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CarUpdateSerializer(car, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DeleteCar(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        car_id = request.data.get('car_id')

        try:
            car = Car.objects.get(id = car_id)
        except:
            return Response({"Error":f"Car for this id {car_id} not found" }, status=status.HTTP_400_BAD_REQUEST)
        
        car.delete()

        return Response({"Success":"Car information deleted"}, status=status.HTTP_200_OK)

class ShowCarDetail(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        car_id = kwargs.get('car_id')
        if not car_id:
            return Response({'error': 'Car ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            car = get_object_or_404(Car, id=car_id)
        except Car.DoesNotExist:
            return Response({'error': 'Car not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CarDetails(instance=car)
        return Response(serializer.data, status=status.HTTP_200_OK)
        