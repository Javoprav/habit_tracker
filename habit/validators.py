from rest_framework import serializers
from datetime import time


def excludeValidator(value):
    """Исключить одновременный выбор связанной привычки и указания вознаграждения."""
    if value.get('associated_habit') and value.get('reward'):
        raise serializers.ValidationError('Исключён одновременный выбор связанной привычки и указания вознаграждения.')
    if value.get('execution_time') > time(00, 2):
        raise serializers.ValidationError('Время выполнения должно быть не больше 120 секунд.')
    if not value.get('associated_habit').is_pleasurable:
        raise serializers.ValidationError('В связанные привычки могут попадать только привычки с признаком приятной '
                                          'привычки.')
    if not value.get('is_pleasurable') and value.get('associated_habit') or value.get('reward'):
        raise serializers.ValidationError('У приятной привычки не может быть вознаграждения или связанной привычки.')
    if value.get('periodic') > 7:
        raise serializers.ValidationError('Нельзя выполнять привычку реже, чем 1 раз в 7 дней.')
