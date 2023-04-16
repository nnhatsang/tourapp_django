from django.urls import path, re_path, include
from rest_framework import routers
from . import views

r = routers.DefaultRouter()
r.register('attraction', views.AttractionViewset)

urlpatterns = [
    path('', include(r.urls)),

]
