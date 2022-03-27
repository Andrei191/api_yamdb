from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (filters, generics, mixins, permissions, status,
                            viewsets)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt import tokens
from users.models import User

from api_yamdb.settings import DEFAULT_FROM_EMAIL  # isort:skip
from .filters import TitleFilter  # isort:skip
from .permissions import (AuthorOrModerPermission,  # isort:skip
                          IsAdminOrReadOnlyPermission)  # isort:skip
from .serializers import (CategorySerializer, CommentSerializer,  # isort:skip
                          GenreSerializer, ReviewSerializer,  # isort:skip
                          TitleCreateSerializer,  # isort:skip
                          TitleReadSerializer,
                          CustomSignUpSerializer,
                          ObtainTokenSerializer)  # isort:skip
from reviews.models import Category, Genre, Review, Title  # isort:skip


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(Avg('reviews__score'))
    serializer_class = TitleCreateSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsAdminOrReadOnlyPermission,)
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH', 'DELETE']:
            return TitleCreateSerializer
        return TitleReadSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrModerPermission,)

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs['review_id'],
            title__id=self.kwargs['title_id']
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs['review_id'],
            title__id=self.kwargs['title_id']
        )
        serializer.save(author=self.request.user, review=review)


class ListCreateDestroyViewSet(
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        mixins.DestroyModelMixin,
        viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsAdminOrReadOnlyPermission,)
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AuthorOrModerPermission,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id,)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


@api_view(['POST'])
@permission_classes([AllowAny])
def registration(request):
    serializer = CustomSignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get("username")
    email = serializer.validated_data.get("email")
    try:
        user, created = User.objects.get_or_create(username=username,
                                                   email=email)
        confirmation_code = default_token_generator.make_token(user)
    except Exception:
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    mail.send_mail(
        'Yamdb confirmation code',
        confirmation_code,
        DEFAULT_FROM_EMAIL,
        [request.data['email']],
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


class CustomAuthToken(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ObtainTokenSerializer

    def post(self, request):
        serializer = ObtainTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        confirmation_code = serializer.data.get('confirmation_code')
        user = get_object_or_404(User, username=username)
        if default_token_generator.check_token(user, confirmation_code):
            token = tokens.AccessToken.for_user(user)
            return Response({'token': f'{token}'}, status=status.HTTP_200_OK)
        return Response({'confirmation_code': 'Неверный код подтверждения'},
                        status=status.HTTP_400_BAD_REQUEST)
