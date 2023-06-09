from django.urls import path, re_path, include
from rest_framework import routers
from . import views

r = routers.DefaultRouter()
r.register('attraction', views.AttractionViewSet)
r.register('rates', views.RateViewSet)
r.register('users', views.UserViewSet)
r.register('tours', views.TourViewSet)
r.register('comments', views.CommentViewSet)
r.register('book_tour', views.BookTourViewSet)
r.register('bills', views.BillViewSet)
r.register('tags', views.TagViewSet)
r.register('blog', views.BlogViewSet)
r.register('comment_blog', views.CommentBlogViewSet)

urlpatterns = [
    path('', include(r.urls)),

]
