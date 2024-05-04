from django.urls import path
from control_core.views import AddCars, ListSearchableCar


urlpatterns = [
    # Add Cars
    path('public/add/cars', AddCars.as_view()),
    # Show All Cars 'Temporary
    path('public/show/cars', ListSearchableCar.as_view()),
    
    # Show All Cars 'Temporary
    path('public/rent/cars', ListSearchableCar.as_view()),
  
]
