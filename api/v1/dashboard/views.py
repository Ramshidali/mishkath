from activity.models import Activity
from api.v1.dashboard.functions import get_student_batch
from api.v1.dashboard.serializers import *
from learn.decorators import check_subscription
from learn.models import GradeBatch, Lesson, Notifications, Subject

from main.functions import get_auto_id
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from users.models import InterviewStatus, Profile


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def dashboard(request):
    response_data = {}
    try:
        profile = Profile.objects.get(user=request.user)
        instance = InterviewStatus.objects.get(profile=profile.pk)

        if instance.status == "pending":
            message = "your in waiting list"

            response_data = {
                "StatusCode": 6000,
                "message": message,
                "interview_status" : "pending",
            }

        elif instance.status == "allotted":

            data = {
                "interview_date": instance.interview_date,
                "interview_time": instance.interview_time,
                "interview_link": instance.zoom_id,
            }

            response_data = {
                "StatusCode": 6000,
                "message": "your interview will be conducted on the following time",
                "data": data,
                "interview_status" : "allotted",
                
            }

        elif instance.status == "passed":
            batch = get_student_batch(request)
            
            if batch:
                total_count_of_topic = Topic.objects.filter(is_deleted=False).count()
                count_student_entrolled_topics = StudentTopic.objects.filter(student_id=profile,is_deleted=False).count()
                persentage_of_all_topics = str(float(count_student_entrolled_topics)/float(total_count_of_topic)*100)
                
                if GradeBatch.objects.filter(batch__pk=batch).exists():
                    grade_from_batch = GradeBatch.objects.get(batch__pk=batch)
                    instance = Subject.objects.filter(grade=grade_from_batch.grade,is_deleted=False)

                    serialized = SubjectWithTopicSerializers(
                        instance, many=True,
                        context={"request": request}
                    )

                    response_data = {
                        "StatusCode": 6000,
                        "interview_status" : "passed",
                        "data": serialized.data,
                        "grade": grade_from_batch.grade.name,
                        "percentage_of_course": persentage_of_all_topics,
                    }

                else:
                    message = "batch is not exists"

                    response_data = {
                        "StatusCode": 6001,
                        "message": message,
                    }
            else:
                    message = "batch is not defined"

                    response_data = {
                        "StatusCode": 6001,
                        "message": message,
                    }

    except Exception as e:
        response_data = {
            "test" : "test",
            "StatusCode": 6001,
            "message": str(e)
        }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def subjects(request):
    response_data = {}
    try:
        batch = get_student_batch(request)

        profile = Profile.objects.get(user=request.user)
        instance = InterviewStatus.objects.get(profile=profile.pk)

        if instance.status == "passed":
            grade_from_batch = GradeBatch.objects.get(batch=batch)
            instance = Subject.objects.filter(grade=grade_from_batch.grade,is_deleted=False)


            serialized_subject = SubjectsSerializers(
                instance, many=True,
                context={"request": request}
            )

            response_data = {
                "StatusCode": 6000,
                "course" : profile.interested_course.name,
                "data": serialized_subject.data,
            }
        else:
            message = ""

            response_data = {
                "StatusCode": 6001,
                "message": message,
            }



    except Exception as e:
        response_data = {
            "StatusCode": 6001,
            "message": str(e)
        }

    return Response(response_data, status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
@check_subscription
def upcomming_classess(request):
    response_data = {}
    try:
        batch = get_student_batch(request)
        
        profile = Profile.objects.get(user=request.user)
        instance = InterviewStatus.objects.get(profile=profile.pk)
        
        if instance.status == "passed": 
            instances = UpCommingLiveClasses.objects.filter(is_deleted=False,batch=batch)
            serialized =    UpCommingClassesSerializers(instances, many=True, context={"request":request})

            response_data = {
                "StatusCode" : 6000,
                "data" : serialized.data,
            }
        else:
            message = ""
            
            response_data = {
                    "StatusCode": 6001,
                    "message" : message,
                }
            
            

    except Exception as e:
        response_data = {
            "StatusCode": 6001,
            "message": str(e)
        }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def notifications(request):
    response_data = {}
    try:
        batch = get_student_batch(request)
        
        profile = Profile.objects.get(user=request.user)
        instance = InterviewStatus.objects.get(profile=profile.pk)
        
        if instance.status == "passed": 
            instances = Notifications.objects.filter(is_deleted=False,batch=batch,student_id=profile).order_by('date_added')
            serialized =    NotificationsSerializers(instances, many=True, context={"request":request})

            response_data = {
                "StatusCode" : 6000,
                "data" : serialized.data,
            }
        else:
            message = ""
            
            response_data = {
                    "StatusCode": 6001,
                    "message" : message,
                }
            
            

    except Exception as e:
        response_data = {
            "StatusCode": 6001,
            "message": str(e)
        }

    return Response(response_data, status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
@check_subscription
def topic_video(request,pk):
    response_data = {}
    # try:
    profile = Profile.objects.get(user=request.user)
    subject_instance = Subject.objects.get(pk=pk)
    
    if Lesson.objects.filter(subject__pk=pk,is_deleted=False).exists():
        if Topic.objects.filter(lesson__subject__pk=pk,is_deleted=False).exists():
            
            topic_instance = Topic.objects.filter(lesson__subject__pk=pk,is_deleted=False).first()
            batch = get_student_batch(request)
            
            if GradeBatch.objects.filter(batch=batch,grade=subject_instance.grade.pk,unlocked_topic=topic_instance,is_deleted=False).exists():
                if StudentTopic.objects.filter(student_id=profile.pk,is_new_content=True,is_completed=False,topic__lesson__subject__pk=pk,is_deleted=False).exists():
                    # print("its ok")
                    topic = StudentTopic.objects.filter(student_id=profile.pk,topic__lesson__subject__pk=pk,is_new_content=True,is_completed=False,is_deleted=False).first()
                    serialized = StudentTopicVideoSerializers(topic, context={"request":request})
                    
                    response_data = {
                        "StatusCode" : 6000,
                        "data" : serialized.data,
                        "subject_id" : pk,
                        
                    }            

                else:
                    # print(topic_instance)
                    
                    if not StudentTopic.objects.filter(topic=pk,is_deleted=False).exists():
                        auto_id = get_auto_id(StudentTopic)
                        
                        StudentTopic.objects.create(
                            auto_id=auto_id,
                            creator=request.user,
                            updater=request.user,

                            topic=topic_instance,
                            student_id=profile,
                            is_completed=False,
                            is_new_content=True,
                        )
                        
                        topic_instance = StudentTopic.objects.filter(topic__lesson__subject__pk=pk,is_deleted=False).last()
                        serialized =  StudentTopicVideoSerializers(topic_instance,context={"request":request})

                        response_data = {
                            "StatusCode" : 6000,
                            "data" : serialized.data,
                            "subject_id" : pk,
                        }
                    else :
                        message = "this topic already registered"
                        
                        response_data = {
                        "StatusCode" : 6001,
                        "message" : message,
                        "subject_id" : pk,
                    }
            else :
                message = "no unlocked topics"
                
                response_data = {
                    "StatusCode" : 6001,
                    "message" : message,
                    "subject_id" : pk,
                    }
                        
        else :
            message = "no topic in this subjects"
                    
            response_data = {
                "StatusCode" : 6001,
                "message" : message,
                "subject_id" : pk,
            }
                
    else :
        message = "no lesson in this subjects"
        
        response_data = {
            "StatusCode" : 6001,
            "message" : message,
            "subject_id" : pk,
            }

    # except Exception as e:
    #     response_data = {
    #         "StatusCode": 6001,
    #         "message": str(e)
    #     }

    return Response(response_data, status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def upcomming_topics(request,subject_pk):
    response_data = {}
    if  Subject.objects.filter(pk=subject_pk,is_deleted=False).exists():
        
        topics = Topic.objects.filter(lesson__subject__pk=subject_pk,is_deleted=False)
        serialized =  TopicSerializer(topics, many=True, context={"request":request})
        
        response_data = {
                "StatusCode" : 6000,
                "data" : serialized.data,
                }
    else:
        message = "subject not found"
        
        response_data = {
                "StatusCode" : 6001,
                "message" : message,
            }
    
    return Response(response_data, status=status.HTTP_200_OK)



# @api_view(['POST'])
# @permission_classes((IsAuthenticated,))
# @renderer_classes((JSONRenderer,))
# def next_topic(request,c_topic_id):
#     response_data = {}
#     subject_pk = None
#     student_topic_instance = None
#     profile = Profile.objects.get(user=request.user)
    
#     if c_topic_id :
    
#         # c_topic_id means current topic id
#         if StudentTopic.objects.filter(student_id__user=request.user,topic__pk=c_topic_id,is_deleted=False).exists():
#             # checking any topic video in student topic
#             if StudentTopic.objects.filter(student_id__user=request.user,is_new_content=True,is_completed=False,is_deleted=False).exists():
#                 student_topic_instance = StudentTopic.objects.get(student_id__user=request.user,topic=c_topic_id,is_deleted=False)
#                 student_topic_instance.is_completed = True
                
                
#                 subject_pk = student_topic_instance.topic.lesson.subject.pk
#                 # print(student_topic_instance)
#                 # check all previous watched videos
#                 previous_topic = StudentTopic.objects.values_list('pk',flat=True)
#                 # print("previous topic",previous_topic)            
#                 if subject_pk :
#                     if Topic.objects.filter(lesson__subject__pk=subject_pk,is_deleted=False).exclude(pk__in=previous_topic).exists():
                        
#                         topic_instance = Topic.objects.filter(lesson__subject__pk=subject_pk,is_deleted=False).exclude(pk=c_topic_id).first()
#                         if StudentTopic.objects.filter(topic__pk=topic_instance.pk).exists():
#                             print("topic instance ====>",topic_instance.pk)
                            
#                             message = ""
                            
#                             response_data = {
#                                 "StatusCode": 6000,
#                                 "message": message,
#                             }
                        
#                         else:                        
#                             auto_id = get_auto_id(StudentTopic)
                            
#                             student_topic_instance.save()

#                             StudentTopic.objects.create(
#                                 auto_id=auto_id,
#                                 creator=request.user,
#                                 updater=request.user,

#                                 topic=topic_instance,
#                                 student_id=profile,
#                                 is_completed=False,
#                                 is_new_content=True,
#                             )
                        
                        
#                         response_data = {
#                             "StatusCode": 6000,
#                             "message": "new topic instance added",
#                             "next_topic" : topic_instance,
#                         }
#                 else : 
#                     message = "no subject_id"
                
#                 # next topic video 
#                 next_Topic = StudentTopic.objects.filter(student_id__user=request.user,is_new_content=True,is_completed=False,is_deleted=False).exclude(topic__pk=student_topic_instance.pk).first()                
#                 batch = get_student_batch(request)

#                 if GradeBatch.objects.filter(batch=batch,unlocked_topic=next_Topic.pk,is_deleted=False).exists():                    
                
                
#                     response_data = {
#                         "StatusCode": 6000,
#                         "message": "success",
#                         "next_topic" : next_Topic.pk,
#                         }
#                 else:
                    
#                     response_data = {
#                         "StatusCode": 6001,
#                         "message": "no any unlocked topics",
#                         "lock_status" : False,
#                         }
                    
#             else:
#                 message = "no new topics"
                
#                 response_data = {
#                     "StatusCode": 6001,
#                     "message": message,
#                     }
#         else:
#               response_data = {
#                 "StatusCode": 6001,
#                 "message": "error"
#             }
#     else:
#         response_data = {
#             "StatusCode": 6001,
#             "message": "no_c_topic_id"
#         }
    
    
#     return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def next_activity(request,c_topic_id):
    response_data = {}
    profile = Profile.objects.get(user=request.user)
    if not StudentActivity.objects.filter(activity__topic__pk=c_topic_id,student__pk=profile.pk,is_completed=True).exists():
        if  Activity.objects.filter(topic__pk=c_topic_id,is_deleted=False).exists():
            
            activity = Activity.objects.filter(topic__pk=c_topic_id,is_deleted=False).first()
            serialized =  NextActivitySerializer(activity, context={"request":request})
            
            response_data = {
                    "StatusCode" : 6000,
                    "data" : serialized.data,
                    }
        else:
            message = "activity not found"
            
            response_data = {
                    "StatusCode" : 6001,
                    "message" : message,
                }
    else:
        message = "activity already completed"
        
        response_data = {
                "StatusCode" : 6001,
                "message" : message,
            }
    
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
@check_subscription
def next_topic(request,c_topic_id):
    response_data = {}
    subject_pk = None
    student_topic_instance = None
    profile = Profile.objects.get(user=request.user)
    
    student_topic_instance = StudentTopic.objects.filter(student_id__user=request.user,topic=c_topic_id,is_deleted=False).first()
    student_topic_instance.is_completed = True
    subject_pk = student_topic_instance.topic.lesson.subject.pk
    
    previous_topic = StudentTopic.objects.values_list('topic__pk',flat=True)
    # print("previus",previous_topic)
    # topic_instance = Topic.objects.filter(lesson__subject__pk=subject_pk,is_deleted=False).exclude(pk__in=previous_topic).first()
    if Topic.objects.filter(lesson__subject__pk=subject_pk,is_deleted=False).exclude(pk__in=previous_topic).exists():
        next_topic = Topic.objects.filter(lesson__subject__pk=subject_pk,is_deleted=False).exclude(pk__in=previous_topic).first()                
        
        if StudentTopic.objects.filter(student_id__user=request.user,is_completed=False,is_new_content=True,is_deleted=False).exists():    
            if StudentTopic.objects.filter(student_id__user=request.user,topic__pk=c_topic_id,is_deleted=False).exists():
                if not StudentTopic.objects.filter(student_id__user=request.user,topic__pk=next_topic.pk,is_deleted=False).exists():
                    batch = get_student_batch(request)
                    
                    # print("pre topi ==>>",previous_topic)
                    # print("next_topic",next_topic.name)
                    if GradeBatch.objects.filter(batch=batch,unlocked_topic=next_topic.pk,is_deleted=False).exists():
                    
                        student_topic_instance.save()
                        auto_id = get_auto_id(StudentTopic)
                                    
                        new_topic_instance = StudentTopic.objects.create(
                        auto_id=auto_id,
                        creator=request.user,
                        updater=request.user,
                        topic=next_topic,
                        student_id=profile,
                        is_completed=False,
                        is_new_content=True,
                        )
                        
                        topic_intance = Topic.objects.filter(pk=new_topic_instance.topic.pk)
                        serialized =  NextTopicSerializer(topic_intance, many=True, context={"request":request})
                               
                        response_data = {
                            "StatusCode": 6000,
                            # "message": message,
                            "data" : serialized.data,   
                        }
                        
                    else:
                        message = "new topic not unlocked"
                
                        response_data = {
                            "StatusCode": 6001,
                            "message": message,
                        }
                else:
                    message = "new topic already existed"
                
                    response_data = {
                        "StatusCode": 6001,
                        "message": message,
                    }
            else:
                message = "current topic alredy existed"
            
                response_data = {
                    "StatusCode": 6001,
                    "message": message,
                }       
        
        else:        
            message = "all topics are covered"
            
            response_data = {
                "StatusCode": 6001,
                "message": message,
            }
    else:
        student_topic_instance.save()
        
        message = "no next topic"
        
        response_data = {
            "StatusCode": 6000,
            "message": message,   
            }
    return Response(response_data, status=status.HTTP_200_OK)
    
    
#grade subscription
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
@check_subscription
def grade_subscription(request):
    response_data = {}
    profile = Profile.objects.get(user=request.user)
    # grade = get_student_grade(request)
    # batch = get_student_batch(request)
    subscription_instance = SubscriptionGrade.objects.filter(grade_batch__pk=profile.grade_batch.pk,is_deleted=False)
    serialized_subscription = SubscriptionSerializer(subscription_instance, many=True,context={"request": request})    
    
    response_data = {
            "StatusCode" : 6000,
            "data" : serialized_subscription.data,
        }
    
    return Response(response_data, status=status.HTTP_200_OK)