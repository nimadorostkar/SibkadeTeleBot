from order.models import Order
import json
from datetime import datetime, timedelta, date
import time
import telebot
from django.core.mail import send_mail
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.conf import settings
from celery import shared_task
from collections import defaultdict


TOKEN = "7445678382:AAG3-dxleieDz_dBJh4YCeMHQeuj389gM6U"


@shared_task
def send_weekly_orders():
    one_week_ago = datetime.now() - timedelta(days=7)
    recent_orders = Order.objects.filter(create_at__gte=one_week_ago)
    orders_by_user = defaultdict(list)
    for order in recent_orders:
        orders_by_user[order.user].append(order)
    print("-----------")
    print(orders_by_user)
    message = f'This is list of orders: \n\n {orders_by_user}'
    bot = telebot.TeleBot(TOKEN)
    bot.send_message(chat_id="-4516176630",text=message)



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


