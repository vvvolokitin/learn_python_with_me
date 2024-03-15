from django.urls import path
from .views import LandingView, DetailNewsView

app_name = 'blog'

urlpatterns = [
    path('project_news/<int:pk>', DetailNewsView.as_view(), name='detail'),
    path('', LandingView.as_view(), name='landing')
]
