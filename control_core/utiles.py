from django.db import transaction
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from control_core.models import Car
from control_account.models import PersonalDetails
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
def ready_car_for_rent(user, car_id: int, req) -> None:
    """
    Update the car availability and renters count.
    """
    car = get_object_or_404(Car, id=car_id)
    car.people_rent_it.add(user)
    car.people_counter = F('people_counter') + 1
    car.save()

@transaction.atomic
def per_info_save(user, fullname, nationality, phoneno, email) -> None:
    """
    Add personal information for an order
    """
    p_data = PersonalDetails.objects.create(
        full_name=fullname,
        nationality=nationality,
        phone_no=phoneno,
        email=email,
        user=user
    )
    p_data.save()