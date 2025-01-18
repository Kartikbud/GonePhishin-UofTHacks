from django.urls import path
from . import views

app_name = 'detector'

urlpatterns = [
    path('', views.monitor_view, name='home'),
    path('history/', views.history_view, name='history'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('signout/', views.signout_view, name='signout'),
] 