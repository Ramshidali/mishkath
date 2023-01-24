from rest_framework import fields, serializers
from api.v1.general.functions import get_otp
from learn.models import Batch

from users.models import OtpRecord, Profile, TemporaryProfile


class StudentDetailsSerializers(serializers.ModelSerializer):
    dob = fields.DateField(input_formats=['%Y-%m-%d'])

    class Meta:
        model = TemporaryProfile
        fields = ['name', 'dob', 'gender', 'email']
        

class PersonalDetailsSerializers(serializers.ModelSerializer):
    nationality_name = serializers.SerializerMethodField()

    class Meta:
        model = TemporaryProfile
        fields = ['nationality', 'country_of_residense', 'permanent_address', 'current_address','nationality_name']

    def get_nationality_name(self,instances):
        if instances.nationality:
            return instances.nationality.name


class ParentsDetailsSerializers(serializers.ModelSerializer):
    class Meta:
        model = TemporaryProfile
        fields = ['fathers_name', 'fathers_phone', 'mothers_name', 'mothers_phone']


class AboutMishkathSerializers(serializers.ModelSerializer):
    class Meta:
        model = TemporaryProfile
        fields = ['mishkath_ad']


class CourseDetailsSerializers(serializers.ModelSerializer):

    interested_course_name = serializers.SerializerMethodField()

    class Meta:
        model = TemporaryProfile
        fields = ['interested_course', 'prefered_medium','interested_course_name']

    def get_interested_course_name(self,instances):
        if instances.interested_course:
            return instances.interested_course.name

# class ProfileSerializers(serializers.ModelSerializer):
#     dob = fields.DateField(input_formats=['%Y-%m-%d'])
#     class Meta:
#         model = Profile
#         # exclude = ['auto_id', 'creator', 'updater', 'user']
#         fields = ['phone','dob']

class BatchSerializers(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = ['from_date', 'to_date']


class OtpGenerationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtpRecord
        exclude = ['password', 'otp']
        
    def verify_otp(self, validated_data):
        otp = validated_data['otp']
        phone = validated_data['phone']
        studentOtp = OtpRecord.objects.get(phone=phone)
        
        if str(studentOtp.otp) == otp:
            
            return True
        else:
            
            return False

    def updateOtp(self, validated_data):
        phone = validated_data['phone']
        otp = get_otp()
        
        if OtpRecord.objects.filter(phone=phone).exists():
            OtpRecord.objects.filter(phone=phone).update(otp=otp)
            
        return otp
    
class ProfileSerializer(serializers.ModelSerializer):
    course_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Profile
        fields = ['name', 'dob','phone','email','interested_course','course_name']
        
    def get_course_name(self,instance):
        if instance.interested_course:
            return instance.interested_course.name
        

