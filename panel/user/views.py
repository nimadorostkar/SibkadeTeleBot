from rest_framework import viewsets, filters, status, pagination, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from user.models import AuthorizedUser
from user.serializers import AuthorizedUserSerializer


class AuthorizedUsers(APIView):
    serializer_class = AuthorizedUserSerializer
    permission_classes = [AllowAny]
    def get(self, *args, **kwargs):
        try:
            authorized_users = AuthorizedUser.objects.all()
            serializer = self.serializer_class(authorized_users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response("Something went wrong, try again", status=status.HTTP_400_BAD_REQUEST)
