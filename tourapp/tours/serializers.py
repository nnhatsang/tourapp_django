from .models import *
from rest_framework import serializers


class AttractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attraction
        exclude = []
