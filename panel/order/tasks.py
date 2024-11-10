from order.models import Order
import json
from datetime import datetime, timedelta, date
import telebot
from celery import shared_task
from collections import defaultdict
from django.db.models import Q, Count

TOKEN = "7445678382:AAG3-dxleieDz_dBJh4YCeMHQeuj389gM6U"



@shared_task
def send_weekly_orders():
    seven_days_ago = datetime.now() - timedelta(days=7)
    orders = Order.objects.filter(create_at__gte=seven_days_ago)
    grouped_orders = {}
    for order in orders:
        user = order.user
        month = order.month
        type_ = order.type

        # Initialize nested dictionary structure if not present
        if user not in grouped_orders:
            grouped_orders[user] = {}
        if month not in grouped_orders[user]:
            grouped_orders[user][month] = {}
        if type_ not in grouped_orders[user][month]:
            grouped_orders[user][month][type_] = []

        # Append the order to the relevant grouping
        grouped_orders[user][month][type_].append(order)

    bot = telebot.TeleBot(TOKEN)
    bot.send_message(chat_id="1759061065",text=grouped_orders)



@shared_task
def my_daily_task():
    orders = Order.objects.filter(status="Done")
    for item in orders:
        expiration_date = datetime.strptime(item.expiration, "%Y-%m-%d")
        reminder_date = expiration_date - timedelta(days=3)
        today = datetime.combine(date.today(), datetime.min.time())

        if today == expiration_date:
            item.status = "Expired"
            item.save()

        if today >= reminder_date:
            bot = telebot.TeleBot(TOKEN)
            bot.send_message(chat_id=item.chat_id, text=f"3 days until the end of your service. \norder_code: {item.order_code} \nyour service expiration is {item.expiration}",reply_to_message_id=item.message_id)

