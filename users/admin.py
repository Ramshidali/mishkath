from django.contrib import admin
from users.models import *

admin.site.register(Profile)
admin.site.register(OtpRecord)
admin.site.register(InterviewStatus)
admin.site.register(TemporaryProfile)