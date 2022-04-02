from django.urls import include, path
from rest_framework import routers

from .views import PostViewSet, GroupViewSet, CommentViewSet, FollowViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'groups', GroupViewSet, basename='group')
router.register(r'follow', FollowViewSet, basename='follow')
router.register(
    r'posts/(?P<post_id>[0-9]+)/comments',
    CommentViewSet,
    basename='comment'
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
