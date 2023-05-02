import datetime

from .models import *
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from datetime import datetime
from typing import Dict


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
        fields = ['id', 'content', 'tour', 'user', 'updated_date']
        extra_kwargs = {
            'user': {
                'read_only': True
            }
        }


class AddCommentBlogSerializer(ModelSerializer):
    class Meta:
        model = CommentBlog
        fields = ['id', 'content', 'blog', 'user', 'updated_date']
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

    def validate(self, data):
        tour = data.get('tour')
        departure_date = tour.departure_date
        end_date = tour.end_date
        user = data.get('user')
        email = user.email
        num_of_adults = data['num_of_adults']
        num_of_children = data['num_of_children']
        if not (tour.price_for_adults or tour.price_for_children):
            raise serializers.ValidationError("Tour price is not set.")
        if (num_of_adults <= 0) and (num_of_children <= 0):
            raise serializers.ValidationError("Invalid number of people.")
        if not email:
            raise serializers.ValidationError(
                'Users who do not have an email, please add email information before booking')

        # if not (departure_date <= datetime.today().date() <= end_date):
        #     raise serializers.ValidationError('Tour is not available on selected date')
        if not (departure_date >= datetime.today().date() and end_date > departure_date):
            raise serializers.ValidationError('Invalid date range')

        return data


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


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


class BlogSerializer(serializers.ModelSerializer):
    image_tour = serializers.SerializerMethodField(source='image')
    user = UserSerializer()

    def get_image_tour(self, obj):
        request = self.context.get('request')
        path = "/%s" % obj.image.name
        # if obj.image:
        #     image_tour = obj.image.url
        if request:
            return request.build_absolute_uri(path)

    class Meta:
        model = Blog
        exclude = ['image']
        extra_kwargs = {
            'image_tour': {
                "read_only": True
            },
        }


class CommentBlogSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        exclude = ['blog']
        model = CommentBlog


class LikeBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeBlog
        fields = '__all__'
