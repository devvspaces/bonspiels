import random
import json
from typing import List
import uuid

from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models.query_utils import Q
from django.forms import formset_factory
from django.contrib import messages
from django.http.response import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, FormView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import logout,authenticate,login
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.encoding import force_text,force_bytes
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.http import JsonResponse

from account.models import Profile, User
from mainapp.mixins import ajax_autocomplete

from .models import (Amenity, Event, EventReview, EventSave,
    EventView, Gallery, Category, ReviewImage, EventCalendar,
    UserTicket, EventReport)
from .forms import EventForm, ReviewForm, UserTicketForm, ContactForm
from .utils import convert_str_date, get_valid_ip, get_trip_advisor



class RegisteredTeams(LoginRequiredMixin, ListView):
    template_name = 'events/registered_teams.html'
    extra_context = {
        'title': 'Registered Teams'
    }
    model = Event
    context_object_name = 'events'
    
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


def get_trips_view(request):
    if request.is_ajax():
        trips = []

        # Get the event id
        uid = request.GET.get('id')

        try:
            event = Event.objects.get(uid=uid)

            # Get the trips
            trips = get_trip_advisor(event.location)

            
        except Exception as e:
            print(e)
            pass

        return JsonResponse(data={'results': trips}, status=200)

    return redirect('mainapp:home')


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
        categories_set = Category.objects.all()
        queryset = self.model.objects.all()

        context["events"] = queryset[:10]
        context["category"] = categories_set

        # Send sets to context
        context['all_events'] = queryset
        context['all_categories'] = categories_set
        
        return context
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data()

        response = ajax_autocomplete(request, context)
        if response is not None:
            return response

        # Check for query strings
        search = request.GET.get('search')
        if search:
            queryset = self.get_queryset()
            search_input = request.GET.get('search-input')
            if search_input:
                # Search location
                queryset = queryset.filter(location__icontains=search_input)
                context['searchInput'] = search_input

            search_tcd = request.GET.get('search-tcd')
            if search_tcd:
                # Search decription and title
                queryset = queryset.filter(
                    Q(title__icontains=search_tcd) | Q(description__icontains=search_tcd) | Q(category__name__iexact=search_tcd)
                )
                context['search_tcd'] = search_tcd
            
            category = request.GET.get('category')
            if category:
                queryset = queryset.filter(category__id=category)
                context['searchCategory'] = int(category)
            # else:
            #     # Search for category
            #     if search_tcd:
            #         queryset = queryset.filter(category__name__iexact=search_tcd)

            start_time = request.GET.get('start_time')
            if start_time:
                context['start_time'] = start_time
                # Convert to datetime
                start_time = convert_str_date(start_time)
                queryset = queryset.filter(start_date__gte = start_time)
            
            end_time = request.GET.get('end_time')
            if end_time:
                context['end_time'] = end_time
                # Convert to datetime
                end_time = convert_str_date(end_time)
                queryset = queryset.filter(end_date__lte = end_time)

            # Sort the queryset
            sort = request.GET.get('sort')
            if sort:
                if sort == 'most_viewed':
                    queryset = queryset.order_by('-views')
                elif sort == 'most_recent':
                    queryset = queryset.order_by('-created')
                elif sort == 'most_liked':
                    queryset = queryset.order_by('-likes')

            
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



from django.http import HttpResponse


from django_xhtml2pdf.utils import generate_pdf

def order_ticket(request, uid):
    resp = HttpResponse(content_type='application/pdf')
    
    ticket = get_object_or_404(UserTicket, uid=uid)

    context = {
        'ticket': ticket,
        'pagesize':'A4'
    }

    result = generate_pdf('events/ticket.html', file_object=resp, context=context)
    return result



