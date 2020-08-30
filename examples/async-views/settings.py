from pathlib import Path

DEBUG = True
SECRET_KEY = "foo"
ROOT_URLCONF = "urls"
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "raw_api",
]
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "django_raw_api_async",
    }
}
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    # "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "raw_api.middleware",
]
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [Path(__file__).parent],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
STATIC_URL = "/static/"
# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "handlers": {"console": {"class": "logging.StreamHandler"}},
#     "root": {"handlers": ["console"], "level": "DEBUG"},
#     "loggers": {
#         "django": {
#             "handlers": ["console"],
#             "level": "DEBUG",
#             "propagate": False,
#         },
#     },
# }
