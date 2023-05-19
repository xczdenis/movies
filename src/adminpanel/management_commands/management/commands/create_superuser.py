from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from loguru import logger

from adminpanel.config.settings import app_settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        username = app_settings.SUPERUSER_LOGIN
        password = app_settings.SUPERUSER_PASSWORD
        email = app_settings.SUPERUSER_EMAIL
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password)
            logger.success("Superuser successfully created")
        else:
            logger.warning("Superuser already exists")
