import csv
from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth import get_user_model


from reviews.models import Comment, Review

User = get_user_model()


class Command(BaseCommand):
    """Заполняет базу данных образцами комментариев.
    1. Очищает таблицу комментариев в базе данных от всех строк.
    2. Импортирует данные из указанного csv-файла, подставляет их в поля
    модели и заполняет базу новыми объектами.
    Запуск команды: python3 manage.py import_7_comment
    """

    def handle(self, *args, **kwargs):
        Comment.objects.all().delete()
        csv_file_path = settings.BASE_DIR / 'static/data/comments.csv'

        with open(csv_file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                new_object = Comment()
                new_object.id = row['id']
                new_object.text = row['text']
                new_object.pub_date = row['pub_date']

                review_id = int(row['review_id'])
                review = Review.objects.get(id=review_id)
                new_object.review = review

                author_id = int(row['author'])
                author = User.objects.get(id=author_id)
                new_object.author = author

                new_object.save()
