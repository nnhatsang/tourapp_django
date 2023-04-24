from django.urls import path, re_path, include
from rest_framework import routers
from . import views

r = routers.DefaultRouter()
r.register('attraction', views.AttractionViewSet)
r.register('rate', views.RateViewSet)
r.register('users', views.UserViewSet)
# r.register('comment', views.CommentViewset)

urlpatterns = [
    path('', include(r.urls)),

]
