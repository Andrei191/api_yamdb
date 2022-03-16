from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Comment, Genre, Category, Review, Title  # isort:skip


class TitleSerializer(serializers.ModelSerializer):
    category = SlugRelatedField(slug_field='name', read_only=True)
    genre = SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    review = serializers.SlugField(
        read_only=True,
        slug_field='id'
    )

    class Meta:
        model = Comment
        fields = ('author', 'review', 'text', 'created')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    title = serializers.SlugRelatedField(queryset=Title.objects.all(),
                                             slug_field='name',)

    class Meta:
        model = Review
        fields = ('title', 'author')
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(), fields=('title', 'author')
            )
        ]

