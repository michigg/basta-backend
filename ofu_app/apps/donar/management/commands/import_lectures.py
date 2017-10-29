from django.core.management.base import BaseCommand, CommandError
from apps.donar.models import Room
from apps.donar.utils import migrate_data_lectures


class Command(BaseCommand):
    help = "Imports Lectures from UnivIS PRG. Requires Room import"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        migrate_data_lectures.main()
        self.stdout.write(self.style.SUCCESS('Successfully migrate data'))
