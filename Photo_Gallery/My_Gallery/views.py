from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.contrib import messages

# Create your views here.
def register(request):
    return render(request, 'register.html')
