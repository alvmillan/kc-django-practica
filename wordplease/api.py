from django.db.models import Count, Q
from django.utils import timezone
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from wordplease.filters import PostFilter
from wordplease.models import Blog, Post
from wordplease.permissions import PostPermissions
from wordplease.serializers import BlogSerializer, BlogPostsSerializer, PostSerializer, \
    PostListSerializer


class BlogViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = Blog.objects.select_related('owner').annotate(posts_count=Count('posts')).all().order_by('name')
    serializer_class = BlogSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name', 'description', 'owner__username')
    ordering_fields = ('name', 'owner', 'created_at')

    def get_serializer_class(self):
        return self.serializer_class if self.action != 'retrieve' else BlogPostsSerializer


class PostsViewSet(ModelViewSet):
    queryset = Post.objects.select_related('published_on__owner').all().order_by('-publication_date')
    serializer_class = PostSerializer
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    filter_class = PostFilter
    search_fields = ('title', 'introduction', 'body')
    ordering_fields = ('title', 'publication_date')
    permission_classes = (IsAuthenticatedOrReadOnly, PostPermissions)

    def get_serializer_class(self):
        return self.serializer_class if self.action != 'list' else PostListSerializer

    def get_queryset(self):
        if self.action == 'retrieve':
            self.queryset.select_related('published_on')

        if not self.request.user.is_authenticated:
            return self.queryset.filter(publication_date__lte=timezone.now())

        elif self.request.user.is_superuser:
            return self.queryset

        else:
            return self.queryset.filter(
                Q(published_on=self.request.user.blog) | Q(publication_date__lte=timezone.now())
            )

    def perform_create(self, serializer):
        serializer.save(published_on=self.request.user.blog)
        return serializer
