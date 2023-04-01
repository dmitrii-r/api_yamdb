import csv
from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth import get_user_model


from reviews.models import Title, Review

User = get_user_model()


class Command(BaseCommand):
    """Заполняет базу данных образцами отзывов.
    1. Очищает таблицу отзывов в базе данных от всех строк.
    2. Импортирует данные из указанного csv-файла, подставляет их в поля
    модели и заполняет базу новыми объектами.
    Запуск команды: python3 manage.py import_6_review
    """

    def handle(self, *args, **kwargs):
        Review.objects.all().delete()
        csv_file_path = settings.BASE_DIR / 'static/data/review.csv'
        reviews = []
        with open(csv_file_path, 'r', encoding='utf-8') as file:            reader = csv.DictReader(file)
            for row in reader:
                new_object = Review()
                new_object.id = row['id']
                new_object.text = row['text']
                new_object.score = row['score']
                new_object.pub_date = row['pub_date']

                title_id = int(row['title_id'])
                title = Title.objects.get(id=title_id)
                new_object.title = title

                author_id = int(row['author'])
                author = User.objects.get(id=author_id)
                new_object.author = author

                reviews.append(new_object)
        Review.objects.bulk_create(reviews)
