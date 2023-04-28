from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from rest_framework import viewsets, viewsets, generics, status
from rest_framework.exceptions import ValidationError
from .models import *
from .serializers import *
from rest_framework.decorators import action
from rest_framework.views import Response
from rest_framework.parsers import MultiPartParser
from .paginators import *
from .perms import *

from django.db.models import DecimalField, ExpressionWrapper, Q
from decimal import Decimal
from datetime import datetime, date
from django.core.paginator import Paginator
from rest_framework.pagination import PageNumberPagination


class AttractionViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = Attraction.objects.filter(active=True)
    serializer_class = AttractionSerializer
    pagination_class = AttractionPaginator
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        query = self.queryset
        kw = self.request.query_params.get('kw')
        if kw:
            query = query.filter(location__icontains=kw)
        return query

    @action(methods=['get'], detail=True, url_path='tours')
    def get_tour(self, request, pk):
        tours = Attraction.objects.get(pk=pk).tours
        # tours=self.get_object()
        kw = self.request.query_params.get('kw')
        if kw is not None:
            tours = tours.filter(name__icontains=kw)
        return Response(TourSerializer(tours, many=True).data, status=status.HTTP_200_OK)


# Ratiing
class RateViewSet(viewsets.ViewSet, generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [OwnerPermisson()]
        return [permissions.AllowAny()]


##USER
class UserViewSet(viewsets.ViewSet, generics.RetrieveAPIView, generics.UpdateAPIView, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, ]
    permission_classes = [permissions.AllowAny]

    def get_permissions(self):
        if self.action in ['partial_update', 'update', 'retrieve', 'current_user', 'get_bill_unpaid', 'get_bill_paid']:
            return [UserOwnerPermisson()]
        return [permissions.AllowAny()]

    @action(methods=['get'], url_path='current_user', detail=False)
    def current_user(self, request):
        return Response(data=UserSerializer(request.user, context={'request': request}).data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True, url_path='change_password')
    def change_password(self, request, pk=None):
        user = self.get_object()
        password = request.data.get('password')
        if len(password) < 8:
            raise ValidationError('Mật khẩu mới phải có ít nhất 8 ký tự.')
        if password:
            user.set_password(password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class TourViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = Tour.objects.filter(active=True)
    serializer_class = TourSerializer
    pagination_class = TourPaginator
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        query = self.queryset
        query = query.select_related('attraction')
        kw = self.request.query_params.get('kw')
        departure_date = self.request.query_params.get('departure_date')
        price_from = self.request.query_params.get('price_from')
        price_to = self.request.query_params.get('price_to')

        if kw:
            query = query.filter(name__icontains=kw)
        if price_from or price_to:
            price_expression = ExpressionWrapper(
                Q(price_for_adults__gte=price_from, price_for_adults__lte=price_to) | \
                Q(price_for_children__gte=price_from, price_for_children__lte=price_to),
                output_field=DecimalField()
            )
            query = query.annotate(price_range=price_expression)
            if price_from:
                query = query.filter(Q(price_range__gte=Decimal(price_from)))
            if price_to:
                query = query.filter(Q(price_range__lte=Decimal(price_to)))
        if departure_date:
            try:
                departure_date = datetime.strptime(departure_date, "%Y-%m-%d").date()
            except:
                query = query.none()
            else:
                query = query.filter(departure_date__year=departure_date.year,
                                     departure_date__month=departure_date.month,
                                     departure_date__day=departure_date.day)
        return query

    @action(methods=['get'], url_path='tags', detail=True)
    def get_tags(self, request, pk):
        tags = self.get_object().tag
        return Response(data=TagSerializer(tags, many=True, context={'request': request}).data)

    #
    @action(detail=True, methods=['get'], url_path='comments', permission_classes=[permissions.AllowAny])
    def get_comments(self, request, pk):
        tour = self.get_object()
        comments = tour.comments.select_related('user')

        paginator = CommentPaginator()
        page = paginator.paginate_queryset(comments, request)
        return paginator.get_paginated_response(
            CommentSerializer(page, many=True, context={'request': request}).data)

    # @action(methods=['get'], url_path='images', detail=True, permission_classes=[permissions.AllowAny])
    # def get_images(self, request, pk):
    #     images = self.get_object().images
    #     return Response(data=ImageTourSerializer(images, many=True, context={'request': request}).data,
    #                     status=status.HTTP_200_OK)

    # @action(methods=['get'], url_path='rate', detail=True, permission_classes=[permissions.AllowAny])
    # def get_rate(self, request, pk):
    #     rates = self.get_object().rate
    #     paginator = RatePaginator()
    #     page = paginator.paginate_queryset(rates, request)
    #     return paginator.get_paginated_response(
    #         RateSerializer(page, many=True, context={'request': request}).data)
# Create your views here.
