from django.contrib import admin
from django.urls import path,include
from app.views import RegisterView


urlpatterns = [
    path('register/',RegisterView.as_view())
]
