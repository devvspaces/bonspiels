import uuid
import json

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.safestring import mark_safe

from account.models import User

from .managers import EventManager
from .utils import strDate, ordinal

CURRENCY = (
    ('NGN', 'Nigerian naira',),
    ('USD', 'United States Dollar',),
    ('GBP', 'British Pounds',),
    ('EUR', 'Euro',),
)

SYMBOLS = {
    'NGN': '₦',
    'USD': '$',
    'GBP': '£',
    'EUR': '€',
}


class Category(models.Model):
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to='events/categories')

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
    
    def get_first_event(self):
        sets = self.event_set.filter(user__active=True, published=True)
        if sets.exists():
            return sets.first()
        return None

class Amenity(models.Model):
    name = models.CharField(max_length=30)
    icon = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.name

WEB_FORMAT = "%Y-%m-%d %H:%M"

class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=25, blank=True)
    organizer = models.CharField(max_length=225)
    email = models.EmailField()

    title = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    
    location = models.CharField(max_length=200)
    lat = models.FloatField(default=10, blank=True)
    lon = models.FloatField(default=10, blank=True)
    
    website = models.URLField(blank=True)
    description = models.TextField()

    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    instagram = models.URLField(blank=True)

    amenities = models.ManyToManyField(Amenity, blank=True)
    featured_image = models.ImageField(upload_to='events')
    seats = models.IntegerField()
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    featured = models.BooleanField(default=False)
    published = models.BooleanField(default=True)

    ticket_name = models.CharField(max_length=30, blank=True)
    ticket_price = models.FloatField(default=0, blank=True, null=True)
    ticket_currency = models.CharField(choices=CURRENCY, max_length=200, blank=True)

    # Information collect tools
    inform_tools_conf = models.CharField(max_length=700, blank=True, editable=False)

    likes = models.IntegerField(default=0, blank=True)
    views = models.IntegerField(default=0, blank=True)

    objects = EventManager()

    def get_currency_symbol(self):
        if self.ticket_currency:
            try:
                return SYMBOLS[self.ticket_currency]
            except KeyError:
                pass

        return '$'

    def get_price(self):
        return self.ticket_price if self.ticket_price else 0

    def get_website(self):
        return self.website if self.website else 'No website provided'

    def get_website_link(self):
        return self.website if self.website else '#'

    def get_tools_dict(self):
        try:
            return json.loads(self.inform_tools_conf)
        except Exception as e:
            pass

        return []

    def populate_information_fields(self):
        html = ''
        if self.inform_tools_conf:
            # convert json to dict
            try:
                json_dict = self.get_tools_dict()

                # loop to create form htmls with format strings
                for field in json_dict:
                    required=''
                    required2=''
                    if field['included_required'] == '11':
                        required='*'
                        required2='required'

                    name = field['name']
                    form_name = field['form_name']
                    _type = field['type']

                    html += f'''
                        <div class="form-group">
                            <label>{name}{required}</label>
                            <input {required2} type="{_type}" class="form-control bg-light" placeholder="Enter your {name}" name="{form_name}">
                        </div>
                    '''
            except Exception as e:
                print(e)
        
        return mark_safe(html)
        

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

    # This function is for the javascript time countdown function 
    # Datetime is returned in this format 29 July 2020 9:56:00 GMT+01:00
    def end_date_js_format(self):
        end_date = self.end_date
        return end_date.strftime("%d %b %Y %H:%M:%S %Z%z")

    def start_date_web_format(self):
        return self.start_date.strftime(WEB_FORMAT)

    def end_date_web_format(self):
        return self.end_date.strftime(WEB_FORMAT)

    def status(self):
        now = timezone.now()
        start_date = self.start_date
        end_date = self.end_date

        if (now >= start_date) and (end_date > now):
            return 'Running'
        elif now < start_date:
            return 'Upcoming'
        elif end_date <= now:
            return 'Completed'
    
    def price_text(self):
        return 'Prices are high' if self.ticket_price and (self.ticket_price > 0) else 'No fee'
    
    def price_val(self):
        return f'{self.get_currency_symbol()}{self.get_price()}' if self.ticket_price else 'Free'

    class Meta:
        ordering = ['start_date']



class Gallery(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    image = models.ImageField(upload_to='events/gallery')
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.uid)


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

    STATUS = (
        ('1', 'Pending',),
        ('2', 'Paid',),
    )

    information = models.CharField(max_length=700, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey('account.User', on_delete=models.CASCADE)
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS, max_length=1, default='1')

    def get_info_dict(self):
        try:
            return json.loads(self.information)
        except Exception as e:
            pass

        return []
    
    def get_status(self):
        if self.get_amount() <= 0:
            return 'No payment required'

        return self.get_status_display()

    def get_key(self, key):
        dic = self.get_info_dict()

        if dic:
            for i in settings.INFORMATION_TOOLS:
                if i['form_name'] == key:
                    for a in dic:
                        try:
                            return a[i['name']]
                        except KeyError:
                            pass

        return 'nil'

    def get_name(self):
        return self.get_key('team_name')

    def get_phone(self):
        return self.get_key('team_phone')

    def get_amount(self):
        return self.event.get_price()

    def __str__(self):
        return str(self.uid)


class EventReport(models.Model):
    reporter = models.ForeignKey('account.User', on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.event.title