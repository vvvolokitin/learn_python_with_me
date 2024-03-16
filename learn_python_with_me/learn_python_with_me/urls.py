from django.conf import settings
from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm
from django.urls import include, path, reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth import get_user_model

User = get_user_model()

# auth_pathes = [
#     path(
#         'registration/',
#         CreateView.as_view(
#             template_name='registration/registration_form.html',
#             form_class=UserCreationForm,
#             success_url=reverse_lazy(
#                 'blog:landing'
#             ),
#         ),
#         name='registration',
#     ),
#     path(
#         '',
#         include(
#             'django.contrib.auth.urls'
#         )
#     ),
# ]


urlpatterns = [
    path('auth/', include('users.urls')),
    path('admin/', admin.site.urls),
    path('lessons/', include('lessons.urls')),
    path('news/', include('news.urls')),
    path('employment/', include('employment.urls')),
    path('', include('blog.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

admin.site.site_header = 'Панель администрирования'

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
