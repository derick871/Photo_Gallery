from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, "index.html")

def register(request):
    return render(request, 'register.html')

def login(request):
    return render(request, 'login.html')

def edit_profile(request):
    return render(request, 'edit_profile.html')

def profile(request):
    return render(request, 'profile')

def photo_details(request):
    return render(request, 'photo_details')



