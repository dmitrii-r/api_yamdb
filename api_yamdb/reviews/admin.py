from django.contrib import admin

from reviews.models import Category, Comment, Genre, Review, Title


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Админка для отзывов."""
    list_display = ('id', 'text', 'author', 'pub_date', 'title', 'score')
    search_fields = ('text', 'author')
    list_filter = ('pub_date', 'author', 'title')
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Админка для комментариев."""
    list_display = ('id', 'text', 'author', 'pub_date', 'review')
    search_fields = ('text', 'author')
    list_filter = ('pub_date', 'author', 'review')
    empty_value_display = '-пусто-'


admin.site.register((Category, Genre, Title,))
