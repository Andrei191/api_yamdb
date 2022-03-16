from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views

app_name = 'api'

#router = routers.DefaultRouter()
#router.register('posts', PostViewSet)
#router.register('groups', GroupViewSet)
#router.register(r'/(?P<id>\d+)/comments', CommentViewSet,
#                basename="comments")
#router.register('follow', FollowViewSet, basename="follows")
#
#
#urlpatterns = [
#    path('v1/api-token-auth/', views.obtain_auth_token),
#    path('v1/', include(router.urls)),
#]
