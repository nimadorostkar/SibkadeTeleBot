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
    # Calculate the date for 7 days ago
    seven_days_ago = datetime.now() - timedelta(days=7)

    # Filter orders from 7 days ago and group by user, month, and type
    orders = (
        Order.objects
        .filter(create_at__gte=seven_days_ago)
        .values('user', 'month', 'type')
        .annotate(order_count=Count('id'))
        .order_by('user', 'month', 'type')
    )

    # Prepare data in a formatted string
    message = ""
    current_user = None
    for order in orders:
        user = order['user']
        month = order['month']
        order_type = order['type']
        count = order['order_count']

        if user != current_user:
            if current_user is not None:
                message += "\n"  # Separate different users with a line break
            message += f"User: {user}\n"
            current_user = user

        message += f"  Month: {month}, Type: {order_type}, Count: {count}\n"

    # Print or send this message via the bot
    print(message)

    message = f'This is list of orders: \n\n\n {message}'
    bot = telebot.TeleBot(TOKEN)
    bot.send_message(chat_id="1759061065",text=message)



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

