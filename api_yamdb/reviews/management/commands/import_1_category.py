import csv
from django.core.management.base import BaseCommand
from django.conf import settings

from reviews.models import Category


class Command(BaseCommand):
    """
    Заполняет базу данных образцами категорий для произведений.
    1. Очищает таблицу категорий в базе данных от всех строк.
    2. Импортирует данные из указанного csv-файла, подставляет их в поля
       модели и заполняет базу новыми объектами.
    Запуск команды: python3 manage.py import_1_category
    """

    def handle(self, *args, **kwargs):
        Category.objects.all().delete()
        csv_file_path = settings.BASE_DIR / 'static/data/category.csv'
        categories = []
        with open(csv_file_path, 'r', encoding='utf-8') as file:            reader = csv.DictReader(file)
            for row in reader:
                new_object = Category()
                new_object.id = row['id']
                new_object.name = row['name']
                new_object.slug = row['slug']
                categories.append(new_object)
        Category.objects.bulk_create(categories)
