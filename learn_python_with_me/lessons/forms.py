from django import forms
from django.contrib.auth import get_user_model

from .models import Comment


class CommentForm(forms.ModelForm):
    """Форма 'Комментария'."""

    class Meta:
        model = Comment
        fields = (
            'text',
        )
