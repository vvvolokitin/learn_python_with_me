from typing import Any

from django.db.models import Count
from django.db.models.base import Model as Model
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView

from .forms import CommentForm
from .models import ProjectNews


class LandingView(ListView):
    """Главная страница сайта."""

    template_name = 'blog/index.html'
    model = ProjectNews
    queryset = ProjectNews.published_news.annotate(
        comment_count=Count('projects_news_comments')
    )
    ordering = '-pub_date'
    paginate_by = 10


class DetailNewsView(DetailView):
    """Новость проекта."""

    template_name = 'blog/detail.html'
    model = ProjectNews

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['projects_news_comments'] = (
            self.object.projects_news_comments.select_related(
                'author'
            )
        )
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(
            self.model.objects.filter(
                is_published=True
            ),
            pk=self.kwargs[
                self.pk
            ]
        )
