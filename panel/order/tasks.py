from order.models import Order
import json
from datetime import datetime, timedelta, date
import telebot
from celery import shared_task
from collections import defaultdict
from django.db.models import Q, Count
from django.utils import timezone

TOKEN = "7445678382:AAG3-dxleieDz_dBJh4YCeMHQeuj389gM6U"



@shared_task
def send_weekly_orders():
    bot = telebot.TeleBot(TOKEN)
    seven_days_ago = timezone.now() - timedelta(days=7)
    orders = (Order.objects.filter(create_at__gte=seven_days_ago).values('user', 'type', 'month').annotate(count=Count('id')))

    user_orders = defaultdict(list)
    for order in orders:
        user = order['user']
        type_and_month = f"{order['month']} month {order['type']}"
        count = order['count']
        user_orders[user].append(f"{type_and_month}, count: {count}")

    message = " "
    for user, orders in user_orders.items():
        message += f"{user}:\n"
        for order in orders:
            message += f"  {order} \n\n"
            bot.send_message(chat_id="1759061065", text=message, parse_mode='Markdown')


    #bot.send_message(chat_id="1759061065",text=message, parse_mode=ParseMode.HTML)
    #bot.send_message(chat_id="1759061065", text=f"```\n{message}\n```", parse_mode='Markdown')


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

