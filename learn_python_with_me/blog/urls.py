from django.urls import path
from .views import LandingView, about_view

app_name = 'blog'

urlpatterns = [
    path('about/', about_view, name='about'),
    path('', LandingView.as_view(), name='landing')
]
