import csv
from django.core.management.base import BaseCommand
from django.conf import settings

from reviews.models import Title, Genre


class Command(BaseCommand):
    """Заполняет промежуточную many-to-many базу данных Произведение - Жанр.
    1. Очищает таблицу в базе данных от всех строк.
    2. Импортирует данные из указанного csv-файла, подставляет их в поля
       модели и заполняет базу новыми объектами.
    Запуск команды: python3 manage.py import_5_genre_title
    """

    def handle(self, *args, **kwargs):
        Title.genre.through.objects.all().delete()
        csv_file_path = settings.BASE_DIR / 'static/data/genre_title.csv'

        with open(csv_file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                title_id = int(row['title_id'])
                genre_id = int(row['genre_id'])
                genre = Genre.objects.get(id=genre_id)
                title = Title.objects.get(id=title_id)
                title.genre.add(genre)
                title.save()
