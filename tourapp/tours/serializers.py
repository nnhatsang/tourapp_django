from .models import *
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers


# from rest_framework.exceptions import AuthenticationFailed
# from .register import register_social_user
# from . import google, facebook
# from django.conf import settings


class AttractionSerializer(ModelSerializer):
    class Meta:
        model = Attraction
        exclude = []


class AttractionCompactSerializer(ModelSerializer):
    class Meta:
        model = Attraction
        field = ['location']


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        field = []


# Tour
class TourSerializer(ModelSerializer):
    attraction = AttractionCompactSerializer()
    image_tour = serializers.SerializerMethodField(source='image')

    def get_image_tour(self, obj):
        request = self.context.get('request')
        path = "/%s" % obj.image.name
        # if obj.image:
        #     image_tour = obj.image.url
        if request:
            return request.build_absolute_uri(path)

    class Meta:
        model = Tour
        exclude = ['customers', 'image']
        extra_kwargs = {
            'image_tour': {
                "read_only": True
            },
        }


class ImageTourSerializer(ModelSerializer):
    image_tour = serializers.SerializerMethodField(source='image')

    def get_image_tour(self, obj):
        request = self.context.get('request')
        path = "/%s" % obj.image.name
        # if obj.image:
        #     image_tour = obj.image.url
        if request:
            return request.build_absolute_uri(path)

    class Meta:
        model = ImageTour
        exclude = ['image']
        extra_kwargs = {
            'image_tour': {
                "read_only": True
            },
        }
