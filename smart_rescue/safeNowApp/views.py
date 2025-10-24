import base64
import os

import openai
from django.shortcuts import render, redirect
from django.http import JsonResponse
from datetime import datetime
from django.contrib import messages
from django.shortcuts import render
from .models import *
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
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
            {"title": "AI Assistance",
             "description": "Our AI translates voice to text and helps categorize cases for quick processing."},
            {"title": "Quality Assurance",
             "description": "Rate and review services to maintain high standards of emergency response."},
            {"title": "Community Driven",
             "description": "Volunteers can register and contribute their skills to help those in need."},
            {"title": "User-Friendly Interface",
             "description": "Simple, intuitive design for easy navigation."},
            {"title": "Multi-Language Support",
             "description": "Accessible in multiple languages for wider usability."},
        ],
        "extra_text": [
            {"title": "Safety First",
             "description": "Every decision we make prioritizes the safety and well-being of workers and rescuers"},
            {"title": "Innovation",
             "description": "Leveraging cutting-edge technology to improve emergency response capabilities"},
            {"title": "Collaboration",
             "description": "Building strong partnerships between authorities, volunteers, and communities"},
        ],
        "core_values": [
            {"title": "Accessibility", "description": "Making emergency reporting easy for everyone, anywhere."},
            {"title": "Transparency", "description": "Keeping users informed about the status of their reports."},
            {"title": "Innovation", "description": "Leveraging AI and smart technology to improve emergency services."},
            {"title": "Empathy", "description": "Understanding the urgency of emergencies and prioritizing human life."},
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


def volunteer(request):
    
    if not "user_id" in request.session:
        messages.error(request, "You need to login first")
        return redirect(index)
    return render(request, 'volunteer.html')

def volunteer_service_submit(request):
    if request.method == "POST":
        errors = User.objects.basic_validator_volunteer(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(volunteer)
        else:
            create_volunteer(request.POST)
            messages.success(request, "You have successfully registered as a volunteer")
            return redirect(volunteer)
    return render(request,'services.html')

def become_a_volunteer(request):
    if request.method == "POST":
        errors = User.objects.basic_validator_volunteer(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(volunteer)
        else:
            create_volunteer(request.POST)
            messages.success(request, "You have successfully registered as a volunteer")
            return redirect(volunteer)
    return render(request, 'volunteer.html')
        
def cancel_service(request):
    if request.method == "POST":
        errors = User.objects.basic_validator_volunteer(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(volunteer)
        else:
            cancel_volunteer(request.POST)
            messages.success(request, "You have successfully canceled your volunteer service")
            return redirect(volunteer)



    



    





def report_case(request):
    if not "user_id" in request.session:
        messages.error(request, "You need to login first")
        return redirect(index)
    errors = CaseEmergency.objects.emergency_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(create_case_page)
    if request.method == "POST":
        text_description = request.POST.get("description", "")
        audio_data = request.POST.get("audio_data")
        image = request.FILES.get("image")
        if audio_data:
            header, encoded = audio_data.split(",", 1)
            audio_bytes = base64.b64decode(encoded)
            audio_text = transcribe_audio(audio_bytes)
            text_description += " " + audio_text
            # ai_response = text_analysis(text_description)
        create_case(request.POST, image, audio_data, text_description)
        return redirect(create_case_page)

    return render(request, 'create_case.html')


load_dotenv()
api_key = os.getenv("ELEVENLABS_API_KEY")
client = ElevenLabs(api_key=api_key)


def transcribe_audio(audio_bytes):
    result = client.speech_to_text.convert(
        file=audio_bytes,
        model_id="scribe_v1",
        diarize=True,
        timestamps_granularity="word"

    )
    print(result)
    print(result.text)
    return result.text


def text_analysis(text):
    deep_api = os.getenv("DEEP_SEEK_API_KEY")
    deepseek = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=deep_api,
    )

    completion = deepseek.chat.completions.create(
        extra_headers={
            "HTTP-Referer": "<YOUR_SITE_URL>",  # Optional. Site URL for rankings on openrouter.ai.
            "X-Title": "<YOUR_SITE_NAME>",  # Optional. Site title for rankings on openrouter.ai.
        },
        extra_body={},
        model="deepseek/deepseek-chat-v3.1:free",
        messages=[
            {
                "role": "user",
                "content": text
            }
        ]
    )
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content

def success_description(request):
    if request.method == "POST":
        description = request.POST.get("description")
        return render(request, "success_description.html", {"description": description})
    return render(request, "create_case.html")

def chat_ai(request):
    if request.method == "POST":
        user_message = request.POST.get("message")
        case_description = request.POST.get("case_description")

        prompt = f"""
        You are Smart Rescue Assistant. 
        The user reported this case: "{case_description}".
        Now they said: "{user_message}".
        Give them advice and helpful guidance related to the case.
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": "You are a helpful emergency advisor."},
                          {"role": "user", "content": prompt}]
            )

            ai_reply = response.choices[0].message.content
            return JsonResponse({"reply": ai_reply})

        except Exception as e:
            return JsonResponse({"reply": f"⚠️ Error: {str(e)}"})
    # if request.method == "POST":
    #     text_description = request.POST.get("description", "")
    #     ai_response = text_analysis(text_description)
    #     return render(request, 'success.html', {'description': ai_response})
