import json
from django.core.management.base import BaseCommand, CommandError

from events.models import Amenity

class Command(BaseCommand):
    help = 'Creating Amenities'

    def handle(self, *args, **options):
        try:
            names = ['Airconditioner', 'Waiting room', 'Advance booking', 'Smoking Allowed', 'Wheel-chair Access']
            icons = ['wind', 'person-booth', 'bookmark', 'smoking-ban', 'wheelchair']
            
            self.stdout.write(self.style.SUCCESS('Started'))

            # Creating codes instances first
            for name, icon in zip(names, icons):
                a = Amenity.objects.create(name=name, icon=icon)
                print(f'Created {a.name}')

            self.stdout.write(self.style.SUCCESS('Completed Successfully'))
        except:
            raise CommandError('Something went wrong here.')