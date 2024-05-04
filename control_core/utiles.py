from django.db import transaction
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from control_core.models import Car
from django.db.models import F

def mail_sender(user) -> None:
    """
    Send email notification.
    """
    send_mail(
        'Car Rent Confirmation',
        'Your car rent request has been confirmed.',
        'from@example.com',
        [user.email],
        fail_silently=False,
    )


@transaction.atomic
def ready_car_for_rent(user, car_id: int) -> None:
    """
    Update the car availability and renters count.
    """
    car = get_object_or_404(Car, id=car_id)
    car.people_rent_it.add(user)
    car.people_counter = F('people_counter') + 1
    car.save()

