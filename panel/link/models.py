from django.db import models

class Link(models.Model):
    type_choices = (
        ("AppleMusic", "AppleMusic"),
        ("AppleOne", "AppleOne"),
        ("Spotify", "Spotify"),)
    duration_choices = (
        ("2 month", "2 month"),
        ("4 month", "4 month"),
        ("6 month", "6 month"),)

    type = models.CharField(max_length=100,choices=type_choices)
    duration = models.CharField(max_length=100,choices=duration_choices)
    code = models.CharField(max_length=255)
    link = models.TextField(max_length=2000)
    is_active = models.BooleanField(default=True)
    usable_times = models.IntegerField()
    used_times = models.IntegerField(default=0)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.type) +" "+ str(self.duration) +" | Id: "+ str(self.id)