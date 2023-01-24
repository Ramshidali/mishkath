from datetime import datetime, timedelta
from payments.models import StudentSubscription, SubscriptionGradeFee
from django.http.response import HttpResponse
import json

from users.models import Profile


def check_subscription(function):
    def wrap(request, *args, **kwargs):
        profile_instance = Profile.objects.get(user=request.user)
        subscription_grade_fee =  SubscriptionGradeFee.objects.filter(subscription_grade__grade_batch__grade__pk=profile_instance.grade_batch.grade.pk).order_by('-date_updated')[0]
        subscribed_date = StudentSubscription.objects.filter(profile__pk=profile_instance.pk,is_deleted=False,subscription_grade_fee__subscription_grade__grade_batch__grade__pk=profile_instance.grade_batch.grade.pk).order_by('-date_updated')[0]
        subscribed_date = str(subscribed_date.subscribed_date.replace(tzinfo=None))
        days_in_month = subscription_grade_fee.month * 28
        date = datetime.strptime(subscribed_date, '%Y-%m-%d %H:%M:%S.%f').date() + timedelta(days=days_in_month)
        today = datetime.now().date()
        
        response_data = {}
        
        if today >= date:
            
            if request.is_ajax():
                response_data['status'] = 'false'
                response_data['message'] = "your subscription as ended."
                response_data['static_message'] = "true"
                return HttpResponse(json.dumps(response_data), content_type='application/javascript')
            
            else:
                response_data['status'] = 'false'
                response_data['message'] = "your subscription as ended."
                response_data['static_message'] = "true"
                return HttpResponse(json.dumps(response_data), content_type='application/javascript')



        return function(request, *args, **kwargs)

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
