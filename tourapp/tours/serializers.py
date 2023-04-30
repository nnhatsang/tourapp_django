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
        fields = ['location']


class AddCommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'tour', 'user']
        extra_kwargs = {
            'user': {
                'read_only': True
            }
        }


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        exclude = []


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
        exclude = ['customers', 'image', 'tag']
        extra_kwargs = {
            'image_tour': {
                'read_only': True
            },
        }


class BookTourSerializer(ModelSerializer):
    class Meta:
        model = BookTour
        exclude = []


class AddTourSerializer(ModelSerializer):
    class Meta:
        model = BookTour
        field = ['num_of_adults', 'num_of_children', 'user', 'tour']


class BillSerializer(ModelSerializer):
    class Meta:
        model = Bill
        exclude = []


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
        exclude = ['image_tour', 'descriptions']
        extra_kwargs = {
            'image_tour': {
                "read_only": True
            },
        }


# Rate


class AddRateSerializer(ModelSerializer):
    class Meta:
        model = Rate
        fields = ['id', 'star_rate', 'tour', 'user']
        extra_kwargs = {
            'user': {
                'read_only': True
            }
        }


class UserSerializer(ModelSerializer):
    image_avatar = serializers.SerializerMethodField(source='avatar')

    def get_image_avatar(self, obj):
        request = self.context.get('request')
        path = "/%s" % obj.avatar.name
        if request:
            return request.build_absolute_uri(path)

    def create(self, validated_data):
        data = validated_data.copy()
        u = User(**data)
        u.set_password(u.password)
        u.is_customer = True
        u.is_active = True
        u.save()
        return u

    class Meta:
        model = User
        exclude = ['groups', 'user_permissions']
        # fields = ['id', 'first_name', 'last_name', 'username', 'password', 'email', 'home_town',
        #           'image_avatar']
        extra_kwargs = {
            'avatar': {
                'write_only': True
            }, 'image_avatar': {
                'read_only': True
            }, 'password': {
                'write_only': True
            }

        }


class CustomerSerializer(ModelSerializer):
    image_avatar = serializers.SerializerMethodField(source='avatar')

    def get_image_avatar(self, obj):
        request = self.context.get('request')
        path = "/%s" % obj.avatar.name
        if request:
            return request.build_absolute_uri(path)

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'phone', 'image_avatar']
        kwargs = {
            'image_avatar': {
                'read_only': True
            },
        }


class CommentSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        exclude = ['tour']
        model = Comment


class RateSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Rate
        exclude = ['tour']
