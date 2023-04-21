from rest_framework import viewsets, viewsets, generics, status
from .models import *
from .serializers import *
from rest_framework.decorators import action
from rest_framework.views import Response
from .paginators import *


class AttractionViewset(viewsets.ModelViewSet, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = Attraction.objects.filter(active=True)
    serializer_class = AttractionSerializer
    pagination_class = AttractionPaginator

    def get_queryset(self):
        q = self.queryset
        kw = self.request.query_params.get('kw')
        if kw:
            q = q.filter(location__icontains=kw)
        return q

    @action(methods=['get'], detail=True, url_path='tours')
    def tour(self, request, pk):
        t=Attraction.objects.get


class CommentViewset(viewsets.ModelViewSet, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

# Create your views here.
