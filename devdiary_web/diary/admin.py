from django.contrib import admin

from .models import Entry


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ("topic", "minutes", "mood", "created_at", "is_long")
    list_editable = ("mood",)
    list_filter = ("mood", "created_at")
    search_fields = ("topic", "notes")
    ordering = ("-created_at",)
