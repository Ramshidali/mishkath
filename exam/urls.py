from django.urls import path, re_path
from . import views

app_name = 'exam'

urlpatterns = [
    path('exams', views.exams,name='exams'),
    re_path(r'^view-exam/(?P<pk>.*)/$', views.view_exam,name='view_exam'),
    re_path(r'^create-exam/(?P<pk>.*)/$', views.create_exam, name='create_exam'),  
    re_path(r'^delete-exam/(?P<pk>.*)/$', views.delete_exam, name='delete_exam'),  
    
    path('exams-question', views.exam_questions,name='exam_questions'),
    re_path(r'^create-exam-question/(?P<pk>.*)/$', views.create_exam_question, name='create_exam_question'),  
    re_path(r'^create-exam-question-exam/(?P<exam_pk>.*)/$', views.create_exam_question_without_exam, name='create_exam_question_without_exam'),  
    re_path(r'^update-exam-question-exam/(?P<pk>.*)/$', views.update_exam_question_without_exam, name='update_exam_question_without_exam'),  
    re_path(r'^delete-question/(?P<pk>.*)/$', views.delete_exam_question, name='delete_exam_question'),  
]