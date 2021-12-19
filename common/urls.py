from django.urls import path
from . import views

app_name = 'common'

urlpatterns = [
    path('<str:anchor>/', views.index_anchor, name='index_anchor'),
]