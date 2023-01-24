from django import forms
from django.forms.widgets import TextInput,Select,DateInput

from payments.models import StudentSubscription, SubscriptionGrade, SubscriptionGradeFee


class SubscriptionGradeForm(forms.ModelForm):
    
    class Meta:
        model = SubscriptionGrade
        fields = ['grade_batch','description']

        widgets = {
            'grade_batch': Select(attrs={'class': 'form-control selectpicker'}),
            'description': TextInput(attrs={'class': 'required form-control','placeholder' : 'enter description'}),
        }
        
class SubscriptionGradeFeeForm(forms.ModelForm):
    
    class Meta:
        model = SubscriptionGradeFee
        fields = ['month','rate']

        widgets = {
            'month': TextInput(attrs={'class': 'required form-control','placeholder' : 'enter month'}),
            'rate': TextInput(attrs={'class': 'required form-control','placeholder' : 'enter rate'}),
        }
        
class StudentSubscriptionForm(forms.ModelForm):
    
    class Meta:
        model = StudentSubscription
        fields = ['profile','subscription_grade_fee']

        widgets = {
            'profile': Select(attrs={'class': 'form-control selectpicker'}),
            'subscription_grade_fee': Select(attrs={'class': 'form-control selectpicker'}),
        }