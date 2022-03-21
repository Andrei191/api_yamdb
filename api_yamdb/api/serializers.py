import datetime as dt
from typing_extensions import Required
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Comment, Genre, Category, Review, Title 


class TitleReadSerializer(serializers.ModelSerializer):
    category = SlugRelatedField(read_only=True, many=False)
    genre = SlugRelatedField(read_only=True, many=True)
    raiting = serializers.IntegerField(read_only=True, Required=False)

    class Meta:
        fields = ('id', 'name', 'year', 'rating', 'description', 'ganre', 'category')
        model = Title

    def get_rating (self, obj):
        pass

class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queriset = Category.objects.all(), 
        slug_field='slug'
    )
    genre = SlugRelatedField(
        queriset = Category.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        fields = ('name', 'year', 'rating', 'description', 'ganre', 'category')
        model = Title

    def validate_year(self, value):
        year = dt.date.today().year
        if not (0 < value <= year):
            raise serializers.ValidationError("Некорректный год")
        return value


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
        fields = ('name', 'slug')


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

