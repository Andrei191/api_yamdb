from django.urls import include, path
from rest_framework import routers

from .views import (CategoryViewSet, CommentViewSet,  # isort:skip
                    GenreViewSet,  # isort:skip
                    ReviewViewSet, TitleViewSet)  # isort:skip
from users.views import UserViewSet  # isort:skip
from .views import registration, CustomAuthToken

router = routers.DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register('titles', TitleViewSet)
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet,
                basename="reviews")
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename="comments")
router.register('users', UserViewSet)


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/token/', CustomAuthToken.as_view()),
    path('v1/auth/signup/', registration),
]
