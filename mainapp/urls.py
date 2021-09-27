from django.urls import path

from . import views


app_name='mainapp'
urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('about/', views.About.as_view(), name='about'),
    path('contact/', views.Contact.as_view(), name='contact'),

    # Ajax url for getting news
    path('facebook_news/', views.get_news_view, name='facebook_url')
]
