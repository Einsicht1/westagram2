from django.urls import path
from .views import SignUp, SignIn


urlpatterns = [
    path('/sign-in', SignIn.as_view()),
    path('/sign-up', SignUp.as_view()),
]

