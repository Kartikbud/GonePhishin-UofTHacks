from django.urls import path
from . import views

app_name = 'detector'

urlpatterns = [
    path('', views.monitor_view, name='monitor'),
    path('history/', views.history_view, name='history'),
] 