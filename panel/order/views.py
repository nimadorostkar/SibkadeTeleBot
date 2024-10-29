from rest_framework import viewsets, filters, status, pagination, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from link.models import Link
from order.models import Order
from order.serializers import OrderSerializer


class AddOrderView(APIView):
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]
    def post(self, *args, **kwargs):
        try:
            data = self.request.data
            serializer = self.serializer_class(data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
            return Response("done", status=status.HTTP_200_OK)
        except:
            return Response("Something went wrong, try again", status=status.HTTP_400_BAD_REQUEST)
