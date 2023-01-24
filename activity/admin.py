from django.contrib import admin
from activity.models import *

# Register your models here.

admin.site.register(Activity)
admin.site.register(ActivityQuestion)
admin.site.register(StudentActivity)
admin.site.register(StudentEnrolledActivity)
