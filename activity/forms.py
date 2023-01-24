from django import forms
from django.forms.widgets import TextInput,Select,FileInput

from activity.models import Activity, ActivityQuestion

class ActivityForm(forms.ModelForm):

    class Meta:
        model = Activity
        fields = ['topic','title','description','time_allotted','image']

        widgets = {
            'title': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter Title'}),
            'topic': Select(attrs={'class': 'form-control selectpicker'}),
            'description': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter Description'}),
            'time_allotted': TextInput(attrs={'type':'number','class': 'required form-control','placeholder' : 'Enter Duration'}),
            'image': FileInput(),    
        }
        

class ActivityQuestionForm(forms.ModelForm):
    
    class Meta:
        model = ActivityQuestion
        fields = ['activity','question','score','option1','option2','option3','option4','right_option','key_points']

        widgets = {
            'activity': Select(attrs={'class': 'form-control selectpicker'}),
            'question': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter Question'}),
            'score': TextInput(attrs={'type':'number','class': 'required form-control','placeholder' : 'Enter Score'}),
            'option1': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter Option 1'}),
            'option2': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter Option 2'}),
            'option3': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter Option 3'}),
            'option4': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter Option 4'}),
            'right_option': Select(attrs={'class': 'form-control selectpicker'}),
            'key_points': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter Key points'}),
        }