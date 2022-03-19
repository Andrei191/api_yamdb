from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, UserViewSet)

app_name = 'api'

router = routers.DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register('titles', TitleViewSet)
router.register(r'titles/(?P<title_id>\d+)/reviews', CommentViewSet,
                basename="reviews")
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments', CommentViewSet,
                basename="comments")
router.register('users',UserViewSet, basename="follows")


urlpatterns = [
    path('v1/', include(router.urls)),
]

