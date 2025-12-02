from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


def home_view(request):
    """Home page view."""
    return render(request, 'home.html')


def register_view(request):
    """Registration page view."""
    return render(request, 'auth/register.html')


def login_view(request):
    """Login page view."""
    return render(request, 'auth/login.html')


def profile_view(request):
    """Profile page view - handle auth in frontend."""
    return render(request, 'auth/profile.html')