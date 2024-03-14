from django.conf import settings
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('lessons/', include('lessons.urls')),
    path('employment/', include('employment.urls')),
    path('', include('blog.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

admin.site.site_header = 'Панель администрирования'

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
