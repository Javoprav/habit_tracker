from telebot import TeleBot
from django.conf import settings
from habit.models import Habit


# def send_telegram_message(habit_id):
#     """Отправка сообщения через бот TG"""
#     habit_set = Habit.objects.get(id=habit_id)
#     bot = TeleBot(settings.TG_BOT_TOKEN)
#     for habit in habit_set:
#
#         message = f"Напоминание о выполнении привычки {habit}"
#         bot.send_message(habit.owner.chat_id, message)
#         print(message)