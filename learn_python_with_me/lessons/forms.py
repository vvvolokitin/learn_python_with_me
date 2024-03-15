from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    """Форма 'Комментария'."""

    class Meta:
        model = Comment
        fields = (
            'text',
        )
