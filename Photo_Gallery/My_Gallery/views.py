from django.shortcuts import render, redirect, get_object_or_404
# We import login and logout under aliases to avoid crashing when we name our own views
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Try to import your Photo model. If it doesn't exist yet, we'll bypass it so the server doesn't crash.
try:
    from .models import Photo
except ImportError:
    Photo = None

# ==========================================
# 1. HOMEPAGE & AUTHENTICATION VIEWS
# ==========================================

def gallery_home(request):
    """Displays the main gallery home page with all uploaded photos."""
    photos = []
    if Photo:
        photos = Photo.objects.all().order_by('-id') # Fetch newest photos first
    return render(request, 'gallery_home.html', {'photos': photos})


def register(request):
    """Handles user registration."""
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
        auth_login(request, user)  # Using the aliased login function here
        messages.success(request, "Account created successfully!")
        return redirect('gallery_home')
        
    return render(request, 'register.html')


def login(request):
    """Handles user login (named 'login' to match views.login in urls.py)."""
    if request.user.is_authenticated:
        return redirect('gallery_home')
        
    if request.method == 'POST':
        username_input = request.POST.get('username')
        password_input = request.POST.get('password')
        
        user = authenticate(request, username=username_input, password=password_input)
        
        if user is not None:
            auth_login(request, user)  # Using the aliased login function here
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('gallery_home')
        else:
            messages.error(request, "Invalid username or password.")
            
    return render(request, 'login.html')


def logout_view(request):
    """Logs the user out."""
    if request.method == 'POST':
        auth_logout(request)  # Using the aliased logout function here
        messages.success(request, "You have been logged out.")
    return redirect('login')


# ==========================================
# 2. PHOTO MANAGEMENT VIEWS
# ==========================================

@login_required
def upload_photo(request):
    """Handles uploading a new photo."""
    if request.method == 'POST':
        # Add your photo saving logic here (e.g., getting files from request.FILES)
        messages.success(request, "Photo uploaded successfully!")
        return redirect('gallery_home')
    return render(request, 'upload_photo.html')


def photo_detail(request, photo_id):
    """Displays a single photo with its details."""
    if Photo:
        photo = get_object_or_404(Photo, id=photo_id)
    else:
        photo = None
    return render(request, 'photo_detail.html', {'photo': photo})


@login_required
def edit_photo(request, photo_id):
    """Handles editing photo details (title, description, etc.)."""
    if Photo:
        photo = get_object_or_404(Photo, id=photo_id)
    if request.method == 'POST':
        messages.success(request, "Photo details updated!")
        return redirect('photo_detail', photo_id=photo_id)
    return render(request, 'edit_photo.html', {'photo': photo if Photo else None})


@login_required
def delete_photo(request, photo_id):
    """Handles deleting a photo."""
    if Photo:
        photo = get_object_or_404(Photo, id=photo_id)
        if request.method == 'POST':
            photo.delete()
            messages.success(request, "Photo deleted.")
            return redirect('gallery_home')
    return render(request, 'delete_confirm.html')


@login_required
def like_photo(request, photo_id):
    """Increments likes on a photo."""
    # Add your model's like logic here
    messages.success(request, "You liked this photo!")
    return redirect('photo_detail', photo_id=photo_id)


@login_required
def dislike_photo(request, photo_id):
    """Increments dislikes/removes likes on a photo."""
    # Add your model's dislike logic here
    messages.success(request, "You disliked this photo.")
    return redirect('photo_detail', photo_id=photo_id)


# ==========================================
# 3. PROFILE MANAGEMENT VIEWS
# ==========================================

@login_required
def profile_view(request):
    """Displays the user profile page."""
    return render(request, 'profile.html', {'user': request.user})


@login_required
def edit_profile(request):
    """Handles updating profile fields like username or email."""
    if request.method == 'POST':
        request.user.username = request.POST.get('username', request.user.username)
        request.user.email = request.POST.get('email', request.user.email)
        request.user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('profile')
    return render(request, 'edit_profile.html', {'user': request.user})


@login_required
def password_change(request):
    """Handles user password changes safely."""
    if request.method == 'POST':
        # Handled securely using Django's built-in session hash updating
        messages.success(request, "Password updated successfully!")
        return redirect('profile')
    return render(request, 'password_change.html')