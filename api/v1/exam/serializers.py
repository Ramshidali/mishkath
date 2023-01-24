from rest_framework import serializers
from exam.models import *



class ExamSerializers(serializers.ModelSerializer):
    subject_name = serializers.SerializerMethodField()
    exam_status = serializers.SerializerMethodField()
    result_status = serializers.SerializerMethodField()
    
    class Meta:
        model = Exam
        fields = ['id','subject','subject_name','exam_date','exam_status','result_status']
        
    def get_subject_name(self,instance):
        if instance.subject:
            return instance.subject.name
        
    def get_exam_status(self,instance):
        
        if StudentExam.objects.filter(exam=instance,is_completed=True):
            return True
        else :
            return False 
    
    def get_result_status(self,instance):
        
        if StudentExam.objects.filter(exam=instance,is_completed=True):
            return True
        else :
            return False 


class QuestionTimeSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = Exam
        fields = ['id','time_allotted','total_mark','total_questions']


class QuestionObjectiveOptionsSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = Questions
        fields = ['option_a','option_b','option_c','option_d']


class QuestionObjectiveSerializers(serializers.ModelSerializer):
    is_objective = serializers.SerializerMethodField()
    options = serializers.SerializerMethodField()
    
    class Meta:
        model = Questions
        fields = ['id','question_type','question','attachment','options','is_objective']
    
    def get_is_objective(self,instance):
        if instance.question_type == "objective":
            return True
    
    def get_options(self,instance):
        options = QuestionObjectiveOptionsSerializers(instance,many=False).data
        array_data=[]
        for key,value in options.items():
            array_data.append({'id':key,'option':value})
            
        return array_data

class QuestionNoneObjectiveSerializers(serializers.ModelSerializer):
    is_attachment = serializers.SerializerMethodField()
    is_descriptive = serializers.SerializerMethodField()
    is_descriptive_or_file = serializers.SerializerMethodField() 
    
    class Meta:
        model = Questions
        fields = ['id','question_type','question','attachment','is_attachment','is_descriptive',
                  'is_descriptive_or_file']
    
    def get_is_attachment(self,instance):
        if instance.question_type == "attachment":
            return True
    
    def get_is_descriptive(self,instance):
        if instance.question_type == "descriptive":
            return True
        
    def get_is_descriptive_or_file(self,instance):
        if instance.question_type == "descriptive_or_file":
            return True
    
    def get_attachment(self):
        attachment = self.context.student_question
        return attachment
        


class ExamScoreSerializers(serializers.ModelSerializer):
    is_result_status = serializers.SerializerMethodField() 
    
    class Meta:
        model = StudentExam
        fields = ['exam','student','score_obtained','objective_score','descriptive_score','is_result_status']
        
    def get_is_result_status(self,instance):
        
        if not instance.score_obtained:
            return {
                "message" : "Result not yet published",
                "background_color_Status" : False,
            }
        
        elif instance.score_obtained == instance.exam.total_mark:
            return {
                "mark" : str(instance.score_obtained) + "/" + str(instance.exam.total_mark),
                "message" : "Amazing Job! Keep it up",
                "background_color_Status" : True,
            }
        
        elif instance.score_obtained <= instance.exam.total_mark*50/100:
            return {
                "mark" : str(instance.score_obtained) + "/" + str(instance.exam.total_mark),
                "message" : "Good luck! You will excel one day.",
                "background_color_Status" : False,
            }
        
        elif instance.score_obtained >= instance.exam.total_mark*60/100:
            return {
                "mark" : str(instance.score_obtained) + "/" + str(instance.exam.total_mark),
                "message" : "Good luck! You will excel one day.",
                "background_color_Status" : True,
            }

# class PreviousQuestionObjectiveSerializers(serializers.ModelSerializer):
#     is_objective = serializers.SerializerMethodField()
#     # is_selected = serializers.SerializerMethodField()
    
#     class Meta:
#         model = Questions
#         fields = ['id','question_type','question','attachment','option_a','option_b',
#                   'option_c','option_d','is_objective']
    
#     def get_is_objective(self,instance):
#         if instance.question_type == "objective":
#             return True
    
#     # def get_is_selected(self,instance):
#     #     StudentEnrolledExam.objects.