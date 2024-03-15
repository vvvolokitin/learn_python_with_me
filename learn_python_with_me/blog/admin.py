from django.contrib import admin, messages

from .models import ProjectNews, CommentOnProjectNews


@admin.register(ProjectNews)
class ProjectNewsAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'is_published',
    )
    list_editable = (
        'is_published',
    )
    search_fields = (
        'title',
    )
    list_display_links = (
        'title',
    )
    list_filter = (
        'is_published',
    )
    actions = (
        'set_published',
        'set_unpublished'
    )

    @admin.action(description='Опубликовать')
    def set_published(self, requst, queryset):
        count = queryset.update(is_published=True)
        self.message_user(requst, f'Опубликовано {count} новостей')

    @admin.action(description='Снять с публикации')
    def set_unpublished(self, requst, queryset):
        count = queryset.update(is_published=False)
        self.message_user(
            requst, f'Снято с публикации {count} новостей', messages.WARNING)
