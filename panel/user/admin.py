from django.contrib import admin
from user.models import AuthorizedUser


class AuthorizedUserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'create_at')
    list_filter = ("create_at",)
    search_fields = ['user_id', 'create_at']
admin.site.register(AuthorizedUser, AuthorizedUserAdmin)