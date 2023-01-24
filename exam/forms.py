from django import forms
from django.forms.widgets import TextInput,Select, DateTimeInput,DateInput,CheckboxInput,FileInput

from exam.models import *

class ExamForm(forms.ModelForm):

    class Meta:
        model = Exam
        fields = ['subject','exam_date','exam_type','grade_batch','time_allotted','total_mark','total_questions']

        widgets = {
            'subject': Select(attrs={'class': 'form-control selectpicker'}),
            'exam_date': DateInput(attrs={'class': 'required form-control','id' : 'mdate'}),
            'exam_type': Select(attrs={'class': 'form-control selectpicker'}),
            'grade_batch': Select(attrs={'class': 'form-control selectpicker'}),
            'time_allotted': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter Allotted Time'}),
            'total_mark': TextInput(attrs={'type':'number','class': 'required form-control','placeholder' : 'Enter Total mark'}),    
            'total_questions': TextInput(attrs={'type':'number','class': 'required form-control','placeholder' : 'Enter Total Questions'}),    
        }
        
        
class ExamQuestionForm(forms.ModelForm):
    
    class Meta:
        model = Questions
        fields = ['exam','question','question_type','option_a','option_b','option_c','option_d','correct_option','attachment',]

        widgets = {
            'exam': Select(attrs={'class': 'form-control selectpicker'}),
            'question': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter Question'}),
            'question_type': Select(attrs={'class': 'form-control selectpicker'}),
            'option_a': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter Option 1'}),
            'option_b': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter Option 2'}),
            'option_c': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter Option 3'}),
            'option_d': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter Option 4'}),
            'correct_option': Select(attrs={'class': 'form-control selectpicker'}),
            'attachment' : FileInput()
        }
        
class ExamQuestionWithoutExamForm(forms.ModelForm):
    
    class Meta:
        model = Questions
        fields = ['question','question_type','option_a','option_b','option_c','option_d','correct_option','attachment',]

        widgets = {
            'question': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter Question'}),
            'question_type': Select(attrs={'class': 'form-control selectpicker'}),
            'option_a': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter Option 1'}),
            'option_b': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter Option 2'}),
            'option_c': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter Option 3'}),
            'option_d': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter Option 4'}),
            'correct_option': Select(attrs={'class': 'form-control selectpicker'}),
            'attachment' : FileInput()
        }