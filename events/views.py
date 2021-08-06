import random

from django.conf import settings
from django.forms import formset_factory
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, FormView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import logout,authenticate,login
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.encoding import force_text,force_bytes
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode

from account.models import User

from .models import Amenity, Event, EventReview, EventSchedule, EventView, Feature, Ticket, Gallery, EventSpeaker, Category, ReviewImage
from .forms import EventForm, EventScheduleForm, EventSpeakerForm, ReviewForm
from .utils import convert_str_date, get_valid_ip


class EventSearch(ListView):
    template_name = 'events/search-map-right.html'
    extra_context = {
        'title': 'Event Search'
    }
    model = Event
    context_object_name = 'events'

    def object_list(self):
        return self.get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["events"] = self.model.objects.all()
        context["category"] = Category.objects.all()
        return context
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data()

        # Check for query strings
        search = request.GET.get('search')
        if search:
            queryset = self.get_queryset()
            description = request.GET.get('description')
            if description:
                queryset = queryset.filter(description__icontains=description)
            
            location = request.GET.get('location')
            if location:
                queryset = queryset.filter(location__icontains=location)
            
            category = request.GET.get('category')
            if category:
                queryset = queryset.filter(category__id=category)
            
            start_time = request.GET.get('start_time')
            if start_time:
                # Convert to datetime
                start_time = convert_str_date(start_time)
                queryset = queryset.filter(s_time__gte = start_time)
            
            end_time = request.GET.get('end_time')
            if end_time:
                # Convert to datetime
                end_time = convert_str_date(end_time)
                queryset = queryset.filter(e_time__lte = end_time)
            
            context[self.context_object_name] = queryset

        return render(request, self.template_name, context)
    


class EventCalendar(TemplateView):
    template_name = 'events/event-calendar.html'
    extra_context = {
        'title': 'Event Calendar'
    }

class EventDetail(DetailView):
    template_name = 'events/event-detail.html'
    extra_context = {
        'title': 'Event Detail'
    }
    slug_field = 'uid'
    slug_url_kwarg = 'uid'
    model = Event

    def get_object(self):
        self.object = get_object_or_404(Event, uid=self.kwargs.get('uid'))
        return self.object
    
    # @property
    # def object(self):
    #     return self.get_object()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.title

        context['schedules'] = self.object.eventschedule_set.all()
        context['eventspeakers'] = self.object.eventspeaker_set.all()
        context['gallery'] = self.object.gallery_set.all()
        context['reviews'] = self.object.eventreview_set.all()
        context['event_views'] = self.object.eventview_set.count()

        valid_events_id_list = Event.objects.values_list('id', flat=True)
        random_event_id_list = random.sample(list(valid_events_id_list), min(len(valid_events_id_list), 10))
        context['related_events'] = Event.objects.filter(id__in=random_event_id_list)

        context['review_form'] = ReviewForm()

        return context
    
    def get(self, request, *args, **kwargs):
        # Count unique ip views
        ip = get_valid_ip(request)
        if ip:
            obj = self.get_object()
            if obj.eventview_set.filter(ip__exact=ip).exists() == False:
                EventView.objects.create(ip=ip, event=obj)
        self.get_object()
        context = self.get_context_data()

        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        request = self.request
        context = self.get_context_data()

        # Check if the user is authenticated
        if not request.user.is_authenticated:
            messages.warning(request, f'Kindly login your account or create a new account with the Login/Sign up button below')
            return redirect('mainapp:home')
        
        review_form = ReviewForm(request.POST, request.FILES)

        if review_form.is_valid():
            comment = review_form.cleaned_data.get('comment')
            stars = review_form.cleaned_data.get('stars')
            
            review = EventReview.objects.create(user=request.user, comment=comment, event=self.get_object(), stars=stars)

            queryImages = dict(request.FILES.lists())
            images = queryImages.get('images')
            if images:
                for i in images:
                    ReviewImage.objects.create(review=review, image=i)
            
            messages.success(request, f'Your review has been successfully submitted')
            return redirect(reverse('events:event-detail', kwargs={'uid': str(self.get_object().uid)}))
            

        context['review_form'] = review_form
        return render(request, self.template_name, context)
    

