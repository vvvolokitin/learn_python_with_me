from django.shortcuts import render
from newsapi import NewsApiClient
from .forms import NewsFilterForm
from decouple import config


def news_list(request):
    api_key = config('API_KEY')
    newsapi = NewsApiClient(api_key=api_key)

    language = 'ru'

    if request.method == 'GET':
        form = NewsFilterForm(request.GET)
        if form.is_valid():
            language = form.cleaned_data['language']

    articles = newsapi.get_everything(
        q='python OR программирование OR it',
        language=language,
        sort_by='relevancy',
        page_size=20
    )

    return render(
        request,
        'news/news.html',
        {
            'articles': articles['articles'],
            'form': form,

        }
    )
