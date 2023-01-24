from django.db import models
from learn.models import Topic

from main.models import BaseModel
from versatileimagefield.fields import VersatileImageField

from users.models import Profile

# Create your models here.

QUESTION_QUESTION_TYPE_CHOICES = (
    ('objective', 'Objective'),
    ('descriptive', 'Descriptive'),
)

QUESTION_RIGHT_OPTION_CHOICES = (
    ('option1', 'Option 1'),
    ('option2', 'Option 2'),
    ('option3', 'Option 3'),
    ('option4', 'Option 4')
)


class Activity(BaseModel):
    topic = models.ForeignKey(Topic, limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    description = models.TextField()
    image = VersatileImageField('Image',upload_to="learn/activity/activity", blank=True, null=True)
    total_questions = models.PositiveIntegerField(blank=True,null=True)
    time_allotted = models.PositiveIntegerField()
    
    class Meta:
        db_table = 'activities_activity'
        verbose_name = ('Activity')
        verbose_name_plural = ('Activity')
        ordering = ('-id',)

    def __str__(self):
        
        return self.title
    
    
    
class ActivityQuestion(BaseModel):
    activity = models.ForeignKey(Activity, limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)
    question = models.CharField(max_length=256)
    score = models.DecimalField(max_digits=2, decimal_places=0, default=0)
    option1 = models.CharField(max_length=255, blank=True, null=True)
    option2 = models.CharField(max_length=255, blank=True, null=True)
    option3 = models.CharField(max_length=255, blank=True, null=True)
    option4 = models.CharField(max_length=255, blank=True, null=True)
    right_option = models.CharField(max_length=128, choices=QUESTION_RIGHT_OPTION_CHOICES, blank=True, null=True)
    key_points = models.TextField(blank=True, null=True)
    
    
    class Meta:
        db_table = 'activity_question'
        verbose_name = ('Activity Question')
        verbose_name_plural = ('Activty Questions')
        ordering = ('-id',)

    def __str__(self):
        return self.question

class StudentActivity(BaseModel):
    activity = models.ForeignKey(Activity, limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)
    student = models.ForeignKey(Profile,limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)

    class Meta:
        verbose_name = ('student activity')
        verbose_name_plural = ('student activity')
          
class StudentEnrolledActivity(BaseModel):
    student_id = models.ForeignKey(Profile,limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)
    question = models.ForeignKey(ActivityQuestion,limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)
    selected_option = models.CharField(null=True,blank=True,max_length=200)
    
    class Meta:
        verbose_name = ('student endrolled activity')
        verbose_name_plural = ('student endrolled activity')

    def __unicode__(self):
        return self.pk