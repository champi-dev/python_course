from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response

from .serializers import EntrySerializer, RegisterSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {"id": user.id, "username": user.username, "token": token.key},
            status=201,
        )


class EntryViewSet(viewsets.ModelViewSet):
    serializer_class = EntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["mood"]
    search_fields = ["topic", "notes"]
    ordering_fields = ["minutes", "created_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        return self.request.user.entries.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
