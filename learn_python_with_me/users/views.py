from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse
from django.db.models import Count, Q
from django.utils import timezone
from django.contrib.auth import get_user_model

from .forms import SignUpForm, LogInForm
from .mixins import UserTestCastomMixin

User = get_user_model()


def user_profile(request, username):
    """Профиль пользователя."""
    profile = get_object_or_404(
        User,
        username=username
    )

    return render(
        request,
        'users/profile.html',
        {
            'profile': profile,
        }
    )


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('blog:landing')
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})


def log_in(request):
    error = False
    if request.user.is_authenticated:
        return redirect('blog:landing')
    if request.method == "POST":
        form = LogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('blog:landing')
            else:
                error = True
    else:
        form = LogInForm()

    return render(request, 'users/login.html', {'form': form, 'error': error})


def log_out(request):
    logout(request)
    return redirect(reverse('users:login'))
