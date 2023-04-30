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
    serializer_class = AddRateSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [OwnerPermisson()]
        return [permissions.IsAuthenticated()]

    def create(self, request):
        serializer = AddRateSerializer(data=request.data)
        if serializer.is_valid():
            # gán người dùng hiện tại vào trường user của đối tượng Rate
            serializer.validated_data['user'] = request.user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


##USER
class UserViewSet(viewsets.ViewSet, generics.RetrieveAPIView, generics.UpdateAPIView, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, ]
    permission_classes = [permissions.AllowAny]

    def get_permissions(self):
        if self.action in ['partial_update', 'update', 'current_user', 'list_bill_paid', 'list_bill_unpaid',
                           'list_liked_tour']:
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

    @action(methods=['get'], url_path='list_bill_paid', detail=False)
    def list_bill_paid(self, request):
        user = request.user
        if user.is_authenticated:
            book_tours = BookTour.objects.filter(user=user)
            bill_paid = Bill.objects.filter(book_tour__in=book_tours, payment_state=True)
            paginator = Paginator(bill_paid, 10)  # phân trang
            page = request.GET.get('page')
            bill_page = paginator.get_page(page) if page else paginator.get_page(1)
            serializer = BillSerializer(bill_page, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data={"error_message": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], url_path='list_bill_unpaid', detail=False)
    def list_bill_unpaid(self, request):
        user = request.user
        if user.is_authenticated:
            book_tours = BookTour.objects.filter(user=user)
            bill_paid = Bill.objects.filter(book_tour__in=book_tours, payment_state=False)
            paginator = Paginator(bill_paid, 10)  # phân trang
            page = request.GET.get('page')
            bill_page = paginator.get_page(page) if page else paginator.get_page(1)
            serializer = BillSerializer(bill_page, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data={"error_message": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], url_path='list_bill_unpaid', detail=False)
    def list_bill_unpaid(self, request):
        user = request.user
        if user.is_authenticated:
            book_tours = BookTour.objects.filter(user=user)
            bill_paid = Bill.objects.filter(book_tour__in=book_tours, payment_state=False)
            paginator = Paginator(bill_paid, 10)  # phân trang
            page = request.GET.get('page')
            bill_page = paginator.get_page(page) if page else paginator.get_page(1)
            serializer = BillSerializer(bill_page, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data={"error_message": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], url_path='list_liked_tour', detail=False)
    def list_liked_tours(self, request):
        user = request.user
        if user.is_authenticated:
            likes = Like.objects.filter(user=user)
            paginator = PageNumberPagination()
            paginated_likes = paginator.paginate_queryset(likes, request)
            serializer = LikeSerializer(paginated_likes, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            return Response(data={"error_message": "User not found"}, status=status.HTTP_400_BAD_REQUEST)


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

    @action(methods=['get'], url_path='customers', detail=True, permission_classes=[permissions.IsAuthenticated])
    def get_customer(self, request, pk):
        customers = self.get_object().customers
        return Response(data=CustomerSerializer(customers, many=True, request={'request': request}).data)

    @action(methods=['get'], url_path='images', detail=True)
    def get_imagetour(self, request, pk=None):
        try:
            tour = Tour.objects.get(pk=pk)
        except Tour.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        imagetours = ImageTour.objects.filter(tour=tour)
        serializer = ImageTourSerializer(imagetours, many=True)

        return Response(serializer.data)

    @action(methods=['get'], url_path='rates', detail=True, permission_classes=[permissions.AllowAny])
    def get_rates(self, request, pk):
        tour = self.get_object()
        rate = tour.rate
        rate = rate.select_related('user')
        paginator = pagination.PageNumberPagination()
        pagination.PageNumberPagination.page_size = 10
        rate = paginator.paginate_queryset(rate, request)
        return paginator.get_paginated_response(RateSerializer(rate, many=True).data)


class CommentViewSet(viewsets.ViewSet, generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = AddCommentSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [OwnerPermisson()]
        return [permissions.IsAuthenticated()]

    def create(self, request):
        user = request.user
        if user:
            try:
                content = request.data.get('content')
                tour = Tour.objects.get(pk=request.data.get('tour'))
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            if tour and content:
                tour = Comment.objects.create(user=user, tour=tour, content=content)
                return Response(data=AddCommentSerializer(tour).data, status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={"error_message": "User not found"}, status=status.HTTP_400_BAD_REQUEST)


class BookTourViewSet(viewsets.ViewSet, generics.UpdateAPIView, generics.DestroyAPIView, generics.ListAPIView,
                      generics.RetrieveAPIView):
    queryset = BookTour.objects.all()
    serializer_class = BookTourSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy','create']:
            return [OwnerPermisson()]
        return [permissions.IsAuthenticated()]
# Create your views here.
