from django.urls import path, re_path

from . import views

app_name = 'learn'

urlpatterns = [
    re_path(r'^unlocked-topics-autocomplete/$', views.UnlockedTopicsAutocomplete.as_view(),
            name='unlocked_topics_autocomplete'),

    path('batches', views.batches, name='batches'),
    re_path(r'^create-batch/(?P<pk>.*)/$', views.create_batch, name='create_batch'),
    re_path(r'^delete-batch/(?P<pk>.*)/$', views.delete_batch, name='delete_batch'),

    path('grades/', views.grades, name='grades'),
    re_path(r'^create-grade/(?P<pk>.*)/$', views.create_grade, name='create_grade'),
    re_path(r'^delete-grade/(?P<pk>.*)/$', views.delete_grade, name='delete_grade'),

    path('grade_batch/', views.grade_batch, name='grade_batch'),
    re_path(r'^create-grade-batch/$', views.create_grade_batch, name='create_grade_batch'),
    re_path(r'^update-grade-batch/(?P<pk>.*)/$', views.update_grade_batch, name='update_grade_batch'),
    re_path(r'^delete-grade-batch/(?P<pk>.*)/$', views.delete_grade_batch, name='delete_grade_batch'),

    path('country/', views.country, name='country'),
    re_path(r'^create-country/(?P<pk>.*)/$', views.create_country, name='create_country'),
    re_path(r'^delete-country/(?P<pk>.*)/$', views.delete_country, name='delete_country'),

    path('courses/', views.courses, name='courses'),
    re_path(r'^create-courses/(?P<pk>.*)/$', views.create_courses, name='create_courses'),
    re_path(r'^delete-courses/(?P<pk>.*)/$', views.delete_courses, name='delete_courses'),

    path('subjects/', views.subjects, name='subjects'),
    re_path(r'^view-subject/(?P<pk>.*)/$', views.view_subject, name='view_subject'),
    re_path(r'^create-subject/(?P<pk>.*)/$', views.create_subjects, name='create_subject'),
    re_path(r'^delete-subject/(?P<pk>.*)/$', views.delete_subject, name='delete_subject'),

    path('lessons/', views.lessons, name='lessons'),
    re_path(r'^view-lesson/(?P<pk>.*)/$', views.view_lesson, name='view_lesson'),
    re_path(r'^create-lesson/(?P<pk>.*)/$', views.create_lesson, name='create_lesson'),
    re_path(r'^create-lesson-with-subject/(?P<sub_pk>.*)/$', views.create_lesson_with_subject,
            name='create_lesson_with_subject'),
    re_path(r'^edit-lesson/(?P<lesson_pk>.*)/$', views.edit_lesson, name='edit_lesson'),
    re_path(r'^delete-lesson/(?P<lesson_pk>.*)/$', views.delete_lesson, name='delete_lesson'),

    path('topics/', views.topics, name='topics'),
    re_path(r'^create-topic-with-lesson/(?P<lesson_pk>.*)/$', views.create_topic_with_lesson,
            name='create_topic_with_lesson'),
    re_path(r'^create-topic/(?P<pk>.*)/(?P<sub_pk>.*)/$', views.create_topic, name='create_topic'),
    re_path(r'^delete-topic/(?P<pk>.*)/(?P<sub_pk>.*)/$', views.delete_topic, name='delete_topic'),
    
    path('up-comming-live-classes/', views.upcomming_live_classes, name='upcomming_live_classes'),
    re_path(r'^create-up-comming-live-classes/(?P<pk>.*)/$', views.create_upcomming_live_classes, name='create_upcomming_live_classes'),    
]
