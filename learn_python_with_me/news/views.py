from django.shortcuts import render
from newsapi import NewsApiClient
from .forms import NewsFilterForm
from decouple import config


def news_list(request):
    api_key = config('API_KEY')
    newsapi = NewsApiClient(api_key=api_key)

    country = 'us'
    category = 'general'

    if request.method == 'GET':
        form = NewsFilterForm(request.GET)
        if form.is_valid():
            country = form.cleaned_data['country']
            category = form.cleaned_data['category']

    articles = newsapi.get_top_headlines(
        country=country,
        category=category,
        page_size=10
    )

    return render(
        request,
        'news/news.html',
        {
            'articles': articles['articles'],
            'form': form
        }
    )
