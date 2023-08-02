from datetime import datetime
from celery import shared_task
from django_celery_beat.models import CrontabSchedule, PeriodicTask, IntervalSchedule
from habit.models import Habit
from django.conf import settings
from telebot import TeleBot
from habit_tracker.celery import app


def send_telegram_message(habit_id):
    """Отправка сообщения через бот TG"""
    habit_set = Habit.objects.get(id=habit_id)
    bot = TeleBot(settings.TG_BOT_TOKEN)
    for habit in habit_set:

        message = f"Напоминание о выполнении привычки {habit}"
        bot.send_message(habit.owner.chat_id, message)
        print(message)

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
