from adminpanel.config.settings.components import pg_settings

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": pg_settings.POSTGRES_DB,
        "USER": pg_settings.POSTGRES_USER,
        "PASSWORD": pg_settings.POSTGRES_PASSWORD,
        "HOST": pg_settings.POSTGRES_HOST,
        "PORT": pg_settings.POSTGRES_PORT,
        "OPTIONS": {
            "options": "-c search_path=public,content",
        },
    },
}

CONN_MAX_AGE = 10
