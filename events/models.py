import uuid

from django.db import models

from account.models import User

class Amenity(models.Model):
    name = models.CharField(max_length=30)
    icon = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    CATEGORY = (
        ('1', 'Concerts',),
        ('2', 'Food fest',),
        ('3', 'Auto show',),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    category = models.CharField(choices=CATEGORY, max_length=10)
    city = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    website = models.URLField()
    description = models.TextField()
    phone = models.CharField(max_length=25)
    email = models.EmailField()
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    dribble = models.URLField(blank=True)
    digg = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    google_plus = models.URLField(blank=True)
    amenities = models.ManyToManyField(Amenity)
    featured_image = models.ImageField(upload_to='events')
    seats = models.IntegerField()
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def all_amenities(self):
        li = []
        for i in Amenity.objects.all():
            ne = {}
            ne['name'] = i.name
            ne['avail'] = i.event_set.filter(id=self.id).exists()
            li.append(ne)
        return li



class Feature(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name 

class Ticket(models.Model):
    title = models.CharField(max_length=30)
    price = models.FloatField()
    row = models.IntegerField()
    featuring = models.ManyToManyField(Feature)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return self.title

class Gallery(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    image = models.ImageField(upload_to='events/gallery')
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.uid)


class EventSpeaker(models.Model):
    name = models.CharField(max_length=20)
    image = models.ImageField(upload_to='events/speakers')
    designation = models.CharField(max_length=30)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return self.name