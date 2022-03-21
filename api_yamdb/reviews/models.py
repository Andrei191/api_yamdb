from cgitb import text
from django.db import models
from users.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


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
    name = models.CharField(max_length=256, verbose_name='Назваание произведения')
    year = models.IntegerField(verbose_name='Год произведения')
    description = models.TextField(verbose_name='Описание произведения')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                              blank=True, null=True,
                              related_name='titles',
                              verbose_name='Категория произвдения',
                              help_text='Выберите категорию')
    genre = models.ManyToManyField(Genre, related_name='titles')

class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, 
        related_name='reviews', null=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='author'
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата обновления', auto_now_add=True, db_index=True
    )
    class Meta:
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=["title", "author"], name="review_unique"
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

