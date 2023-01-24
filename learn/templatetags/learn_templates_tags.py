
from datetime import datetime, timedelta
from django import template
from learn.models import Lesson, StudentTopic, Topic
from users.models import InterviewStatus, Profile

register = template.Library()


@register.simple_tag
def get_lessons_in_subject(sub_pk):
    if Lesson.objects.filter(subject__pk=sub_pk,is_deleted=False).exists():
        lessons = Lesson.objects.filter(subject__pk=sub_pk,is_deleted=False)
        return lessons
    
@register.simple_tag
def get_topics_in_subject(sub_pk):
    if Topic.objects.filter(lesson__subject__pk=sub_pk,is_deleted=False).exists():
        topics = Topic.objects.filter(lesson__subject__pk=sub_pk,is_deleted=False)
        return topics
    
@register.simple_tag
def get_topics_in_lesson(lesson_pk):
    if Topic.objects.filter(lesson__pk=lesson_pk,is_deleted=False).exists():
        topics = Topic.objects.filter(lesson__pk=lesson_pk,is_deleted=False)
        return topics
        
        
@register.simple_tag
def get_total_status(sub_pk):
    topic_instances_count = Topic.objects.filter(lesson__subject__pk=sub_pk,is_deleted=False).count()
    lesson_instances_count = Lesson.objects.filter(subject__pk=sub_pk,is_deleted=False).count()
    latest_added_topic = Topic.objects.filter(lesson__subject__pk=sub_pk,is_deleted=False).first()
    return {
        'lesson_instances_count' : lesson_instances_count,
        'topic_instances_count' : topic_instances_count,
        'latest_added_topic' : latest_added_topic,
    }
    
# @register.simple_tag
# def get_topic_percentage(student_pk,sub_pk):
#     profile_instance = Profile.objects.get(pk=student_pk)
#     total_topic = Topic.objects.filter(lesson__subject__grade__pk=profile_instance.grade_batch.grade.pk,is_deleted=False).count()
#     encrolled_topic = StudentTopic.objects.filter(topic__lesson__subject__pk=sub_pk,is_deleted=False,is_completed=True).count()
    
#     # perscentage = total_topic/encrolled_topic
#     perscentage = encrolled_topic/total_topic*100
    
#     return perscentage