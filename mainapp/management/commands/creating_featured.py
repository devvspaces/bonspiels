from django.core.management.base import BaseCommand, CommandError
from django.core.files import File

from events.models import FeaturedLocation

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent

class Command(BaseCommand):
    help = 'Creating Featured Locations'

    def handle(self, *args, **options):
        try:
            # path = "/Users/HP6460B/bonspiels/mainapp/management/commands/"
            names = ['California', 'London', 'Dubai', 'New York']
            images_path = ["location-1.jpg", 'location-2.jpg','location-3.jpg','location-4.jpg']
            
            self.stdout.write(self.style.SUCCESS('Started'))

            # Creating codes instances first
            for name, image in zip(names, images_path):
                location = FeaturedLocation(name=name)

                location.image.save(f'{name}.jpg', File(open(os.path.join(BASE_DIR, image), 'rb')))

            self.stdout.write(self.style.SUCCESS('Completed Successfully'))
        except Exception as e:
            e
            print(e)
            raise CommandError('Something went wrong here.')