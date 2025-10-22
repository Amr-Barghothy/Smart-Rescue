from django.urls import path
from . import views

urlpatterns = [
    path('dashboard', views.dashboard_view),
    path('aboutus', views.about_view,name='aboutus'),
    path('about', views.about,name='about'),
    path('', views.index),
    path('create_case', views.create_case_page),
]