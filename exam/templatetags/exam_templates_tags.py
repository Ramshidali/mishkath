
from datetime import datetime, timedelta
from django import template
from exam.models import *

register = template.Library()


@register.simple_tag
def get_questions_in_exam(exam_pk):
    if Questions.objects.filter(exam__pk=exam_pk,is_deleted=False).exists():
        questions = Questions.objects.filter(exam__pk=exam_pk,is_deleted=False)
        return questions
    
@register.simple_tag
def get_entrolled_exams(exam_pk):
    if StudentExam.objects.filter(exam__pk=exam_pk,is_deleted=False).exists():
        entrolled_exam = StudentExam.objects.filter(is_completed=True,exam__pk=exam_pk,is_deleted=False)
        return entrolled_exam
    
# @register.simple_tag
# def get_total_activity_questions(activity_pk):
#     total_activities = ActivityQuestion.objects.filter(activity__pk=activity_pk,is_deleted=False).count()
#     entrolled_students = StudentActivity.objects.filter(activity__pk=activity_pk,is_deleted=False,is_completed=True).count()
#     return {
#         "total_activities" : total_activities,
#         "entrolled_students" : entrolled_students,
#     }
        
        
# @register.simple_tag
# def get_total_lesson(sub_pk):
#     lesson_instances_count = Lesson.objects.filter(subject__pk=sub_pk,is_deleted=False).count()
#     return lesson_instances_count
    
# @register.simple_tag
# def get_topic_percentage(student_pk,sub_pk):
#     profile_instance = Profile.objects.get(pk=student_pk)
#     total_topic = Topic.objects.filter(lesson__subject__grade__pk=profile_instance.grade_batch.grade.pk,is_deleted=False).count()
#     encrolled_topic = StudentTopic.objects.filter(topic__lesson__subject__pk=sub_pk,is_deleted=False,is_completed=True).count()
    
#     # perscentage = total_topic/encrolled_topic
#     perscentage = encrolled_topic/total_topic*100
    
#     return perscentage