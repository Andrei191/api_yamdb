from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from users.models import User

from .permissions import IsAdminOrReadOnlyPermission

from reviews.models import Comment, Genre, Category, Review, Title  # isort:skip

class TitleSerializer(serializers.ModelSerializer):
    category = SlugRelatedField(slug_field='name', read_only=True)
    genre = SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('author', 'review', 'text', 'created')
        read_only_fields = ('review',)


class CategorySerializer(serializers.ModelSerializer):
    permission_classes = (IsAdminOrReadOnlyPermission, )
    class Meta:
        model = Category
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Review
        fields = ('title', 'author')
        read_only_fields = ('post',)
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(), fields=('title', 'author')
            )
        ]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
