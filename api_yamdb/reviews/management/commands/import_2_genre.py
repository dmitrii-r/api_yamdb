import csv
from django.core.management.base import BaseCommand
from django.conf import settings

from reviews.models import Genre


class Command(BaseCommand):
    """Заполняет базу данных образцами жанров для произведений.
    1. Очищает таблицу жанров в базе данных от всех строк.
    2. Импортирует данные из указанного csv-файла, подставляет их в поля
       модели и заполняет базу новыми объектами.
    Запуск команды: python3 manage.py import_2_genre
    """

    def handle(self, *args, **kwargs):
        Genre.objects.all().delete()
        csv_file_path = settings.BASE_DIR / 'static/data/genre.csv'

        with open(csv_file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                new_object = Genre()
                new_object.id = row['id']
                new_object.name = row['name']
                new_object.slug = row['slug']
                new_object.save()
