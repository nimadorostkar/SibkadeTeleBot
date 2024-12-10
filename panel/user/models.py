from django.db import models


class AuthorizedUser(models.Model):
    user_id = models.CharField(max_length=255)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user_id) +" "+ str(self.create_at)