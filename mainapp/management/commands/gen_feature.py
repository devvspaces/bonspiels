import json
from django.core.management.base import BaseCommand, CommandError
from events.models import Feature

class Command(BaseCommand):
    help = 'Creating Featured For tickets'

    def handle(self, *args, **options):
        try:
            names = ['Refreshment', 'VIP Seats', 'Pick & Drop']
            
            self.stdout.write(self.style.SUCCESS('Started'))

            # Creating codes instances first
            for i in names:
                Feature.objects.create(name=i)

            self.stdout.write(self.style.SUCCESS('Completed Successfully'))
        except Exception as e:
            e
            print(e)
            raise CommandError('Something went wrong here.')