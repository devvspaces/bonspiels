from django.core.management.base import BaseCommand, CommandError
from django.core.files import File

from mainapp.models import HomeBackground

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent

class Command(BaseCommand):
    help = 'Creating Home Backgrounds'

    def handle(self, *args, **options):
        try:
            images_path = ["event-grid-1", 'event-grid-2', 'event-grid-3',]
            
            self.stdout.write(self.style.SUCCESS('Started'))

            for image in images_path:
                img = HomeBackground()

                img.image.save(f'{image}.jpg', File(open(os.path.join(BASE_DIR, image+'.jpg'), 'rb')))

            self.stdout.write(self.style.SUCCESS('Completed Successfully'))
        except Exception as e:
            e
            print(e)
            raise CommandError('Something went wrong here.')