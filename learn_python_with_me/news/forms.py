from django import forms


class NewsFilterForm(forms.Form):
    COUNTRIES = [
        ('us', 'США'),
        ('gb', 'Великобритания'),
        ('ca', 'Канада'),
    ]

    CATEGORIES = [
        ('general', 'Главные'),
        ('business', 'Бизнес'),
        ('health', 'Здоровье'),
    ]

    country = forms.ChoiceField(choices=COUNTRIES, label='Select Country')
    category = forms.ChoiceField(choices=CATEGORIES, label='Select Category')
