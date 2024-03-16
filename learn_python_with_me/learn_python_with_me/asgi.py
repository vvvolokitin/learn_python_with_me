
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'learn_python_with_me.settings')

application = get_asgi_application()
