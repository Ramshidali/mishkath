from django import views
from django.conf.urls import include
from django.contrib import admin
from django.views.static import serve
from django.urls import path,re_path

from mishkath import settings


admin.autodiscover()
admin.site.enable_nav_sidebar = False

urlpatterns = [
    path('admin/', admin.site.urls),
    path('app/accounts/', include('registration.backends.default.urls')),
    
    path('',include(('main.urls'),namespace='main')),
    
    path('app/students/',include(('users.urls'),namespace='users')),
    path('app/learn/',include(('learn.urls'),namespace='learn')),
    path('app/activity/',include(('activity.urls'),namespace='activity')),
    path('app/exams/',include(('exam.urls'),namespace='exam')),
    path('app/payments/',include(('payments.urls'),namespace='payments')),

    re_path('api/v1/auth/',
            include(('api.v1.authentication.urls', 'authentication'), namespace='api_v1_authentication')),
    
    re_path('api/v1/general/',
            include(('api.v1.general.urls', 'general'), namespace='api_v1_general')),
    
    re_path('api/v1/users/',
            include(('api.v1.users.urls', 'users'), namespace='api_v1_users')),
    
    re_path('api/v1/dashboard/',
            include(('api.v1.dashboard.urls', 'dashboard'), namespace='api_v1_dashboard')),
    
    re_path('api/v1/exam/',
            include(('api.v1.exam.urls', 'exam'), namespace='api_v1_exam')),
    
    re_path('api/v1/activity/',
            include(('api.v1.activity.urls', 'activity'), namespace='api_v1_activity')),
    
    
    
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^videos/(?P<path>.*)$', serve, {'document_root': settings.VIDEO_URL}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]
