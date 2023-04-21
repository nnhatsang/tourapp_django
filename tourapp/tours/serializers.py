from .models import *
from rest_framework import serializers


class AttractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attraction
        # exclude = []
        fields = ['location']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_date', 'updated_date']