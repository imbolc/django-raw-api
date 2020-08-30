import os

from django.core.asgi import get_asgi_application  # isort:skip

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
application = get_asgi_application()
