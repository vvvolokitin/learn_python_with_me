from typing import Any
from django.contrib.auth.decorators import login_required

from django.db.models import Count, F
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView

from .forms import CommentForm
from .models import Choice, Lesson, Result, TestAnswer, TestQuestion


class LessonListView(ListView):
    """Страница уроков."""

    template_name = 'lessons/index.html'
    model = Lesson
    queryset = Lesson.objects.filter(
        is_published=True,
        category__is_published=True
    ).annotate(
        comment_count=Count('comments'),
        question_count=Count('lesson_questions')
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
        context['result'] = (
            Result.objects.get(
                user=self.request.user,
                lesson=self.object
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


@login_required
def test_view(request, category_slug, lesson_slug, question_id):
    lesson = Lesson.objects.get(slug=lesson_slug)
    test = lesson.lesson_questions.all()
    current_question, previous_question, next_question = None, None, None

    for index, question in enumerate(test):
        if question.id == question_id:
            current_question = question
            if index != len(test) - 1:
                next_question = test[index + 1]
            if index != 0:
                previous_question = test[index-1]
    context = {
        'lesson': lesson,
        'test': test,
        'question': current_question,
        'next_question': next_question,
        'previous_question': previous_question,
    }
    return render(
        request,
        'lessons/test.html',
        context
    )


@login_required
def grade_question(request, category_slug, lesson_slug, question_id):
    """Проверка правильности ответа."""
    question = get_object_or_404(TestQuestion, pk=question_id)
    lesson = get_object_or_404(Lesson, slug=lesson_slug)
    user = request.user
    can_answer = question.user_can_answer(request.user)
    scores = question.level.scores
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

            is_correct = correct_answer == user_answer
            if not is_correct:
                return render(
                    request,
                    'lessons/partial.html',
                    {
                        'is_correct': is_correct,
                    }
                )
            choice = Choice(
                user=user,
                question=question,
                answer=user_answer
            )
            choice.save()

            result, created = Result.objects.get_or_create(
                user=user,
                lesson=lesson
            )

        elif question.question_type == 'multiple':
            correct_answer = question.get_answers().filter(is_correct=True)
            answers_ids = request.POST.getlist('answer')
            user_answers = []
            if answers_ids:
                for answer_id in answers_ids:
                    user_answer = TestAnswer.objects.get(pk=answer_id)
                    user_answers.append(user_answer.name)

                is_correct = correct_answer == user_answers
                if not is_correct:
                    return render(
                        request,
                        'lessons/partial.html',
                        {
                            'is_correct': is_correct,
                        }
                    )

                for user_answer in user_answers:
                    choice = Choice(
                        user=user,
                        question=question,
                        answer=user_answer
                    )
                    choice.save()
                result, created = Result.objects.get_or_create(
                    user=user,
                    lesson=lesson
                )

    except:
        return render(
            request,
            'lessons/partial.html',
            {'question': question}
        )

    result.correct = F('correct') + 1
    result.scores = F('scores') + scores
    user.experience = F('experience') + scores
    user.save()
    result.save()
    # if not result.test_complete and result.correct == lesson.lesson_questions.count():
    #     result.test_complete = True
    #     result.save()

    return render(
        request,
        'lessons/partial.html',
        {
            'is_correct': is_correct,
        }
    )


@login_required
def test_results(request, category_slug, lesson_slug):
    """Вывод результата теста."""
    user = request.user
    lesson = get_object_or_404(Lesson, slug=lesson_slug)
    test = lesson.lesson_questions.all()
    result = Result.objects.get(
        user=user,
        lesson=lesson
    )

    correct = result.correct
    scores = result.scores
    context = {'quiz': lesson,
               'profile': user,
               'correct': correct,
               'scores': scores,
               'experience': user.experience,
               'number': len(test),
               'skipped': len(test) - (correct)}
    return render(request,
                  'lessons/results.html', context)
