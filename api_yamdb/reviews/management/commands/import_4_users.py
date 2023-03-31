import csv
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()


class Command(BaseCommand):
    """Заполняет базу данных образцами пользователей.
    1. Очищает таблицу пользователей в базе данных от всех строк.
    2. Импортирует данные из указанного csv-файла, подставляет их в поля
       модели и заполняет базу новыми объектами.
    Запуск команды: python3 manage.py import_4_users
    """

    def handle(self, *args, **kwargs):
        User.objects.all().delete()
        csv_file_path = settings.BASE_DIR / 'static/data/users.csv'

        with open(csv_file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                new_object = User()
                new_object.id = row['id']
                new_object.username = row['username']
                new_object.email = row['email']
                new_object.role = row['role']
                new_object.bio = row['bio']
                new_object.save()
