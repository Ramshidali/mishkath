
from datetime import datetime, timedelta
from django import template
from learn.models import StudentTopic, Topic
from payments.models import StudentSubscription
from users.models import InterviewStatus, Profile

register = template.Library()


@register.simple_tag
def get_interview_status(student_pk):
    if InterviewStatus.objects.filter(profile__pk=student_pk,is_deleted=False,status="pending"):
        return 'pending'
    elif InterviewStatus.objects.filter(profile__pk=student_pk,is_deleted=False,status="allotted"):
        return 'allotted'
    elif InterviewStatus.objects.filter(profile__pk=student_pk,is_deleted=False,status="passed"):
        return 'passed'
    
@register.simple_tag
def get_subscription_status(student_pk):
    
    profile = Profile.objects.get(pk=student_pk)
    subscribed_date = StudentSubscription.objects.filter(is_deleted=False,profile__pk=profile.pk).order_by('-date_added').first()
    
    if subscribed_date:
        
        str_subscribed_date = str(subscribed_date.subscribed_date.replace(tzinfo=None))
        days_in_month = subscribed_date.subscription_grade_fee.month * 28
        date = datetime.strptime(str_subscribed_date, '%Y-%m-%d %H:%M:%S.%f').date() + timedelta(days=days_in_month)
        today = datetime.now().date()
        
        if not today >= date :
            return "subscribed"
        else :
            return "subscription_ended"
    else :
            return "not_subscribed"
        
        
@register.simple_tag
def get_batch(student_pk):
    profile_instance = Profile.objects.get(pk=student_pk)
    if profile_instance.grade_batch is not None:
        return True
    else :
        return False
    
@register.simple_tag
def get_topic_percentage(student_pk,sub_pk):
    profile_instance = Profile.objects.get(pk=student_pk)
    total_topic = Topic.objects.filter(lesson__subject__grade__pk=profile_instance.grade_batch.grade.pk,is_deleted=False).count()
    encrolled_topic = StudentTopic.objects.filter(topic__lesson__subject__pk=sub_pk,is_deleted=False,is_completed=True).count()
    
    # perscentage = total_topic/encrolled_topic
    perscentage = encrolled_topic/total_topic*100
    
    return perscentage