from django.urls import path, re_path
from . import views

app_name = 'general'

urlpatterns = [
    # country
    re_path(r'^countries/$', views.contry_code),
    re_path(r'^courses/$', views.courses),
]