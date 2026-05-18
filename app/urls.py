from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('send-quote/', views.send_quote, name='send_quote'),
    ]