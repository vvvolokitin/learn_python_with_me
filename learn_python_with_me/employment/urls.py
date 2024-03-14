from django.urls import path

from .views import EmploymentQuestionDetailView, EmploymentQuestionListView


app_name = 'employment'

urlpatterns = [
    path('<int:pk>/', EmploymentQuestionDetailView.as_view(), name='detail'),
    path('', EmploymentQuestionListView.as_view(), name='index')
]
