from django.urls import path

from . import views

app_name = 'contact'

urlpatterns = [
    path('create/', views.contact_create, name='contact_create'),
]