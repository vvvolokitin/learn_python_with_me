from django.urls import path, register_converter
from .views import signup, log_in, log_out, user_profile, EditProfile
from .converters import UsernamePathConverter


register_converter(UsernamePathConverter, 'username')
app_name = 'users'

urlpatterns = [
    path(
        'edit_profile/',
        EditProfile.as_view(),
        name='edit_profile'
    ),
    path(
        'profile/<username:username>/',
        user_profile,
        name='profile'
    ),
    path('signup/', signup, name='signup'),
    path('login/', log_in, name='login'),
    path('logout/', log_out, name='logout'),
]
