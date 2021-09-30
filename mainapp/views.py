import random

from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import logout,authenticate,login
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.encoding import force_text,force_bytes
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.http import JsonResponse
from django.core.paginator import Paginator

from account.models import User
from account.forms import (UserRegisterForm, LoginForm, ChangePasswordForm,
    ResetPasswordValidateEmailForm, ForgetPasswordForm)
from account.tokens import acount_confirm_token

from events.models import Category, Event, FeaturedLocation, Gallery
from events.utils import get_fb_posts

from .mixins import ajax_autocomplete


def verification_message(request, user, template):
	site=get_current_site(request)
	uid=urlsafe_base64_encode(force_bytes(user.pk))
	token=acount_confirm_token.make_token(user)
	message=render_to_string(template,{
		"user": user.profile.username,
		"uid": uid,
		"token": token,
		"domain": site.domain,
		'from': settings.DEFAULT_FROM_EMAIL
	})
	return message

def send_verification(user, request):
    site=get_current_site(request)
    uid=urlsafe_base64_encode(force_bytes(user.pk))
    token=acount_confirm_token.make_token(user)

    subject = f"Bonspiels Email Verification"
    message = verification_message(request, user, "account/activation_email.html")

    return user.email_user(subject,message)

def get_news_view(request):
    if request.is_ajax():
        # Get the news
        news = get_fb_posts()

        return JsonResponse(data={'results': news}, status=200)

    return redirect('mainapp:home')

class Home(TemplateView):
    template_name = 'mainapp/index.html'
    extra_context = {
    }

    form_class = LoginForm
    register_form = UserRegisterForm
    reset_form = ResetPasswordValidateEmailForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = Event.objects.filter(user__active=True, published=True)
        categories_set = Category.objects.all()
        

        # Sending the form to the template
        context['form'] = self.form_class()
        context['reg_form'] = self.register_form()
        context['reg_form'] = self.reset_form()

        context['events'] = queryset[:5]

        # Send sets to context
        context['all_events'] = queryset
        context['all_categories'] = categories_set

        # Get featured and upcoming events (4)
        context['featured_events'] = queryset.filter(featured=True)[:2]
        context['upcoming_events'] = queryset.get_upcoming()[:2]

        # Get the gallery events
        # valid_events_id_list = queryset.values_list('id', flat=True)
        # random_event_id_list = random.sample(list(valid_events_id_list), min(len(valid_events_id_list), 6))
        # context['gallery_events'] = queryset.filter(id__in=random_event_id_list)

        # Get the events by location
        locations = FeaturedLocation.objects.all()

        # Paginate the locations by four
        location_page_obj = Paginator(locations, 4)

        # Add the object list of all pages into a list
        location_page_list = []

        for i in location_page_obj.page_range:
            location_page_list.append(location_page_obj.page(i).object_list)

        context['location_page_list'] = location_page_list

        return context
    

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()

        response = ajax_autocomplete(request, context)
        if response is not None:
            return response

        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        request = self.request
        context = self.get_context_data()

        # Know which form was sent to decide the processing
        submit = request.POST.get('submit')

        if submit == 'login':
            form = self.form_class(request.POST)
            if form.is_valid():
                email = form.cleaned_data.get('email')
                password = form.cleaned_data.get('password')

                user = authenticate(request, username=email, password=password)
                if user:
                    login(request, user)
                    messages.success(request, f'Welcome, {user.profile.username}')
                else:
                    # Send email verification link to user
                    user = User.objects.get(email=email)
                    send_verification(user, request)
                    messages.success(request, f'A link was sent to your email {user.email}, use the link to verify you account.')
                
                return redirect('mainapp:home')
            else:
                messages.warning(request, 'Please correct your email / password.')
                context['form'] = form

        elif submit == 'register':
            form = self.register_form(request.POST)
            if form.is_valid():
                user = form.save()
                
                # Send email verification link to user
                send_verification(user, request)
                messages.success(request, f'You account is successfully created. A link was sent to your email {user.email}, use the link to verify you account.')
                return redirect('mainapp:home')
            else:
                messages.warning(request, 'Registration form is not valid')
                context['reg_form'] = form
        
        elif submit == 'reset':
            form = self.reset_form(request.POST)
            if form.is_valid():
                email = form.cleaned_data.get('email')
                user = User.objects.get(email=email)

                # Send the reset link to user
                subject = "Bonspiels Password Reset"
                message = verification_message(request, user, "account/password_reset.html")
                user.email_user(subject, message)
            
            print(form.errors)

            messages.success(request, 'A password reset link has been sent to your email if it is registered, click on the link to reset your password')
            return redirect('mainapp:home')
        
        return render(request, self.template_name, context)


class About(TemplateView):
    template_name = 'mainapp/about.html'
    extra_context = {
        'title': 'About Us',
    }


class Contact(TemplateView):
    template_name = 'mainapp/contact.html'
    extra_context = {
        'title': 'Contact Us',
    }