from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    """Запускает команды на импорт базы данных из csv для всех моделей."""

    def handle(self, *args, **kwargs):
        call_command('import_1_category')
        call_command('import_2_genre')
        call_command('import_3_title')
        call_command('import_4_users')
        call_command('import_5_genre_title')
        call_command('import_6_review')
        call_command('import_7_comment')
