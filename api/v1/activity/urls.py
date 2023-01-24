from django.urls import path, re_path
from . import views

app_name = 'activity'

urlpatterns = [
    re_path(r'^activity-subject/$', views.activity_subjects),
    re_path(r'^activity/(?P<sub_pk>.*)/$', views.activity),
    re_path(r'^all-activity/(?P<sub_pk>.*)/$', views.all_activity),
    re_path(r'^activity-status/(?P<sub_pk>.*)/$', views.activity_status),
    
    re_path(r'^activity-question/(?P<pk>.*)/$', views.activity_question),
    re_path(r'^post-activity-answers/(?P<activity_pk>.*)/$', views.post_activity_answers),
]