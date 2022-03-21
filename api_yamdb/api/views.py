import django_filters
from django.shortcuts import render
from .permissions import IsAdminOrReadOnly, 
from rest_framework import filters, viewsets
from rest_framework.pagination import PageNumberPagination
from reviews.models import Category, Comment, Genre, Review, Title

from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, TitleReadSerializer,
                          TitleWriteSerializer)


class TitleFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name="category__slug")
    genre = django_filters.CharFilter(field_name="genre__slug")
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    year = django_filters.NumberFilter(field_name="year")
    class Meta:
        model = Title
        fields = ["category", "genre", "name", "year"]

class TitleViewSet(viewsets.ModelViewSet):
    """View для модели Title."""
    queryset = Title.objects.all()
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    filter_class = TitleFilter    
    permission_classes = (IsAdminOrReadOnly,)


    def get_serializer_class(self):
        if self.action == ('list', 'retrive'):
            return TitleReadSerializer
        return TitleWriteSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    """View для модели Category."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(viewsets.ModelViewSet):
    """View для модели Genre."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
