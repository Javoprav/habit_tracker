from datetime import datetime
from celery import shared_task
from django_celery_beat.models import CrontabSchedule, PeriodicTask
from habit.models import Habit
from django.conf import settings
from telebot import TeleBot


def send_telegram_message(habit):
    """Отправка сообщения через бот TG"""
    bot = TeleBot(settings.TG_BOT_TOKEN)
    # chat_id = settings.TG_CHAT_ID
    message = f"Напоминание о выполнении привычки {habit.name}"
    bot.send_message(habit.owner.chat_id, message)


# @shared_task
# def check_time_habit():
#     """Проверка времени привычки"""
#     now_date = datetime.now()
#     habits_set = Habit.objects.all()
#     for habit in habits_set:
#         if habit.time.hour == now_date.time().hour and habit.time.minute == now_date.time().minute:
#             send_telegram_message(habit)


def create_habit_schedule(habit):
    """Создание периодичности и задачи на отправку"""
    crontab_schedule, _ = CrontabSchedule.objects.get_or_create(
            minute=habit.time.minute,
            hour=habit.time.hour,
            day_of_month=f'*/{habit.periodic}',
            month_of_year='*',
            day_of_week='*',
        )

    PeriodicTask.objects.create(
        crontab=crontab_schedule,
        name=f'Habit Task - {habit.name}',
        task='habit.tasks.send_telegram_message',
        args=[habit],
    )
