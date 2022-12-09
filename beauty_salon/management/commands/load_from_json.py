import json

from django.core.management.base import BaseCommand

from beauty_salon.utils import fill_database


class Command(BaseCommand):
    def handle(self, *args, **options):
        salons_filepath = 'salons.json'

        fill_database(salons_filepath)