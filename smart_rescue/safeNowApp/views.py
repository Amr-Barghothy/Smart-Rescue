from django.shortcuts import render, redirect
from django.contrib import messages
# Create your views here.


def index(request):
    return render(request, 'index.html')


def create_case_page(request):
    if not "id" in request.session:
        messages.error(request, "You need to login first")
        return redirect(index)
    return render(request, 'create_case.html')