from django import forms
from django.utils import timezone
from django.core.validators import validate_email, RegexValidator
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
        exclude = ('slug',)


phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

class ContactForm(forms.Form):
    name = forms.CharField(max_length=25, required=False)
    phone = forms.CharField(max_length=17, required=False, validators=[phone_regex])
    message = forms.CharField(widget=forms.Textarea)
    email = forms.EmailField()