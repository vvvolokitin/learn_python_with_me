from django.urls import path
from .views import LessonListView, LessonDetailView, test_view, grade_question, test_results

app_name = 'lessons'

urlpatterns = [
    
    path('<slug:category_slug>/<slug:lesson_slug>/test/<int:question_id>/',
         test_view, name='test'),
    path('<slug:category_slug>/<slug:lesson_slug>/test/<int:question_id>/grade/',
         grade_question, name='grade_question'),
          path('<slug:category_slug>/<slug:lesson_slug>/test/results',
         test_results, name='test_results'),
    path('<slug:category_slug>/<slug:lesson_slug>',
         LessonDetailView.as_view(), name='detail'),
    # path('<slug:category_slug>/', CategoryListView.as_view(), name='category'),
    path('', LessonListView.as_view(), name='index')
]
