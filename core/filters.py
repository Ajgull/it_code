import django_filters

from core.consts import STATUS_CHOICES
from core.models import Comment, Post, User


class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    description = django_filters.CharFilter(
        field_name='description', lookup_expr='startswith'
    )
    status = django_filters.ChoiceFilter(choices=STATUS_CHOICES)
    score_lte = django_filters.RangeFilter(field_name='score', lookup_expr='lte')

    class Meta:
        model = Post
        fields = ['title', 'description', 'author', 'category']


class CommentFilter(django_filters.FilterSet):
    content_iexact = django_filters.CharFilter(
        field_name='content', lookup_expr='iexact'
    )
    content_endswith = django_filters.CharFilter(
        field_name='content', lookup_expr='endswith'
    )

    class Meta:
        model = Comment
        fields = ['author', 'content_iexact']


class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(field_name='user', lookup_expr='icontains')

    class Meta:
        model = User
        fields = ['email']
