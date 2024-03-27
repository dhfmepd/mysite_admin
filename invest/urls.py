from django.urls import path
from .views import base_views, note_views

app_name = 'invest'

urlpatterns = [
    path('calendar/', base_views.calendar_main, name='calendar'),
    path('note/create/calendar/', note_views.note_create_calendar, name='note_create_calendar'),
    path('note/detail/calendar/<int:note_id>', note_views.note_detail_calendar, name='note_detail_calendar'),
]