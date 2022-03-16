from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'pub_date', 'author')
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Comment)
admin.site.register(Title)
admin.site.register(Review)
