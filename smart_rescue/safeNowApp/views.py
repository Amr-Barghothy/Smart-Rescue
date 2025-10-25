import base64
import os
from io import BytesIO

import qrcode
from django.contrib import messages
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from openai import OpenAI
from django.utils import translation
from django.conf import settings
from django.utils.translation import gettext_lazy as _



def dashboard_view(request):
    cases = CaseEmergency.objects.all()
    return render(request, 'dashboard.html', {'cases': cases})


def about_view(request):
    return render(request, 'about.html')
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from .models import *


def about(request):
    user = get_user(request.session['user_id'])
    context = {
    "features": [
        {"title": _("Real-Time Reporting"),
         "description": _("Submit cases with text, voice, or image uploads for comprehensive incident documentation.")},
        {"title": _("AI Assistance"),
         "description": _("Our AI translates voice to text and helps categorize cases for quick processing.")},
        {"title": _("Quality Assurance"),
         "description": _("Rate and review services to maintain high standards of emergency response.")},
        {"title": _("Community Driven"),
         "description": _("Volunteers can register and contribute their skills to help those in need.")},
        {"title": _("User-Friendly Interface"),
         "description": _("Simple, intuitive design for easy navigation.")},
        {"title": _("Multi-Language Support"),
         "description": _("Accessible in multiple languages for wider usability.")},
    ],
    "extra_text": [
        {"title": _("Safety First"),
         "description": _("Every decision we make prioritizes the safety and well-being of workers and rescuers")},
        {"title": _("Innovation"),
         "description": _("Leveraging cutting-edge technology to improve emergency response capabilities")},
        {"title": _("Collaboration"),
         "description": _("Building strong partnerships between authorities, volunteers, and communities")},
    ],
    "core_values": [
        {"title": _("Accessibility"), "description": _("Making emergency reporting easy for everyone, anywhere.")},
        {"title": _("Transparency"), "description": _("Keeping users informed about the status of their reports.")},
        {"title": _("Innovation"), "description": _("Leveraging AI and smart technology to improve emergency services.")},
        {"title": _("Empathy"), "description": _("Understanding the urgency of emergencies and prioritizing human life.")},
    ],
       "user": user

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
    user = get_user(request.session['user_id'])
    if 'user_id' in request.session:
        context = {
            'current_year': datetime.now().year,
            'user': user,
            'cases': get_all_cases()
        }
        return render(request, 'dashboard.html', context)
    else:
        messages.error(request, 'You are not logged in.')
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


def create_case_page(request):
    user = get_user(request.session['user_id'])
    if not "user_id" in request.session:
        messages.error(request, "You need to login first")
        return redirect(index)
    context = {
        'user': user,
    }
    return render(request, 'create_case.html', context)


def show_services(request):
    if not "user_id" in request.session:
        messages.error(request, "You need to login first")
        return redirect(index)
    user = get_user(request.session['user_id'])
    context = {
        'user': user,
        'services': get_all_services()
    }
    return render(request, 'services.html', context)


def volunteer(request):
    if not "user_id" in request.session:
        messages.error(request, "You need to login first")
        return redirect(index)
    user = get_user(request.session['user_id'])
    if not user.is_volunteer:
        messages.error(request, "You don't have permission to do that.")
        return redirect(display_dashboard)
    return render(request, 'volunteer.html')


def volunteer_service_submit(request):
    if not "user_id" in request.session:
        messages.error(request, "You need to login first")
        return redirect(index)
    user = get_user(request.session['user_id'])
    if not user.is_volunteer:
        messages.error(request, "You don't have permission to do that.")
        return redirect(display_dashboard)
    if request.method == "POST":
        errors = User.objects.basic_validator_volunteer(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(volunteer)
        else:
            create_service(request.POST["title"], request.POST["description"], request.POST["location"],
                           request.POST["availability"], request.POST["category"], user)
            messages.success(request, "You have successfully registered as a volunteer")
            return redirect(show_services)
    return render(request, 'services.html')


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
        text_description = request.POST.get("text_description", "")
        audio_data = request.POST.get("audio_data")
        image = request.FILES.get("image")
        if audio_data:
            header, encoded = audio_data.split(",", 1)
            audio_bytes = base64.b64decode(encoded)
            audio_text = transcribe_audio(audio_bytes)
            text_description += " " + audio_text
        if image:
            ai_response = image_analysis(image)
        else:
            ai_response = text_analysis(text_description)
        request.session["ai_response"] = ai_response
        request.session["text_description"] = text_description
        user = get_user(request.session['user_id'])
        case = create_case(request.POST, image, audio_data, text_description, user)
        pdf_buffer = BytesIO()
        pdf = canvas.Canvas(pdf_buffer, pagesize=A4)
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(100, 800, f"Case #{case.id}")
        pdf.setFont("Helvetica", 12)
        pdf.drawString(100, 770, "Description:")
        pdf.setFont("Helvetica", 11)
        pdf.drawString(120, 750, text_description[:800])
        pdf.save()
        pdf_buffer.seek(0)

        pdf_filename = f"case_{case.id}.pdf"
        case.pdf_file.save(pdf_filename, ContentFile(pdf_buffer.getvalue()))

        pdf_url = request.build_absolute_uri(case.pdf_file.url)
        qr = qrcode.make(pdf_url)
        qr_buffer = BytesIO()
        qr.save(qr_buffer, format="PNG")
        qr_buffer.seek(0)

        qr_filename = f"case_{case.id}_qr.png"
        case.qr_code.save(qr_filename, ContentFile(qr_buffer.getvalue()))

        case.save()
        messages.success(request, "Case created successfully with QR code!")
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
    if not deep_api:
        raise ValueError("DEEP_SEEK_API_KEY not found in environment variables.")

    deepseek = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=deep_api,
    )

    completion = deepseek.chat.completions.create(
        extra_headers={
            "HTTP-Referer": "<YOUR_SITE_URL>",
            "X-Title": "<YOUR_SITE_NAME>",
        },
        model="deepseek/deepseek-chat-v3.1:free",
        messages=[{"role": "user",
                   "content": f"You are a rescue bot the user is currently under a dangerous situation you should proived them with steps to help them calm down or fix the issue or at least control it till the help arrives this what the user is saying: {text}"}],
    )

    message = completion.choices[0].message
    content = message["content"] if isinstance(message, dict) else message.content

    print(content)
    return content


def image_analysis(image):
    deep_api = os.getenv("DEEP_SEEK_API_KEY")
    if not deep_api:
        raise ValueError("DEEP_SEEK_API_KEY not found in environment variables.")
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
                "content": [
                    {
                        "type": "text",
                        "text": "Analyis this image and give a steps to help with the problem in the image it can be a wound or something dangerous"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image,
                        }
                    }
                ]
            }
        ]
    )
    return completion.choices[0].message.content


def success_description(request):
    # if request.method == "POST":
    #     description = request.POST.get("description")
    return render(request, "success.html", {"description": "description"})


# return render(request, "create_case.html")


def chat_ai(request):
    if request.method != "POST":
        user_message = request.POST.get("message")
        case_description = request.POST.get("case_description")

        try:
            ai_reply = request.session["ai_response"]
            return JsonResponse({"reply": ai_reply})

        except Exception as e:
            return JsonResponse({"reply": f"⚠️ Error: {str(e)}"})
    # if request.method == "POST":
    #     text_description = request.POST.get("description", "")
    #     ai_response = text_analysis(text_description)
    #     return render(request, 'success.html', {'description': ai_response})
def set_language(request):
   lang = request.GET.get('lang', 'en')
   if lang in dict(settings.LANGUAGES):
       translation.activate(lang)
       request.session[translation.LANGUAGE_SESSION_KEY] = lang
   return redirect(request.META.get('HTTP_REFERER', '/'))
