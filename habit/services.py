from django_celery_beat.models import CrontabSchedule, PeriodicTask
from telebot import TeleBot
from django.conf import settings
from habit.models import Habit


def create_habit_schedule(habit):
    """Создание периодичности и задачи на отправку"""
    crontab_schedule, _ = CrontabSchedule.objects.get_or_create(
            minute=habit.time.minute,
            hour=habit.time.hour,
            day_of_month=f'*/{habit.periodic}',
            month_of_year='*',
            day_of_week='*',
        )
    # interval, created = IntervalSchedule.objects.get_or_create(
    #     every=habit.periodic,
    #     period=IntervalSchedule.DAYS,
    # )

    PeriodicTask.objects.create(
        crontab=crontab_schedule,
        # interval=interval,
        name=f'Habit Task - {habit.name}',
        task='habit.tasks.send_telegram_message',
        args=[habit.id],
    )


def send_telegram_message2(habit_id):
    """Отправка сообщения через бот TG"""
    habit_set = Habit.objects.get(id=habit_id)
    bot = TeleBot(settings.TG_BOT_TOKEN)
    for habit in habit_set:
        print(habit_set)
        print(habit)
        message = f"Напоминание о выполнении привычки {habit.name}"
        bot.send_message(habit.owner.chat_id, message)
        print(message)