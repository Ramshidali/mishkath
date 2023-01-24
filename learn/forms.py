from django import forms
from django.forms.widgets import TextInput,Select,DateInput,CheckboxInput,FileInput
from learn.models import Batch, Grade, GradeBatch, Lesson, Subject, Topic, UpCommingLiveClasses
from dal import autocomplete
from main.models import Country, Courses

class BatchesForm(forms.ModelForm):
    is_active = forms.BooleanField()

    class Meta:
        model = Batch
        fields = ['title','from_date','to_date','is_active']

        widgets = {
            'title': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter Title'}),
            'from_date': DateInput(attrs={'class': 'required form-control','id' : 'mdate'}),
            'to_date': DateInput(attrs={'class': 'required form-control','id' : 'mdate2'}),
            'is_active': CheckboxInput(attrs={'class':'custom-control-input'}),
        }
        
class ClassForm(forms.ModelForm):
    
    class Meta:
        model = Grade
        fields = ['name','image','description','qualification']

        widgets = {
            'name': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter Title'}),
            'image': FileInput(),
            'description': TextInput(attrs={'class': 'required form-control','placeholder' :'description'}),
            'qualification': TextInput(attrs={'type':'number','class': 'required form-control','placeholder' :'qualification'}),
        }
        
class GradeBatchForm(forms.ModelForm):

    class Meta:
        model = GradeBatch
        fields = ['grade','batch','unlocked_topic']

        widgets = {
            'grade': Select(attrs={'class': 'form-control selectpicker'}),
            'batch': Select(attrs={'class': 'form-control selectpicker'}),
            'unlocked_topic': autocomplete.ModelSelect2Multiple(url='learn:unlocked_topics_autocomplete',
                attrs={'class': 'select2 form-control unlocked_topic','data-placeholder': 'topics','data-minimum-input-length': 0}),
        }
        

        
class CountryForm(forms.ModelForm):
    is_active = forms.BooleanField()

    class Meta:
        model = Country
        fields = ['name','country_code','phone_code','phone_number_length','is_active']

        widgets = {
            'name': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter Name'}),
            'country_code': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter Country code'}),
            'phone_code': TextInput(attrs={'class': 'required form-control','placeholder' :'Enter Phone Code'}),
            'phone_number_length': TextInput(attrs={'type':'number','class': 'required form-control','placeholder' :'qualification'}),
            'is_active': CheckboxInput(attrs={'class':'custom-control-input'}),
        }
        
class CoursesForm(forms.ModelForm):

    class Meta:
        model = Courses
        fields = ['name']

        widgets = {
            'name': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter Name'}),
        }
        
class SubjectsForm(forms.ModelForm):

    class Meta:
        model = Subject
        fields = ['grade','name','image','description','duration']

        widgets = {
            'grade': Select(attrs={'class': 'form-control selectpicker'}),
            'name': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter Name'}),
            'description': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter Description'}),
            'duration': TextInput(attrs={'type':'number','class': 'required form-control','placeholder' : 'Enter Duration'}),
            'image': FileInput(),   
        }
        
class LessonFormWithoutSubject(forms.ModelForm):
    
    class Meta:
        model = Lesson
        fields = ['name','description','image']

        widgets = {
            'name': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter Name'}),
            'description': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter Description'}),
            'image': FileInput(),   
        }

class LessonFormWithSubject(forms.ModelForm):
    
    class Meta:
        model = Lesson
        fields = ['subject','name','description','image']

        widgets = {
            'subject': Select(attrs={'class': 'form-control selectpicker'}),
            'name': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter Name'}),
            'description': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter Description'}),
            'image': FileInput(),
        }

class TopicFormWithoutLesson(forms.ModelForm):
    is_processed = forms.BooleanField()
        
    class Meta:
        model = Topic
        fields = ['name','description','duration','video','is_processed','playlist','attachment','image']

        widgets = {
            'name': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter Name'}),
            'description': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter Description'}),
            'duration': TextInput(attrs={'type':'number','class': 'required form-control','placeholder' : 'Enter Duration'}),
            'playlist': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter playlist'}),
            'attachment': FileInput(),
            'video': FileInput(),   
            'image': FileInput(), 
            'is_processed': Select(attrs={'class': 'form-control selectpicker'}), 
        }
        
class TopicFormWithLesson(forms.ModelForm):
    is_processed = forms.BooleanField()
        
    class Meta:
        model = Topic
        fields = ['lesson','name','description','duration','video','is_processed','playlist','attachment','image']

        widgets = {
            'lesson': Select(attrs={'class': 'form-control selectpicker'}),
            'name': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter Name'}),
            'description': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter Description'}),
            'duration': TextInput(attrs={'type':'number','class': 'required form-control','placeholder' : 'Enter Duration'}),
            'playlist': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter playlist'}),
            'attachment': FileInput(),
            'video': FileInput(),   
            'image': FileInput(), 
            'is_processed': Select(attrs={'class': 'form-control selectpicker'}), 
        }
        
class UpCommingLiveClassesForm(forms.ModelForm):
        
    class Meta:
        model = UpCommingLiveClasses
        fields = ['topic','batch','zoom_id','class_date','class_time']

        widgets = {
            'topic': Select(attrs={'class': 'form-control selectpicker'}),
            'batch': Select(attrs={'class': 'form-control selectpicker'}),
            'zoom_id': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter Name'}),
            'class_date': DateInput(attrs={'class': 'required form-control','id' : 'mdate'}),
            'class_time': TextInput(attrs={'class': 'required form-control','id' : 'timepicker'}),
            
        }