from django.core.management.base import BaseCommand, CommandError
from apps.food.models import Menu, HappyHour, SingleFood
from apps.food.utils import migrate_data


class Command(BaseCommand):
    help = "Imports Food from special Websites"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        migrate_data.main()
