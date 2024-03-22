from django import template
from lessons.models import Result
register = template.Library()


@register.simple_tag
def get_count_correct_answers(lesson, user):
    result = Result.objects.get(
        user=user,
        lesson=lesson
    )
    return result.correct
