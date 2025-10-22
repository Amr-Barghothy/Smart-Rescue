from django.shortcuts import render,redirect
from . import models
from datetime import datetime
from django.contrib import messages

# Create your views here.
from django.shortcuts import render
from .models import *     


def dashboard_view(request):
    cases = CaseEmergency.objects.all()
    return render(request, 'dashboard.html', {'cases': cases})
def about_view(request):
    return render(request, 'about.html')



def about(request):
    context = {
        "features": [
            { "title": "Real-Time Reporting", "description": "Submit cases with text, voice, or image uploads for comprehensive incident documentation."},
            {"title": "Quality Assurance", "description": "Rate and review services to maintain high standards of emergency response."},
            {"title": "Community Driven", "description": "Volunteers can register and contribute their skills to help those in need."},
        ],
        "extra_text": [
            {"title": "Safety First",
             "description": "Every decision we make prioritizes the safety and well-being of workers and rescuers"},
            {"title": "Innovation",
             "description": "Leveraging cutting-edge technology to improve emergency response capabilities"},
            {"title": "Collaboration",
             "description": "Building strong partnerships between authorities, volunteers, and communities"},
        ],
    }
    return render(request, "about.html", context)


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
    return render(request, 'index.html')


def create_case_page(request):
    if not "id" in request.session:
        messages.error(request, "You need to login first")
        return redirect(index)
    return render(request, 'create_case.html')
