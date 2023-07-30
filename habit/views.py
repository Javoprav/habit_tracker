from django.shortcuts import render
from rest_framework import viewsets
from habit.models import Habit
from habit.serializers.serializers import HabitSerializers
from users.models import UserRoles


class HabitsViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializers
    queryset = Habit.objects.all()
    # permission_classes = [IsAuthenticated]
    # pagination_class = HabitPagination

    def perform_create(self, serializer) -> None:
        """Сохраняет новому объекту владельца"""
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """Список привычек только для юзера или модератора"""
        user = self.request.user
        if user.is_staff or user.is_superuser or user.role == UserRoles.MODERATOR:
            return Habit.objects.all()
        else:
            return Habit.objects.filter(owner=user)

