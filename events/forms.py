from django import forms
from django.utils import timezone
from django.core.validators import validate_email
from django.contrib.auth import password_validation
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.hashers import check_password

from django.forms import fields
from django.forms import formset_factory
from django.shortcuts import get_object_or_404

from .models import Event, UserTicket
from .utils import convert_str_date


class UserTicketForm(forms.ModelForm):
    class Meta:
        model = UserTicket
        fields = '__all__'
       
        
class ReviewForm(forms.Form):
    stars = forms.IntegerField()
    comment = forms.CharField(max_length=800)

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        # exclude = ('amenities',)