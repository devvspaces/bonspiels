from django.contrib import admin

from .models import (Amenity, Event, FeaturedLocation,
EventCalendar, Gallery, Category, ReviewImage,
EventReview, UserTicket, EventSave, EventReport)


@admin.action(description='Mark selected events as published')
def make_published(modeladmin, request, queryset):
    queryset.update(published=True)

class EventAdmin(admin.ModelAdmin):
    list_display = ('organizer','title', 'start_date', 'end_date', 'location', 'featured', 'published',)
    search_fields = ('title', 'location', 'email', 'website',)
    list_filter = ('featured', 'category', 'amenities', 'start_date', 'end_date',)
    list_editable = ('featured',)
    actions = [make_published]

admin.site.register(Amenity)
admin.site.register(Category)
admin.site.register(Event, EventAdmin)
admin.site.register(Gallery)
admin.site.register(EventReview)
admin.site.register(ReviewImage)
admin.site.register(FeaturedLocation)
admin.site.register(EventCalendar)
admin.site.register(UserTicket)
admin.site.register(EventSave)
admin.site.register(EventReport)