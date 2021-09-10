from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import FormView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

from .models import Profile, User, NewsletterSubscriber
from .forms import (ChangePasswordForm, ForgetPasswordForm,
    ProfileForm, UserForm, NewsletterForm)
from .tokens import acount_confirm_token

def activate_email(request, uidb64, token):
	try:
		uid=force_text(urlsafe_base64_decode(uidb64))
		user=User.objects.get(pk=uid)
	except (TypeError, ValueError, OverflowError, User.DoesNotExist):
		user=None
	if user!=None and acount_confirm_token.check_token(user,token):
		user.active=True
		user.save()

		messages.success(request,f'{user.email}, your email is verified successfully, you can now login')
		return redirect('mainapp:home')
	else:
		messages.warning(request, 'Invalid Link, kindly ')
		return redirect('mainapp:home')


class ChangePassword(LoginRequiredMixin, UpdateView):
    template_name = 'account/change_password.html'
    extra_context = {
        'title': 'Change Password'
    }
    form_class = ChangePasswordForm

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['form'] = self.form_class()

        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        request = self.request
        context = self.get_context_data()

        cloned = request.POST.copy()
        cloned['user_pk'] = request.user.pk

        form = self.form_class(cloned)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Your password is successfully changed, please login with your new password')
            return redirect('account:logout')
        else:
            messages.warning(request, 'You did not properly fill the change password form.')
        
        context['form'] = form
        
        return render(request, self.template_name, context)


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'account/profile.html'
    extra_context = {
        'title': 'Profile'
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ProfileForm(instance=self.request.user.profile)
        context["uform"] = UserForm(instance=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        
        uform = UserForm(instance=self.request.user, data=request.POST)
        form = ProfileForm(instance=self.request.user.profile, data=request.POST, files=request.FILES)

        if uform.is_valid() and form.is_valid():
            uform.save()
            form.save()
            messages.success(request, f'Your profile is successfully updated')
            return redirect('account:profile')

        context['form'] = form
        context['uform'] = uform

        return render(request, self.template_name, context)
class ResetPasswordVerify(FormView):
    template_name = 'account/reset_password_page.html'
    extra_context = {
        'title': 'Reset your password',
    }
    form_class = ForgetPasswordForm

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['form'] = self.form_class()

        # Get uidb4 and token from kwargs
        uidb64 = self.kwargs.get('uidb64')
        token = self.kwargs.get('token')

        uid=force_text(urlsafe_base64_decode(uidb64))
        user=get_object_or_404(User, pk=uid)

        if acount_confirm_token.check_token(user,token):
            messages.success(request,'You can now set a new password')
        else:
            messages.warning(request, 'This password reset link is already invalid.')
            return redirect('mainapp:home')

        return render(request, self.template_name, context)
    
    def post(self, *args, **kwargs):
        request = self.request

        # Get uidb4 from kwargs and get the user instance
        uidb64 = self.kwargs.get('uidb64')
        uid=force_text(urlsafe_base64_decode(uidb64))
        user=get_object_or_404(User, pk=uid)

        form = self.get_form_class()
        form = form(request.POST)

        if form.is_valid():
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            messages.success(request, 'You password has been successfully changed, now login with your new password')
            return redirect('mainapp:home')
        
        context = self.get_context_data()
        context['form'] = form

        return render(request, self.template_name, context)


def newletter_submit(request):
    # Validate form and save email
    form = NewsletterForm(data=request.POST)
    if form.is_valid():
        email = form.cleaned_data.get('email')
        obj = NewsletterSubscriber.objects.get_or_create(email=email)
        messages.success(request, 'You have successfully subscribed to our newsletter')
    else:
        messages.warning(request, 'Invalid email provided, please correct your email to receive our newletters')
    return redirect('mainapp:home')


def Logout(request):
    logout(request)
    messages.success(request, 'We will miss you')
    return redirect('mainapp:home')