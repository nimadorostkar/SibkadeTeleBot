from rest_framework import serializers
from user.models import AuthorizedUser

class AuthorizedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthorizedUser
        fields = "__all__"