import uuid

from django.db import models
from django.utils import timezone

from account.models import User

from .managers import EventManager
from .utils import strDate, ordinal


class Category(models.Model):
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to='events/categories')

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
    
    def get_first_event(self):
        return self.event_set.filter(user__active=True, published=True).first()

class Amenity(models.Model):
    name = models.CharField(max_length=30)
    icon = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    category = models.ManyToManyField(Category)
    city = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    website = models.URLField(blank=True)
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
    amenities = models.ManyToManyField(Amenity, blank=True)
    featured_image = models.ImageField(upload_to='events')
    seats = models.IntegerField()
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    s_time = models.DateTimeField(null=True)
    e_time = models.DateTimeField(null=True)
    featured = models.BooleanField(default=False)
    published = models.BooleanField(default=False)

    objects = EventManager()

    def __str__(self):
        return self.title

    def calc_rating(self):
        queryset = self.eventreview_set.all()
        x = queryset.count()
        rating = sum([i.stars for i in queryset])/(x if x else 1)
        return rating
    
    def get_stars(self):
        rating = int(self.calc_rating())
        all = [False] * 5
        for i in range(rating):
            all[i] = True
        
        return all
    
    def get_first_image(self):
        return self.gallery_set.first()
        

    def days_since_created(self):
        delta = timezone.now() - self.created
        days = delta.days
        seconds = delta.seconds
        hours = int(seconds/(60*60))
        mins = int(seconds/60)
        if days > 0:
            return strDate(days, 'day')
        elif hours > 0:
            return strDate(hours, 'hour')
        elif mins > 0:
            return strDate(mins, 'minute')
        elif seconds > 0:
            return strDate(seconds, 'second')
        
        return 'now'
            
    
    def all_amenities(self):
        li = []
        for i in Amenity.objects.all():
            ne = {}
            ne['name'] = i.name
            ne['avail'] = i.event_set.filter(id=self.id).exists()
            li.append(ne)
        return li

    def start_date(self):
        queryset = self.eventschedule_set.all()
        start_date = queryset[0].start_date

        for i in queryset:
            if i.start_date < start_date:
                start_date = i.start_date
        
        if self.s_time != start_date:
            self.s_time = start_date
            self.save()
        
        return start_date
    
    def end_date(self):
        queryset = self.eventschedule_set.all()
        end_date = queryset.last().end_date

        for i in queryset:
            if i.end_date > end_date:
                end_date = i.end_date
        
        if self.e_time != end_date:
            self.e_time = end_date
            self.save()
        
        return end_date
    
    # This function is for the javascript time countdown function 
    # Datetime is returned in this format 29 July 2020 9:56:00 GMT+01:00
    def end_date_js_format(self):
        end_date = self.end_date()
        return end_date.strftime("%d %b %Y %H:%M:%S %Z%z")

    def status(self):
        now = timezone.now()
        start_date = self.start_date()
        end_date = self.end_date()

        if (now >= start_date) and (end_date > now):
            return 'Running'
        elif now < start_date:
            return 'Upcoming'
        elif end_date <= now:
            return 'Completed'
    
    def price_text(self):
        queryset = self.ticket_set.all()
        if queryset.count() > 0:
            return 'Prices are high'
        
        return 'No fee'
    
    def price_val(self):
        queryset = self.ticket_set.all()
        if queryset:
            return '$$$'
        
        return 'Free'
    
    @property
    def organizer(self):
        return self.user.profile.full_name

    class Meta:
        ordering = ['s_time']

class EventSchedule(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return self.title



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


    def get_featured(self):
        row = ordinal(self.row) + ' row'
        features = [i.name for i in self.featuring.all()]
        features.insert(0, row)
        return ', '.join(features)

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


class EventCalendar(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey('account.User', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return str(self.uid)
    

class EventSave(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey('account.User', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return str(self.uid)


class EventView(models.Model):
    ip = models.CharField(max_length=200)
    # ip = models.GenericIPAddressField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return self.ip


class EventLike(models.Model):
    user = models.ForeignKey('account.User', on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return self.ip

class EventReview(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey('account.User', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    comment = models.TextField()
    stars = models.IntegerField(default=0)

    def get_stars(self):
        all = [False] * 5
        for i in range(self.stars):
            all[i] = True
        
        return all

    def __str__(self):
        return str(self.uid)

class ReviewImage(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    image = models.ImageField(upload_to='events/reviews/gallery')
    review = models.ForeignKey(EventReview, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.uid)


class FeaturedLocation(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='events/locations')

    def get_events(self):
        return Event.objects.filter(location__icontains=self.name, user__active=True, published=True)[:2]
    
    def count_listings(self):
        return Event.objects.filter(location__icontains=self.name).count()

    def __str__(self):
        return self.name


class UserTicket(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    attendees = models.IntegerField(default=1)
    ticket = models.ForeignKey(Ticket, on_delete=models.DO_NOTHING)
    user = models.ForeignKey('account.User', on_delete=models.CASCADE)
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def get_amount(self):
        return self.attendees * self.ticket.price

    def __str__(self):
        return str(self.uid)