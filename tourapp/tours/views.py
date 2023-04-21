from rest_framework import viewsets, viewsets, generics, status
from .models import *
from .serializers import *
from rest_framework.decorators import action
from rest_framework.views import Response
from .paginators import *


class AttractionViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = Attraction.objects.filter(active=True)
    serializer_class = AttractionSerializer
    pagination_class = AttractionPaginator

    def get_queryset(self):
        query = self.queryset
        kw = self.request.query_params.get('kw')
        if kw:
            query = query.filter(location__icontains=kw)
        return query

    @action(methods=['get'], detail=True, url_path='tours')
    def tour(self, request, pk):
        tours = Attraction.objects.get(pk=pk).tours
        # tours=self.get_object()
        kw = self.request.query_params('kw')
        if kw is not None:
            tours = tours.filter(name__icontains = kw)
        return Response(AttractionSerializer(tours, many=True).data,status=status.HTTP_200_OK)


class TourViewSet(viewsets.ViewSet, generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Tour.objects.all()
    serializer_class = CommentSerializer

# Create your views here.
