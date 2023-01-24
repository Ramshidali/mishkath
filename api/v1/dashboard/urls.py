from django.urls import path, re_path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # dashboard tab
    re_path(r'^$', views.dashboard),
    re_path(r'^upcomming-live-classes/$', views.upcomming_classess),
    re_path(r'^notifications/$', views.notifications),
    
    # subject tab
    re_path(r'^subjects/$', views.subjects),
    re_path(r'^topic-video/(?P<pk>.*)/$', views.topic_video),
    re_path(r'^upcomming-topics/(?P<subject_pk>.*)/$', views.upcomming_topics),
    
    re_path(r'^next-activity/(?P<c_topic_id>.*)/$', views.next_activity),
    re_path(r'^next-topic/(?P<c_topic_id>.*)/$', views.next_topic),
    
    # subcription
    re_path(r'^grade-subscription/$', views.grade_subscription),
    
]