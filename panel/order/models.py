from django.db import models
from link.models import Link

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