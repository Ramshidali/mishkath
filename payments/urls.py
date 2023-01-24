from django.urls import path, re_path

from . import views

app_name = 'payments'

urlpatterns = [
    path('subscription-grade', views.subscription_grade, name='subscription_grade'),
    re_path(r'^view-subscription-grade/(?P<pk>.*)/$', views.view_subscription_grade, name='view_subscription_grade'),
    re_path(r'^create-subscription-grade/(?P<pk>.*)/$', views.create_subscription_grade, name='create_subscription_grade'),
    
    re_path(r'^create-subscription-grade-fee/(?P<pk>.*)/(?P<sub_pk>.*)/$', views.create_subscription_grade_fee, name='create_subscription_grade_fee'),
    re_path(r'^delete-subscription-grade-fee/(?P<pk>.*)/$', views.delete_subscription_grade_fee, name='delete_subscription_grade_fee'),
    
    re_path(r'^create-student-subscription/(?P<pk>.*)/(?P<sub_pk>.*)/$', views.create_student_subscription, name='create_student_subscription'),
    
]