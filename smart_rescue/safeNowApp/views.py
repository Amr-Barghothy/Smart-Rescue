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
    return render(request, 'index.html')


def create_case_page(request):
    if not "id" in request.session:
        messages.error(request, "You need to login first")
        return redirect(index)
    return render(request, 'create_case.html')
