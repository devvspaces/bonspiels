from django.core.management.base import BaseCommand, CommandError
from django.core.files import File

from mainapp.models import HomeLocation

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent

BASE_DIR = os.path.join(BASE_DIR, 'icons_bonspiels')

print(BASE_DIR)

class Command(BaseCommand):
    help = 'Creating Home Locations'

    def handle(self, *args, **options):
        try:
            # path = "/Users/HP6460B/bonspiels/mainapp/management/commands/"
            names = ['Alberta', 'British-Columbia', 'europe', 'Manitoba', 'New-Brunswick', 'Newfoundland', 'Northern-Ontario', 'Northwest-Territories', 'Nova-Scotia', 'Nunavut', 'Ontario', 'Prince-Edward-Island', 'Quebec', 'Saskatchewan', 'United-States', 'Yukon']
            images_path = [f'{i}.png' for i in names]
            
            self.stdout.write(self.style.SUCCESS('Started'))

            # Creating codes instances first
            for name, image in zip(names, images_path):
                location = HomeLocation(name=name)

                location.image.save(f'{name}.png', File(open(os.path.join(BASE_DIR, image), 'rb')))

                location.save()

            self.stdout.write(self.style.SUCCESS('Completed Successfully'))
        except Exception as e:
            e
            print(e)
            raise CommandError('Something went wrong here.')