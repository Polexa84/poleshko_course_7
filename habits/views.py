from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import Habit
from .serializers import HabitSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action

class HabitPagination(PageNumberPagination):
    page_size = 5  # Количество привычек на странице

class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = HabitPagination

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def public(self, request):
        """
        Эндпоинт для получения списка публичных привычек.
        """
        public_habits = Habit.objects.filter(is_public=True)
        page = self.paginate_queryset(public_habits)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(public_habits, many=True)
        return Response(serializer.data)