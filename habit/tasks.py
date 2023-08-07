
from django.conf import settings
from telebot import TeleBot
from habit_tracker.celery import app
from habit.models import Habit


@app.task
def send_telegram_message(habit_id):
    """Отправка сообщения через бот TG"""
    habit = Habit.objects.get(id=habit_id)
    bot = TeleBot(settings.TG_BOT_TOKEN)
    message = f"Напоминание о выполнении привычки {habit.action} в {habit.time} в {habit.place}"
    bot.send_message(habit.owner.chat_id, message)

# @shared_task
# def check_time_habit():
#     """Проверка времени привычки"""
#     now_date = datetime.now()
#     habits_set = Habit.objects.all()
#     for habit in habits_set:
#         if habit.time.hour == now_date.time().hour and habit.time.minute == now_date.time().minute:
#             send_telegram_message(habit)


# @shared_task
# def check_time():
#     bot = TeleBot(settings.TG_BOT_TOKEN)
#     time = datetime.now().time()
#     time_start_task = datetime.now() - timedelta(minutes=1)
#     data_habit = Habit.objects.filter(time__gte=time_start_task)
#     for item in data_habit.filter(time__lte=time):
#         text = f'Напоминание о выполнении привычки  {item.action} в {item.time} в {item.place}'
#         bot.send_message(item.owner.chat_id, text)
