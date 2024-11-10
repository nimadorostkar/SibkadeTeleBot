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

    # Organize data by user for a more structured format
    user_data = {}
    for order in orders:
        user = order['user']
        month = order['month']
        order_type = order['type']
        count = order['order_count']

        if user not in user_data:
            user_data[user] = {}
        if month not in user_data[user]:
            user_data[user][month] = {}
        user_data[user][month][order_type] = count

    # Convert the data to a string format for easy reading
    message = ""
    for user, months in user_data.items():
        message += f"User: {user}\n"
        for month, types in months.items():
            message += f"  Month: {month}\n"
            for order_type, count in types.items():
                message += f"    Type: {order_type}, Count: {count}\n"
        message += "\n"  # Separate different users with a line break

    # Print or send this message via the bot
    print(message)

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

