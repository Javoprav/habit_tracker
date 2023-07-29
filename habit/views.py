from django.shortcuts import render
from rest_framework import viewsets
from habit.models import Habit
from habit.serializers.serializers import HabitSerializers
from users.models import UserRoles


class HabtsViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializers
    queryset = Habit.objects.all()
    # permission_classes = [IsAuthenticated]
    # pagination_class = HabitPagination

    def perform_create(self, serializer) -> None:
        """Сохраняет новому объекту владельца"""
        serializer.save(owner=self.request.user)

    # def perform_update(self, serializer):
    #     self.object = serializer.save()
    #     send_mail_user_update.delay(self.object.pk)

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser or user.role == UserRoles.MODERATOR:
            return Habit.objects.all()
        else:
            return Habit.objects.filter(owner=user)