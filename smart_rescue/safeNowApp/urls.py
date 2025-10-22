from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view),
    path('aboutus', views.about_view,name='aboutus'),
    path('about', views.about,name='about'),
]