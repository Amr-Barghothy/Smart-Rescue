from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Home page with login/register
    path('createuserform', views.create_user_form, name='createuserform'),  # Registration POST
    path('loginuserform', views.login_user_form, name='loginuserform'),    # Login POST
    path('dashboard', views.display_dashboard, name='dashboard'),          # User dashboard
    path('logoutform', views.logout_form, name='logoutform'),    
    path('about', views.about,name='about'),
    path('aboutus', views.about_view,name='aboutus'),
    path('create_case', views.create_case_page),
    path('services', views.show_services, name='services'),
    path('volunteer', views.volunteer),
    path('report_case', views.report_case, name='report_case'),

]