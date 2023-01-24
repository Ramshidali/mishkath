from django.urls import path, re_path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.students,name='students'),
    re_path(r'^create-interview-schedule/(?P<pk>.*)/$', views.create_interview_schedule,name='create_interview_schedule'),
    re_path(r'^subscription-update/(?P<pk>.*)/$', views.subscription_update,name='subscription_update'),
    re_path(r'^assign-batch/(?P<pk>.*)/$', views.assign_batch,name='assign_batch'),
    re_path(r'^view-profile/(?P<pk>.*)/$', views.view_profile,name='view_profile'),
    re_path(r'^edit-profile/(?P<pk>.*)/$', views.edit_profile,name='edit_profile'),
    re_path(r'^delete-profile/(?P<pk>.*)/$', views.delete_profile,name='delete_profile'),
    
        
]