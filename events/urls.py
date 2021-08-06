from django.urls import path

from . import views


app_name='events'
urlpatterns = [
    path('add/', views.CreateEvent.as_view(), name='add-event'),
    path('detail/<str:uid>/', views.EventDetail.as_view(), name='event-detail'),
    path('search/', views.EventSearch.as_view(), name='event-search'),
    path('event-calendar/', views.EventCalendar.as_view(), name='event-calendar'),
]
