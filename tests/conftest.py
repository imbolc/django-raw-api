import django
from django.conf import settings
from django.core.management import call_command


def pytest_configure():
    settings.configure(
        DATABASES={
            # Can't use sqlite as `sync_to_async` assumes multi-threading
            "default": {
                "ENGINE": "django.db.backends.postgresql_psycopg2",
                "NAME": "django_raw_api",
            }
        },
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            "django.contrib.admin",
            "raw_api",
        ],
        ROOT_URLCONF="urls",
        MIDDLEWARE=[
            "django.contrib.sessions.middleware.SessionMiddleware",
            "django.contrib.auth.middleware.AuthenticationMiddleware",
            "raw_api.middleware",
        ],
    )
    django.setup()
    call_command("migrate")
