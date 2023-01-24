from rest_framework import serializers
from main.models import Country, Courses

class CountrySerializers(serializers.ModelSerializer):
    
    class Meta:
        model = Country
        fields = ['id','name','country_code','phone_code','is_active','phone_number_length']


class CoursesSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = Courses
        fields = ['id','name']