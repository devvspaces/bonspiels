from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Profile, NewsletterSubscriber, FacebookUser
from .forms import UserRegisterForm, FacebookUserForm


class UserAdmin(BaseUserAdmin):
	# The forms to add and change user instances
	# form = UserUpdateForm
	add_form = UserRegisterForm

	# The fields to be used in displaying the User model.
	# These override the definitions on the base UserAdmin
	# that reference specific fields on auth.User.
	list_display=('email', 'username', 'active',)
	list_filter = ('active','staff','admin',)
	search_fields=['email']
	fieldsets = (
		('User', {'fields': ('email', 'password')}),
		('Permissions', {'fields': ('admin','staff','active',)}),
	)
	# add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
	# overrides get_fieldsets to use this attribute when creating a user.
	add_fieldsets = (
		(None, {
                'classes': ('wide',),
                'fields': ('email', 'password',)
            }
		),
	)
	ordering = ('email',)
	filter_horizontal = ()


class FacebookUserAdmin(admin.ModelAdmin):
	form = FacebookUserForm


admin.site.register(User, UserAdmin)
admin.site.register(FacebookUser, FacebookUserAdmin)
admin.site.register([Profile, NewsletterSubscriber])