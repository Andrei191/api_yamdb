from django.shortcuts import render

from .models import Category, Comment, Genre, Review, Title
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer)

#class TitleViewSet
