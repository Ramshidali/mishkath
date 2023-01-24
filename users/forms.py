from django import forms
from django.forms.widgets import TextInput,Select,DateInput
from users.models import InterviewStatus, Profile

class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

class InterviewScheduleForm(forms.ModelForm):

    class Meta:
        model = InterviewStatus
        fields = ['status','zoom_id','interview_date','interview_time']

        widgets = {
            'status': Select(attrs={'class': 'form-control selectpicker','placeholder' : 'status'}),
            'zoom_id': TextInput(attrs={'class': 'required form-control','placeholder' : 'Zoom ID'}),
            'interview_date': DateInput(attrs={'class': 'required form-control'}),
            'interview_time': TimeInput(attrs={'class':'form-control','id':'timepicker','placeholder':'Check time'}),
        }

class AssignBatchForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ['grade_batch']

        widgets = {
            'grade_batch': Select(attrs={'class': 'form-control selectpicker'}),
        }

class EditProfileForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        exclude = ['id','auto_id','creator','updater','date_added','date_updated','is_deleted','deleted_reason','user']
        
        widgets = {
            'name': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter Name'}),
            'dob': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter Date of Birth'}),
            'phone': TextInput(attrs={'class': 'required form-control','type':'tel','placeholder' : 'Enter Phone'}),
            'gender': Select(attrs={'class': 'form-control selectpicker'}),
            'email': TextInput(attrs={'class': 'required form-control email','type':'email','placeholder' : 'Enter Email'}),
            'nationality': Select(attrs={'class': 'form-control selectpicker'}),
            'country_of_residense': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter Country of residents'}),
            'permanent_address': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter Permenent Address'}),
            'current_address': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter Current Address'}),
            'fathers_name': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter Father Name'}),
            'fathers_phone': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter Father Phone Number'}),
            'mothers_name': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter Mothers Name '}),
            'mothers_phone': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter Mother phone'}),
            'mishkath_ad': Select(attrs={'class': 'form-control selectpicker'}),
            'mishkath_ad_message': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter Ad message'}),
            'interested_course': Select(attrs={'class': 'form-control selectpicker'}),
            'prefered_medium': Select(attrs={'class': 'form-control selectpicker'}),
            'grade_batch': Select(attrs={'class': 'form-control selectpicker'})
        }
