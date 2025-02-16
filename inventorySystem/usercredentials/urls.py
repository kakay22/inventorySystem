from django.contrib import admin # type: ignore
from django.urls import path, include #type: ignore
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('logout_view', views.logout_view, name='logout_view'),
]
