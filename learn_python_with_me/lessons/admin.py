from django.contrib import admin, messages

from .models import Lesson, Category, Comment, TestAnswer, TestQuestion, Choice, Result


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'is_published',
        'category',
    )
    list_editable = (
        'is_published',
        'category',
    )
    search_fields = (
        'title',
    )
    list_display_links = (
        'title',
    )
    list_filter = (
        'category__title',
        'is_published'
    )
    actions = (
        'set_published',
        'set_unpublished'
    )

    @admin.action(description='Опубликовать')
    def set_published(self, requst, queryset):
        count = queryset.update(is_published=True)
        self.message_user(requst, f'Опубликовано {count} уроков')

    @admin.action(description='Снять с публикации')
    def set_unpublished(self, requst, queryset):
        count = queryset.update(is_published=False)
        self.message_user(
            requst, f'Снято с публикации {count} уроков', messages.WARNING)


class LessonTabularInline(admin.TabularInline):
    model = Lesson
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = (
        LessonTabularInline,
    )
    list_display = (
        'title',
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'post',
        'author',
        'is_published',
    )
    list_editable = (
        'is_published',
    )


class AnswerInline(admin.TabularInline):
    model = TestAnswer
    extra = 4


@admin.register(TestQuestion)
class TestQuestionAdmin(admin.ModelAdmin):
    list_display = (
        'question',
        'lesson'
    )
    inlines = (
        AnswerInline,
    )


@admin.register(TestAnswer)
class TestAnswerAdmin(admin.ModelAdmin):
    pass
