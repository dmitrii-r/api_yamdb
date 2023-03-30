from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    """Категории (типы) произведений."""
    name = models.CharField(max_length=100, verbose_name='Название категории')
    slug = models.SlugField(max_length=40, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Категории жанров."""
    name = models.CharField(max_length=100, verbose_name='Название жанра')
    slug = models.SlugField(max_length=40, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    """
    Произведения, к которым пишут отзывы (определённый фильм, книга и т.д.)
    """
    name = models.CharField(max_length=200)
    year = models.IntegerField(verbose_name='Год выпуска',)
    description = models.TextField(max_length=3000)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='categories',
        blank=True,
        null=True,
        verbose_name='Категория',
        help_text='Категория, к которой относится произведение',
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        related_name='genres',
        verbose_name='Жанр',
        help_text='Жанр произведения',
    )

    def __str__(self):
        return self.name
