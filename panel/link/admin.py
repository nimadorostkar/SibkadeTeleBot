from django.contrib import admin
from .models import Link

class LinkAdmin(admin.ModelAdmin):
    list_display = ('code', 'type', 'duration', 'is_active')
    list_filter = ("type", "duration", "is_active")
    search_fields = ['code', 'link']
admin.site.register(Link, LinkAdmin)