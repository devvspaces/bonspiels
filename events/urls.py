from django.urls import path

from . import views


app_name='events'
urlpatterns = [
    path('add/', views.CreateEvent.as_view(), name='add-event'),
    path('edit/<str:uid>/', views.UpdateEvent.as_view(), name='event-update'),
    path('duplicate/<str:uid>/', views.duplicate_event, name='event-duplicate'),
    path('detail/<str:slug>/', views.EventDetail.as_view(), name='event-detail'),
    
    path('search/', views.EventSearch.as_view(), name='event-search'),
    path('calendar/', views.EventCalendarView.as_view(), name='event-calendar'),
    path('my-events/', views.MyEvent.as_view(), name='my-event'),
    path('add-calendar/<str:uid>/', views.add_event_to_calendar, name='add-calendar'),
    path('events/organizer/<str:uid>/', views.OrganizerEvents.as_view(), name='organizer-events'),
    # path('events/my_tickets/', views.UserEventTickets.as_view(), name='my-tickets'),
    # path('order/tickets/<str:uid>', views.order_ticket, name='order-ticket'),

    path('save/<str:uid>/', views.add_event_to_saved, name='save-event'),
    path('saved/', views.SavedEvents.as_view(), name='saved-events'),
    # path('report/<str:uid>/', views.report_event_now, name='report-events'),

    path('events/registered_teams/', views.RegisteredTeams.as_view(), name='registered-teams'),
    
    path('trip_advisor/', views.get_trips_view, name='trip-advisor'),

]