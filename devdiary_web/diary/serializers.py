from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import Entry


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, validators=[validate_password], style={"input_type": "password"}
    )

    class Meta:
        model = get_user_model()
        fields = ["id", "username", "email", "password"]
        extra_kwargs = {"email": {"required": False}}

    def create(self, validated_data):
        return get_user_model().objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
        )


class EntrySerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Entry
        fields = ["id", "author", "topic", "minutes", "mood", "notes", "created_at"]
        read_only_fields = ["id", "created_at"]
