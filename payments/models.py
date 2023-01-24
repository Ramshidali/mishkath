from django.db import models
from learn.models import GradeBatch

from main.models import BaseModel
from users.models import Profile

# Create your models here.

# monthly payment 
class SubscriptionGrade(BaseModel):
    grade_batch = models.ForeignKey(GradeBatch,limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)
    description = models.TextField(blank=True,null=True)
    
    class Meta:
        db_table = 'subscription_grade'
        verbose_name = ('Subscription Grade')
        verbose_name_plural = ('Subscription Grade')
    
    def __str__(self):
        return str(self.grade_batch.grade.name)

class SubscriptionGradeFee(BaseModel):
    month = models.IntegerField()
    rate = models.IntegerField()
    subscription_grade = models.ForeignKey(SubscriptionGrade,limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'subscription_grade_fee'
        verbose_name = ('subscription grade fee')
        verbose_name_plural = ('subscription grade fee')
    
    def __str__(self):
        return f'for {self.month} month Rs : {self.rate}/-'

class StudentSubscription(BaseModel):
    profile = models.ForeignKey(Profile,limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)
    subscription_grade_fee = models.ForeignKey(SubscriptionGradeFee,limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)
    subscribed_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'student_subscription'
        verbose_name = ('student subscription')
        verbose_name_plural = ('student subscription')
    
    def __str__(self):
        return str(self.profile.name)
