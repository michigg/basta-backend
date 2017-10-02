from django.core.management.base import BaseCommand, CommandError
from apps.events.models import Event
from apps.events.utils.json_generator import controller_json_events
from apps.events.utils import migrate_data


class Command(BaseCommand):
    help = "Imports Food from special Websites"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        controller_json_events.main("apps/events/utils/json_generator/jsons/")
        migrate_data.main("apps/events/utils/json_generator/jsons/")
        self.stdout.write(self.style.SUCCESS('Successfully migrate data'))
