from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth import get_user_model

from .models import MyUser

User = get_user_model()


class SignUpForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ("username", "email")


class LogInForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class PasswordForm(forms.Form):
    class Meta:
        model = MyUser
        fields = ("password")


class EditProfileForm(UserChangeForm):
    """Форма 'Редактирования профиля'."""

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'bio',

        )
