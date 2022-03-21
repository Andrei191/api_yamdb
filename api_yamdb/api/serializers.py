import datetime as dt

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from users.models import User

from .permissions import IsAdminOrReadOnlyPermission

from reviews.models import Comment, Genre, Category, Review, Title  # isort:skip


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name','slug','id')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name','slug',)


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True,)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category',)
        read_only_fields = fields


class TitleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field="slug",
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field="slug", many=True
    )

    class Meta:
        model = Title
        fields = ('name', 'year', 'description', 'genre', 'category',)

    def validate_year(self, value):
        year = dt.date.today().year
        if not (year - 2000000 < value <= year):
            raise serializers.ValidationError("Проверьте год произведения!")
        return value


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'author', 'text', 'created')
        read_only_fields = ('id',)



class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(slug_field="name", read_only=True)
    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )

    def validate_score(self, value):
        if 0 > value > 10:
            raise serializers.ValidationError("Оценка по 10-бальной шкале!")
        return value

    class Meta:
        model = Review
        fields = ('id', 'title', 'author', 'score')
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(), fields=('title', 'author')
            )
        ]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
