from django.contrib import admin

from .models import Amenity, Event, Feature, FeaturedLocation, Ticket, Gallery, EventSpeaker, EventSchedule, Category, ReviewImage, EventReview

admin.site.register(Amenity)
admin.site.register(Category)
admin.site.register(Event)
admin.site.register(Feature)
admin.site.register(Ticket)
admin.site.register(Gallery)
admin.site.register(EventSpeaker)
admin.site.register(EventSchedule)
admin.site.register(EventReview)
admin.site.register(ReviewImage)
admin.site.register(FeaturedLocation)