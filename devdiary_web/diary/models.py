from django.conf import settings
from django.db import models


class Entry(models.Model):
    MOOD_CHOICES = [("+", "good"), ("=", "ok"), ("-", "bad")]

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="entries",
    )
    topic = models.CharField(max_length=100)
    minutes = models.PositiveIntegerField()
    mood = models.CharField(max_length=1, choices=MOOD_CHOICES, default="=")
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, default="")

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "entries"

    def __str__(self):
        return f"{self.topic} ({self.minutes} min)"

    def is_long(self):
        return self.minutes >= 60
