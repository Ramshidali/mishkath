from django.contrib import admin

from payments.models import *

# Register your models here.

admin.site.register(SubscriptionGrade)
admin.site.register(SubscriptionGradeFee)
admin.site.register(StudentSubscription)