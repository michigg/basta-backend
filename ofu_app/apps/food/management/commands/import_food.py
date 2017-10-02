from django.core.management.base import BaseCommand, CommandError
from apps.food.models import Menu, HappyHour, SingleFood
from apps.food.utils.json_generator import controller_json_food
from apps.food.utils import migrate_data

class Command(BaseCommand):
    help = "Imports Food from special Websites"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        controller_json_food.main("apps/food/utils/json_generator/jsons/")
        migrate_data.main("apps/food/utils/json_generator/jsons/")

