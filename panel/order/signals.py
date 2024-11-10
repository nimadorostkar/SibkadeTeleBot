from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Order
import telebot
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta, date

def add_months(current_date, months_to_add):
    return current_date + relativedelta(months=months_to_add)



@receiver(pre_save, sender=Order)
def store_old_response(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = sender.objects.get(pk=instance.pk)
            instance._old_response = old_instance.response
            instance._old_link = old_instance.link
        except sender.DoesNotExist:
            instance._old_response = None
            instance._old_link = None


@receiver(post_save, sender=Order)
def handle_response_update(sender, instance, **kwargs):
    TOKEN = "7445678382:AAG3-dxleieDz_dBJh4YCeMHQeuj389gM6U"
    if (
            (hasattr(instance, '_old_response') and instance._old_response != instance.response) or
            (hasattr(instance, '_old_link') and instance._old_link != instance.link)
    ):

        expiration = add_months(datetime.now(), instance.month)
        Order.objects.filter(pk=instance.pk).update(expiration=expiration.date())

        message = f"Your order has been updated:\n Order Code: {instance.order_code}\n"
        if instance._old_response != instance.response:
            message += f"Response updated: {instance.response}\n"
        if instance._old_link != instance.link:
            message += f"Link updated: {instance.link}\n"
        message += f"Expiration: {expiration.date()}"

        bot = telebot.TeleBot(TOKEN)
        bot.send_message(chat_id=instance.chat_id,text=message, reply_to_message_id=instance.message_id)
