import random, string
import pytz
from datetime import datetime
import socket

import inflect
p = inflect.engine()


from django.template.defaultfilters import slugify



def random_text(p=5):
    return ''.join(random.sample(string.ascii_uppercase + string.ascii_lowercase,p))

def get_unique_slug(instance, slug=None, length=5):
    if not slug:
        slug = slugify(instance.title)
    
    exists = instance.__class__.objects.filter(slug = slug).exists()
    
    if exists:
        code = random_text(length)
        slug_title = slugify(instance.title)
        slug = f'{slug_title}-{code}'
        
        return get_unique_slug(instance, slug=slug)
    
    return slug


def strDate(val, att):
    if val > 1:
        return f'{val} {att}s ago'
    return f'{val} {att} ago'

def convert_str_date(val):
    return pytz.utc.localize(datetime.strptime(val, '%Y-%m-%d %H:%M'))


def get_valid_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    try:
        socket.inet_aton(ip)
        return ip
    except socket.error:
        return

def ordinal(i):
    return p.ordinal(i)