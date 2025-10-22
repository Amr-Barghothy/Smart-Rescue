from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('dashboard' , views.display_dashboard)  ,
    # path('createuserform' , views.create_user_form),
    # path('registeruserform', views.create_user_form, name='registeruserform'),

    # path('loginuserform' , views.login_user_form),
    path('logoutform' , views.logout_form),
    path('register', views.register, name='register'),
    path('loginuserform', views.login_user_form, name='loginuserform'),
    path('createuserform', views.create_user_form, name='createuserform'),
]
    
    
