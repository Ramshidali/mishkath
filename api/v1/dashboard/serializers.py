from datetime import timedelta,datetime
from rest_framework import serializers

from activity.models import Activity, StudentActivity
from api.v1.dashboard.functions import get_student_batch

from learn.models import GradeBatch, Notifications, StudentTopic, Subject, Topic, UpCommingLiveClasses
from payments.models import StudentSubscription, SubscriptionGrade, SubscriptionGradeFee
from users.models import Profile

class SubjectsSerializers(serializers.ModelSerializer):
    total_topic = serializers.SerializerMethodField()
    is_progress = serializers.SerializerMethodField()
    
    class Meta:
        model = Subject
        fields = ['id','name','image','description','duration','total_topic','is_progress']
        
    def get_total_topic(self, instance):
        topic_instance = Topic.objects.filter(lesson__subject=instance,is_deleted=False).count()    
        return topic_instance
    
    def get_is_progress(self,instance):
        request = self.context.get("request")
        profile_instance = Profile.objects.get(user=request.user)
        
        if StudentTopic.objects.filter(topic__lesson__subject=instance,student_id__pk=profile_instance.pk).exists():
            return True
        else:
            return False


class SubjectWithTopicSerializers(serializers.ModelSerializer):
    topic = serializers.SerializerMethodField()
    percentage_topic = serializers.SerializerMethodField()
    is_progress = serializers.SerializerMethodField()
    
    class Meta:
        model = Subject
        fields = ['id','grade','name','image','description','topic','percentage_topic','is_progress']
        
    def get_topic(self, instance):
        request = self.context.get("request")
        profile_instance = Profile.objects.get(user=request.user)
        
        if StudentTopic.objects.filter(topic__lesson__subject=instance,student_id=profile_instance,is_deleted=False):
            student_topic_instance = StudentTopic.objects.filter(topic__lesson__subject=instance,student_id=profile_instance,is_deleted=False).last()
            return student_topic_instance.topic.name
    
    def get_percentage_topic(self, instance):
        request = self.context.get("request")
        profile_instance = Profile.objects.get(user=request.user)
        
        if Topic.objects.filter(lesson__subject = instance,is_deleted=False).exists():
            
            count_student_entrolled_topics = StudentTopic.objects.filter(student_id=profile_instance,topic__lesson__subject=instance,is_deleted=False).count()
            count_of_topics = Topic.objects.filter(lesson__subject = instance,is_deleted=False).count()
            persentage_of_encroled_topic = str(float(count_student_entrolled_topics)/float(count_of_topics)*100)
        
        
            # print("Cut of pic",count_of_topics)
            # print("percent enrolleds",type(persentage_of_encroled_topic))
            # print(count_student_entrolled_topics)
            return str(persentage_of_encroled_topic)
        
        else:
            return str('0')
    
    def get_is_progress(self,instance):
        request = self.context.get("request")
        profile_instance = Profile.objects.get(user=request.user)
        
        if StudentTopic.objects.filter(topic__lesson__subject=instance,student_id__pk=profile_instance.pk).exists():
            return True
        else:
            return False      


class UpCommingClassesSerializers(serializers.ModelSerializer):
    subject = serializers.SerializerMethodField()
    topic_name = serializers.SerializerMethodField()
    topic_image = serializers.SerializerMethodField()

    class Meta:
        model = UpCommingLiveClasses
        fields = ['topic','zoom_id','class_date','class_time','subject','topic_name','topic_image']
        
    def get_subject(self, instance):
        if instance.topic.lesson.subject:
            return instance.topic.lesson.subject.name

    def get_topic_name(self,instance):
        if instance.topic:
            return instance.topic.name
        
    def get_topic_image(self,instance):
        request = self.context.get('request')
        if instance.topic:
            return request.build_absolute_uri(instance.topic.image),
        

class NotificationsSerializers(serializers.ModelSerializer):

    class Meta:
        model = Notifications
        fields = ['date_added','title',]
        

class StudentTopicVideoSerializers(serializers.ModelSerializer):
    topic = serializers.SerializerMethodField()
    is_activity = serializers.SerializerMethodField()
    
    class Meta:
        model = StudentTopic
        fields = ['is_completed','is_new_content','student_id','topic','is_activity']
        
    def get_topic(self,instance):
        request = self.context.get('request')
        return {
            "topic_id" : instance.topic.pk,
            "topic_name" : instance.topic.name,
            "topic_duration" : instance.topic.duration,
            "topic_description" : instance.topic.description,
            "topic_image" : request.build_absolute_uri(instance.topic.image.url),
            "topic_video" : request.build_absolute_uri(instance.topic.video.url),
            "topic_subject" : instance.topic.lesson.subject.name,
        }
    
    def get_is_activity(self,instance):
        request = self.context.get("request")
        profile_instance = Profile.objects.get(user=request.user)
        
        if StudentActivity.objects.filter(activity__topic__pk=instance.topic.pk,student__pk=profile_instance.pk,is_completed=True).exists():
            return True
        else:
            return False


class TopicSerializer(serializers.ModelSerializer):
    lock_status = serializers.SerializerMethodField()
    is_activity = serializers.SerializerMethodField()
    
    class Meta:
        model = Topic
        fields = ['id','lock_status','date_added','name','image','description','duration','video','attachment','lesson','is_activity']
        
    def get_lock_status(self,instance):
        request = self.context.get("request")
        batch = get_student_batch(request)
        if GradeBatch.objects.filter(batch=batch,unlocked_topic=instance,is_deleted=False).exists():
            return True
        else:
            return False
    
    def get_is_activity(self,instance):
        request = self.context.get("request")
        profile_instance = Profile.objects.get(user=request.user)
        
        if StudentActivity.objects.filter(activity__topic__pk=instance.pk,student__pk=profile_instance.pk,is_completed=True).exists():
            activity_instance = StudentActivity.objects.get(activity__topic__pk=instance.pk,student__pk=profile_instance.pk,is_completed=True)
            
            return {
                "activity_name" : activity_instance.activity.title,
                "completed_status" : True,
                }
        else:
            return {
                "completed_status" : False,
                }
    
        

class NextTopicSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Topic
        fields = ['id','video']

        
class SubscriptionSerializer(serializers.ModelSerializer):
    subscription_details = serializers.SerializerMethodField()
    
    class Meta:
        model = SubscriptionGrade
        fields = ['grade_batch','description','subscription_details']
    
    def get_subscription_details(self,instance):
        request = self.context.get("request")
        profile_instance = Profile.objects.get(user=request.user)
        subscription_grade_fee =  SubscriptionGradeFee.objects.filter(subscription_grade__pk=instance.pk).order_by('-date_updated')[0]
        subscribed_date = StudentSubscription.objects.filter(profile__pk=profile_instance.pk,is_deleted=False,subscription_grade_fee__subscription_grade__pk=instance.pk).order_by('-date_updated')[0]
        subscribed_date = str(subscribed_date.subscribed_date.replace(tzinfo=None))
        days_in_month = subscription_grade_fee.month * 28
        date = datetime.strptime(subscribed_date, '%Y-%m-%d %H:%M:%S.%f').date() + timedelta(days=days_in_month)
        # date = datetime.strptime(str(subscribed_date),'%y/%m/%d %H:%M:%S') + timedelta(days=days_in_month)
        return {
            "grade" : instance.grade_batch.grade.name,
            "batch" : instance.grade_batch.batch.title,
            "subscribed_for" : subscription_grade_fee.month,
            "subscribed_rate" : subscription_grade_fee.rate,
            "expring_date" : date,
        }
        
        


class NextActivitySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Activity
        fields = ['id']