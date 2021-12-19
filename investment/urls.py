from django.urls import path

from . import views

app_name = 'investment'

urlpatterns = [
    path('dashboard/', views.investment_dashboard, name='dashboard'),
]