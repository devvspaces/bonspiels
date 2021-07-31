from django.contrib import admin

from .models import Amenity, Event, Feature, Ticket, Gallery, EventSpeaker

admin.site.register(Amenity)
admin.site.register(Event)
admin.site.register(Feature)
admin.site.register(Ticket)
admin.site.register(Gallery)
admin.site.register(EventSpeaker)