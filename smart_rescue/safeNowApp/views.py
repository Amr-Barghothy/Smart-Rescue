from django.shortcuts import render,redirect
from . import models
from datetime import datetime
from django.contrib import messages

# Create your views here.


def index(request):
    context = {
    'current_year': datetime.now().year
    }
    return render(request, 'index.html', context)

def create_user_form(request):
    if request.method == 'POST':
        errors = models.User.objects.basic_validator_reg(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            print("Errors") 
            return redirect('/')    
        else:
            new_user = models.create_user(request.POST)
            request.session['user_id'] = new_user.id
            return redirect('/dashboard')
    else:
        return render(request, 'index.html')

def display_dashboard(request):
    if 'user_id' in request.session:
        context = {
            
            'current_year': datetime.now().year,
        }
        return render(request, 'dashboard.html', context)
    else:
        return redirect('/')

def logout_form(request):
    if 'user_id' in request.session:
        del request.session['user_id']
        return redirect('/')
    else:
        return redirect('/')
    
def login_user_form(request):
    if request.method == 'POST':
        errors = models.User.objects.basic_validator_login(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = models.login_user(request.POST, request.session)
        if user:
            return redirect('/dashboard')
        else:
            messages.error(request, "Invalid email or password")
            return redirect('/')

        
    
    
    
def register(request):
    return create_user_form(request)