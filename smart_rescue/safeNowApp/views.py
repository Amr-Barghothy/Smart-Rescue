from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib import messages
from .models import *
import base64
from openai import OpenAI







def dashboard_view(request):
    cases = CaseEmergency.objects.all()
    return render(request, 'dashboard.html', {'cases': cases})


def about_view(request):
    return render(request, 'about.html')


def about(request):
    context = {
        "features": [
            {"title": "Real-Time Reporting",
             "description": "Submit cases with text, voice, or image uploads for comprehensive incident documentation."},
            {"title": "Quality Assurance",
             "description": "Rate and review services to maintain high standards of emergency response."},
            {"title": "Community Driven",
             "description": "Volunteers can register and contribute their skills to help those in need."},
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
        errors = User.objects.basic_validator_reg(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            print("Errors")
            return redirect('/')
        else:
            new_user = create_user(request.POST)
            request.session['user_id'] = new_user.id
            return redirect(display_dashboard)
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
        errors = User.objects.basic_validator_login(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = login_user(request.POST, request.session)
        if user:
            return redirect(display_dashboard)
        else:
            messages.error(request, "Invalid email or password")
            return redirect('/')


def register(request):
    return create_user_form(request)
    return render(request, 'index.html')


def create_case_page(request):
    if not "user_id" in request.session:
        messages.error(request, "You need to login first")
        return redirect(index)
    return render(request, 'create_case.html')


def show_services(request):
    if not "user_id" in request.session:
        messages.error(request, "You need to login first")
        return redirect(index)
    return render(request, 'services.html')


def report_case(request):
   if request.method == "POST":
       text_description = request.POST.get("description", "")
       audio_data = request.POST.get("audio_data")
       image = request.FILES.get("image")
       # If user recorded audio, convert Base64 to bytes and transcribe
       if audio_data:
           header, encoded = audio_data.split(",", 1)
           audio_bytes = base64.b64decode(encoded)
           # Transcribe with AI
           audio_text = transcribe_audio(audio_bytes)
           text_description += " " + audio_text  # Append transcription to description
       # Save report
       CaseEmergency.objects.create(
           title=request.POST.get("title"),
           category=request.POST.get("category"),
           authorities=request.POST.get("authorities"),
           lat=33.7490,
           long=-84.3880,
           description=text_description,
           image=image,
           audio=audio_bytes,
           status=request.POST.get("status"),
       )
       return redirect(create_case_page)
   return render(request, 'create_case.html')

def transcribe_audio(audio_bytes):
    
    response = OpenAI.Audio.transcribe.create(
        model="whisper-1",
        file=audio_bytes
    )
    return response['text']
           
