from django.urls import path
from .views import crawling_views

app_name = 'interface'

urlpatterns = [
    path('crawling/', crawling_views.main, name='crawling_main'),
]