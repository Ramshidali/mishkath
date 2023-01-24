from django.contrib import admin
from learn.models import *

admin.site.register(Batch)
admin.site.register(Grade)
admin.site.register(Subject)
admin.site.register(Lesson)
admin.site.register(Topic)
admin.site.register(StudentEnrollGrade)
admin.site.register(StudentEnrollSubject)
admin.site.register(StudentEnrollLesson)
admin.site.register(StudentEnrolledLesson)
admin.site.register(StudentTopic)
admin.site.register(UpcomingActivity)
admin.site.register(BatchEnrolledLesson)
admin.site.register(BatchStudentPractise)
admin.site.register(BatchExam)
admin.site.register(GradeBatch)
admin.site.register(UpCommingLiveClasses)
admin.site.register(Notifications)

