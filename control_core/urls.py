from django.urls import path
from control_core.views import OrderAgent, ShowCarDetail, AddCars, ListSearchableCar, RentAgent, DeleteCar, CarUpdateView, FilterCars


urlpatterns = [
    # Add Cars
    path('public/add/cars', AddCars.as_view()),
    # Update Cars
    path('public/update/cars', CarUpdateView.as_view()),
    # Delete Cars
    path('public/delete/cars', DeleteCar.as_view()),
    # OPtional APi
    path('public/show/cars', ListSearchableCar.as_view()),
    # Api to work as an agent for rent a car
    path('public/rent/cars', RentAgent.as_view()),
    # Show All Cars by passing cars
    path('public/filter/cars', FilterCars.as_view()),

    # Show A specific car details
    path('public/show-car-details/<int:car_id>/', ShowCarDetail.as_view()),
    path('public/show-orders', OrderAgent.as_view()),
  
]
