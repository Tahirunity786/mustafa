from django.urls import path
from control_core.views import AddCars, ListSearchableCar, RentAgent, DeleteCar, CarUpdateView, FilterCars


urlpatterns = [
    # Add Cars
    path('public/add/cars', AddCars.as_view()),
    # Update Cars
    path('public/update/cars', CarUpdateView.as_view()),
    # Delete Cars
    path('public/delete/cars', DeleteCar.as_view()),
    # Show All Cars 'Temporary
    path('public/show/cars', ListSearchableCar.as_view()),
    # Show All Cars 'Temporary
    path('public/rent/cars', RentAgent.as_view()),
    # Show All Cars 'Temporary
    path('public/filter/cars', FilterCars.as_view()),
  
]
