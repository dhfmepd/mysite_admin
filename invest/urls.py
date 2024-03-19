from django.urls import path
from . import views

app_name = 'invest'

urlpatterns = [
    path('calendar/', views.calendar_main, name='calendar'),
    path('note/create/calendar/<int:day>', views.note_create_calendar, name='note_create_calendar'),
]