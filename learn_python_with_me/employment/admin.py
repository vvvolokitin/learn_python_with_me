from django.contrib import admin

from .models import Question, Grade, TagQuestion


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        'question',
        'is_published',
    )
    list_editable = (
        'is_published',
    )
    search_fields = (
        'question',
        'tags__tag',
        'grade__grade'
    )
    list_filter = (
        'is_published',
        'tags__tag',
        'grade__grade'
    )


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    pass


@admin.register(TagQuestion)
class TageQuestionAdmin(admin.ModelAdmin):
    pass
