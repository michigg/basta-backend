from django.core.management.base import BaseCommand, CommandError
from apps.donar.models import Room
from apps.donar.utils import migrate_data


class Command(BaseCommand):
    help = "Imports Rooms from Univis PRG"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        migrate_data.main()
        self.stdout.write(self.style.SUCCESS('Successfully migrate data'))