class CreateEvent(LoginRequiredMixin, TemplateView):
    template_name = 'events/add-event.html'
    extra_context = {
        'title': 'Add event'
    }
    form_class = EventForm
    event_schedule_form = formset_factory(EventScheduleForm)
    event_speaker_form = formset_factory(EventSpeakerForm)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add the forms to the context
        context['form'] = self.form_class()
        context['event_form'] = self.event_schedule_form(error_messages={'missing_management_form': 'Sorry, something went wrong.'})
        context['speaker_form'] = self.event_speaker_form(prefix='speaker', error_messages={'missing_management_form': 'Sorry, something went wrong.'})
        
        # Get the amenities and put to context
        context['amenities'] = Amenity.objects.all()

        # Get the features and put to context
        context['features'] = Feature.objects.all()

        # Tickets types
        context['tickets'] = range(3)

        return context
    
    def post(self, request, *args, **kwargs):
        request = self.request
        context = self.get_context_data()

        cloned = request.POST.copy()
        cloned['user'] = request.user

        queryDict = dict(cloned.lists())
        queryImages = dict(request.FILES.lists())

        # Getting the added amenities
        amenities = []
        for k,v in queryDict.items():
            if not k.find('amenities-'):
                if v[0] == 'on':
                    amenity_id = k.split('-')[1]
                    amenities.append(get_object_or_404(Amenity, id=int(amenity_id)))
        
        # Creating the tickets
        # Let's know if a ticket was added first
        useTicket = queryDict.get('use-ticket')
        if useTicket and useTicket == 'on':
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

        # Validating the event schedules
        event_form = self.event_schedule_form(cloned, error_messages={'missing_management_form': 'Sorry, something went wrong.'})

        # Validating the event speakers
        speaker_form = self.event_speaker_form(cloned, request.FILES, prefix='speaker',  error_messages={'missing_management_form': 'Sorry, something went wrong.'})

        form = self.form_class(cloned, request.FILES)
        if form.is_valid() and event_form.is_valid() and speaker_form.is_valid():
            event = form.save()

            # Create event schedules
            for i in event_form:
                EventSchedule.objects.create(
                    event=event,
                    start_date=i.cleaned_data.get('start_time'),
                    end_date=i.cleaned_data.get('end_time'),
                    title=i.cleaned_data.get('title'),
                    description=i.cleaned_data.get('description')
                )
            
            # Create speakers
            for i in speaker_form:
                EventSpeaker.objects.create(
                    event=event,
                    name=i.cleaned_data.get('name'),
                    image=i.cleaned_data.get('image'),
                    designation=i.cleaned_data.get('designation')
                )

            # Add the event tickets
            if useTicket and useTicket == 'on':
                for title, price, row, features in zip(ticket_titles, prices, rows, t_features):
                    ticket_1 = Ticket(title=title, price=price, row=row)
                    ticket_1.event = event
                    ticket_1.save()
                    ticket_1.featuring.set(features)
            
            # Add amenities to event
            event.amenities.set(amenities)

            # Getting and creating gallery images
            gallery = queryImages.get('gallery')
            if gallery:
                for i in gallery:
                    Gallery.objects.create(image=i, event=event)

            messages.success(request, 'Event has been successfully created')
            return redirect(reverse('events:event-detail', kwargs={'uid': str(event.uid)}))
        
        context['form'] = form
        context['event_form'] = event_form
        context['speaker_form'] = speaker_form
        messages.warning(request, 'Please make sure you correct the errors on the form')
        
        print(form.errors)
        print(event_form.errors)
        print(speaker_form.errors)
        
        return render(request, self.template_name, context)


# class CreateEvent(LoginRequiredMixin, TemplateView):
#     template_name = 'events/add-event.html'
#     extra_context = {
#         'title': 'Add event'
#     }
#     form_class = EventForm
#     event_schedule_form = formset_factory(EventScheduleForm)
#     event_speaker_form = formset_factory(EventSpeakerForm)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)