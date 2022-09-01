from django.urls import include, path
from movies.api.v1 import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"movies", views.FilmworkViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
