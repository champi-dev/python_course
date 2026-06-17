from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView,
)

from .forms import EntryForm
from .models import Entry


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"✓ Welcome, {user.username}!")
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html",
                  {"form": form, "heading": "Sign up"})


class HomeView(LoginRequiredMixin, ListView):
    model = Entry
    template_name = "diary/home.html"
    context_object_name = "entries"

    def get_queryset(self):
        return self.request.user.entries.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_minutes"] = (
            self.get_queryset().aggregate(total=Sum("minutes"))["total"] or 0
        )
        return context


class EntryDetailView(LoginRequiredMixin, DetailView):
    model = Entry

    def get_queryset(self):
        return self.request.user.entries.all()


class EntryCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Entry
    form_class = EntryForm
    template_name = "diary/entry_form.html"
    success_url = reverse_lazy("home")
    success_message = "✓ Saved “%(topic)s”."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["heading"] = "New entry"
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class EntryUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Entry
    form_class = EntryForm
    template_name = "diary/entry_form.html"
    success_message = "✓ Updated “%(topic)s”."

    def get_queryset(self):
        return self.request.user.entries.all()

    def get_success_url(self):
        return reverse("entry_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["heading"] = "Edit entry"
        return context


class EntryDeleteView(LoginRequiredMixin, DeleteView):
    model = Entry
    success_url = reverse_lazy("home")

    def get_queryset(self):
        return self.request.user.entries.all()

    def form_valid(self, form):
        messages.success(self.request, f"🗑 Deleted “{self.object.topic}”.")
        return super().form_valid(form)


@login_required
def stats(request):
    my_entries = request.user.entries
    distinct_topics = my_entries.values("topic").distinct().count()
    total_minutes = my_entries.aggregate(total=Sum("minutes"))["total"] or 0
    return render(request, "diary/stats.html",
                  {"distinct_topics": distinct_topics,
                   "total_minutes": total_minutes})
