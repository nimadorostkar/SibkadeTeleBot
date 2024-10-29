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



TOKEN = "7445678382:AAG3-dxleieDz_dBJh4YCeMHQeuj389gM6U"


def send_weekly_orders():
    print('---022---')
    today = datetime.now()
    one_week_ago = today - timedelta(days=7)
    orders = Order.objects.filter(create_at__gte=one_week_ago)
    print('---000---')




def my_daily_task():
    print('-44-')
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

@shared_task
def min():
    print('---022---')






''' 
subject = 'Test Email from Django'
message = 'This is a test email sent from Django using SMTP on Liara server.'
recipient_list = ['nimadorostkar97@gmail.com']
email = EmailMessage(subject,message,settings.EMAIL_FROM_ADDRESS,recipient_list,)
email.send(fail_silently=False)
'''