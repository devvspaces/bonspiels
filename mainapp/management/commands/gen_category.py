from django.core.management.base import BaseCommand, CommandError
from django.core.files import File

from events.models import Category

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent

class Command(BaseCommand):
    help = 'Creating Featured Locations'

    def handle(self, *args, **options):
        try:
            names = ['Food', 'Auto Show', 'Sports', 'Music Club']
            images = ['popular-event-1.jpg', 'popular-event-3.jpg', 'popular-event-4.jpg', 'popular-event-2.jpg', ]
            
            self.stdout.write(self.style.SUCCESS('Started'))

            # Creating codes instances first
            for name, image in zip(names, images):
                c = Category(name=name)
                c.image.save(f'{name}.jpg', File(open(os.path.join(BASE_DIR, image), 'rb')))

            self.stdout.write(self.style.SUCCESS('Completed Successfully'))
        except Exception as e:
            e
            print(e)
            raise CommandError('Something went wrong here.')