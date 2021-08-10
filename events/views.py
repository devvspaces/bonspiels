import random
from typing import List

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models.query_utils import Q
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

from account.models import Profile, User

from .models import (Amenity, Event, EventReview, EventSchedule, EventView, Feature,
Ticket, Gallery, EventSpeaker, Category, ReviewImage, EventCalendar, UserTicket)
from .forms import EventForm, EventScheduleForm, EventSpeakerForm, ReviewForm, EventTicketForm, UserTicketForm
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
        context["events"] = self.model.objects.all()[:10]
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
    


class EventCalendarView(LoginRequiredMixin, ListView):
    template_name = 'events/event-calendar.html'
    extra_context = {
        'title': 'Event Calendar'
    }
    model = EventCalendar
    context_object_name = 'events'
    
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class UserEventTickets(LoginRequiredMixin, ListView):
    template_name = 'events/tickets.html'
    extra_context = {
        'title': 'Ticket Orders'
    }
    model = UserTicket
    context_object_name = 'tickets'
    
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

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

    def get_context_data(self, **kwargs):
        self.get_object()
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
        
        user = self.request.user
        user_data = {}
        if user.is_authenticated:
            user_data = {'name': user.profile.full_name, 'email': user.email, 'phone': user.profile.phone, 'attendees': 1}
        context['ticket_form'] = UserTicketForm(initial=user_data)

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
        
        # Identify the form submitted
        submit = request.POST.get('submit')

        if submit == 'buy_ticket':
            cloned = request.POST.copy()
            cloned['user'] = request.user.id
            ticket_form = UserTicketForm(cloned)

            if ticket_form.is_valid():
                ticket_form.save()
                messages.success(request, 'Ticket is created succesfully')
                return redirect('events:my-tickets')
            
            print(ticket_form.errors)
            messages.warning(request, 'Please fill your ticket form correctly')

            context['ticket_form'] = ticket_form

        else:
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
    event_ticket_form = formset_factory(EventTicketForm, extra=3)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add the forms to the context
        context['form'] = self.form_class()
        context['event_form'] = self.event_schedule_form(error_messages={'missing_management_form': 'Sorry, something went wrong.'})
        context['speaker_form'] = self.event_speaker_form(prefix='speaker', error_messages={'missing_management_form': 'Sorry, something went wrong.'})
        context['ticket_form'] = self.event_ticket_form(prefix='ticket', error_messages={'missing_management_form': 'Sorry, something went wrong.'})
        
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

        # print(cloned)

        queryDict = dict(cloned.lists())
        queryImages = dict(request.FILES.lists())

        # Getting the added amenities
        amenities = []
        for k,v in queryDict.items():
            if not k.find('amenities-'):
                if v[0] == 'on':
                    amenity_id = k.split('-')[1]
                    amenities.append(get_object_or_404(Amenity, id=int(amenity_id)))

        # Validating the event schedules
        event_form = self.event_schedule_form(cloned, error_messages={'missing_management_form': 'Sorry, something went wrong.'})

        # Validating the event speakers
        speaker_form = self.event_speaker_form(cloned, request.FILES, prefix='speaker',  error_messages={'missing_management_form': 'Sorry, something went wrong.'})

        # Validating the event tickets
        ticket_form = self.event_ticket_form(cloned, prefix='ticket',  error_messages={'missing_management_form': 'Sorry, something went wrong.'})

        form = self.form_class(cloned, request.FILES)
        if form.is_valid() and event_form.is_valid() and speaker_form.is_valid() and ticket_form.is_valid():
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
            
            # Create tickets
            for i in ticket_form:
                ticket_m = Ticket.objects.create(
                    event=event,
                    title=i.cleaned_data.get('title'),
                    price=i.cleaned_data.get('price'),
                    row=i.cleaned_data.get('row'),
                )
                ticket_m.featuring.set(i.cleaned_data.get('featuring'))
            
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
        context['ticket_form'] = ticket_form
        messages.warning(request, 'Please make sure you correct the errors on the form')
        
        print(form.errors)
        print(event_form.errors)
        print(speaker_form.errors)
        print(ticket_form.errors)
        
        return render(request, self.template_name, context)


class MyEvent(LoginRequiredMixin, ListView):
    template_name = 'events/my_events.html'
    extra_context = {
        'title': 'My Events'
    }
    model = Event
    paginate_by = 10
    context_object_name = 'events'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class OrganizerEvents(LoginRequiredMixin, ListView):
    template_name = 'events/my_events.html'
    extra_context = {
        'title': ''
    }
    model = Event
    paginate_by = 10
    context_object_name = 'events'

    def get_object(self):
        return get_object_or_404(Profile, uid = self.kwargs.get('uid'))

    def get_queryset(self):
        return super().get_queryset().filter(user=self.get_object().user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context["title"] = f'{user.full_name()} events'
        context['custom_title'] = f'{user.full_name()} events'
        return context
    


@login_required
def add_event_to_calendar(request, uid):
    event = get_object_or_404(Event, uid=uid)
    relation = EventCalendar.objects.get_or_create(user=request.user, event=event)
    messages.success(request, f'Event is added to you calendar')
    return redirect('events:event-calendar')
