from django.contrib import admin


from .models import HomeLocation, HomeBackground

# Register your models here.
admin.site.register([HomeLocation, HomeBackground])