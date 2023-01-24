from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from activity.models import Activity, ActivityQuestion, StudentActivity, StudentEnrolledActivity
from api.v1.activity.serializers import ActivityQuestionSerializers, ActivitySerializers, ActivitySubjectSerializers

from api.v1.dashboard.functions import get_student_batch
from learn.models import Subject
from main.functions import get_auto_id
from users.models import Profile

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def activity_subjects(request):
    
    batch = get_student_batch(request)
       
    instances = Subject.objects.filter(is_deleted=False)

    serialized = ActivitySubjectSerializers(instances, many=True, context={"request":request})

    response_data = {
        "StatusCode" : 6000,
        "data" : serialized.data,
    }
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def activity(request,sub_pk):
    profile = Profile.objects.get(user=request.user)
    
    if Activity.objects.filter(topic__lesson__subject__pk=sub_pk,is_deleted=False).exists():
        
        student_enrolled_activity = StudentActivity.objects.filter(student_id=profile.pk).values_list('activity__pk',flat=True)    
        
        instances = Activity.objects.filter(topic__lesson__subject__pk=sub_pk,is_deleted=False).exclude(pk__in=student_enrolled_activity).first()
        
        serialized = ActivitySerializers(instances,context={"request":request})

        response_data = {
            "StatusCode" : 6000,
            "data" : serialized.data,
        }
    else:
        response_data = {
            "StatusCode" : 6001,
            "data" : "n activity in this subject",
        }
        
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def all_activity(request,sub_pk):           
    instances = Activity.objects.filter(topic__lesson__subject__pk=sub_pk,is_deleted=False)

    serialized = ActivitySerializers(instances,many=True,context={"request":request})

    response_data = {
        "StatusCode" : 6000,
        "data" : serialized.data,
    }
    
    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def activity_status(request,sub_pk):
    
    activity_instance = Activity.objects.filter(topic__lesson__subject__pk=sub_pk,is_deleted=False).count()
    entrolled_activity = StudentActivity.objects.filter(activity__topic__lesson__subject__pk=sub_pk,is_completed=True,is_deleted=False).count()
    
    
    response_data = {
        "StatusCode" : 6000,
        "activity_status" : str(entrolled_activity) + "/" + str(activity_instance),
        }
    return Response(response_data, status=status.HTTP_200_OK)
    
    

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def activity_question(request,pk):
    profile = Profile.objects.get(user=request.user)
    
    if not StudentActivity.objects.filter(student=profile,activity__pk=pk,is_completed=True,is_deleted=False):    
        student_enrolled_activity = StudentEnrolledActivity.objects.filter(student_id=profile,is_deleted=False).values_list('question__pk',flat=True)
        # print(student_enrolled_activity)
        instance = ActivityQuestion.objects.filter(activity__pk=pk,is_deleted=False).exclude(pk__in=student_enrolled_activity).first()  
        # total and completed questions from activity
        total_questions =  ActivityQuestion.objects.filter(activity__pk=pk,is_deleted=False).count()
        completed_questions =  StudentEnrolledActivity.objects.filter(activity__pk=pk,student_id=profile,is_deleted=False).count()
        
        if not total_questions == completed_questions :
            current_question = completed_questions + 1
        else:
            current_question = completed_questions
        
        if instance:    
            serialized = ActivityQuestionSerializers(instance,context={"request":request},many=False)

            response_data = {
                "StatusCode" : 6000,
                "data" : serialized.data,
                "total_questions" : total_questions,
                "current_question" : current_question,
                "completed_questions" : completed_questions,
            }
        
        else:
            response_data = {
                "StatusCode" : 6001,
                "message" : "no question in this activity",
            }
    else:
        response_data = {
            "StatusCode" : 6000,
            "message" : "all activities are completed",
        }
        
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def post_activity_answers(request,activity_pk):
    response_data = {}
    
    if ActivityQuestion.objects.filter(activity__pk=activity_pk,is_deleted=False).exists():
        
        question_pk = request.data['question_id']
        selected_op = request.data['selected_op']
        question_instance = ActivityQuestion.objects.get(pk=question_pk)
        activity_instance = Activity.objects.get(pk=question_instance.activity.pk)
        profile = Profile.objects.get(user=request.user)
        
        
        if not StudentActivity.objects.filter(student=profile.pk,activity__pk=activity_instance.pk).exists():
            
            StudentEnrolledActivity.objects.create(
                auto_id=get_auto_id(StudentEnrolledActivity),
                creator=request.user,
                updater=request.user,
                student_id=profile,
                activity=activity_instance,
                question=question_instance,
                selected_option=selected_op,
                )
            
            # total and completed questions from activity
            total_questions =  ActivityQuestion.objects.filter(activity__pk=activity_pk,is_deleted=False).count()
            completed_questions =  StudentEnrolledActivity.objects.filter(activity__pk=activity_pk,student_id=profile,is_deleted=False).count()
            
            if total_questions == completed_questions:
                StudentActivity.objects.create(
                    auto_id=get_auto_id(StudentEnrolledActivity),
                    creator=request.user,
                    updater=request.user,
                    activity=activity_instance,
                    student=profile,
                    is_completed=True,
                )    
            
            response_data = {
                "StatusCode" : 6000,
                "message" : "objective question successfully completed",
                }
        else:
            response_data = {
                "StatusCode" : 6001,
                "message" : "this question already completed"
                }
    else:
        response_data = {
            "StatusCode" : 6001,
            "message" : "question not found in this activity"
            }
    
    return Response(response_data, status=status.HTTP_200_OK)