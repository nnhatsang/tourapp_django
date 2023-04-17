from rest_framework import viewsets, viewsets, generics, status
from .models import *
from .serializers import *


class AttractionViewset(viewsets.ModelViewSet, generics.ListAPIView):
    queryset = Attraction.objects.filter(active=True)
    serializer_class = AttractionSerializer

# Create your views here.
