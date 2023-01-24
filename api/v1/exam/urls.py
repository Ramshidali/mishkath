from django.urls import path, re_path
from . import views

app_name = 'exam'

urlpatterns = [
    re_path(r'^allotted-exam/$', views.allotted_exam,),
    re_path(r'^questions/$', views.questions,),
    re_path(r'^post-answer/$', views.post_answer,),    
    re_path(r'^previous-question/(?P<pre_question>.*)/$', views.previous_question,),    
    re_path(r'^time-allotted/$', views.time_allotted,),    
    re_path(r'^exam-result/(?P<exam_pk>.*)/$', views.exam_result,),    
]