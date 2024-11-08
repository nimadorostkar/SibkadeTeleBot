from django.db import models
from link.models import Link
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import telebot



class Order(models.Model):
    status_choices = (
        ("New", "New"),
        ("Done", "Done"),
        ("In-process", "In-process"),
        ("Expired", "Expired"),
        ("Cancelled", "Cancelled"),)

    status = models.CharField(max_length=15, default="New", choices=status_choices)
    order_code = models.CharField(max_length=255)
    link = models.ForeignKey(Link, on_delete=models.CASCADE, blank=True, null=True)
    user = models.CharField(max_length=255)
    chat_id = models.CharField(max_length=255)
    message_id = models.CharField(max_length=255)
    expiration = models.CharField(max_length=255)
    input = models.CharField(max_length=255, blank=True, null=True)
    response = models.CharField(max_length=10000, blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.user) +" "+ str(self.order_code)



''' 
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
'''
