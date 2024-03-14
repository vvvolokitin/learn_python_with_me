from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView

from .models import Grade, Question, TagQuestion


class EmploymentQuestionListView(ListView):
    """Страница вопросов на собеседовании."""

    template_name = 'employment/index.html'
    model = Question
    queryset = Question.objects.filter(
        is_published=True
    )
    paginate_by = 15


class EmploymentQuestionDetailView(DetailView):
    """Вопрос на собеседовании."""
    template_name = 'employment/detail.html'
    model = Question

    def get_object(self, queryset=None):
        return get_object_or_404(
            self.model.objects.filter(
                is_published=True
            ),
            pk=self.kwargs['pk']
        )
