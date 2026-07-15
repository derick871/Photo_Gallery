from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages

def register(request):
    if request.user.is_authenticated:
        return redirect('gallery_home')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Validation checks
        if User.objects.filter(username=username).exists():
            messages.error(request, "This username is already taken.")
            return render(request, 'register.html')
            
        if User.objects.filter(email=email).exists():
            messages.error(request, "An account with this email already exists.")
            return render(request, 'register.html')
            
        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return render(request, 'register.html')
            
        # Create user and log them in
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        messages.success(request, "Account created successfully!")
        return redirect('gallery_home')
        
    return render(request, 'register.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('gallery_home')
        
    if request.method == 'POST':
        username_input = request.POST.get('username')
        password_input = request.POST.get('password')
        
        # Authenticate using the username
        user = authenticate(request, username=username_input, password=password_input)
        
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('gallery_home')
        else:
            messages.error(request, "Invalid username or password.")
            
    return render(request, 'login.html')


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, "You have been logged out.")
    return redirect('login')

def edit_profile(request):
    if request.method == 'post':
        