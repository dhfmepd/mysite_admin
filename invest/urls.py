from django.urls import path
from .views import base_views

app_name = 'invest'

urlpatterns = [
    path('calendar/', base_views.calendar_main, name='calendar'),
    path('note/create/calendar', base_views.note_create_calendar, name='note_create_calendar'),
]