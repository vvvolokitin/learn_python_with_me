from django import forms

from .models import CommentOnProjectNews


class CommentForm(forms.ModelForm):
    """Форма 'Комментария'."""

    class Meta:
        model = CommentOnProjectNews
        fields = (
            'text',
        )
