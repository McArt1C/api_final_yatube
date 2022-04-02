from django.shortcuts import get_object_or_404
from rest_framework import viewsets, serializers, filters
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination

from posts.models import Post, Group, User
from .serializers import GroupSerializer, PostSerializer, CommentSerializer
from .serializers import FollowSerializer
from .permissions import IsOwnerOrIsAuthenticated, IsOwnerOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def validate_text(self, value):
        if len(value) > 0:
            raise serializers.ValidationError('Текст не должен быть пустым!')
        return value


@action(detail=True, gmethods=['get', 'post'])
class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsOwnerOrReadOnly,)


@action(detail=True, gmethods=['get', 'post'])
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        post_id = self.kwargs.get("post_id")
        post = get_object_or_404(Post, pk=post_id)
        return post.comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


@action(detail=True, gmethods=['get', 'post'])
class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = (IsOwnerOrIsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('user__username', 'following__username')

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user)
        return user.follower.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
