from rest_framework import serializers
from activity.models import *
from learn.models import StudentTopic, Subject

class ActivitySubjectSerializers(serializers.ModelSerializer):
    progress_of_activities = serializers.SerializerMethodField()
    
    class Meta:
        model = Subject
        fields = ['id','name','progress_of_activities']
        
    def get_progress_of_activities(self, instance):
        activity_instance = Activity.objects.filter(topic__lesson__subject__pk=instance.pk,is_deleted=False).count()
        entrolled_activity = StudentActivity.objects.filter(activity__topic__lesson__subject__pk=instance.pk,is_completed=True,is_deleted=False).count()  
        
        return str(entrolled_activity) + "/" + str(activity_instance)
    

class ActivitySerializers(serializers.ModelSerializer):
    activity_lock_status = serializers.SerializerMethodField()
    
    class Meta:
        model = Activity
        fields = ['id','title','description','image','total_questions','activity_lock_status']
        
    def get_activity_lock_status(self,instance):
        profile = Profile.objects.get(user=self.context['request'].user)
        if StudentTopic.objects.filter(student_id__pk=profile.pk,topic__pk=instance.topic.pk,is_completed=True):
            return True
        else:
            return False       
        
        
class ActivityOptionsSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = ActivityQuestion
        fields = ['option1','option2','option3','option4']
        

class ActivityQuestionSerializers(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()
    
    class Meta:
        model = ActivityQuestion
        fields = ['id','question','options']
        
    def get_options(self,instance):
        options = ActivityOptionsSerializers(instance,many=False).data
        array_data=[]
        for key,value in options.items():
            array_data.append({'id':key,'option':value})
            
        return array_data
        
        
    
        