from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, FormView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import logout,authenticate,login
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.encoding import force_text,force_bytes
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode

from datetime import datetime
from account.models import User

from .models import Amenity, Event, Feature, Ticket, Gallery, EventSpeaker
from .forms import EventForm

class EventDetail(DetailView):
    template_name = 'events/event-detail.html'
    extra_context = {
        'title': 'Event Detail'
    }
    slug_field = 'uid'
    slug_url_kwarg = 'uid'
    model = Event

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.title

        return context
    

class CreateEvent(TemplateView):
    template_name = 'events/add-event.html'
    extra_context = {
        'title': 'Add event'
    }
    form_class = EventForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get the amenities and put to context
        context['amenities'] = Amenity.objects.all()

        # Get the features and put to context
        context['features'] = Feature.objects.all()

        # Tickets types
        context['tickets'] = range(3)

        # Days of the weeks
        context['days'] = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        return context
    

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()

        # Sending the form to the template
        context['form'] = self.form_class()

        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        request = self.request
        context = self.get_context_data()

        cloned = request.POST.copy()
        cloned['user'] = request.user

        queryDict = dict(cloned.lists())
        queryImages = dict(request.FILES.lists())

        # print(queryDict)
        # print(queryImages) closed_mon-1
        amenities = []

        for k,v in queryDict.items():
            if not k.find('amenities-'):
                if v[0] == 'on':
                    amenity_id = k.split('-')[1]
                    amenities.append(get_object_or_404(Amenity, id=int(amenity_id)))
        
        # Creating the tickets
        # tickets = []
        t_features = [[] for i in range(3)]
        ticket_titles = queryDict.get('ticket_title')
        rows = queryDict.get('row')
        prices = queryDict.get('price')
        for k,v in queryDict.items():
            if not k.find('feature-'):
                if v[0] == 'on':
                    ticket_no, feature_id = k.split('-')[1], k.split('-')[2]
                    # Add the feature to the appropriate t_features index
                    t_features[int(ticket_no)].append(get_object_or_404(Feature, id=int(feature_id)))
        
        days_n = list(range(1,8))
        for k,v in queryDict.items():
            if not k.find('closed_mon-'):
                if v[0] == 'on':
                    c_no = int(k.split('-')[1])
                    days_n.remove(c_no)

        if len(days_n) > 0:
            start_time = queryDict.get('start_time')[days_n[0]]
            end_time = queryDict.get('start_time')[days_n[0]]
        else:
            start_time = queryDict.get('start_time')[0]
            end_time = queryDict.get('start_time')[0]

        start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M')
        end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M')

        form = self.form_class(cloned, request.FILES)
        if form.is_valid():
            event = form.save()

            event.start_time = start_time
            event.end_time = end_time

            # Add the event tickets
            for title, price, row, features in zip(ticket_titles, prices, rows, t_features):
                ticket_1 = Ticket(title=title, price=price, row=row)
                ticket_1.event = event
                ticket_1.save()
                ticket_1.featuring.set(features)
            
            # Add amenities to event
            event.amenities.set(amenities)

            # Getting and creating gallery images
            for i in queryImages.get('gallery'):
                Gallery.objects.create(image=i, event=event)

            event.save()

            messages.success(request, 'Event has been successfully created')
            return redirect(reverse('events:event-detail', kwargs={'uid': str(event.uid)}))
        
        context['form'] = form
        
        print(form.errors)
        
        return render(request, self.template_name, context)