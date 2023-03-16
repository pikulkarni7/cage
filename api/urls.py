from django.urls import path

from api import views

app_name = 'api'

urlpatterns = [
    path('notify', views.trigger_notify_task, name='notify'),
]
