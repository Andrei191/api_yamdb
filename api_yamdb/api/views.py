from django.shortcuts import get_list_or_404, get_object_or_404, render
from rest_framework import filters, mixins, permissions, viewsets
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User

from .permissions import (IsAdminOrReadOnlyPermission,
                          IsAuthorOrReadOnlyPermission,
                          IsModerOrReadOnlyPermission)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer,
                          UserSerializer)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    #permission_classes = (IsAuthorOrReadOnlyPermission, IsModerOrReadOnlyPermission, IsAdminOrReadOnlyPermission)

    #def get_queryset(self):
    #    title_id = self.kwargs.get("title_id")
    #    title = get_object_or_404(Title, id=title_id)
    #    review_id = self.kwargs.get("review_id")
    #    review = get_object_or_404(Review, title=title)
    #    return title.comments.all()


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('category__name',)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    #permission_classes = (IsAdminOrReadOnlyPermission,)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    #permission_classes = (IsAuthorOrReadOnlyPermission,IsModerOrReadOnlyPermission, IsAdminOrReadOnlyPermission)

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        review = Review.objects.filter(title_id=title_id)
        return review

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        review = get_object_or_404(Review, title_id=title_id)
        serializer.save(author=self.request.user, review=review)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    #permission_classes = (IsAdminOrReadOnlyPermission, )
