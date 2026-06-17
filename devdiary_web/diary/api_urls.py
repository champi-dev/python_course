from django.urls import path
from rest_framework.routers import DefaultRouter

from . import api

router = DefaultRouter()
router.register(r"entries", api.EntryViewSet, basename="entry")

urlpatterns = [
    path("register/", api.RegisterView.as_view(), name="api_register"),
] + router.urls
