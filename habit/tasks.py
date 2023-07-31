from datetime import datetime
from celery import shared_task
from habit.models import Habit
from django.conf import settings
from telebot import TeleBot


def send_telegram_message(habit):
    bot = TeleBot(settings.TG_BOT_TOKEN)
    chat_id = settings.TG_CHAT_ID
    message = f"Напоминание о выполнении привычки {habit.name}"
    bot.send_message(chat_id, message)


@shared_task
def check_time_habit():
    """Проверка времени привычки"""
    now_date = datetime.now()
    habits_list2 = Habit.objects.all()
    for habit in habits_list2:
        if habit.time.hour == now_date.time().hour and habit.time.minute == now_date.time().minute:
            send_telegram_message(habit)
