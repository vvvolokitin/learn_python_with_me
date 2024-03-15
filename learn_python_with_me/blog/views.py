from django.shortcuts import render
from django.views.generic import ListView


from .models import News



class LandingView(ListView):
    """Главная страница сайта."""

    template_name = 'landing.html'
    model = News
    queryset = News.objects.all()
    ordering = '-pub_date'
    paginate_by = 10



