# Generated by Django 3.2 on 2023-03-29 04:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название категории')),
                ('slug', models.SlugField(max_length=40, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название жанра')),
                ('slug', models.SlugField(max_length=40, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('year', models.IntegerField(verbose_name='Год выпуска')),
                ('description', models.TextField(max_length=3000)),
                ('category', models.ForeignKey(help_text='Категория, к которой относится произведение', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='categories', to='reviews.category', verbose_name='Категория')),
                ('genre', models.ManyToManyField(help_text='Жанр произведения', related_name='genres', to='reviews.Genre', verbose_name='Жанр')),
            ],
        ),
    ]
