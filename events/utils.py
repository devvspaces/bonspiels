import random, string
import pytz
from datetime import datetime
import socket
import urllib

# from bs4 import BeautifulSoup
# import requests


import re
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException, WebDriverException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

import inflect
p = inflect.engine()


from django.template.defaultfilters import slugify

from account.models import FacebookUser



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



# Code to get results from trip advisor
def get_trip_advisor(address):

    if not address:
        return []

    # Uri encode the address for the search
    uri_encoded_address = urllib.parse.quote(address, safe='')

    # Create the search link
    base_url = 'https://www.tripadvisor.com/'
    link = f"{base_url}/Search?q={uri_encoded_address}"


    # Creating the webdriver
    chrome_options = webdriver.ChromeOptions()

    # Other driver settings
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    # chrome_options.add_argument("--disable-infobars")
    # chrome_options.add_argument("--disable-extensions")
    # chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920x1080')
    chrome_options.add_argument("--disable-popup-blocking")

    chrome_options.add_argument("--headless")

    trips = []

    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_window_size(1920, 1080)

        try:
            driver.get(link)
            alert = driver.switch_to_alert()
            alert.accept()
        except:
            print("No Alert")
        
        # Find the show more button and click it
        show = driver.find_element_by_css_selector('.show-block.show-more')
        try:
            show.click()
        except ElementClickInterceptedException as e:
            print(e)
            # driver.find_element_by_css_selector('#_evidon_banner')

            try:
                not_wanted = ['_evidon_banner', '_evidon-background']
                for i in not_wanted:
                    js = f"var aa=document.getElementById('{i}');aa.remove()"
                    driver.execute_script(js)
            except Exception as e:
                print(e)

            show.click()

        time.sleep(5)


        listings = driver.find_elements_by_css_selector('.ui_columns.result-content-columns')


        for i in listings:
            title = i.find_element_by_css_selector('.result-title').text

            try:
                review_el = i.find_element_by_css_selector('.review_count')
            except NoSuchElementException:
                continue

            review_count = review_el.text.split(' ')[0]
            review_link = review_el.get_attribute('href')
            trip_link = review_link.split('#')[0]

            rating_text = i.find_element_by_css_selector('.ui_bubble_rating').get_attribute('alt').split(' ')[0]

            address = i.find_element_by_css_selector('.address-text').text

            # Get the background image link
            my_property = i.find_element_by_css_selector('.inner').value_of_css_property("background-image")
            image = re.split('[()]',my_property)[1].replace('\"', '')

            try:
                category = i.find_element_by_css_selector('.thumbnail-overlay-tag').text
            except NoSuchElementException:
                continue

            trip =  {
                        'title': title,
                        'review_count': review_count,
                        'trip_link': trip_link,
                        'rating_text': rating_text,
                        'address': address,
                        'image': image,
                        'category': category,
                    }

            trips.append(trip)

            # print(trip)

        # print(trips)

        driver.quit()

    except Exception as e:
        print(e)
        driver.quit()

    return trips

# get_trip_advisor('Surry Hills NSW, Australia')


# Code to get results from trip advisor
def get_fb_posts():
    posts = []

    # Get active fb account
    accounts = FacebookUser.objects.filter(active=True)
    val  = accounts.exists()
    # val = True

    if val:
        print('Got an account here')
        account = accounts.first()

        # link = 'https://m.facebook.com/codecell.com.bd'
        link = account.link

        # Creating the webdriver
        chrome_options = webdriver.ChromeOptions()

        # Other driver settings
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        # chrome_options.add_argument("--disable-infobars")
        # chrome_options.add_argument("--disable-extensions")
        # chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920x1080')
        chrome_options.add_argument("--headless")

        driver = webdriver.Chrome(options=chrome_options)
        driver.set_window_size(1920, 1080)

        print('Created driver')

        try:

            driver.get(link)

            print('Got the page', driver.title, driver.current_url)

            found = False

            # Find the posts button and click it
            for i in driver.find_elements_by_css_selector('._484w'):
                print('found tabs', i.text)
                if i.text.lower() == 'posts':
                    driver.get(i.get_attribute('href'))
                    found = True
                    print('found the posts tab')
                    break

            if found:

                print('wanted to get the posts')
                posts_els = driver.find_elements_by_css_selector('.story_body_container')

                while len(posts_els) < 15:
                    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                    time.sleep(1)
                    posts_els = driver.find_elements_by_css_selector('.story_body_container')

                print(f'Scraped {len(post_els)} posts')

                for i in posts_els:

                    print('Started loop')

                    text = ''
                    created = ''
                    image = ''
                    link = ''
                    
                    try:
                        text = i.find_element_by_css_selector('._5rgt').text
                    except NoSuchElementException:
                        pass

                    try:
                        created = i.find_element_by_css_selector('._52jc').text
                    except NoSuchElementException:
                        pass

                    try:
                        link = i.find_element_by_css_selector('._5msj').get_attribute('href')
                    except NoSuchElementException:
                        pass

                    # image
                    try:
                        image = i.find_element_by_css_selector('._5sgi').get_attribute('src')
                    except NoSuchElementException:
                        pass

                    trip =  {
                                'text': text,
                                'created': created,
                                'image': image,
                                'link': link
                            }

                    print(trip)

                    posts.append(trip)

            driver.quit()

        except Exception as e:
            print('Got exception')
            driver.quit()
            print(e)
            
    else:
        pass

    return posts