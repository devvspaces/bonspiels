from django.contrib import admin

from .models import (Amenity, Event, Feature, FeaturedLocation,
EventCalendar, Ticket, Gallery, EventSpeaker, EventSchedule,
Category, ReviewImage, EventReview, UserTicket, EventSave)


class EventScheduleInline(admin.StackedInline):
    model = EventSchedule
    extra = 0

class TicketInline(admin.StackedInline):
    model = Ticket
    max_num = 3

class EventSpeakerInline(admin.StackedInline):
    model = EventSpeaker
    extra = 0


@admin.action(description='Mark selected events as published')
def make_published(modeladmin, request, queryset):
    queryset.update(published=True)

class EventAdmin(admin.ModelAdmin):
    list_display = ('organizer','title', 'start_date', 'end_date', 'city', 'location', 'featured', 'published',)
    search_fields = ('title', 'city', 'location', 'email', 'website',)
    list_filter = ('featured', 'city', 'category', 'amenities', 's_time', 'e_time',)
    list_editable = ('featured',)
    actions = [make_published]

    inlines = [
        TicketInline,
        EventScheduleInline,
        EventSpeakerInline
    ]

admin.site.register(Amenity)
admin.site.register(Category)
admin.site.register(Event, EventAdmin)
admin.site.register(Feature)
admin.site.register(Ticket)
admin.site.register(Gallery)
admin.site.register(EventSpeaker)
admin.site.register(EventSchedule)
admin.site.register(EventReview)
admin.site.register(ReviewImage)
admin.site.register(FeaturedLocation)
admin.site.register(EventCalendar)
admin.site.register(UserTicket)
admin.site.register(EventSave)