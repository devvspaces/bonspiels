import random
import os
from pathlib import Path
from datetime import timedelta

from django.core.files import File
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from account.models import User
from events.models import Event, Amenity, EventSchedule, Category, EventSpeaker, Gallery



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent


class Command(BaseCommand):
    help = 'Creating Events'

    def handle(self, *args, **options):
        try:
            # No of events to create
            num = 50
            titles = ['Picture', 'Home', 'going', 'music', 'Live party', 'Homecoming', 'Summer Holiday', 'Metal club', 'Openig up']
            user = User.objects.first()
            categories = Category.objects.all()
            cities = ['Manitoba', 'California', 'London', 'New york', 'Dubai', 'New-Brunswick', 'Newfoundland and Labrador', 'Northwest Territories', 'alberta']
            description = "Productivity is never an accident. It is always the result of a commitment to excellence, intelligent planning, and focused effort. \
                There are some people who live in a dream world, and there are some who face reality; and then there are those who turn one into the other"
            phone = '+233-533248378'
            email = user.email
            amenity_ids = [i.id for i in Amenity.objects.all()]
            images = ['related-event-1','related-event-5','related-event-4','related-event-2','related-event-3',]
            names = ['Peter', 'Michael', 'Ayomide', 'Usher', 'Mark', 'Samantha', 'John', 'Ferani', 'Aishat', 'Solomon', 'Grundy']
            designations = ['Show stopper', 'MC', 'Events arranger', 'Public Awareness', 'Caterer']
            teams = ['team-1','team-2','team-3','team-4','team-5','team-6']

            gallery = ['event-grid-1', 'event-grid-2', 'event-grid-3', 'event-grid-4', 'event-grid-5', 'gallery-1', 'gallery-2',  'gallery-3']
            
            self.stdout.write(self.style.SUCCESS('Loaded basic data, Starting'))

            for n in range(num):
                # Create an event
                title = ' '.join(random.sample(titles, 8)).lower().capitalize()[:45]
                city = random.choice(cities)
                location = f'25, block street, avenue, {city}'
                seats = random.randint(50, 1000)
                featured = random.choice([True, False])

                event = Event(title=title, featured=featured, user=user, email=email, phone=phone, location=location, city=city, seats=seats, description=description)
                
                # Adding the featured image
                image = random.choice(images)
                event.featured_image.save(f'abc-{n}.jpg', File(open(os.path.join(BASE_DIR, image+'.jpg'), 'rb')))

                print('Created event and added image')

                amenities = [Amenity.objects.get(id=i) for i in random.sample(amenity_ids, 3)]
                event.amenities.set(amenities)
                category = random.choice(categories)
                event.category.set([category])

                print('Created event and added relateds')

                # Creating gallery for event
                for a,b in enumerate(random.sample(gallery, 3)):
                    gal = Gallery(event=event)
                    event.featured_image.save(f'galler-y-{b}.jpg', File(open(os.path.join(BASE_DIR, b+'.jpg'), 'rb')))

                # Create a schedule
                start_time = timezone.now() + timedelta(days=random.randint(2, 9))
                end_time = start_time + timedelta(days=random.randint(2, 9))
                e_title = ' '.join(random.sample(titles, 8)).lower().capitalize()[:45]
                EventSchedule.objects.create(title=e_title, description=description, start_date=start_time, end_date=end_time, event=event)

                print('Created event schedule and added to event')
                for x in range(random.randint(1, 3)):
                    name = random.choice(names)
                    designation = random.choice(designations)
                    img = random.choice(teams)

                    event_speaker = EventSpeaker(event=event, name=name, designation=designation)
                    event_speaker.image.save(f'speaker-{n}.jpg', File(open(os.path.join(BASE_DIR, img+'.jpg'), 'rb')))
                    
                    print('Created and saved speaker')

                # Create random speakers
                print(f'Event {n}')
            
            self.stdout.write(self.style.SUCCESS('Completed Successfully'))
        except Exception as e:
            print(e)
            e

            # Clean the created shits
            for i in Event.objects.all():
                i.delete()
            raise CommandError('Something went wrong here.')