class EventDetail(DetailView):
    template_name = 'events/event-detail.html'
    extra_context = {
        'title': 'Event Detail'
    }
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    model = Event

    def get_object(self):
        query = { self.slug_field : self.kwargs.get(self.slug_url_kwarg)}
        self.object = get_object_or_404(Event, **query)
        return self.object

    def get_context_data(self, **kwargs):
        self.get_object()

        context = super().get_context_data(**kwargs)
        context["title"] = self.object.title

        context['gallery'] = self.object.gallery_set.all()
        context['reviews'] = self.object.eventreview_set.all()

        valid_events_id_list = Event.objects.filter(published=True, user__active=True).values_list('id', flat=True)
        random_event_id_list = random.sample(list(valid_events_id_list), min(len(valid_events_id_list), 10))
        context['related_events'] = Event.objects.filter(id__in=random_event_id_list)

        context['review_form'] = ReviewForm()

        context['contact'] = ContactForm()

        context['trips'] = []

        return context
    
    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        # Check if the organizer is active
        if (obj.user.is_active == False) or (obj.published == False):
            return redirect('mainapp:home')
        
        obj.views = obj.views + 1
        obj.save()

        context = self.get_context_data()

        return render(request, self.template_name, context)

    def redirect_to_self(self):
        # Redirects the current view back to the save page
        return redirect(reverse('events:event-detail', kwargs={'slug': str(self.get_object().slug)}))
    
    def post(self, request, *args, **kwargs):
        request = self.request
        context = self.get_context_data()

        # Check if the user is authenticated
        if not request.user.is_authenticated:
            messages.warning(request, f'Kindly login your account or create a new account with the Login/Sign up button below')
            return redirect('mainapp:home')
        
        # Identify the form submitted
        submit = request.POST.get('submit')

        event = self.get_object()

        if submit == 'buy_ticket':
            ticket_errors = []
            ticket_infomation = []
            # Validate submited form

            info_tools = event.get_tools_dict()
            post = request.POST

            for fobj in info_tools:
                # Get the field
                label = fobj['name']
                name = fobj['form_name']
                info = post.get(name)

                d_info = {label:info}

                if name == 'line_up':
                    names = ['first', 'second', 'third', 'fourth']

                    d_info = {'line_up': []}

                    for i in names:
                        datax = post.get(i)
                        dataxi = post.get(f'{i}_line')

                        dataxi = 'Yes' if dataxi == 'on' else ''

                        data_obj = {
                            i.capitalize() : datax,
                            'captain': dataxi
                        }

                        d_info['line_up'].append(data_obj)

                elif fobj['included_required'] == '11':
                    if not info:
                        ticket_errors.append(f'{label} is required')
                        continue

                # Add information to ticket information
                ticket_infomation.append(d_info)

            if len(ticket_errors) == 0:
                # Create ticket
                ticket = UserTicket(event=event, user=request.user, information=json.dumps(ticket_infomation))
                ticket.save()
                
                messages.success(request, 'Ticket is created succesfully')
                return self.redirect_to_self()


            messages.warning(request, 'Please fill your ticket form correctly')

            context['ticket_errors'] = ticket_errors

        elif submit == 'enquiry':
            contact = ContactForm(request.POST)

            if contact.is_valid():
                # Send message to the event organizer
                subject = 'General enquiry from Bonspiels Event'
                message=render_to_string('events/inquiry.html',{
                    "event": event,
                    "name": contact.cleaned_data.get('name'),
                    "email": contact.cleaned_data.get('email'),
                    "phone": contact.cleaned_data.get('phone'),
                    "message": contact.cleaned_data.get('message'),
                    'from': settings.DEFAULT_FROM_EMAIL
                })

                print(message)

                # Send email to organizer
                organizer_email = event.email

                send_mail(subject=subject, message=message, from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=[organizer_email], fail_silently=True)

                messages.success(request, 'Your enquiry has been delivered to the event organizer successfully')

                return self.redirect_to_self()

            messages.warning(request, 'Errors found in inquiry form')

            print(contact.errors)

            context['contact'] = contact

        else:
            review_form = ReviewForm(request.POST, request.FILES)
            if review_form.is_valid():
                comment = review_form.cleaned_data.get('comment')
                stars = review_form.cleaned_data.get('stars')
                
                review = EventReview.objects.create(user=request.user, comment=comment, event=event, stars=stars)

                queryImages = dict(request.FILES.lists())
                images = queryImages.get('images')
                if images:
                    for i in images:
                        ReviewImage.objects.create(review=review, image=i)
                
                messages.success(request, f'Your review has been successfully submitted')
                
                return self.redirect_to_self()
            
            context['review_form'] = review_form

        return render(request, self.template_name, context)
    

class CreateEvent(LoginRequiredMixin, TemplateView):
    template_name = 'events/add-event.html'
    extra_context = {
        'title': 'Add event'
    }
    form_class = EventForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add the forms to the context
        context['form'] = self.form_class()

        # Get the amenities and put to context
        context['amenities'] = Amenity.objects.all()

        inform_tools = settings.INFORMATION_TOOLS
        context['inform_tools'] = inform_tools

        context['r_suffix'] = settings.INFORMATION_TOOLS_REQUIRED_SUFFIX

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

        form = self.form_class(cloned, request.FILES)
        if form.is_valid():
            event = form.save()

            # Add amenities to event
            event.amenities.set(amenities)

            # Getting and creating gallery images
            gallery = queryImages.get('gallery')
            if gallery:
                for i in gallery:
                    Gallery.objects.create(image=i, event=event)

            infofields = []

            # Get the appropriate information tools
            for fobj in context['inform_tools']:
                if request.POST.get(fobj['form_name']) == 'on':
                    val = '10'
                    if request.POST.get(fobj['form_name']+settings.INFORMATION_TOOLS_REQUIRED_SUFFIX)=='on':
                        val = '11'
                    # Copy the demo obj and add a key
                    demo = fobj.copy()
                    demo['included_required'] = val
                    infofields.append(demo)

            # compile infofields dict in to json string
            json_str = json.dumps(infofields)

            event.inform_tools_conf = json_str

            event.published = True

            event.save()
            
            messages.success(request, 'Event has been successfully created')
            return redirect(reverse('events:event-detail', kwargs={'slug': str(event.slug)}))
        
        context['form'] = form
        messages.warning(request, 'Please make sure you correct the errors on the form')
        
        print(form.errors)
        
        return render(request, self.template_name, context)



