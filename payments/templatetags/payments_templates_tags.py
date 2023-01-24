
from datetime import datetime, timedelta
import profile
from django import template
from payments.models import StudentSubscription, SubscriptionGradeFee
from users.models import Profile

register = template.Library()


@register.simple_tag
def get_subscription_grade_fee(pk):
    "pk : subscription grade pk"
    if SubscriptionGradeFee.objects.filter(subscription_grade__pk=pk,is_deleted=False).exists():
        subscription_grade_fee = SubscriptionGradeFee.objects.filter(subscription_grade__pk=pk,is_deleted=False)
        return subscription_grade_fee
            
        
@register.simple_tag
def get_subscribed_students(pk):
    subscribed_students = StudentSubscription.objects.filter(subscription_grade_fee__subscription_grade__pk=pk,is_deleted=False)
    
    return subscribed_students

@register.simple_tag
def get_subscription_end_date(student_pk):
    profile_instance = Profile.objects.get(pk=student_pk)
    subscribed_date = StudentSubscription.objects.get(profile__pk=profile_instance.pk,is_deleted=False)
    str_subscribed_date = str(subscribed_date.subscribed_date.replace(tzinfo=None))
    days_in_month = subscribed_date.subscription_grade_fee.month * 28
    date = datetime.strptime(str_subscribed_date, '%Y-%m-%d %H:%M:%S.%f').date() + timedelta(days=days_in_month)
    today = datetime.now().date()
        
    if today >= date :
        return {
            'date' : date,
            'color' : "red",
        }
    else :
            return {
                'date' : date,
                'color' : "green",
            }
    
    

