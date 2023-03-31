from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    """
    Запускает команды на импорт базы данных из csv для всех моделей.
    Начать импорт: python3 manage.py import_all

    Нумерация пользователей в csv начинается с 100, поэтому, если нет желания
    удалять уже занесенных в базу пользователей (и их меньше 100), то можно
    запустить команду с опцией --do-not-delete-users:
    python3 manage.py import_all --do-not-delete-users
    """

    def add_arguments(self, parser):
        parser.add_argument(
            '--do-not-delete-users',
            action='store_true',
            help='Do not delete existing users'
        )

    def handle(self, *args, **kwargs):
        call_command('import_1_category')
        call_command('import_2_genre')
        call_command('import_3_title')
        if kwargs['do_not_delete_users']:
            call_command('import_4_users', do_not_delete_users=True)
        else:
            call_command('import_4_users')
        call_command('import_5_genre_title')
        call_command('import_6_review')
        call_command('import_7_comment')
