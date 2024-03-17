from django.urls import path
from .views import LandingView, DetailNewsView

app_name = 'blog'

urlpatterns = [
    path('project_news/<int:pk>/', DetailNewsView.as_view(),
         name='project_news_detail'),
    path('', LandingView.as_view(), name='landing')
]
