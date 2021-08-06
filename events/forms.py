from django import forms
from django.utils import timezone
from django.core.validators import validate_email
from django.contrib.auth import password_validation
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.hashers import check_password

from django.forms import fields
from django.forms import formset_factory
from django.shortcuts import get_object_or_404

from .models import Event, EventSchedule, EventSpeaker
from .utils import convert_str_date



class ReviewForm(forms.Form):
    stars = forms.IntegerField()
    comment = forms.CharField(max_length=800)


class EventSpeakerForm(forms.ModelForm):
    class Meta:
        model = EventSpeaker
        fields = '__all__'
        exclude = ('event',)
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        exclude = ('amenities','end_time', 'start_time')

class EventScheduleForm(forms.Form):
    start_time = forms.CharField(max_length=30)
    end_time = forms.CharField(max_length=30)
    title = forms.CharField(max_length=30)
    description = forms.CharField(max_length=800)

    def clean_start_time(self):
        start_time = self.cleaned_data.get('start_time')
        try:
            t = convert_str_date(start_time)
            return t
        except Exception as e:
            raise forms.ValidationError('Your datetime is not in the correct format')
        
        return start_time
    
    def clean_end_time(self):
        end_time = self.cleaned_data.get('end_time')
        err = ''
        try:
            t = convert_str_date(end_time)
            if timezone.now() > t:
                err = 'Your event end time has passed'
        except Exception as e:
            err = 'Your datetime is not in the correct format'
        
        if err:
            raise forms.ValidationError(err)
        
        return end_time
    
    # def save(self):
    #     # Get the details and save to event
    #     event_id = self.data.get('event_id')
    #     event = get_object_or_404(Event, id=event_id)

    #     e = self.cleaned_data.get('start_time')
    #     start_time = convert_str_date(e)
    #     end_time = convert_str_date(self.cleaned_data.get('end_time'))
    #     title = self.cleaned_data.get('title')
    #     description = self.cleaned_data.get('description')

    #     event_schedule = EventSchedule.objects.create(event=event, start_date=start_time, end_date=end_time, title=title, description=description)

    #     return event_schedule