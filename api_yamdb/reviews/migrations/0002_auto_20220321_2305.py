# Generated by Django 2.2.16 on 2022-03-21 20:05

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GenreTitle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name': 'Комментарий', 'verbose_name_plural': 'Комментарии'},
        ),
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ('pub_date',), 'verbose_name': 'Отзыв', 'verbose_name_plural': 'Отзывы'},
        ),
        migrations.RemoveConstraint(
            model_name='review',
            name='review_unique',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='created',
        ),
        migrations.RemoveField(
            model_name='review',
            name='rating',
        ),
        migrations.AddField(
            model_name='comment',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, db_index=True, default=django.utils.timezone.now, verbose_name='дата публикации'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='review',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, db_index=True, default=django.utils.timezone.now, verbose_name='дата публикации'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='review',
            name='score',
            field=models.IntegerField(default=1, error_messages={'validators': 'Оценка от 1 до 10!'}, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)], verbose_name='оценка'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='review',
            name='text',
            field=models.CharField(default='string', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=256, unique=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='автор'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='review',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='reviews.Review', verbose_name='отзыв'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.CharField(max_length=200, verbose_name='текст комментария'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.CharField(max_length=256, unique=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL, verbose_name='автор'),
        ),
        migrations.AlterField(
            model_name='review',
            name='title',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='reviews.Title', verbose_name='произведение'),
        ),
        migrations.AlterField(
            model_name='title',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='titles', to='reviews.Category'),
        ),
        migrations.AlterField(
            model_name='title',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='title',
            name='genre',
        ),
        migrations.AlterField(
            model_name='title',
            name='name',
            field=models.CharField(max_length=256),
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('title', 'author'), name='unique review'),
        ),
        migrations.AddField(
            model_name='genretitle',
            name='genre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviews.Genre'),
        ),
        migrations.AddField(
            model_name='genretitle',
            name='title',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviews.Title'),
        ),
        migrations.AddField(
            model_name='title',
            name='genre',
            field=models.ManyToManyField(through='reviews.GenreTitle', to='reviews.Genre'),
        ),
    ]