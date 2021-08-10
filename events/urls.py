from django.urls import path

from . import views


app_name='events'
urlpatterns = [
    path('add/', views.CreateEvent.as_view(), name='add-event'),
    path('detail/<str:uid>/', views.EventDetail.as_view(), name='event-detail'),
    path('search/', views.EventSearch.as_view(), name='event-search'),
    path('event-calendar/', views.EventCalendarView.as_view(), name='event-calendar'),
    path('my-events/', views.MyEvent.as_view(), name='my-event'),
    path('add-calendar/<str:uid>/', views.add_event_to_calendar, name='add-calendar'),
    path('events/organizer/<str:uid>/', views.OrganizerEvents.as_view(), name='organizer-events'),
    path('events/my_tickets/', views.UserEventTickets.as_view(), name='my-tickets'),
]
