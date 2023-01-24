from django.contrib import admin

from exam.models import *

# Register your models here.

admin.site.register(Exam)
admin.site.register(Questions)
admin.site.register(StudentExam)
admin.site.register(StudentEnrolledExam)

