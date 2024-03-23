import os

from django.core.paginator import Paginator
from django.shortcuts import render
from dotenv import load_dotenv
from newsapi import NewsApiClient

from .forms import NewsFilterForm

load_dotenv()


def news_list(request):
    newsapi = NewsApiClient(
        api_key=os.getenv('API_KEY')
    )
    language = 'ru'

    if request.method == 'GET':
        form = NewsFilterForm(request.GET)
        if form.is_valid():
            language = form.cleaned_data['language']

    articles = newsapi.get_everything(
        q='python OR программирование OR it',
        language=language,
        sort_by='relevancy',
    )
    paginator = Paginator(articles['articles'], 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'news/news.html',
        {
            'page_obj': page_obj,
            'form': form,

        }
    )
