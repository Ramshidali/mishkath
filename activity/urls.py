from django.urls import path, re_path
from . import views

app_name = 'activity'

urlpatterns = [
    path('activities', views.activities,name='activities'),
    re_path(r'^view-activity/(?P<pk>.*)/$', views.view_activity,name='view_activity'),
    re_path(r'^create-activity/(?P<pk>.*)/$', views.create_activity,name='create_activity'),
    re_path(r'^delete-activity/(?P<pk>.*)/$', views.delete_activity,name='delete_activity'),
    
    path('activity_questions', views.activity_questions,name='activity_questions'),
    re_path(r'^create_activity_question/(?P<pk>.*)/$', views.create_activity_question,name='create_activity_question'),
]