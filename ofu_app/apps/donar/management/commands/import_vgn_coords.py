from django.core.management.base import BaseCommand, CommandError
from apps.donar.utils import migrate_data_vgn_coords

class Command(BaseCommand):
    help = "Imports Rooms from Univis PRG"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        migrate_data_vgn_coords.migrate()
