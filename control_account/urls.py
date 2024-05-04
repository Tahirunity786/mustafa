from django.urls import path
from control_account.views import CreateUserView, UserLoginView

urlpatterns = [
    path('public/usr/register', CreateUserView.as_view()),
    path('public/usr/login', UserLoginView.as_view())
]
