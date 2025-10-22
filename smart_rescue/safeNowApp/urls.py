from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('create_case', views.create_case_page),
]