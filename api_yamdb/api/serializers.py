from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from users.models import User  # isort:skip
from reviews.models import (Comment, Genre,  # isort:skip
                            Category, Review, Title)  # isort:skip


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug',)


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True,)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(source='reviews__score__avg',
                                      read_only=True,)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description',
                  'genre', 'category', 'rating',)
        read_only_fields = fields


class TitleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug',
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description',
                  'genre', 'category', 'rating')


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(slug_field='text', read_only=True)
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(slug_field='name', read_only=True)
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    def validate_score(self, value):
        if 0 > value >= 10:
            raise serializers.ValidationError('Оценка по 10-бальной шкале!')
        return value

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context.get("view").kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (
            request.method == 'POST'
            and Review.objects.filter(title=title, author=author).exists()
        ):
            raise ValidationError('Вы уже написали отзыв!')
        return data

    class Meta:
        fields = '__all__'
        model = Review


class CustomSignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        max_length=254,
    )
    username = serializers.RegexField(
        regex=r'^[\w.@+-]',
        required=True,
        max_length=150
    )

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate(self, value):
        username = value['username']
        if username == 'me':
            raise ValidationError('Недопустимое имя')
        return value


class ObtainTokenSerializer(serializers.Serializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]',
        required=True,
        max_length=150
    )
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'username', 'bio', 'email', 'role'
        )


class MeSerializer(serializers.ModelSerializer):
    role = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'username', 'bio', 'email', 'role'
        )
