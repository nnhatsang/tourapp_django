from  rest_framework import viewsets
from. models import *
from .serializers import *
class AttractionViewset(viewsets.ModelViewSet):
    queryset = Attraction.objects.all()
    serializer_class = AttractionSerializer
# Create your views here.
