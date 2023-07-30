from rest_framework import serializers


def excludeValidator(value):
    """Исключить одновременный выбор связанной привычки и указания вознаграждения."""
    if value.get('associated_habit') and value.get('reward'):
        raise serializers.ValidationError('Исключён одновременный выбор связанной привычки и указания вознаграждения.')
