from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import UpdateView

from .forms import EditProfileForm, LogInForm, SignUpForm, PasswordForm
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


class EditProfile(LoginRequiredMixin, UpdateView):
    template_name = 'users/edit_profile.html'
    model = User
    form_class = EditProfileForm

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy(
            'users:profile',
            kwargs={
                'username': self.request.user
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
    return render(
        request,
        'users/signup.html',
        {'form': form}
    )


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
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                return redirect('blog:landing')
            else:
                error = True
    else:
        form = LogInForm()

    return render(
        request,
        'users/login.html',
        {
            'form': form,
            'error': error}
    )


def log_out(request):
    logout(request)
    return redirect(reverse('users:login'))
