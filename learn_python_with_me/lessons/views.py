from typing import Any
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Count, Q, F
from django.http import JsonResponse

from .models import Lesson, Category, TestAnswer, TestQuestion, Choice, Result
from .forms import CommentForm


class LessonListView(ListView):
    """Страница уроков."""

    template_name = 'lessons/index.html'
    model = Lesson
    queryset = Lesson.objects.filter(
        is_published=True,
        category__is_published=True
    ).annotate(
        comment_count=Count('comments')
    )
    paginate_by = 10


class LessonDetailView(DetailView):
    """Урок."""

    template_name = 'lessons/detail.html'
    model = Lesson
    slug_url_kwarg = 'lesson_slug'

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (
            self.object.comments.select_related(
                'author'
            )
        )
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(
            self.model.objects.filter(
                is_published=True,
                category__is_published=True
            ),
            slug=self.kwargs[
                self.slug_url_kwarg
            ]
        )


def test_view(request, category_slug, lesson_slug, question_id):
    lesson = Lesson.objects.get(slug=lesson_slug)
    test = lesson.lesson_questions.all()
    current_question, next_question = None, None

    for index, question in enumerate(test):
        if question.id == question_id:
            current_question = question
            if index != len(test) - 1:
                next_question = test[index + 1]
    context = {
        'lesson': lesson,
        'test': test,
        'question': current_question,
        'next_question': next_question,
    }
    return render(
        request,
        'lessons/test.html',
        context
    )


def grade_question(request, category_slug, lesson_slug, question_id):
    question = get_object_or_404(TestQuestion, pk=question_id)
    lesson = get_object_or_404(Lesson, slug=lesson_slug)
    can_answer = question.user_can_answer(request.user)
    try:
        if not can_answer:
            return render(
                request,
                'lessons/partial.html',
                {
                    'question': question,
                    'error_message': 'Вы уже отвечали на этот вопрос.'
                }
            )

        if question.question_type == 'single':
            correct_answer = question.get_answers().get(is_correct=True)
            user_answer = question.question_answers.get(
                pk=request.POST['answer'])
            choice = Choice(
                user=request.user,
                question=question,
                answer=user_answer
            )
            choice.save()
            is_correct = correct_answer == user_answer
            result, created = Result.objects.get_or_create(
                user=request.user,
                lesson=lesson
            )
            if is_correct:
                result.correct = F('correct') + 1
            else:
                result.wrong = F('wrong') + 1
            result.save()

        elif question.question_type == 'multiple':
            correct_answer = question.get_answers().filter(is_correct=True)
            answers_ids = request.POST.getlist('answer')
            user_answers = []
            if answers_ids:
                for answer_id in answers_ids:
                    user_answer = TestAnswer.objects.get(pk=answer_id)
                    user_answers.append(user_answer.name)
                    choice = Choice(
                        user=request.user,
                        question=question,
                        answer=user_answer
                    )
                    choice.save()
                is_correct = correct_answer == user_answers
                result, created = Result.objects.get_or_create(
                    user=request.user,
                    lesson=lesson
                )
                if is_correct:
                    result.correct = F('correct') + 1
                else:
                    result.wrong = F('wrong') + 1
                result.save()

    except:
        return render(
            request,
            'lessons/partial.html',
            {'question': question}
        )
    return render(
        request,
        'lessons/partial.html',
        {
            'is_correct': is_correct,
            'correct_answer': correct_answer,
            'question': question
        }
    )


def test_results(request, category_slug, lesson_slug):
    profile = request.user
    lesson = get_object_or_404(Lesson, slug=lesson_slug)
    test = lesson.lesson_questions.all()
    results = Result.objects.filter(
        user=profile,
        lesson=lesson
    ).values()
    correct = [i['correct'] for i in results][0]
    wrong = [i['wrong'] for i in results][0]
    context = {'quiz': lesson,
               'profile': profile,
               'correct': correct,
               'wrong': wrong,
               'number': len(test),
               'skipped': len(test) - (correct + wrong)}
    return render(request,
                  'lessons/results.html', context)
