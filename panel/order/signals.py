from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Order
import telebot




@receiver(pre_save, sender=Order)
def store_old_response(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = sender.objects.get(pk=instance.pk)
            instance._old_response = old_instance.response
        except sender.DoesNotExist:
            instance._old_response = None

@receiver(post_save, sender=Order)
def handle_response_update(sender, instance, **kwargs):
    TOKEN = "7445678382:AAG3-dxleieDz_dBJh4YCeMHQeuj389gM6U"
    if hasattr(instance, '_old_response') and instance._old_response != instance.response:
        print(f" {instance.response} has been updated.")
        bot = telebot.TeleBot(TOKEN)
        bot.send_message(chat_id=instance.chat_id,text=f"Your order is ready: \n {instance.response} ", reply_to_message_id=instance.message_id)

