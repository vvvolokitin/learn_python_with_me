from django import forms


class NewsFilterForm(forms.Form):
    LANGUAGES = [
        ('ru', 'Русский'),
        ('en', 'Англйский'),
    ]

    language = forms.ChoiceField(choices=LANGUAGES, label='Выбор языка')
