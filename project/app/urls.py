from django.contrib import admin
from django.urls import path,include
from app.views import RegisterView,LoginView,GuestView,StatusView,ProfileView
from rest_framework.authtoken import views



urlpatterns = [
    path('register/',RegisterView.as_view()),
path('login/', LoginView.as_view()),
    path('guests/',GuestView.as_view()),
    path('all-status/',StatusView.as_view()),
    path('profile/',ProfileView.as_view())
]
