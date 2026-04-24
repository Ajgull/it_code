import django_filters
from django.db.models import QuerySet
from django.utils import timezone

from core.consts import STATUS_CHOICES
from core.models import Category, Comment, Post, Tag, User


class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    description = django_filters.CharFilter(field_name='description', lookup_expr='startswith')
    status = django_filters.ChoiceFilter(choices=STATUS_CHOICES)
    score_lte = django_filters.RangeFilter(field_name='score', lookup_expr='lte')

    category = django_filters.NumberFilter(field_name='category__id', lookup_expr='exact')

    author = django_filters.NumberFilter(field_name='author__id')
    author_username = django_filters.CharFilter(field_name='author__username', lookup_expr='icontains')

    created_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    created_today = django_filters.BooleanFilter(method='filter_created_today')

    class Meta:
        model = Post
        fields = ['title', 'description', 'author', 'category']

    def filter_created_today(self, queryset: QuerySet, name: str, value: bool) -> QuerySet:
        if value:
            today = timezone.now().date()
            return queryset.filter(created_at__date=today)
        return queryset


class CommentFilter(django_filters.FilterSet):
    content_iexact = django_filters.CharFilter(field_name='content', lookup_expr='iexact')
    content_endswith = django_filters.CharFilter(field_name='content', lookup_expr='endswith')

    class Meta:
        model = Comment
        fields = ['author', 'content_iexact']


class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(field_name='user', lookup_expr='icontains')

    class Meta:
        model = User
        fields = ['email']


class CategoryFilter(django_filters.FilterSet):
    class Meta:
        model = Category
        fields = ['title']


class TagFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Tag
        fields = ['name']
