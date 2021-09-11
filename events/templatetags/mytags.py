import json

from django import template
from django.template.defaultfilters import stringfilter

from events.models import Event

register=template.Library()


# Code to return checked if the amentity id is in the event
@register.simple_tag()
def is_checked(event_id, amentity_id):
	event = Event.objects.get(id=event_id)
	return 'checked' if event.amenities.filter(id=amentity_id).exists() else ''


# Code to return checked if the tool is included
@register.simple_tag()
def check_included_tool(value):
	return 'checked' if value.startswith('1') else ''


# Code to return checked if the tool is required
@register.simple_tag()
def check_required_tool(value):
	return 'checked' if value.endswith('1') else ''