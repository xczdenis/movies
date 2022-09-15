import os

from django.contrib.auth.models import User

username = os.environ.get("SUPERUSER_LOGIN")
email = os.environ.get("SUPERUSER_EMAIL")
password = os.environ.get("SUPERUSER_PASSWORD")

credentials_is_valid = True
user_is_exists = False

if not username:
    credentials_is_valid = False
    print("env SUPERUSER_LOGIN is not set")
else:
    if User.objects.filter(username=username).exists():
        user_is_exists = True

if not email:
    credentials_is_valid = False
    print("env SUPERUSER_EMAIL is not set")
else:
    if User.objects.filter(email=email).exists():
        user_is_exists = True

if not password:
    credentials_is_valid = False
    print("env SUPERUSER_PASSWORD is not set")

if credentials_is_valid:
    if not user_is_exists:
        User.objects.create_superuser(username, email, password)
        print("\033[01;32mSuperuser successfully created!\033[00m")
    else:
        print("Superuser with passed credentials is already exists")
else:
    print("Superuser not created because passed credentials are not valid")
