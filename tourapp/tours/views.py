from  rest_framework import viewsets,viewsets, generics,status
from. models import *
from .serializers import *
class AttractionViewset(viewsets.ModelViewSet):
    queryset = Attraction.objects.all()
    serializer_class = AttractionSerializer
# Create your views here.