class UpdateEvent(LoginRequiredMixin, TemplateView):
    template_name = 'events/update_event.html'
    extra_context = {
        'title': 'Update event'
    }
    form_class = EventForm

    def get_object(self):
        return get_object_or_404(Event, uid=self.kwargs.get('uid'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.get_object()

        # Get the amenities and put to context
        context['amenities'] = Amenity.objects.all()

        inform_tools = settings.INFORMATION_TOOLS
        event_tools = event.get_tools_dict()

        # Merge event tools and inform-tools
        for a in inform_tools:
            for b in event_tools:
                if a['form_name'] == b['form_name']:
                    a['included_required'] = b['included_required']
                    break

        context['inform_tools'] = inform_tools

        context['r_suffix'] = settings.INFORMATION_TOOLS_REQUIRED_SUFFIX

        context['event'] = event
        context['form'] = self.form_class(instance=event, initial={
            'start_date': event.start_date_web_format(),
            'end_date': event.end_date_web_format(),
        })

        return context
    
    def post(self, request, *args, **kwargs):
        request = self.request
        context = self.get_context_data()

        cloned = request.POST.copy()
        cloned['user'] = request.user
        
        event = context['event']

        queryDict = dict(cloned.lists())
        queryImages = dict(request.FILES.lists())

        # Getting the added amenities
        amenities = []
        for k,v in queryDict.items():
            if not k.find('amenities-'):
                if v[0] == 'on':
                    amenity_id = k.split('-')[1]
                    amenities.append(get_object_or_404(Amenity, id=int(amenity_id)))

        form = self.form_class(cloned, request.FILES, instance=event)
        if form.is_valid():
            event = form.save()

            # Add amenities to event
            event.amenities.set(amenities)

            # Getting and creating gallery images
            gallery = queryImages.get('gallery')
            if gallery:
                # Clear the current gallery set
                for i in event.gallery_set.all():
                    i.delete()

                # Add the new images
                for i in gallery:
                    Gallery.objects.create(image=i, event=event)

            infofields = []

            # Get the appropriate information tools
            for fobj in context['inform_tools']:
                if request.POST.get(fobj['form_name']) == 'on':
                    val = '10'
                    if request.POST.get(fobj['form_name']+settings.INFORMATION_TOOLS_REQUIRED_SUFFIX)=='on':
                        val = '11'
                    # Copy the demo obj and add a key
                    demo = fobj.copy()
                    demo['included_required'] = val
                    infofields.append(demo)

            # compile infofields dict in to json string
            json_str = json.dumps(infofields)

            event.inform_tools_conf = json_str

            event.published = True

            event.save()
            
            messages.success(request, 'Event has been successfully updated')
            return redirect(reverse('events:event-detail', kwargs={'slug': str(event.slug)}))
        
        context['form'] = form
        messages.warning(request, 'Please make sure you correct the errors on the form')
        
        print(form.errors)
        
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
    
    def get(self, request, *args, **kwargs):
        # Check if the organizer is active
        if self.get_object().user.is_active == False:
            return redirect('mainapp:home')
        
        return super().get(request, *args, **kwargs)


class SavedEvents(LoginRequiredMixin, ListView):
    template_name = 'events/my_events.html'
    extra_context = {
        'title': 'My saved events',
        'custom_title': 'Saved events'
    }
    model = EventSave
    paginate_by = 10
    context_object_name = 'events'

    def get_queryset(self):
        return [i.event for i in super().get_queryset().filter(user=self.request.user).filter(event__user__active=True, event__published=True,)]


@login_required
def add_event_to_calendar(request, uid):
    event = get_object_or_404(Event, uid=uid)
    relation = EventCalendar.objects.get_or_create(user=request.user, event=event)
    messages.success(request, f'Event is added to you calendar')
    return redirect('events:event-calendar')



@login_required
def add_event_to_saved(request, uid):
    event = get_object_or_404(Event, uid=uid)
    relation = EventSave.objects.get_or_create(user=request.user, event=event)
    messages.success(request, f'Event has been saved, go to My Saved events')

    # Redirect back to previous view
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def report_event_now(request, uid):
    event = get_object_or_404(Event, uid=uid)
    report = EventReport.objects.get_or_create(reporter=request.user, event=event)
    messages.success(request, f'Event has been reported')
    return redirect(reverse('events:event-detail', kwargs={'slug': str(event.slug)}))


@login_required
def duplicate_event(request, uid):
    event = get_object_or_404(Event, uid=uid)

    # copy the unclonable fields
    old_amenities = event.amenities.all()

    event.pk = None
    event.uid = uuid.uuid4()
    event.slug = None
    event.save()

    # Set unclonable fields
    event.amenities.set(old_amenities)
    
    messages.success(request, f'Event is successfully duplicated')
    return redirect(reverse('events:event-detail', kwargs={'slug': str(event.slug)}))


