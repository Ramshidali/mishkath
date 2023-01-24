from django.urls import path, re_path
from . import views

app_name = 'user'

urlpatterns = [
    re_path(r'^login/$', views.login_with_password,),
    # profile
    re_path(r'^student-details/$', views.student_details),
    re_path(r'^personal-details/$', views.personal_details),
    re_path(r'^parents-details/$', views.parents_details),
    re_path(r'^about-mishkath/$', views.about_mishkath),
    re_path(r'^course-details/$', views.course_details),
    re_path(r'^sign-up/$', views.sign_up),
    
    re_path(r'^send-otp/$', views.otp_generation),
    re_path(r'^send-otp-nonchecking/$', views.non_check_otp_generation),
    re_path(r'^verify-otp/$', views.otp_verify),
    
    # get user details from profile
    re_path(r'^profile/$', views.profile),
    re_path(r'^courses-percentage/$', views.courses_percentage),
    re_path(r'^courses-in-progress/$', views.courses__in_progress),
    
    re_path(r'^forget-password/$', views.forget_password),  
]