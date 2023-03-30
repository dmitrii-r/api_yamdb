from django.contrib import admin

from reviews.models import Category, Genre, Title

admin.site.register((Category, Genre, Title,))
