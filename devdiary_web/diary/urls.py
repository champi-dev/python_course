from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("signup/", views.signup, name="signup"),
    path("add/", views.EntryCreateView.as_view(), name="add_entry"),
    path("entry/<int:pk>/", views.EntryDetailView.as_view(), name="entry_detail"),
    path("entry/<int:pk>/edit/", views.EntryUpdateView.as_view(), name="entry_edit"),
    path("entry/<int:pk>/delete/", views.EntryDeleteView.as_view(), name="entry_delete"),
    path("stats/", views.stats, name="stats"),
]
