from django.urls import path

from . import views

urlpatterns = [
    path('', views.stt, name='index'),
]