from django.db import models
from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField()
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                              blank=True, null=True,
                              related_name='titles',
                              verbose_name='категория',
                              help_text='Выберите категорию')
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL,
                              blank=True, null=True,
                              related_name='titles',
                              verbose_name='жанр',
                              help_text='Выберите жанр')


class Review(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='author')
    rating = models.IntegerField()
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["title", "author"], name="review_unique",
            )
        ]


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

