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


class AttractionViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = Attraction.objects.filter(active=True)
    serializer_class = AttractionSerializer
    pagination_class = AttractionPaginator

    def get_queryset(self):
        query = self.queryset
        kw = self.request.query_params.get('kw')
        if kw:
            query = query.filter(location__icontains=kw)
        return query

    @action(methods=['get'], detail=True, url_path='tours')
    def tour(self, request, pk):
        tours = Attraction.objects.get(pk=pk).tours
        # tours=self.get_object()
        kw = self.request.query_params('kw')
        if kw is not None:
            tours = tours.filter(name__icontains=kw)
        return Response(AttractionSerializer(tours, many=True).data, status=status.HTTP_200_OK)


# class TourViewSet(viewsets.ViewSet, generics.UpdateAPIView, generics.DestroyAPIView):
#     queryset = Tour.objects.all()
#     serializer_class = CommentSerializer


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

# Create your views here.
