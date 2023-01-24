from datetime import date
from api.v1.dashboard.functions import get_student_batch
from api.v1.exam.serializers import *
from exam.models import Exam
from main.functions import get_auto_id
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def allotted_exam(request):
    
    exam_type = request.GET.get('exam_type')
    batch = get_student_batch(request)
       
    instances = Exam.objects.filter(grade_batch__batch__pk=batch,exam_type=exam_type,is_deleted=False)

    serialized = ExamSerializers(instances, many=True, context={"request":request})

    response_data = {
        "StatusCode" : 6000,
        "data" : serialized.data,
    }
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def time_allotted(request):
    exam_pk = request.GET.get('exam_pk')
       
    instances = Exam.objects.get(pk=exam_pk,is_deleted=False)

    serialized = QuestionTimeSerializers(instances,context={"request":request})

    response_data = {
        "StatusCode" : 6000,
        "data" : serialized.data,
    }
    return Response(response_data, status=status.HTTP_200_OK)
    

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def questions(request):
    today = date.today()
    profile = Profile.objects.get(user=request.user)
    pk = request.GET.get('exam_pk')
    try:
        pre_question = request.GET.get('pre_question')
    except:
        pre_question = ''
    
    if Exam.objects.filter(pk=pk,is_deleted=False).exists():
        exam_instance = Exam.objects.get(pk=pk,is_deleted=False)
        student_enrolled_exams = StudentEnrolledExam.objects.values_list('question__pk',flat=True)
        
        instance = Questions.objects.filter(exam__pk=pk,is_deleted=False).exclude(pk__in=student_enrolled_exams).first()
        total_questions = Questions.objects.filter(exam__pk=pk,is_deleted=False).count()
        completed_questions = StudentEnrolledExam.objects.filter(student=profile.pk,student_exam__pk=pk,is_deleted=False).count()
        if not total_questions == completed_questions :
            current_question = completed_questions + 1
        else:
            current_question = completed_questions
            
        if exam_instance.exam_date == today:
            if Questions.objects.filter(exam__pk=pk,is_deleted=False).exists():
                if not total_questions == completed_questions: 
                    
                    if instance.question_type == "objective":
                        serialized = QuestionObjectiveSerializers(instance, context={"request":request})
                        
                        response_data = {
                            "StatusCode" : 6000,
                            "data" : serialized.data,
                            "completed_questions" : completed_questions,
                            "current_question" : current_question,
                            "total_questions" : total_questions,
                            "previous_question_pk" : pre_question,
                            }
                        
                    elif instance.question_type == "attachment":
                        serialized = QuestionNoneObjectiveSerializers(instance, context={"request":request})
                        
                        response_data = {
                            "StatusCode" : 6000,
                            "data" : serialized.data,
                            "completed_questions" : completed_questions,
                            "Total_questions" : total_questions,
                            "previous_question_pk" : pre_question,
                            }
                    
                    elif instance.question_type == "descriptive":
                        serialized = QuestionNoneObjectiveSerializers(instance, context={"request":request})
                        
                        response_data = {
                            "StatusCode" : 6000,
                            "data" : serialized.data,
                            "completed_questions" : completed_questions,
                            "Total_questions" : total_questions,
                            "previous_question_pk" : pre_question,
                            }
                    
                    elif instance.question_type == "descriptive_or_file":
                        serialized = QuestionNoneObjectiveSerializers(instance, context={"request":request})
                        
                        response_data = {
                            "StatusCode" : 6000,
                            "data" : serialized.data,
                            "completed_questions" : completed_questions,
                            "Total_questions" : total_questions,
                            "previous_question_pk" : pre_question,
                            }
                        
                    else:
                        response_data = {
                            "StatusCode" : 6001,
                            # "data" : serialized.data,
                            'message' : 'question type issue'
                            }
                        
                else:
                    response_data = {
                        "StatusCode" : 6001,
                        "message" : "exam completed result will publish soon" 
                        }
            else:
                response_data = {
                    "StatusCode" : 6001,
                    "message" : "no questions" 
                    }
        elif exam_instance.exam_date <= today:
            
            response_data = {
                "StatusCode" : 6001,
                "message" : f'exam completed on {exam_instance.exam_date}'
                }
        elif exam_instance.exam_date >= today:
        
            response_data = {
                "StatusCode" : 6001,
                "message" : f'exam scheduled on {exam_instance.exam_date}'
                }
        else:
            
            response_data = {
                "StatusCode" : 6001,
                "message" : "exam date not scheduled"
                }
    else:
            
        response_data = {
            "StatusCode" : 6001,
            "message" : "exam not scheduled"
            }
        
    return Response(response_data, status=status.HTTP_200_OK)
    
    
    
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def post_answer(request):
    response_data = {}
    c_question_id = request.data['c_question_id']
    
    if Questions.objects.filter(pk=c_question_id,is_deleted=False).exists():
        c_question_instance = Questions.objects.get(pk=c_question_id)
        c_question_type = c_question_instance.question_type
        profile = Profile.objects.get(user=request.user)    
        
        if not StudentEnrolledExam.objects.filter(student__user=request.user,question__pk=c_question_id):
            if c_question_type == "objective" :
                selected_option = request.data['selected_option']
                # auto_id = get_auto_id(StudentEnrolledExam)
                            
                StudentEnrolledExam.objects.create(
                    auto_id=get_auto_id(StudentEnrolledExam),
                    creator=request.user,
                    updater=request.user,
                    student=profile,
                    student_exam=c_question_instance.exam,
                    question=c_question_instance,
                    selected_option=selected_option,
                    )    
                
                response_data = {
                    "StatusCode" : 6000,
                    "message" : "objective question successfully completed",
                    "c_question_pk" : c_question_id,
                    }
                
            elif c_question_type == "attachment":
                attachment = request.data['attachment']
                auto_id = get_auto_id(StudentEnrolledExam)
                
                StudentEnrolledExam.objects.create(
                    auto_id=auto_id,
                    creator=request.user,
                    updater=request.user,
                    student=profile,
                    student_exam=c_question_instance.exam,
                    question=c_question_instance,
                    attachment=attachment,
                    )        
                
                response_data = {
                    "StatusCode" : 6000,
                    "message" : "attachment question successfully completed"
                    }
                
            elif c_question_type == "descriptive":
                descriptive = request.data['descriptive']
                auto_id = get_auto_id(StudentEnrolledExam)
                
                StudentEnrolledExam.objects.create(
                    auto_id=auto_id,
                    creator=request.user,
                    updater=request.user,
                    student=profile,
                    student_exam=c_question_instance.exam,
                    question=c_question_instance,
                    descriptive_answer=descriptive,
                    )
                
                response_data = {
                    "StatusCode" : 6000,
                    "message" : "descriptive question successfully completed"
                    }
                
            elif c_question_type == "descriptive_or_file":
                try:
                    descriptive = request.data['descriptive']            
                except :
                    descriptive = ''
                try:
                    attachment = request.data['attachment']
                except : 
                    attachment = ''
                
                auto_id = get_auto_id(StudentEnrolledExam)
                
                StudentEnrolledExam.objects.create(
                    auto_id=auto_id,
                    creator=request.user,
                    updater=request.user,
                    student=profile,
                    student_exam=c_question_instance.exam,
                    question=c_question_instance,
                    descriptive_answer=descriptive,
                    attachment=attachment,
                    )
                
                response_data = {
                    "StatusCode" : 6000,
                    "message" : "descriptive or file question successfully completed"
                    }
            
            else:
                response_data = {
                    "StatusCode" : 6001,
                    "message" : "question not completed"
                    }
            total_questions = Questions.objects.filter(exam__pk=c_question_instance.exam.pk,is_deleted=False).count()
            completed_questions = StudentExam.objects.filter(student=profile.pk,exam__pk=c_question_instance.exam.pk,is_completed=True,is_deleted=False).count()
            
            if total_questions == completed_questions :
                StudentExam.objects.create(
                    auto_id=get_auto_id(StudentExam),
                    creator=request.user,
                    updater=request.user,
                    exam=c_question_instance.exam,
                    student=profile,
                    is_completed=True
                    )
        else:
            response_data = {
                "StatusCode" : 6001,
                "message" : "this question already completed"
                }
    else:
        response_data = {
            "StatusCode" : 6001,
            "message" : "this question not found"
            }
    
    return Response(response_data, status=status.HTTP_200_OK)
    

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def previous_question(request,pre_question):
    profile = Profile.objects.get(user=request.user)    
    pre_question_instance = Questions.objects.get(pk=pre_question)
    student_question = StudentEnrolledExam.objects.get(question=pre_question_instance)
    
       
    if pre_question_instance.question_type == "objective" :
        try:
            selected_option = student_question.selected_option
            
            serialized = QuestionObjectiveSerializers(pre_question_instance, context={"request":request})
                    
            response_data = {
                "StatusCode" : 6000,
                "data" :{
                    "selected_option" : selected_option,
                    "data" : serialized.data,
                }
                }
            
        except:
            serialized = QuestionObjectiveSerializers(pre_question_instance, context={"request":request})
                    
            response_data = {
                "StatusCode" : 6000,
                "data" : serialized.data,
                }
            
    elif pre_question_instance.question_type == "attachment":
         
        try:
            attachment = student_question.attachment
        
            serialized = QuestionNoneObjectiveSerializers(pre_question_instance, context={"request":request})
                
            response_data = {
                "StatusCode" : 6000,
                "data" :{
                    "attachment" : attachment.url,
                    "data" : serialized.data,
                }
                }
        except:
            serialized = QuestionNoneObjectiveSerializers(pre_question_instance, context={"request":request})
                
            response_data = {
                "StatusCode" : 6000,
                "data" :{
                    "data" : serialized.data,
                }
                }
        
    elif pre_question_instance.question_type == "descriptive":
        try:
        
            descriptive_answer = student_question.descriptive_answer
            
            serialized = QuestionNoneObjectiveSerializers(pre_question_instance, context={"request":request})
                    
            response_data = {
                "StatusCode" : 6000,
                "data" :{
                    "descriptive_answer" : descriptive_answer,
                    "data" : serialized.data,
                }
                }
        except:
            serialized = QuestionNoneObjectiveSerializers(pre_question_instance, context={"request":request})
                    
            response_data = {
                "StatusCode" : 6000,
                "data" : serialized.data,
                }
        
    elif pre_question_instance.question_type == "descriptive_or_file":
        
        try:
            if pre_question_instance.attachment :
                attachment = student_question.attachment
                serialized = QuestionNoneObjectiveSerializers(pre_question_instance, context={"request":request})
                
                response_data = {
                "StatusCode" : 6000,
                "data" :{
                    "attachment" : attachment.url,
                    "data" : serialized.data,
                }
                }
                
            elif pre_question_instance.descriptive_answer :
                descriptive_answer = student_question.descriptive_answer
                serialized = QuestionNoneObjectiveSerializers(pre_question_instance, context={"request":request})
                
                response_data = {
                "StatusCode" : 6000,
                "data" :{
                    "descriptive_answer" : descriptive_answer,
                    "data" : serialized.data,
                }
                }
        except: 
            
            serialized = QuestionNoneObjectiveSerializers(pre_question_instance, context={"request":request})
                
            response_data = {
                "StatusCode" : 6001,
                "data" : serialized.data,
                }
            
            
    
    else:
        response_data = {
            "StatusCode" : 6001,
            "message" : "question not completed"
            }
    return Response(response_data, status=status.HTTP_200_OK)
    
    


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def exam_result(request,exam_pk):
    today = date.today()
    profile = Profile.objects.get(user=request.user)
    
    score_instance = StudentExam.objects.get(exam__pk=exam_pk,student__pk=profile.pk)
    
    serialized = ExamScoreSerializers(score_instance, context={"request":request})
                
    response_data = {
        "StatusCode" : 6000,
        "data" : serialized.data,
        }
    return Response(response_data, status=status.HTTP_200_OK)
    
    
    
    
    