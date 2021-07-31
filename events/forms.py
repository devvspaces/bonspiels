from django import forms
from django.core.validators import validate_email
from django.contrib.auth import password_validation
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.hashers import check_password
from django.forms import fields
from django.shortcuts import get_object_or_404

from .models import Event, Ticket, Gallery, Amenity


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        exclude = ('amenities','end_time', 'start_time')
