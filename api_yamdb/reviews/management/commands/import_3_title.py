import csv
from django.core.management.base import BaseCommand
from django.conf import settings

from reviews.models import Title, Category


class Command(BaseCommand):
    """Заполняет базу данных образцами произведений.
    1. Очищает таблицу произведений в базе данных от всех строк.
    2. Импортирует данные из указанного csv-файла, подставляет их в поля
       модели и заполняет базу новыми объектами.
    Запуск команды: python3 manage.py import_3_title
    """

    def handle(self, *args, **kwargs):
        Title.objects.all().delete()
        csv_file_path = settings.BASE_DIR / 'static/data/titles.csv'

        with open(csv_file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                new_object = Title()
                new_object.id = row['id']
                new_object.name = row['name']
                new_object.year = row['year']

                category_id = int(row['category'])
                category = Category.objects.get(id=category_id)
                new_object.category = category

                new_object.save()
