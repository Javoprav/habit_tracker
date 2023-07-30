from rest_framework import serializers
from habit.models import Habit
from habit.validators import excludeValidator


class HabitSerializers(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        validators = [excludeValidator]
