import django_filters

from wordplease.models import Post


class PostFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name="categories")

    class Meta:
        model = Post
        fields = ['category']

