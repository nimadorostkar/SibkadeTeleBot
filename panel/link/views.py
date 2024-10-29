from rest_framework import viewsets, filters, status, pagination, mixins
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from link.models import Link
from link.serializers import LinkSerializer
from rest_framework.generics import GenericAPIView


class LinkView(APIView):
    permission_classes = [AllowAny]
    def get(self, *args, **kwargs):
        try:
            links = Link.objects.filter(is_active=True)
            data = {}
            for link in links:
                type = link.type
                duration = link.duration
                if type not in data:
                    data[type] = {}
                data[type][duration] = {
                    "code": link.code,
                    "link": link.link}
            return Response(data, status=status.HTTP_200_OK)
        except:
            return Response("Something went wrong, try again", status=status.HTTP_400_BAD_REQUEST)


class LinkItemView(APIView):
    permission_classes = [AllowAny]
    def get(self, *args, **kwargs):
        try:
            link = Link.objects.get(code=self.kwargs["code"])
            # do sth...
            return Response("done", status=status.HTTP_200_OK)
        except:
            return Response("Something went wrong, try again", status=status.HTTP_400_BAD_REQUEST)



class LinkItemAddUsageView(APIView):
    permission_classes = [AllowAny]
    def get(self, *args, **kwargs):
        try:
            link = Link.objects.get(id=self.kwargs["id"])
            link.used_times += 1
            if link.used_times >= link.usable_times:
                link.is_active = False
            link.save()
            return Response("done", status=status.HTTP_200_OK)
        except:
            return Response("Something went wrong, try again", status=status.HTTP_400_BAD_REQUEST)


class LinkSearchView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LinkSerializer
    queryset = Link.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['code','type','duration','link']
    ordering_fields = ['id','duration','code','type']
    filterset_fields = ['duration', 'is_active','code','type','create_at']

    def get(self, request, format=None):
        query = self.filter_queryset(Link.objects.all())
        serializer = self.serializer_class(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)